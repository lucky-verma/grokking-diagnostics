---
status: active
audience: [researcher, artifact]
lifetime: permanent
last_reviewed: 2026-05-14 16:40 UTC
auto_generated: true
---

# Paper Sources Coverage Dashboard

Auto-generated from `docs/paper_sources.json` by `tools/paper-hygiene/generate-coverage.py`. **DO NOT EDIT BY HAND** — regenerate via `python3 tools/paper-hygiene/generate-coverage.py <paper-slug>`.

**19 tables, 57 cells**

| Status | Count |
|---|---|
| ✅ verified | 57 |

## Cell-level coverage

### `appendix_c1_empirical_validation` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `identity_error` | — | — | 0.000000210 PR_mean_err, PR_max_err=1.73e-6, PR_norm_max_err=2.56e-7, n_valid_rows=183, n_skipped=37 | — | source: eval/c1_empirical_validation.json; field identity_error_bias_corrected.PR_mean_err matches |
| ✅ | `cv_trajectory_canonical_s42` | — | — | 0.392 mean CV(lambda) at epoch 100 -> 1.880 at epoch 20000, with intermediate phase-scale oscillations; measured and C1-predicted PR_norm match to displayed precision | — | source: eval/c1_empirical_validation.json; field cv_trajectory_canonical_s42.0.mean_CV_lambda matches |
| ✅ | `seeds` | — | — | canonical_seed42 plus cross_seed_s7, cross_seed_s11, cross_seed_s31, cross_seed_s123 | — | source: eval/c1_empirical_validation.json; field _seeds string list matches |

### `appendix_lambda_c_sensitivity` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `kappa_source` | — | — | 18.58316710113753 from eval/adamw_relaxation/kappa_cross_seed.json canonical_s42 full fit | — | source: eval/adamw_relaxation/lambda_c_sensitivity_table.json; field kappa matches |
| ✅ | `p099_lambda_c_bound` | — | — | 0.012390703266361401 | — | source: eval/adamw_relaxation/lambda_c_sensitivity_table.json; field rows[p_relax=0.99].derived_lambda_c matches |
| ✅ | `p099_ratio` | — | — | 0.7842217257190759 | — | source: eval/adamw_relaxation/lambda_c_sensitivity_table.json; field rows[p_relax=0.99].ratio_derived_over_empirical matches |
| ✅ | `p099_in_ci` | — | — | True | — | source: eval/adamw_relaxation/lambda_c_sensitivity_table.json; field rows[p_relax=0.99].in_empirical_95_ci boolean matches |

### `appendix_mamba_scope_probes` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `mamba_4L_d128_e2_mod_add` | — | — | wd_c=0.016321, ci_95=[0.013809, 0.018160], n_grok=42, n_points=70 | — | derived (no folders) |
| ✅ | `mamba_4L_d128_mod_mul` | — | — | wd_c=0.019086, ci_95=[0.016877, 0.021855], n_grok=37, n_points=70 | — | derived (no folders) |

### `discussion_mlp_pilot_mlp_scope_probe` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `mlp_pilot_done` | — | — | DONE 2026-04-25T00:14:41Z ok=12 fail=0 | — | source: eval/mlp_pilot/mlp_pilot_summary.json; status done and grid ok=12 fail=0 match |
| ✅ | `mlp_pilot_grok_by_wd` | — | — | wd0.01: 0/3 grok; wd0.1: 1/3; wd0.5: 3/3; wd1.0: 3/3 | — | source: eval/mlp_pilot/mlp_pilot_summary.json; field aggregate_by_wd matches displayed numbers |

### `fig10_mlp_cross_arch` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `transformer_small_pooled_4ops` | — | — | wd_c=0.007739, ci_95=[0.005574, 0.010647], n_grok=102, n_points=140 | — | source: eval/multitask_logistic.json; field transformer_small_pooled_4ops matches displayed numbers |
| ✅ | `transformer_medium_pooled_4ops` | — | — | wd_c=0.012762, ci_95=[0.007647, 0.019415], n_grok=82, n_points=140 | — | source: eval/multitask_logistic.json; field transformer_medium_pooled_4ops matches displayed numbers |
| ✅ | `mlp_4L_h512_mod_add` | — | — | wd_c=0.051081, ci_95=[0.049527, 0.059119], n_grok=13, n_points=70 | — | source: eval/multitask_logistic.json; field mlp_4L_h512_mod_add matches displayed numbers |
| ✅ | `lstm_4L_h512_mod_add` | — | — | wd_c=0.036457, ci_95=[0.029895, 0.047333], n_grok=22, n_points=70 | — | source: eval/multitask_logistic.json; field lstm_4L_h512_mod_add matches displayed numbers |
| ✅ | `mamba_4L_d128_mod_add` | — | — | wd_c=0.014389, ci_95=[0.010565, 0.015954], n_grok=46, n_points=70 | — | source: eval/multitask_logistic.json; field mamba_4L_d128_mod_add matches displayed numbers |

