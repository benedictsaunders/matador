# coding: utf-8
# Distributed under the terms of the MIT license.

""" This file implements the BatchRun class for chaining
FullRelaxer instances across several structures with
high-throughput.

"""


from collections import defaultdict
import multiprocessing as mp
import os
import glob
import time
from matador.utils.print_utils import print_notify
from matador.compute.slurm import get_slurm_env, get_slurm_walltime
from matador.scrapers.castep_scrapers import cell2dict, param2dict
from matador.compute.compute import FullRelaxer


class BatchRun:
    """ A class that implements the running of multiple generic jobs on
    a series of files without collisions with other nodes using the
    FullRelaxer class. Jobs that have started are listed in jobs.txt,
    failed jobs are moved to bad_castep, completed jobs are moved to
    completed and listed in finished_cleanly.txt.

    Based on run.pl, run2.pl and PyAIRSS class CastepRunner.

    """

    def __init__(self, seed, **kwargs):
        """ Check directory has valid contents and prepare log files
        and directories if not already prepared, then begin running
        calculations.

        Note:
            This class is usually initialised by the run3 script, which
            has a full description of possible arguments.

        Parameters:
            seed (:obj:`list` of :obj:`str`): single entry of param/cell
                file seed for CASTEP geometry optimisations of res
                files, or a list of filenames of $seed to run arbitrary
                executables on. e.g. ['LiAs'] if LiAs.cell and LiAs.param
                exist in cwd full of res files, e.g.2. ['LiAs_1', 'LiAs_2']
                if LiAs_1.in/LiAs_2.in exist, and executable = 'pw6.x < $seed.in'.

        Keyword arguments:
            Exhaustive list found in argparse parser inside `matador/cli/run3.py`.

        """
        # parse args, then co-opt them for passing directly into FullRelaxer
        prop_defaults = {'ncores': None, 'nprocesses': 1, 'nnodes': 1,
                         'executable': 'castep', 'no_reopt': False,
                         'redirect': None, 'debug': False, 'custom_params': False,
                         'verbosity': 0, 'archer': False, 'slurm': False,
                         'intel': False, 'conv_cutoff': False, 'conv_kpt': False,
                         'memcheck': False, 'maxmem': None, 'killcheck': True,
                         'kpts_1D': False, 'spin': False, 'ignore_jobs_file': False,
                         'rough': 4, 'rough_iter': 2, 'fine_iter': 20, 'max_walltime': None,
                         'limit': None, 'profile': False, 'polltime': 30}
        self.args = {}
        self.args.update(prop_defaults)
        self.args.update(kwargs)
        self.debug = self.args.get('debug')
        self.seed = seed
        # if only one seed, check if it is a file, and if so treat
        # this run as a generic run, not a CASTEP cell/param run
        if len(self.seed) == 1:
            if '*' in self.seed[0]:
                self.seed = glob.glob(self.seed[0])
            elif not os.path.isfile(self.seed[0]):
                self.seed = self.seed[0]

        if isinstance(self.seed, str):
            self.mode = 'castep'
        else:
            self.mode = 'generic'

        if self.args.get('no_reopt'):
            self.args['reopt'] = False
        else:
            self.args['reopt'] = True
        if 'no_reopt' in self.args:
            del self.args['no_reopt']
        self.nprocesses = int(self.args['nprocesses'])
        del self.args['nprocesses']
        self.limit = self.args.get('limit')
        del self.args['limit']

        # assign number of cores
        self.all_cores = mp.cpu_count()
        self.slurm_avail_tasks = os.environ.get('SLURM_NTASKS')
        self.slurm_env = None
        self.slurm_walltime = None
        if self.slurm_avail_tasks is not None:
            self.slurm_avail_tasks = int(self.slurm_avail_tasks)
            self.slurm_env = get_slurm_env()

        if self.slurm_env is not None:
            self.slurm_walltime = get_slurm_walltime(self.slurm_env)

        if self.args.get('max_walltime') is not None:
            self.max_walltime = self.args.get('max_walltime')
        elif self.slurm_walltime is not None:
            self.max_walltime = self.slurm_walltime
        else:
            self.max_walltime = None

        self.start_time = None
        if self.max_walltime is not None:
            self.start_time = time.time()

        if self.args.get('ncores') is None:
            if self.slurm_avail_tasks is None:
                self.args['ncores'] = int(self.all_cores / self.nprocesses)
            else:
                self.args['ncores'] = int(self.slurm_avail_tasks / self.nprocesses)
        if self.args['nnodes'] < 1 or self.args['ncores'] < 1 or self.nprocesses < 1:
            raise SystemExit('Invalid number of cores, nodes or processes.')

        if self.mode == 'castep':
            self.castep_setup()
        else:
            self.generic_setup()

        # prepare folders and text files
        self.paths = dict()
        if self.args.get('conv_cutoff'):
            self.paths['completed_dir'] = 'completed_cutoff'
        elif self.args.get('conv_kpt'):
            self.paths['completed_dir'] = 'completed_kpts'
        else:
            self.paths['completed_dir'] = 'completed'
        self.paths['failed_dir'] = 'bad_castep'
        self.paths['jobs_fname'] = 'jobs.txt'
        self.paths['completed_fname'] = 'finished_cleanly.txt'
        self.paths['failures_fname'] = 'failures.txt'
        self.paths['memory_fname'] = 'memory_exceeded.txt'
        if not os.path.isfile(self.paths['jobs_fname']):
            with open(self.paths['jobs_fname'], 'a'):
                pass
        if not os.path.isfile(self.paths['completed_fname']):
            with open(self.paths['completed_fname'], 'a'):
                pass
        if not os.path.isfile(self.paths['failures_fname']):
            with open(self.paths['failures_fname'], 'a'):
                pass
        if self.args.get('memcheck'):
            if not os.path.isfile(self.paths['memory_fname']):
                with open(self.paths['memory_fname'], 'a'):
                    pass

    def spawn(self, join=False):
        """ Spawn processes to perform calculations.

        Keyword arguments:
            join (bool): whether or not to attach to FullRelaxer
                process. Useful for testing.

        """
        from random import sample
        procs = []
        error_queue = mp.Queue()
        for proc_id in range(self.nprocesses):
            procs.append(mp.Process(target=self.perform_new_calculations,
                                    args=(sample(self.file_lists['res'],
                                                 len(self.file_lists['res']))
                                          if self.mode == 'castep' else self.seed, error_queue, proc_id)))
        for proc in procs:
            proc.start()
            if join:
                proc.join()

        errors = []
        # wait for each proc to write to error queue
        for _, proc in enumerate(procs):
            result = error_queue.get()
            if isinstance(result[1], Exception):
                print_notify('Process {} raised error: {}\n'.format(result[0], result[1]))
                errors.append(result)

        try:
            if errors:
                error_message = ''
                for error in errors:
                    error_message += 'Process {} raised error {}. '.format(error[0], error[1])
                if len(set([type(error[1]) for error in errors])) == 1:
                    raise type(errors[0][1])(error_message)
                raise BundledErrors(error_message)

        # the only errors that reach here are fatal, e.g. WalltimeError, SystemExit or KeyboardInterrupt,
        except Exception as err:
            result = [proc.join(timeout=10) for proc in procs]
            result = [proc.terminate() for proc in procs if proc.is_alive()]
            raise err

    def perform_new_calculations(self, res_list, error_queue, proc_id):
        """ Perform all calculations that have not already
        failed or finished to completion.

        Parameters:
            res_list (:obj:`list` of :obj:`str`): list of structure filenames.
            error_queue (multiprocessing.Queue): queue to push exceptions to
            proc_id (int): process id for logging

        """
        job_count = 0
        if isinstance(res_list, str):
            res_list = [res_list]
        for res in res_list:
            locked = os.path.isfile('{}.lock'.format(res))
            if not self.args.get('ignore_jobs_file'):
                listed = self._check_jobs_file(res)
            else:
                listed = []
            running = any([listed, locked])
            if not running:
                try:
                    # check we haven't reached job limit
                    if job_count == self.limit:
                        error_queue.put((proc_id, job_count))
                        return

                    # write lock file
                    if not os.path.isfile('{}.lock'.format(res)):
                        with open(res + '.lock', 'a') as job_file:
                            pass
                    else:
                        print('Another node wrote this file when I wanted to, skipping...')
                        continue

                    # write to jobs file
                    with open(self.paths['jobs_fname'], 'a') as job_file:
                        job_file.write(res + '\n')

                    # create full relaxer object for creation and running of job
                    job_count += 1
                    hostname = os.uname()[1]
                    relaxer = FullRelaxer(node=None, res=res,
                                          param_dict=self.param_dict,
                                          cell_dict=self.cell_dict,
                                          mode=self.mode, paths=self.paths, compute_dir=hostname,
                                          timings=(self.max_walltime, self.start_time),
                                          **self.args)
                    # if memory check failed, let other nodes have a go
                    if not relaxer.enough_memory:
                        with open(self.paths['memory_fname'], 'a') as job_file:
                            job_file.write(res + '\n')
                        if os.path.isfile('{}.lock'.format(res)):
                            os.remove('{}.lock'.format(res))
                        with open(self.paths['jobs_fname'], 'r+') as job_file:
                            flines = job_file.readlines()
                            job_file.seek(0)
                        for line in flines:
                            if res not in line:
                                job_file.write(line)
                            job_file.truncate()

                    elif relaxer.success:
                        with open(self.paths['completed_fname'], 'a') as job_file:
                            job_file.write(res + '\n')
                    else:
                        with open(self.paths['failures_fname'], 'a') as job_file:
                            job_file.write(res + '\n')

                # push errors to error queue and raise
                except Exception as err:
                    error_queue.put((proc_id, err))
                    raise err

        error_queue.put((proc_id, job_count))

    def generic_setup(self):
        """ Undo things that are set ready for CASTEP jobs... """
        self.cell_dict = None
        self.param_dict = None

    def castep_setup(self):
        """ Set up CASTEP jobs from res files, and $seed.cell/param. """
        # read cell/param files
        exts = ['cell', 'param']
        for ext in exts:
            if not os.path.isfile('{}.{}'.format(self.seed, ext)):
                raise SystemExit('Failed to find {} file, {}.{}'.format(ext, self.seed, ext))
        self.cell_dict, cell_success = cell2dict(self.seed + '.cell', db=False)
        if not cell_success:
            print(self.cell_dict)
            raise SystemExit('Failed to parse cell file')
        self.param_dict, param_success = param2dict(self.seed + '.param', db=False)
        if not param_success:
            print(self.param_dict)
            raise SystemExit('Failed to parse param file')

        # scan directory for files to run
        self.file_lists = defaultdict(list)
        self.file_lists['res'] = [file.name for file in os.scandir() if file.name.endswith('.res')]
        if len(self.file_lists['res']) < 1:
            error = (
                'run3 in CASTEP mode requires at least 1 res file in folder, found {}'
                .format(len(self.file_lists['res']))
            )
            raise SystemExit(error)

        # do some prelim checks of parameters
        if self.param_dict['task'].upper() in ['GEOMETRYOPTIMISATION', 'GEOMETRYOPTIMIZATION']:
            if 'geom_max_iter' not in self.param_dict:
                raise SystemExit('geom_max_iter is unset, please fix this.')
            elif int(self.param_dict['geom_max_iter']) <= 0:
                raise SystemExit('geom_max_iter is only {}!'.format(self.param_dict['geom_max_iter']))

        # parse convergence args and set them up
        self.convergence_run_setup()

        # delete source from cell and param
        del self.cell_dict['source']
        del self.param_dict['source']

    def convergence_run_setup(self):
        """ Set the correct args for a convergence run. """
        # check if we're doing a conv run
        if self.args.get('conv_cutoff'):
            if os.path.isfile('cutoff.conv'):
                with open('cutoff.conv', 'r') as f:
                    flines = f.readlines()
                    self.args['conv_cutoff'] = []
                    for line in flines:
                        if not line.startswith('#'):
                            self.args['conv_cutoff'].append(int(line))
            else:
                raise SystemExit('Missing cutoff.conv file')
        else:
            self.args['conv_cutoff'] = None

        if self.args.get('conv_kpt'):
            if os.path.isfile('kpt.conv'):
                with open('kpt.conv', 'r') as f:
                    flines = f.readlines()
                    self.args['conv_kpt'] = []
                    for line in flines:
                        if not line.startswith('#'):
                            self.args['conv_kpt'].append(float(line))
            else:
                raise SystemExit('Missing with conv.kpt file')
        else:
            self.args['conv_kpt'] = None

    def _check_jobs_file(self, res):
        """ Check if structure is listed in jobs.txt file.

        Parameters:
            res (str): structure name.

        Returns:
            bool: True if already listed in jobs file.

        """
        with open(self.paths['jobs_fname'], 'r') as job_file:
            flines = job_file.readlines()
            for line in flines:
                if res in line:
                    return True
        return False


