# Synthetic Data Generation Methodology

**Author:** Gregory Schwartz
**Date:** December 2, 2025
**Project:** Dental Vendor Adoption Prediction with GNNs

---

## Approach: Mechanism-First Data Generation

I generated synthetic data by defining causal mechanisms first, then producing data that obeys them:

1. **Define mechanisms (the "why"):**
   - Why do practices switch vendors? → Integration pain, change fatigue
   - Why do KPIs vary? → Vendor quality, integration friction, seasonality

2. **Encode mechanisms as formulas:**
   - `P_switch = base × integration_multiplier × fatigue_multiplier`
   - `Days_AR = baseline + vendor_effect + integration_bonus + seasonality + noise`

3. **Generate data that follows these mechanisms**

The result is synthetic data with explainable structure that mirrors real-world causation. When a model learns from this data, it must discover the underlying causal relationships—not just memorize arbitrary patterns.

---

## 1. Overview

I developed a two-phase synthetic data generation pipeline to create realistic training data for predicting dental practice vendor adoption decisions. The approach combines:

1. **Phase 1 (LLM Research):** Real vendor knowledge extraction using large language models
2. **Phase 2 (Python Simulation):** Mechanism-based synthetic practice data generation

This methodology grounds the synthetic data in real-world vendor capabilities while enabling controlled simulation of practice behavior over time.

### Data Scale

| Component | Count |
|-----------|-------|
| Dental Practices (Sites) | 100 |
| Vendors | 20 |
| Vendor Categories | 7 |
| Time Period | 2019-2024 (72 months) |
| Total Contracts | 866 |
| Monthly KPI Records | 7,200 |

---

## 2. Phase 1: LLM-Based Vendor Research

### Purpose

I used large language models to research real dental industry vendors and extract structured information about their:
- EHR integration capabilities
- Key features and specializations
- DSO (Dental Service Organization) partnerships
- Geographic coverage
- Quality certifications

This grounded the synthetic data in actual vendor characteristics rather than random generation.

### Models Used

| Model | Use Case |
|-------|----------|
| Claude Opus 4.1 | Primary research (Batches 1, 4) |
| Claude Sonnet 4.5 | Secondary research (Batches 2, 5) |
| ChatGPT Pro | Validation and telephony vendors (Batch 3) |

### Research Batches

I organized the research into 5 batches by vendor category:

| Batch | Category | Vendors | Primary Model |
|-------|----------|---------|---------------|
| 1 | Lab | V001-V004 | Claude Opus |
| 2 | RCM | V005-V007 | Claude Sonnet + GPT Pro |
| 3 | Telephony | V008-V010 | ChatGPT Pro |
| 4 | Scheduling + Clearinghouse | V011-V015 | Claude Opus |
| 5 | IT_MSP + Supplies | V016-V020 | Claude Sonnet |

### Prompt Template

For each batch, I provided the LLM with a structured prompt requesting:

```
For each vendor, investigate their official website and extract:

1. EHR Integration Capabilities
   - Which dental EHR systems do they integrate with?
   - Examples: Dentrix, Dentrix Ascend, OpenDental, Eaglesoft, Curve Dental, Denticon

2. Integration Type (choose one per EHR)
   - full_api: Real-time API, certified integration partner, bidirectional sync
   - partial_csv: CSV import/export, file-based data exchange, one-way sync
   - none: No documented integration, manual entry only

3. Key Features & Specializations
   - What do they specialize in?
   - Digital workflow capabilities
   - Notable technologies (AI, CAD/CAM, etc.)

4. Peer Adoption Evidence
   - Customer counts ("500+ practices", "nationwide network")
   - DSO partnerships (Smile Brands, PDS, Aspen Dental, Heartland Dental, etc.)
   - Scale indicators ("multi-state", "regional", "national")

5. Coverage/Geographic Reach
   - National vs regional
   - Multi-location capabilities

Output Format:
- Include source URLs for each fact
- Rate confidence: high/medium/low
- Flag any contradictions or ambiguities
```

### 20 Vendors Researched

| ID | Vendor Name | Category | Tier |
|----|-------------|----------|------|
| V001 | National Dentex | Lab | 2 |
| V002 | Glidewell Labs | Lab | 3 |
| V003 | DDS Lab | Lab | 2 |
| V004 | ROE Dental | Lab | 1 |
| V005 | Vyne Dental | RCM | 3 |
| V006 | iCoreConnect | RCM | 2 |
| V007 | DentalXChange | RCM | 1 |
| V008 | Weave | Telephony | 3 |
| V009 | Lighthouse 360 | Telephony | 2 |
| V010 | Solutionreach | Telephony | 2 |
| V011 | Yapi | Scheduling | 2 |
| V012 | Dental Intelligence | Scheduling | 3 |
| V013 | NexHealth | Scheduling | 2 |
| V014 | DentalXChange | Clearinghouse | 2 |
| V015 | NEA FastAttach | Clearinghouse | 1 |
| V016 | Henry Schein TechCentral | IT_MSP | 3 |
| V017 | Pact-One (Premium) | IT_MSP | 2 |
| V018 | Pact-One (Basic) | IT_MSP | 1 |
| V019 | Patterson Dental | Supplies | 2 |
| V020 | Benco Dental | Supplies | 2 |

