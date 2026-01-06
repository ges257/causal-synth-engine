# Challenges: Building Synthetic Data for PE Rollup Intelligence

This document captures the key challenges overcome during the development of the Causal Synth Engine.

---

## Challenge 1: Cold-Start Data Scarcity

**Problem:** Private equity vendor data doesn't exist in public datasets. PE firms pay consultants $1M+/year for intelligence that should be table stakes.

**Why it matters:**
- Each portfolio company tracks vendors differently
- Contracts, pricing, and switching decisions are confidential
- A typical PE fund sees only 10-20 vendor transitions per year

**Naive solution:** Generate random synthetic data.

**Why naive fails:** Random data has no structure. A model trained on random switches learns nothing about *why* practices switch vendors. Predictions are statistically valid but operationally useless.

**Our solution:** Mechanism-first data generation. Define the causal rules first, then generate data that obeys them.

---

## Challenge 2: LLM Research Reliability

**Problem:** LLMs hallucinate. Asking "what EHR integrations does Weave support?" could return fabricated information.

**Diagnosis:** Early research prompts returned plausible-sounding but unverifiable claims about vendor capabilities.

**Solution:**
1. Required LLMs to cite specific sources (vendor websites, press releases)
2. Cross-validated findings across multiple models (Claude Opus, Sonnet, ChatGPT Pro)
3. Focused on structural patterns rather than specific claims

**Example of cross-validation:**
- Claude Opus: "All lab vendors use portal-based ordering"
- ChatGPT Pro: "Glidewell, National Dentex, and Modern Dental all require STL file upload"
- **Conclusion:** Lab category = always partial_csv (validated across models)

---

## Challenge 3: Encoding Real Mechanisms vs. Arbitrary Rules

**Problem:** How do you know your causal mechanisms reflect reality?

**Diagnosis:** Initial mechanism designs were based on intuition. "Integration quality probably affects switching" is a hypothesis, not a fact.

**Solution:** Ground mechanisms in observable patterns from LLM research:

| Discovered Pattern | Encoded Mechanism |
|-------------------|-------------------|
| "Telephony requires real-time call pop" | Telephony = always full_api |
| "Labs use portal-based STL uploads" | Lab = always partial_csv |
| "Premium RCM vendors have certified integrations" | RCM integration = tier-dependent |

**Validation:** Ablation studies on downstream R-GCN confirmed integration_quality was the dominant feature (-25.5% PR-AUC when removed).

---

## Challenge 4: Avoiding Trivial Learnability

**Problem:** If the synthetic data is too simple, any model achieves 99% accuracy. If too complex, nothing learns.

**Diagnosis:** Early generators created perfectly separable classes. A decision tree could achieve 100% accuracy by checking one feature.

**Solution:** Added realistic noise and confounders:
- **Seasonality:** December/January peaks in A/R
- **Site-level baselines:** Each practice has inherent characteristics
- **Change fatigue:** Recent switches reduce future switching probability
- **Random noise:** N(0, σ) on all KPIs

**Result:** Final dataset required an R-GCN to achieve 0.94 PR-AUC. Simple baselines (logistic regression) achieved only 0.72.

---

## Challenge 5: Multi-Model Orchestration

**Problem:** Different LLMs have different strengths. Which model for which task?

**Solution:** Task-specific model selection:

| Task | Best Model | Reasoning |
|------|-----------|-----------|
| Deep vendor research | Claude Opus | Best at following complex prompts |
| Pattern synthesis | Claude Sonnet | Good balance of speed and quality |
| Telephony vendors | ChatGPT Pro | Better at real-time web access |
| Cross-validation | All three | Consensus reduces hallucination |

---

## Key Lessons Learned

| Lesson | Impact |
|--------|--------|
| **Mechanism-first beats data-first** | Model learned causal structure, not arbitrary patterns |
| **Cross-model validation reduces hallucination** | Structural patterns confirmed across Claude + GPT |
| **Category rules > vendor rules** | "All labs use portals" more reliable than "Glidewell uses X" |
| **Noise is necessary** | Trivial data = trivial model = no generalization |
| **Ablation validates mechanisms** | -25.5% PR-AUC drop confirms integration_quality matters |

---

> See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for full pipeline documentation.
