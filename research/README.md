# LLM Research Pipeline

This directory contains the LLM-driven vendor research that grounds the synthetic data in real-world evidence.

## Overview

We used Claude Opus, Claude Sonnet, and ChatGPT Pro to research 20 real dental vendors across 7 categories. The goal was to extract **structural patterns** about integration types, not vendor-specific claims that could be hallucinated.

## Research Process

### Batch Organization

| Batch | Category | Vendors | Model |
|-------|----------|---------|-------|
| 1 | Lab | V001-V004 | Claude Opus 4.1 |
| 2 | RCM | V005-V007 | Claude Sonnet 4.5 |
| 3 | Telephony | V008-V010 | ChatGPT Pro |
| 4 | Scheduling + Clearinghouse | V011-V015 | Claude Opus 4.1 |
| 5 | IT/MSP + Supplies | V016-V020 | Claude Sonnet 4.5 |

### What We Extracted

For each vendor:
- EHR integration capabilities (Dentrix, OpenDental, Eaglesoft, etc.)
- Integration type classification (full_api, partial_csv, none)
- DSO partnership indicators
- Coverage regions
- Pricing model indicators

### Key Discovery

**5 of 7 categories have FIXED integration patterns:**

- Lab: ALL use portal-based workflows (partial_csv)
- Telephony: ALL require real-time sync (full_api)
- Scheduling: ALL require real-time sync (full_api)
- Supplies: ALL use separate e-commerce portals (partial_csv)

This structural insight, discovered through cross-vendor analysis, became the foundation for the causal mechanism in data generation.

## Directory Structure

```
research/
├── prompts/          # LLM research prompts (sample included)
│   └── batch1_lab_vendors.md
└── results/          # Research outputs (not included in repo)
```

## Why Not Include All Results?

The full research results contain ~450 knowledge graph triples with vendor-specific claims. We include:
- Sample prompts to demonstrate methodology
- Pattern summaries in documentation

We don't include raw results because:
1. Vendor claims may become outdated
2. Focus is on methodology, not specific facts
3. The important insight is the **category-level patterns**, not individual vendor details

## Replication

To replicate this research:
1. Use the prompt template in `prompts/batch1_lab_vendors.md`
2. Adapt for each vendor category
3. Cross-validate findings across multiple LLMs
4. Extract category-level patterns, not vendor-specific claims
