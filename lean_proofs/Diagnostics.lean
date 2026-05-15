/-
  Lean 4 formalization of diagnostic identity modules.

  Source: paper theory package, Appendix C.
  Modules:
    A1: Three-regime regularized competition (memorize / generalize / collapse)
    B1: Large-WD collapse (regularizer dominance)
    C1: Participation ratio = 1 / (1 + CV^2) identity
    E1: Attention-score rank bounded by head dimension
    (D1 Hoeffding skipped — mathlib has stronger result.)

  Status: skeleton + statements. Proofs use mathlib4 lemmas where possible.
  Build: `cd lean_proofs && lake build` (mathlib pull on first run, ~30 min).
-/

import Mathlib.Algebra.Order.Field.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Analysis.MeanInequalities
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

namespace Diagnostics

open scoped Real

/-! ## Module A1: Three-Regime Regularized Competition -/

/-- Affine objective `J_λ(f) = ℓ_f + λ · ω_f` -/
def J (l ω lam : ℝ) : ℝ := l + lam * ω

/-- M-G crossover threshold from A1 -/
noncomputable def lambdaMG (lM lG ωM ωG : ℝ) : ℝ := (lG - lM) / (ωM - ωG)

/-- G-C crossover threshold from A1 -/
noncomputable def lambdaGC (lG lC ωG ωC : ℝ) : ℝ := (lC - lG) / (ωG - ωC)

/-- A1 part 1: below `lambdaMG`, memorizer beats generalizer. -/
theorem A1_memorize_below
    (lM lG ωM ωG lam : ℝ)
    (h_loss : lM ≤ lG) (h_norm : ωG < ωM)
    (h_lam : lam < lambdaMG lM lG ωM ωG) (h_lam_nn : 0 ≤ lam) :
    J lM ωM lam < J lG ωG lam := by
  unfold lambdaMG at h_lam
  have h_pos : 0 < ωM - ωG := by linarith
  have h_step : lam * (ωM - ωG) < lG - lM :=
    (lt_div_iff₀ h_pos).mp h_lam
  unfold J
  nlinarith [h_step]

/-- A1 part 2: between `lambdaMG` and `lambdaGC`, generalizer wins. -/
theorem A1_generalize_middle
    (lM lG lC ωM ωG ωC lam : ℝ)
    (h_loss1 : lM ≤ lG) (h_loss2 : lG < lC)
    (h_norm1 : ωG < ωM) (h_norm2 : ωC < ωG)
    (h_above : lambdaMG lM lG ωM ωG < lam)
    (h_below : lam < lambdaGC lG lC ωG ωC) :
    J lG ωG lam < J lM ωM lam ∧ J lG ωG lam < J lC ωC lam := by
  refine ⟨?_, ?_⟩
  · -- generalizer beats memorizer
    unfold lambdaMG at h_above
    have h_pos : 0 < ωM - ωG := by linarith
    have h_step : lG - lM < lam * (ωM - ωG) :=
      (div_lt_iff₀ h_pos).mp h_above
    unfold J
    nlinarith [h_step]
  · -- generalizer beats collapse
    unfold lambdaGC at h_below
    have h_pos : 0 < ωG - ωC := by linarith
    have h_step : lam * (ωG - ωC) < lC - lG :=
      (lt_div_iff₀ h_pos).mp h_below
    unfold J
    nlinarith [h_step]

/-- A1 part 3: above `lambdaGC`, collapse wins. -/
theorem A1_collapse_above
    (lG lC ωG ωC lam : ℝ)
    (h_loss : lG < lC) (h_norm : ωC < ωG)
    (h_lam : lambdaGC lG lC ωG ωC < lam) :
    J lC ωC lam < J lG ωG lam := by
  unfold lambdaGC at h_lam
  have h_pos : 0 < ωG - ωC := by linarith
  have h_step : lC - lG < lam * (ωG - ωC) :=
    (div_lt_iff₀ h_pos).mp h_lam
  unfold J
  nlinarith [h_step]

/-! ## Module B1: Large-Weight-Decay Collapse -/