### Key Findings from LLM Research

**Integration Patterns Discovered:**

| Category | Integration Type | Rationale |
|----------|-----------------|-----------|
| Lab | Always `partial_csv` (1) | Portal-based STL file upload |
| Telephony | Always `full_api` (2) | Real-time call pop required |
| Scheduling | Always `full_api` (2) | Instant calendar write-back |
| Supplies | Always `partial_csv` (1) | Separate e-commerce portal |
| RCM | Variable (0, 1, 2) | Depends on tier and EHR |
| Clearinghouse | Variable (1, 2) | Vendor-specific |
| IT_MSP | Variable (1, 2) | Based on EHR ownership |

**Note:** Full LLM research results are available on request. See `llm_research_sample.md` for a complete example of Batch 1 (Lab Vendors) research output.

---

## 3. Phase 2: Python Generation Pipeline

I built a 6-step Python pipeline that generates synthetic practice data using the real vendor characteristics extracted in Phase 1.

### Pipeline Architecture

```
generate_all_data.py (Master Script)
    │
    ├── Step 1: generate_sites.py → sites.csv
    ├── Step 2: generate_vendors.py → vendors.csv
    ├── Step 3: generate_integration_matrix.py → integration_matrix.csv
    ├── Step 4: generate_initial_state.py → initial_state_2019.csv
    ├── Step 5: simulate_switches.py → contracts_2019_2024.csv
    └── Step 6: generate_kpis.py → kpis.csv
```

### Step 1: Generate Sites (`generate_sites.py`)

Creates 100 synthetic dental practices with realistic distributions.

**Output:** `sites.csv` (100 rows)

| Column | Description | Distribution |
|--------|-------------|--------------|
| site_id | Unique identifier | S001-S100 |
| region | Geographic region | South 35%, Northeast 25%, West 20%, Midwest 20% |
| ehr_system | Practice management system | Dentrix 35%, OpenDental 25%, Eaglesoft 20%, Curve 10%, Other 10% |
| date_joined | Network join date | Random throughout 2019 |
| annual_revenue | Practice annual revenue | Log-normal, median ~$2M, range $800K-$5M |

### Step 2: Generate Vendors (`generate_vendors.py`)

Defines the 20 vendors using real names from LLM research.

**Output:** `vendors.csv` (20 rows)

| Column | Description |
|--------|-------------|
| vendor_id | V001-V020 |
| name | Real vendor name |
| category | One of 7 categories |
| tier | 1 (budget), 2 (standard), 3 (premium) |
| monthly_price_per_site | Category-based pricing with tier deltas |

**Pricing by Category:**

| Category | Monthly Price Range |
|----------|-------------------|
| Lab | $7,500 - $8,500 |
| RCM | $2,000 - $3,000 |
| Telephony | $400 - $1,000 |
| Scheduling | $300 - $600 |
| Clearinghouse | $100 - $300 |
| IT_MSP | $1,000 - $2,500 |
| Supplies | $900 - $1,500 |

### Step 3: Generate Integration Matrix (`generate_integration_matrix.py`)

Creates integration quality scores for every site-vendor pair, applying the category-specific rules discovered from LLM research.

**Output:** `integration_matrix.csv` (2,000 rows = 100 sites x 20 vendors)

| Column | Description |
|--------|-------------|
| site_id | Practice identifier |
| vendor_id | Vendor identifier |
| integration_quality | 0 (none), 1 (partial_csv), 2 (full_api) |

**Integration Rules Applied:**

```python
# Fixed patterns (from LLM research)
if category == 'Lab':
    integration_quality = 1  # Always partial_csv (portal upload)
elif category == 'Telephony':
    integration_quality = 2  # Always full_api (real-time required)
elif category == 'Scheduling':
    integration_quality = 2  # Always full_api (calendar sync)
elif category == 'Supplies':
    integration_quality = 1  # Always partial_csv (e-commerce)

# Variable patterns
elif category == 'RCM':
    # Tier 1 + major EHRs: 80% full_api
    # Tier 2+: 40% full_api
    integration_quality = probabilistic_assignment()
elif category == 'IT_MSP':
    # Henry Schein owns Dentrix family → full_api
    # Others → partial_csv
    integration_quality = ownership_based_assignment()
```

### Step 4: Generate Initial State (`generate_initial_state.py`)

Creates the baseline vendor contracts as of January 1, 2019.

**Output:** `initial_state_2019.csv` (700 rows = 100 sites x 7 categories)

Each site starts with exactly one vendor per category, selected using weighted probability:

```python
selection_weight = 0.5 * integration_quality + 0.3 * tier
vendor = softmax_sample(vendors_in_category, weights=selection_weight)
```

### Step 5: Simulate Vendor Switches (`simulate_switches.py`)

Simulates realistic vendor switching behavior from 2019-2024 using causal mechanisms.

