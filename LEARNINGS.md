# Learnings: LLM-Driven Synthetic Data Generation

Key insights from building a research-derived market simulator for the PE Rollup Intelligence Platform.

---

## 1. Mechanism-First vs. Data-First

**Traditional ML:** Collect data → Find patterns → Hope they generalize

**This project:** Define mechanisms → Generate data → Model must rediscover mechanisms

| Approach | Outcome |
|----------|---------|
| Random synthetic data | Model memorizes noise, 0% generalization |
| Mechanism-first data | Model learns causal structure, validates via ablation |

**Validation:** Removing `integration_quality` caused -25.5% PR-AUC drop, proving the R-GCN learned the encoded mechanism.

---

## 2. LLM Research Patterns

### What Works
- **Structural questions:** "What integration method do dental labs use?" → Consistent answer (portal uploads)
- **Category-level patterns:** "Do telephony vendors need real-time sync?" → Yes (Call Pop requires it)
- **Cross-model consensus:** Same answer from Claude + GPT = likely true

### What Doesn't Work
- **Specific claims:** "Does Vendor X integrate with Dentrix?" → Often hallucinated
- **Pricing data:** Vendors don't publish exact pricing → LLMs guess
- **Partnership details:** "Is Vendor X a Heartland Dental partner?" → Unverifiable

### Solution: Three-Layer Ontology

| Layer | Source | Reliability |
|-------|--------|-------------|
| **Structure** | LLM research | High (vendor websites exist) |
| **Parameters** | Web-grounded patterns | Medium (category-level rules) |
| **Instances** | Python generation | Deterministic (follows rules) |

---

## 3. Multi-Model Orchestration

Different LLMs excel at different tasks:

| Model | Strength | Used For |
|-------|----------|----------|
| Claude Opus | Complex reasoning, long prompts | Deep vendor research |
| Claude Sonnet | Speed + quality balance | Pattern synthesis |
| ChatGPT Pro | Real-time web access | Telephony vendor research |

**Key insight:** Cross-validation across models reduces hallucination. If Claude and GPT agree on a structural pattern, it's likely real.

---

## 4. Category Rules > Vendor Rules

**Fragile:** "Glidewell integrates with Dentrix via API"
- Could be outdated
- Could be hallucinated
- Changes when vendor updates

**Robust:** "All dental labs use portal-based ordering (partial_csv)"
- Structural characteristic of the industry
- Confirmed across multiple vendors
- Unlikely to change

**Implementation:** Encode category-level rules, not vendor-specific claims.

```python
if category == 'Lab':
    integration_quality = 1  # Always partial_csv
elif category == 'Telephony':
    integration_quality = 2  # Always full_api
```

---

## 5. Noise is Necessary

Early generators created perfectly separable data:
- Decision tree: 100% accuracy
- No generalization value

**Solution:** Add realistic noise sources:

| Noise Source | Purpose |
|--------------|---------|
| Site baselines | Each practice has inherent characteristics |
| Seasonality | December/January peaks in A/R |
| Change fatigue | Recent switches reduce future probability |
| Random noise | N(0, σ) on all KPIs |

**Result:** Final dataset required R-GCN to achieve 0.94 PR-AUC. Simple baselines achieved only 0.72.

---

## 6. Ablation Validates Design

The ultimate test: does removing a feature hurt the model?

| Feature Removed | PR-AUC | Delta |
|-----------------|--------|-------|
| Full model | 0.9407 | - |
| `integration_quality` | 0.6852 | **-25.5%** |
| `vendor_tier` | 0.9368 | -0.4% |
| `site_region` | 0.9260 | -1.6% |

**Conclusion:** The synthetic data successfully encoded integration_quality as the dominant causal driver. The model learned the mechanism, not arbitrary patterns.

---

## Summary Table

| Lesson | Implication |
|--------|-------------|
| Mechanism-first | Define causation before generating data |
| Category > vendor | Structural patterns more reliable than specifics |
| Cross-model validation | Consensus reduces hallucination |
| Three-layer ontology | Separate structure, parameters, instances |
| Noise required | Trivial data = trivial model |
| Ablation validates | Feature importance confirms mechanism encoding |

---

> See [CHALLENGES.md](CHALLENGES.md) for implementation challenges.
> See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for full pipeline documentation.