/-- B1: if `λ > L_max / ε`, no minimizer of `J` lies in `F_ε`.
    Stated as: `J(f0) < J(f)` for any candidate `f` with norm gap `ε` from `f0`.
    Requires `Lmax > 0` to ensure the regularizer-dominance regime is nontrivial. -/
theorem B1_collapse_dominates
    (Lmax ε lam : ℝ) (h_eps : 0 < ε) (h_Lmax_pos : 0 < Lmax)
    (h_lam : Lmax / ε < lam)
    (l_f l_f0 ω_f ω_f0 : ℝ)
    (h_l_f : 0 ≤ l_f ∧ l_f ≤ Lmax)
    (h_l_f0 : 0 ≤ l_f0) (h_l_f0_ub : l_f0 ≤ Lmax)
    (h_omega_gap : ε ≤ ω_f - ω_f0) :
    l_f0 + lam * ω_f0 < l_f + lam * ω_f := by
  obtain ⟨h_lnn, h_lub⟩ := h_l_f
  have h_pos : 0 < lam := by
    have hd : 0 < Lmax / ε := div_pos h_Lmax_pos h_eps
    linarith
  have h_omega_lt : lam * ω_f0 + lam * ε ≤ lam * ω_f := by
    have hmul := mul_le_mul_of_nonneg_left h_omega_gap h_pos.le
    nlinarith
  have h2 : Lmax < lam * ε := (div_lt_iff₀ h_eps).mp h_lam
  -- l_f0 ≤ Lmax < lam*ε ≤ lam*(ω_f - ω_f0), so l_f0 + lam*ω_f0 < lam*ω_f ≤ l_f + lam*ω_f
  nlinarith

/-! ## Module C1: Participation Ratio = 1 / (1 + CV^2) -/

/-- Participation ratio (normalized) on a finite vector of head energies. -/
noncomputable def PRnorm (a : Fin n → ℝ) : ℝ :=
  let H : ℝ := n
  let s1 := (Finset.univ.sum a) ^ 2
  let s2 := Finset.univ.sum (fun i => (a i) ^ 2)
  s1 / (H * s2)

/-- Coefficient of variation squared on a finite vector. -/
noncomputable def CVsq (a : Fin n → ℝ) : ℝ :=
  let H : ℝ := n
  let mean := (Finset.univ.sum a) / H
  let var := Finset.univ.sum (fun i => (a i - mean) ^ 2) / H
  var / (mean ^ 2)

/-- Variance identity: `Σ aᵢ² = Σ (aᵢ - μ)² + n·μ²` where `μ = (Σ aᵢ)/n`.
    Standard algebra; expanded directly via `Finset.sum_add_distrib` + `ring`. -/
