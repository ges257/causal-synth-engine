# Learnings: LLM-Driven Synthetic Data Generation

Key insights from building a research-derived market simulator for the PE Rollup Intelligence Platform.

---

## 1. Mechanism-First vs. Data-First

**Traditional ML:** Collect data → Find patterns → Hope they generalize

**This project:** Define mechanisms → Generate data → Model must rediscover mechanisms

| Approach | Outcome |
|----------|---------|
| Random synthetic data | Model memorizes noise, no generalization |
| Mechanism-first data | Model learns causal structure, validates via ablation |

**Validation:** Removing `integration_quality` caused -25.5% PR-AUC drop, proving the R-GCN learned the encoded mechanism.

---

## 2. Manual LLM Research > Automated Tools

**Original plan:** Use PyG TXT2KG for automated knowledge graph extraction.

**What happened:** Manual LLM research with structured prompts gave better results.

**Why manual won:**
- Higher confidence with source URLs
- Category pattern discovery (critical insight)
- Extracted more data than planned (KPIs, pricing, certifications)

**Lesson:** For domain-specific knowledge extraction, structured LLM prompts can outperform generic KG tools.

---

## 3. Category Rules > Vendor Rules

**Fragile:** "Glidewell integrates with Dentrix via partial_csv"
- Could be outdated
- Could be hallucinated
- Changes when vendor updates

**Robust:** "ALL dental labs use portal-based ordering (partial_csv)"
- Structural characteristic of the industry
- Confirmed across 4 lab vendors
- Unlikely to change

**Implementation:**
```python
if category == 'Lab':
    integration_quality = 1  # Always partial_csv
elif category == 'Telephony':
    integration_quality = 2  # Always full_api
```

---

## 4. Cross-Model Validation Reduces Hallucination

**Process:**
1. Research same vendors with Claude Opus, Sonnet, and ChatGPT Pro
2. Compare structural findings
3. Accept only consensus patterns

**Example validation:**
| Model | Finding |
|-------|---------|
| Claude Opus | "Lab vendors use portal-based workflows" |
| ChatGPT Pro | "Glidewell, National Dentex require STL upload" |
| **Consensus** | Lab = partial_csv (confirmed) |

**Result:** 5 of 7 categories have FIXED patterns discovered through consensus.

---

## 5. Three-Layer Data Ontology

| Layer | Source | Reliability |
|-------|--------|-------------|
| **Structure** | LLM research (20 real vendors) | High |
| **Parameters** | Web-grounded category patterns | Medium |
| **Instances** | Python generation (100 practices) | Deterministic |

**Key insight:** Keep real structure, parameterize with discovered rules, generate instances programmatically.

---

## 6. Industry Benchmarks Validate When No Ground Truth

**Problem:** No real PE vendor data to validate against.

**Solution:** Validate against published industry benchmarks:

| Metric | Synthetic | Industry | Validation |
|--------|-----------|----------|------------|
| Days A/R | 27.3 days | 30-40 days | PASS |
| Denial Rate | 5.6% | 7-9% | PASS |
| Switch Rate | 4.0% annual | ~5% | PASS |

---

## 7. Ablation Studies Validate Mechanism Encoding

**The ultimate test:** Does removing a feature hurt the model?

| Feature Removed | PR-AUC | Delta |
|-----------------|--------|-------|
| Full model | 0.9407 | - |
| `integration_quality` | 0.6852 | **-25.5%** |
| `vendor_tier` | 0.9368 | -0.4% |
| `site_region` | 0.9260 | -1.6% |

**Conclusion:** The synthetic data successfully encoded integration_quality as the dominant causal driver.

---

## Summary

| Learning | Application |
|----------|-------------|
| Mechanism-first | Define causation before generating data |
| Manual LLM > tools | Structured prompts for domain knowledge |
| Category > vendor | Encode structural patterns, not specifics |
| Cross-model consensus | Validate with multiple LLMs |
| Three-layer ontology | Structure → Parameters → Instances |
| Industry benchmarks | External validation without ground truth |
| Ablation validates | Confirms mechanism encoding worked |

---

> See [CHALLENGES.md](CHALLENGES.md) for implementation challenges.
> See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for full pipeline documentation.
