# Challenges: Building Synthetic Data for PE Rollup Intelligence

This document captures the key challenges overcome during the development of the Causal Synth Engine.

---

## Challenge 1: Cold-Start Data Scarcity

**Problem:** Private equity vendor data is fragmented, private, and sparse. Training a GNN on real PE data leads to massive overfitting—the model memorizes the few examples rather than learning generalizable patterns.

**Naive solution:** Generate random synthetic data.

**Why naive fails:** Random data has no structure. A model trained on random switches learns nothing about *why* practices switch vendors.

**Solution:** Mechanism-first data generation. Define the causal rules first, then generate data that obeys them.

---

## Challenge 2: LLM Research Tool Selection

**Original Plan:** Use PyG TXT2KG tool for automated knowledge graph extraction from vendor websites.

**Actual Implementation:** Used manual LLM research with structured prompts (Claude Opus, Sonnet, ChatGPT Pro).

**Why different:**
- Manual LLM research gave higher quality results with confidence levels and source URLs
- PyG TXT2KG would have required NVIDIA NIM API setup
- Manual approach enabled category pattern discovery (critical insight)

**Result:** Extracted MORE data than planned—KPIs, pricing, certifications, DSO partnerships vs. just integration_quality.

---

## Challenge 3: Category Pattern Discovery

**Problem:** Initial design assumed generic integration quality assignments across all vendors.

**Discovery:** LLM research revealed that 5 of 7 categories have FIXED integration patterns:

| Category | Pattern | Evidence |
|----------|---------|----------|
| Lab | ALL partial_csv | STL file uploads, portal workflows |
| Telephony | ALL full_api | Call Pop requires real-time sync |
| Scheduling | ALL full_api | Calendar write-back requires real-time |
| Supplies | ALL partial_csv | Separate e-commerce portals |
| RCM | Tier-dependent | Premium vendors have certified integrations |

**Impact:** These structural patterns, not assumed but discovered, made the synthetic data realistic.

---

## Challenge 4: Cross-Model Validation

**Problem:** LLMs hallucinate. Asking "what EHR integrations does Weave support?" could return fabricated information.

**Solution:** Cross-validated findings across multiple models:
- Claude Opus 4.1 (Batches 1, 4)
- Claude Sonnet 4.5 (Batches 2, 5)
- ChatGPT Pro (Batch 3, validations)

**Example:**
- Claude: "All lab vendors use portal-based ordering"
- ChatGPT: "Glidewell, National Dentex, DDS Lab all require STL file upload"
- **Consensus:** Lab category = always partial_csv

---

## Challenge 5: Vendor Replacement During Research

**Problem:** Some vendors in the initial list had insufficient public documentation or no longer existed.

**Vendors Replaced:**
- V004: Original vendor → ROE Dental Laboratory
- V005: Original vendor → Vyne Dental
- V006: Original vendor → iCoreConnect

**Process:** Created SUPPLEMENT prompts for replacement vendors, maintained data quality standards.

---

## Challenge 6: Integration Quality Grounding

**Problem:** How to assign integration_quality (0/1/2) for 2,000 site×vendor pairs without real data?

**Solution:**
1. Researched 110 vendor×EHR combinations from vendor websites
2. Discovered category-level rules
3. Applied deterministic rules based on discovered patterns

**Coverage:**
- 58.2% full_api (quality=2)
- 39.1% partial_csv (quality=1)
- 2.7% none (quality=0)

---

## Challenge 7: Validation Against Industry Benchmarks

**Problem:** How to validate synthetic data without real PE data to compare against?

**Solution:** Validated against published industry benchmarks:

| Metric | Synthetic | Industry | Status |
|--------|-----------|----------|--------|
| Days A/R | 27.3 days | 30-40 days | PASS |
| Denial Rate | 5.6% | 7-9% | PASS |
| Switch Rate | 4.0% annual | ~5% | PASS |

---

## Key Lessons Learned

| Lesson | Impact |
|--------|--------|
| **Manual LLM > automated tools** | Higher quality, category pattern discovery |
| **Category rules > vendor rules** | Structural patterns more reliable than specifics |
| **Cross-model consensus** | Reduces hallucination risk |
| **Industry benchmarks validate** | External validation when no ground truth |
| **Ablation confirms mechanism** | -25.5% PR-AUC drop validates integration_quality |

---

> See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for full pipeline documentation.