lemma sum_sq_eq_sum_sub_mean_sq_add_n_mul_mean_sq
    (n : ℕ) (a : Fin n → ℝ) (h_n : 0 < n) :
    Finset.univ.sum (fun i => (a i)^2)
      = Finset.univ.sum (fun i => (a i - (Finset.univ.sum a) / (n : ℝ))^2)
        + (n : ℝ) * ((Finset.univ.sum a) / (n : ℝ))^2 := by
  set H : ℝ := (n : ℝ)
  set s : ℝ := Finset.univ.sum a
  set μ : ℝ := s / H
  have hH_ne : (H : ℝ) ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) := by exact_mod_cast h_n
    linarith
  -- Σ aᵢ² = Σ ((aᵢ-μ)² + 2μ·aᵢ - μ²)
  have hpoint : ∀ i, (a i)^2 = (a i - μ)^2 + 2 * μ * (a i) - μ^2 := by
    intro i; ring
  calc Finset.univ.sum (fun i => (a i)^2)
      = Finset.univ.sum (fun i => (a i - μ)^2 + 2 * μ * (a i) - μ^2) := by
        apply Finset.sum_congr rfl; intros; exact hpoint _
    _ = Finset.univ.sum (fun i => (a i - μ)^2)
        + Finset.univ.sum (fun i => 2 * μ * (a i))
        - Finset.univ.sum (fun i => μ^2) := by
        rw [Finset.sum_sub_distrib, Finset.sum_add_distrib]
    _ = Finset.univ.sum (fun i => (a i - μ)^2)
        + 2 * μ * s
        - (n : ℝ) * μ^2 := by
        congr 1
        congr 1
        · rw [show (fun i => 2 * μ * (a i)) = (fun i => (2 * μ) * (a i)) from rfl,
              ← Finset.mul_sum]
        · simp [Finset.sum_const, Finset.card_fin]
    _ = Finset.univ.sum (fun i => (a i - μ)^2) + H * μ^2 := by
        have hsμ : s = H * μ := by
          show s = H * (s / H)
          rw [mul_div_assoc', mul_comm, mul_div_assoc, div_self hH_ne, mul_one]
        rw [hsμ]; ring

/-- C1 identity: `PR_norm = 1 / (1 + CV²)`.
    Substitutes the variance identity above into the algebra. -/
theorem C1_identity (n : ℕ) (a : Fin n → ℝ)
    (h_pos : 0 < (Finset.univ.sum a))
    (h_n : 0 < n) :
    PRnorm a = 1 / (1 + CVsq a) := by
  unfold PRnorm CVsq
  set H : ℝ := (n : ℝ) with hH_def
  set s : ℝ := Finset.univ.sum a with hs_def
  set S2 : ℝ := Finset.univ.sum (fun i => (a i)^2) with hS2_def
  set μ : ℝ := s / H with hμ_def
  have hH_pos : 0 < H := by
    show (0 : ℝ) < (n : ℝ)
    exact_mod_cast h_n
  have hH_ne : H ≠ 0 := ne_of_gt hH_pos
  have hμ_pos : 0 < μ := div_pos h_pos hH_pos
  have hμ_ne : μ ≠ 0 := ne_of_gt hμ_pos
  -- Variance identity: S2 = Σ(a-μ)² + H·μ²
  have hvar : S2 = Finset.univ.sum (fun i => (a i - μ)^2) + H * μ^2 := by
    have := sum_sq_eq_sum_sub_mean_sq_add_n_mul_mean_sq n a h_n
    convert this using 2
  -- Goal after `set`: s² / (H * S2) = 1 / (1 + (Σ(a-μ)² / H) / μ²)
  -- Use: S2 > 0 (since Σ(a-μ)² ≥ 0 and H·μ² > 0)
  have h_var_nn : 0 ≤ Finset.univ.sum (fun i => (a i - μ)^2) := by
    apply Finset.sum_nonneg; intros; positivity
  have hHμ2_pos : 0 < H * μ^2 := by positivity
  have hS2_pos : 0 < S2 := by rw [hvar]; linarith
  have hμ2_pos : 0 < μ^2 := by positivity
  -- 1 + (Σ(a-μ)²/H)/μ² = (H·μ² + Σ(a-μ)²) / (H·μ²) = S2 / (H·μ²)
  have h_one_plus : 1 + (Finset.univ.sum (fun i => (a i - μ)^2) / H) / μ^2
                  = S2 / (H * μ^2) := by
    rw [hvar]; field_simp; ring
  rw [h_one_plus]
  -- 1 / (S2 / (H·μ²)) = H·μ² / S2 = H · (s/H)² / S2 = s² / (H·S2)
  rw [one_div_div, hμ_def]
  field_simp

/-! ## Module E1: Head-Dimension Capacity Bound -/

/-- E1: `rank(QK^T) ≤ d_h` for `Q, K ∈ R^{T × d_h}`. -/
theorem E1_rank_bound
    {T d_h : ℕ} (Q K : Matrix (Fin T) (Fin d_h) ℝ) :
    (Q * K.transpose).rank ≤ d_h := by
  calc (Q * K.transpose).rank
      ≤ Q.rank := Matrix.rank_mul_le_left Q K.transpose
    _ ≤ Fintype.card (Fin d_h) := Matrix.rank_le_card_width Q
    _ = d_h := Fintype.card_fin d_h

/-! ## Module D1 (deferred to mathlib MeasureTheory.Concentration). -/

end Diagnostics