class BundledErrors(Exception):
    """ Raise this after collecting all exceptions from
    processes.
    """
    pass


def reset_job_folder(debug=False):
    """ Remove all lock files and clean up jobs.txt
    ready for job restart.

    Note:
        This should be not called by a FullRelaxer instance, in case
        other instances are running.

    Returns:
        num_remaining (int): number of structures left to relax

    """
    res_list = glob.glob('*.res')
    if debug:
        print(res_list)
    for f in res_list:
        root = f.replace('.res', '')
        exts_to_rm = ['res.lock', 'kill']
        for ext in exts_to_rm:
            if os.path.isfile('{}.{}'.format(root, ext)):
                if debug:
                    print('Deleting {}.{}'.format(root, ext))
                os.remove('{}.{}'.format(root, ext))

    # also remove from jobs file
    if os.path.isfile('jobs.txt'):
        with open('jobs.txt', 'r+') as f:
            flines = f.readlines()
            if debug:
                print('Initially {} jobs in jobs.txt'.format(len(flines)))
            f.seek(0)
            for line in flines:
                line = line.strip()
                if line in res_list:
                    print('Excluding {}'.format(line))
                    continue
                else:
                    f.write(line)
            f.truncate()
            flines = f.readlines()
            if debug:
                print('{} jobs remain in jobs.txt'.format(len(flines)))

    return len(res_list)