**Output:** `contracts_2019_2024.csv` (866 rows = 700 initial + 166 switches)

**Switching Probability Formula:**

```python
P_switch = base_monthly * integration_multiplier * fatigue_multiplier

# Base rate: 5% annual → 0.42% monthly
base_monthly = 0.05 / 12

# Integration pain drives switching
integration_multiplier = {
    0: 2.0,   # Manual entry is painful → more likely to switch
    1: 1.3,   # CSV workflow → moderate friction
    2: 0.7    # Full API → sticky, less likely to switch
}[integration_quality]

# Change fatigue prevents rapid switching
fatigue_multiplier = {
    '<12 months': 0.3,   # Recently switched → exhausted
    '12-24 months': 0.7, # Hesitant
    '>24 months': 1.0    # Ready for change
}[time_since_last_switch]
```

**Results:** 166 switches over 72 months = 4% annual switch rate

### Step 6: Generate KPIs (`generate_kpis.py`)

Generates monthly Days A/R and Denial Rate time series with causal vendor effects.

**Output:** `kpis.csv` (7,200 rows = 100 sites x 72 months)

**KPI Generation Formula:**

```python
Days_AR = (
    baseline_days_ar          # Site baseline: [30, 40] days
    + vendor_effect           # Tier-based: [-4.5, +4.5] days
    + integration_bonus       # Full API reduces friction: [-3, 0] days
    + seasonality             # Dec/Jan peaks: [-2, +2] days
    + noise                   # Random: N(0, 1.5)
)

Denial_Rate = (
    baseline_denial_rate      # Site baseline: [5, 9]%
    + vendor_effect           # Tier-based: [-0.75, +0.75]%
    + integration_bonus       # Full API reduces errors: [-1, 0]%
    + noise                   # Random: N(0, 0.3)
)
```

**Vendor Effects by Tier:**
- Tier 3 (Premium): Improves KPIs (negative effect)
- Tier 2 (Standard): Neutral
- Tier 1 (Budget): Worsens KPIs (positive effect)

**RCM Category Multiplier:** 1.5x (RCM vendors have largest impact on A/R and denials)

---

## 4. Data Schema Summary

### sites.csv
```
site_id     | string  | S001-S100
region      | string  | Northeast, South, West, Midwest
ehr_system  | string  | Dentrix, OpenDental, Eaglesoft, Curve, Other
date_joined | date    | 2019-XX-XX
annual_revenue | float | $800K - $5M
```

### vendors.csv
```
vendor_id            | string | V001-V020
name                 | string | Real vendor names
category             | string | Lab, RCM, Telephony, Scheduling, Clearinghouse, IT_MSP, Supplies
tier                 | int    | 1, 2, or 3
monthly_price_per_site | float | Category-dependent
```

### integration_matrix.csv
```
site_id             | string | Foreign key to sites
vendor_id           | string | Foreign key to vendors
integration_quality | int    | 0 (none), 1 (partial_csv), 2 (full_api)
```

### contracts_2019_2024.csv
```
contract_id         | string | Unique contract identifier
site_id             | string | Foreign key to sites
category            | string | Vendor category
vendor_id           | string | Foreign key to vendors
contract_start_date | date   | When contract began
contract_end_date   | date   | When contract ended (NULL if active)
```

### kpis.csv
```
site_id     | string | Foreign key to sites
month       | date   | YYYY-MM-01
days_ar     | float  | Days in Accounts Receivable
denial_rate | float  | Claim denial rate (%)
```

---

## 5. Validation Results

I validated the synthetic data against industry benchmarks:

| Metric | Generated | Industry Benchmark | Status |
|--------|-----------|-------------------|--------|
| Days A/R mean | 27.3 days | 30-40 days | PASS |
| Denial Rate mean | 5.62% | 7-9% | PASS |
| Annual switch rate | 4.0% | ~5% | PASS |
| EHR distribution | Dentrix 35% | ~40% market share | BORDERLINE |

### Switch Distribution

- Total switches (2019-2024): 166
- Average per year: 27.7
- Switches concentrated in practices with poor integration (quality=0)

### KPI Distributions

- Days A/R: Normal distribution around 27 days
- Denial Rate: Normal distribution around 5.6%
- Both show expected vendor tier effects and seasonality patterns

---

## 6. Reproducibility

The pipeline is fully reproducible with a fixed random seed:

```bash
python3 generate_all_data.py --seed 42 --n_sites 100
```

All generated data is deterministic given the same seed.

---

## 7. Source Code Reference

**Location:** `src/`

| File | Description |
|------|-------------|
| `generate_all_data.py` | Master pipeline script |
| `generate_sites.py` | Site generation |
| `generate_vendors.py` | Vendor catalog |
| `generate_integration_matrix.py` | Integration quality rules |
| `generate_initial_state.py` | Initial contracts |
| `simulate_switches.py` | Switch simulation |
| `generate_kpis.py` | KPI time series |

---

## 8. References

- LLM Research Sample: See `llm_research_sample.md` for complete Batch 1 example
- Full Results: Available on request