### `fig1_phase_diagram` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `wd_axis_logistic_n210` | — | — | 210 | — | source: a5_wdc_fit.json; field n_records matches |
| ✅ | `three_scale_axis_n90` | — | — | 90 | — | source: a6_phase_boundaries.json; filtered run count 90 matches |

### `fig2_two_phase` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `canonical_replicated_n50` | — | — | 50 | — | source: a6_phase_boundaries.json; filtered run count 50 matches |

### `fig3_five_phase` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `canonical_anti_grok_seed42_focus` | — | — | test_acc 0.459 final (anti-grok collapse) | — | source: a6_phase_boundaries.json; filtered one run; final_test_acc=0.4589 matches |
| ✅ | `cross_seed_underlay` | — | — | 4 cross-seed underlay traces: seeds 7, 11, 31, 123 | — | All four cross-seed raw history files exist and are loaded directly by src/gen_fig3_cross_seed.py. |
| ✅ | `e8_retention_context` | — | — | 20 runs; retention rates 5/5, 4/5, 3/5, 4/5 at wd 0.1, 0.5, 1.0, 2.0 | — | Retention-rate context is reported from the long-horizon retention aggregate and used only for the seed-dependent-fragility qualifier. |

### `fig4_dh_amplitude` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `sat_exp_fit_n44` | — | — | 44 | — | source: a2_per_head_dim_scaling.json; field n_runs matches |
| ✅ | `random_label_null` | — | — | mean=0.0875, std=0.0247, n=15 (rounded 0.087+-0.025 in text) | — | source: a3_perm_test.json; field null_amp_stats.mean matches |

### `fig5_wdc_nu` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `logistic_wd_c_n210` | — | — | wd_c=0.0158, ci=[0.0109, 0.0200], n_bootstrap_ok=1500 | — | source: a5_wdc_fit.json; field wd_c_fit matches displayed numbers |
| ✅ | `nu_power_law_n140` | — | — | nu=0.7575, n_points=140, ci=[0.7248, 0.7987] | — | source: a5_wdc_fit.json; field nu_fit matches displayed numbers |
| ✅ | `nu_jackknife_n148` | — | — | nu_full=0.7621, nu_bias_corrected=0.7609, se=0.0194, ci_95=[0.7228, 0.7989], n_points=148 | — | source: a5_nu_jackknife.json; fields match displayed numbers |
| ✅ | `b3_universality_check` | — | — | nu=0.7575, ci=[0.7248,0.7987], snic_rejected=true, 3d_ising_rejected=true | — | source: b3_snic_universality.json; fields match displayed numbers |

### `fig7_esd_alpha` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `alpha_init` | — | — | 2.072 at epoch 100 | — | source: esd_alpha_trace.json; field alpha_median_series[0] matches |
| ✅ | `alpha_grok_onset` | — | — | 1.392 at epoch 500 | — | source: esd_alpha_trace.json; field alpha_median_series[1] matches |
| ✅ | `alpha_phase5_final` | — | — | 1.346 at epoch 20000 | — | source: esd_alpha_trace.json; field alpha_median_series[-1] matches |
| ✅ | `alpha_heavy_tail_after_onset` | — | — | all post-onset medians < 2 through Phase 5 | — | source: esd_alpha_trace.json; all post-onset alpha medians < 2 |
| ✅ | `seed_coverage` | — | — | Main Fig. 7 is seed-42 only; matched-grid cross-seed Weightwatcher is deferred. Coarser cross-seed sidecar evidence exists but is not used for the main figure claim. | — | Seed coverage is an explicit scope note: Fig. 7 main trace is canonical seed 42; cross-seed Weightwatcher sidecar is not promoted to the main figure. |

### `fig8_intervention_forest` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `B_minus_A_peak_sigma_H` | — | — | mean_diff=-0.037925, ci_95_diff=[-0.056988, -0.020457], n=20, p_value_t=9.3e-4 | — | source: eval/intervention_stats.json; field paired_tests.B_minus_A.peak_ent.mean_diff matches |
| ✅ | `C_minus_A_peak_sigma_H` | — | — | mean_diff=-0.016874, ci_95_diff=[-0.035729, 0.000482], n=19, p_value_t=0.0938 | — | source: eval/intervention_stats.json; field paired_tests.C_minus_A.peak_ent.mean_diff matches |
| ✅ | `C_minus_B_peak_sigma_H` | — | — | mean_diff=0.022695, ci_95_diff=[-0.003974, 0.044167], n=19, p_value_t=0.0854 | — | source: eval/intervention_stats.json; field paired_tests.C_minus_B.peak_ent.mean_diff matches |

