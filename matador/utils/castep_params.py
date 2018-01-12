""" This file contains a Python list of all CASTEP parameters,automatically generated from file_utils.scrape_castep_params.
"""

CASTEP_VERSION = 18.1

CASTEP_PARAMS = [
                 'backup_interval',
                 'basis_de_dloge',
                 'basis_precision',
                 'born_charge_sum_rule',
                 'bs_eigenvalue_tol',
                 'bs_max_cg_steps',
                 'bs_max_iter',
                 'bs_nbands',
                 'bs_nextra_bands',
                 'bs_perc_extra_bands',
                 'bs_re_est_k_scrn',
                 'bs_write_eigenvalues',
                 'bs_xc_definition',
                 'bs_xc_functional',
                 'calculate_born_charges',
                 'calculate_densdiff',
                 'calculate_elf',
                 'calculate_hirshfeld',
                 'calculate_raman',
                 'calculate_stress',
                 'calc_full_ex_pot',
                 'calc_molecular_dipole',
                 'charge',
                 'charge_unit',
                 'checkpoint',
                 'cml_filename',
                 'cml_output',
                 'comment',
                 'continuation',
                 'cut_off_energy',
                 'data_distribution',
                 'devel_code',
                 'dipole_correction',
                 'dipole_dir',
                 'dipole_unit',
                 'efermi_tol',
                 'efield_calc_ion_permittivity',
                 'efield_convergence_win',
                 'efield_dfpt_method',
                 'efield_energy_tol',
                 'efield_freq_spacing',
                 'efield_ignore_molec_modes',
                 'efield_max_cg_steps',
                 'efield_max_cycles',
                 'efield_oscillator_q',
                 'efield_unit',
                 'electronic_minimizer',
                 'elec_convergence_win',
                 'elec_dump_file',
                 'elec_eigenvalue_tol',
                 'elec_energy_tol',
                 'elec_force_tol',
                 'elec_method',
                 'elec_restore_file',
                 'elec_temp',
                 'elnes_eigenvalue_tol',
                 'elnes_nbands',
                 'elnes_nextra_bands',
                 'elnes_perc_extra_bands',
                 'elnes_xc_definition',
                 'elnes_xc_functional',
                 'energy_unit',
                 'entropy_unit',
                 'exchange_reflect_kpts',
                 'excited_state_scissors',
                 'fft_max_prime_factor',
                 'fine_cut_off_energy',
                 'fine_gmax',
                 'fine_grid_scale',
                 'finite_basis_corr',
                 'finite_basis_npoints',
                 'finite_basis_spacing',
                 'fixed_npw',
                 'fix_occupancy',
                 'force_constant_unit',
                 'force_unit',
                 'frequency_unit',
                 'ga_bulk_slice',
                 'ga_fixed_n',
                 'ga_max_gens',
                 'ga_mutate_amp',
                 'ga_mutate_rate',
                 'ga_pop_size',
                 'geom_convergence_win',
                 'geom_disp_tol',
                 'geom_energy_tol',
                 'geom_force_tol',
                 'geom_frequency_est',
                 'geom_lbfgs_max_updates',
                 'geom_linmin_tol',
                 'geom_max_iter',
                 'geom_method',
                 'geom_modulus_est',
                 'geom_spin_fix',
                 'geom_stress_tol',
                 'geom_tpsd_init_stepsize',
                 'geom_tpsd_iterchange',
                 'geom_use_linmin',
                 'grid_scale',
                 'impose_trs',
                 'inv_length_unit',
                 'iprint',
                 'ir_intensity_unit',
                 'k_scrn_averaging_scheme',
                 'k_scrn_den_function',
                 'length_unit',
                 'magres_convergence_win',
                 'magres_conv_tol',
                 'magres_jcoupling_task',
                 'magres_max_cg_steps',
                 'magres_max_sc_cycles',
                 'magres_method',
                 'magres_task',
                 'magres_write_response',
                 'magres_xc_definition',
                 'magres_xc_functional',
                 'mass_unit',
                 'max_cg_steps',
                 'max_diis_steps',
                 'max_scf_cycles',
                 'max_sd_steps',
                 'md_barostat',
                 'md_cell_t',
                 'md_damping_reset',
                 'md_damping_scheme',
                 'md_delta_t',
                 'md_elec_convergence_win',
                 'md_elec_eigenvalue_tol',
                 'md_elec_energy_tol',
                 'md_elec_force_tol',
                 'md_ensemble',
                 'md_eqm_cell_t',
                 'md_eqm_ion_t',
                 'md_eqm_method',
                 'md_eqm_t',
                 'md_extrap',
                 'md_extrap_fit',
                 'md_hug_compression',
                 'md_hug_dir',
                 'md_hug_method',
                 'md_hug_t',
                 'md_ion_t',
                 'md_langevin_t',
                 'md_nhc_length',
                 'md_nose_t',
                 'md_num_beads',
                 'md_num_iter',
                 'md_opt_damped_delta_t',
                 'md_pathint_init',
                 'md_pathint_num_stages',
                 'md_pathint_staging',
                 'md_sample_iter',
                 'md_temperature',
                 'md_thermostat',
                 'md_use_pathint',
                 'md_use_plumed',
                 'md_xlbomd',
                 'md_xlbomd_history',
                 'message_size',
                 'metals_method',
                 'mixing_scheme',
                 'mix_charge_amp',
                 'mix_charge_gmax',
                 'mix_cut_off_energy',
                 'mix_history_length',
                 'mix_metric_q',
                 'mix_spin_amp',
                 'mix_spin_gmax',
                 'nbands',
                 'ndown',
                 'nelectrons',
                 'nextra_bands',
                 'nlxc_calc_full_ex_pot',
                 'nlxc_div_corr_npts_step',
                 'nlxc_div_corr_on',
                 'nlxc_div_corr_s_width',
                 'nlxc_div_corr_tol',
                 'nlxc_exchange_fraction',
                 'nlxc_exchange_reflect_kpts',
                 'nlxc_exchange_screening',
                 'nlxc_impose_trs',
                 'nlxc_k_scrn_averaging_scheme',
                 'nlxc_k_scrn_den_function',
                 'nlxc_page_ex_pot',
                 'nlxc_ppd_integral',
                 'nlxc_ppd_size_x',
                 'nlxc_ppd_size_y',
                 'nlxc_ppd_size_z',
                 'nlxc_re_est_k_scrn',
                 'nspins',
                 'num_backup_iter',
                 'num_dump_cycles',
                 'num_farms',
                 'num_occ_cycles',
                 'num_proc_in_smp',
                 'num_proc_in_smp_fine',
                 'nup',
                 'optics_nbands',
                 'optics_nextra_bands',
                 'optics_perc_extra_bands',
                 'optics_xc_definition',
                 'optics_xc_functional',
                 'opt_strategy',
                 'opt_strategy_bias',
                 'page_ex_pot',
                 'page_wvfns',
                 'pdos_calculate_weights',
                 'perc_extra_bands',
                 'phonon_calculate_dos',
                 'phonon_calc_lo_to_splitting',
                 'phonon_const_basis',
                 'phonon_convergence_win',
                 'phonon_dfpt_method',
                 'phonon_dos_limit',
                 'phonon_dos_spacing',
                 'phonon_energy_tol',
                 'phonon_fine_cutoff_method',
                 'phonon_fine_method',
                 'phonon_finite_disp',
                 'phonon_force_constant_cutoff',
                 'phonon_force_constant_cut_scale',
                 'phonon_force_constant_ellipsoid',
                 'phonon_max_cg_steps',
                 'phonon_max_cycles',
                 'phonon_method',
                 'phonon_preconditioner',
                 'phonon_sum_rule',
                 'phonon_sum_rule_method',
                 'phonon_use_kpoint_symmetry',
                 'phonon_write_dynamical',
                 'phonon_write_force_constants',
                 'popn_bond_cutoff',
                 'popn_calculate',
                 'popn_write',
                 'ppd_integral',
                 'ppd_size_x',
                 'ppd_size_y',
                 'ppd_size_z',
                 'pressure_unit',
                 'print_clock',
                 'print_memory_usage',
                 'pspot_beta_phi_type',
                 'pspot_nonlocal_type',
                 'raman_method',
                 'raman_range_high',
                 'raman_range_low',
                 'rand_seed',
                 'relativistic_treatment',
                 'reuse',
                 're_est_k_scrn',
                 'run_time',
                 'secondd_method',
                 'sedc_apply',
                 'sedc_d_g06',
                 'sedc_d_jchs',
                 'sedc_d_ts',
                 'sedc_lambda_obs',
                 'sedc_n_obs',
                 'sedc_s6_g06',
                 'sedc_s6_jchs',
                 'sedc_scheme',
                 'sedc_sr_jchs',
                 'sedc_sr_ts',
                 'smearing_scheme',
                 'smearing_width',
                 'spectral_eigenvalue_tol',
                 'spectral_max_iter',
                 'spectral_max_steps_per_iter',
                 'spectral_nbands',
                 'spectral_nextra_bands',
                 'spectral_perc_extra_bands',
                 'spectral_re_est_k_scrn',
                 'spectral_task',
                 'spectral_theory',
                 'spectral_write_eigenvalues',
                 'spectral_xc_definition',
                 'spectral_xc_functional',
                 'spin',
                 'spin_fix',
                 'spin_orbit_coupling',
                 # always scraped as polariZed
                 # 'spin_polarised',
                 'spin_polarized',
                 'spin_treatment',
                 'spin_unit',
                 'stop',
                 'task',
                 'tddft_approximation',
                 'tddft_convergence_win',
                 'tddft_eigenvalue_method',
                 'tddft_eigenvalue_tol',
                 'tddft_max_iter',
                 'tddft_method',
                 'tddft_nextra_states',
                 'tddft_num_states',
                 'tddft_position_method',
                 'tddft_selected_state',
                 'tddft_xc_definition',
                 'tddft_xc_functional',
                 'thermo_calculate_helmholtz',
                 'thermo_t_npoints',
                 'thermo_t_spacing',
                 'thermo_t_start',
                 'thermo_t_stop',
                 'time_unit',
                 'tssearch_cg_max_iter',
                 'tssearch_disp_tol',
                 'tssearch_energy_tol',
                 'tssearch_force_tol',
                 'tssearch_lstqst_protocol',
                 'tssearch_max_path_points',
                 'tssearch_method',
                 'tssearch_qst_max_iter',
                 'velocity_unit',
                 'verbosity',
                 'volume_unit',
                 'wannier_ion_cmoments',
                 'wannier_ion_cut',
                 'wannier_ion_cut_fraction',
                 'wannier_ion_cut_tol',
                 'wannier_ion_moments',
                 'wannier_ion_rmax',
                 'wannier_max_sd_steps',
                 'wannier_min_algor',
                 'wannier_print_cube',
                 'wannier_restart',
                 'wannier_sd_step',
                 'wannier_spread_tol',
                 'wannier_spread_type',
                 'write_bands',
                 'write_bib',
                 'write_cell_structure',
                 'write_checkpoint',
                 'write_cif_structure',
                 'write_cst_esp',
                 'write_formatted_density',
                 'write_formatted_elf',
                 'write_formatted_potential',
                 'write_geom',
                 'write_md',
                 'write_none',
                 'write_orbitals',
                 'write_otfg',
                 'xc_definition',
                 'xc_functional',
                 'xc_vxc_deriv_epsilon',
                ]