### `fig9_multitask_grok_rate` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `multitask_full_grid` | — | — | 56 task-scale-WD cells (4 tasks x 2 scales x 7 WD values), each n=5 seeds; grok_rate plotted as groked/n | — | source: eval/multitask_summary.json; multitask_full_grid has 56 cells with n=5 each |
| ✅ | `multitask_per_wd_pooled` | — | — | pooled grok rate increases from 7/40 at WD=0.003 to 40/40 at WD=0.07 | — | source: eval/multitask_summary.json; multitask_per_wd endpoints 7/40 and 40/40 match |
| ✅ | `multitask_per_task_pooled` | — | — | mod_add 51/70, mod_div 50/70, mod_mul 49/70, mod_sub 34/70 | — | source: eval/multitask_summary.json; field multitask_per_task matches displayed numbers |

### `sec_retention_discriminator` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `rf_holdout_auc` | — | — | 0.7992424242424242 | — | source: eval/holdout_retention.json; field rf.holdout_auc matches |
| ✅ | `rf_holdout_brier` | — | — | 0.09807870321913324 | — | source: eval/holdout_retention.json; field rf.holdout_brier matches |
| ✅ | `logistic_holdout_auc` | — | — | 0.678030303030303 | — | source: eval/holdout_retention.json; field logistic.holdout_auc matches |
| ✅ | `train_holdout_sizes` | — | — | train=998, holdout=50 | — | source: eval/holdout_retention.json; field sample_sizes matches displayed numbers |
| ✅ | `gate_verdict` | — | — | CORRELATIONAL_ONLY; below pre-registered AUC >= 0.85 predictor gate | — | source: eval/holdout_retention.json; field gate.verdict string matches |
| ✅ | `top5_features` | — | — | wd 0.247, weight_norm 0.220, sim_mean 0.145, ent_std 0.130, test_acc 0.123 | — | source: eval/holdout_retention.json; field rf.top5_features matches displayed numbers |

### `sec_intervention_stratified` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `wd005_B_minus_A_peak_ent` | — | — | mean_diff=-0.05515, p_t=0.004463, d=-1.190, n=10 | — | source: eval/intervention_stats.json; field stratified_by_wd.wd0.05.B_minus_A__peak_ent matches displayed numbers |
| ✅ | `wd0015_B_minus_A_peak_ent` | — | — | mean_diff=-0.02070, p_t=0.08611, d=-0.609, n=10 | — | source: eval/intervention_stats.json; field stratified_by_wd.wd0.015.B_minus_A__peak_ent matches displayed numbers |
| ✅ | `wd005_C_minus_B_peak_ent` | — | — | mean_diff=0.04821, p_t=0.001428, d=1.586, n=9 | — | source: eval/intervention_stats.json; field stratified_by_wd.wd0.05.C_minus_B__peak_ent matches displayed numbers |

### `tab_controls` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `add_vs_random_perm` | — | — | obs_diff=0.0245, p=0.00940, n_perm=10000 | — | source: a3_perm_test.json; field amplitude_perm matches displayed numbers |
| ✅ | `cohen_d_add_vs_random` | — | — | d=1.1068, n_a=12, n_b=15 | — | source: a7_cohens_d.json; field add_vs_random_amplitude matches displayed numbers |
| ✅ | `task_universality_m6_n28` | — | — | 28 | — | source: a6_phase_boundaries.json; filtered run count 28 matches |

### `tab_kuramoto` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `r2_median_n50` | — | — | r2_median=0.843, n_r2_ok(R2>0.9)=10, n_fit=50 post Phase A | — | source: b4_kuramoto_phase1.json; fields match displayed numbers |

### `tab_numrunsmain` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `total_runs` | — | — | 1120 | — | source: docs/paper_sources.json; field _total_runs_main_after_public_integration matches |

### `tab_perm_symmetry` ✅

| | Cell | Seeds | Eff | Value | Folders | Notes |
|---|---|---|---|---|---|---|
| ✅ | `m_perm_n50_canonical` | — | — | 0.578 +- 0.096, n=50 post Phase A | — | source: b1_permutation_symmetry.json; fields match displayed numbers |
| ✅ | `b5_direct_perm_test` | — | — | PR_norm median trace init 0.86 -> P1 onset 0.71 at epoch 500 -> epoch 1000 value 0.48 -> P2-4 oscillates 0.18-0.55 -> P5 collapse 0.13 | — | source: b5_direct_perm_test.json; PR_norm init/onset/1K/P2-4 range/final match |
| ✅ | `cross_seed_pr_norm` | — | — | 4 non-canonical cross-seed cohort seeds aggregated; common 11-checkpoint grid, n_valid_seeds=4 except epoch 17500 where n_valid_seeds=3 | — | source: eval/pysr_sweep/cross_seed_aggregated/pr_norm_cross_seed.csv; source exists; non-JSON value check skipped |
| ✅ | `t_test_p_value` | — | — | legacy M_perm p<1e-10 (superseded by direct PR_norm trace) | — | derived (no folders) |

## Action items (cells needing fixes)

✅ No cells need attention.

---
_Regenerate: `python scripts/verify_numerical_claims.py`_
