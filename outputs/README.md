# Generated Outputs

This directory contains the CSV files produced by the data generation pipeline.

## Output Files

Running `python src/generate_all_data.py` produces:

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `vendors.csv` | 20 | 5 | Vendor entities with category and tier |
| `sites.csv` | 100 | 7 | Synthetic dental practices |
| `integration_matrix.csv` | 2,000 | 3 | Site×vendor integration quality |
| `initial_state_2019.csv` | 700 | 4 | Starting contracts (7 per site) |
| `contracts_2019_2024.csv` | 866 | 5 | Full contract history with switches |
| `kpis.csv` | 7,200 | 4 | Monthly performance metrics |

## Sample Schemas

### vendors.csv
```csv
vendor_id,name,category,tier,monthly_price_per_site
V001,National Dentex,Lab,1,8000
V008,Weave,Telephony,1,700
...
```

### sites.csv
```csv
site_id,name,region,ehr_system,chair_count,annual_revenue,founded_year
S001,Smile Dental Northeast,Northeast,Dentrix,6,2500000,2010
...
```

### integration_matrix.csv
```csv
site_id,vendor_id,integration_quality
S001,V001,1
S001,V008,2
...
```

### contracts_2019_2024.csv
```csv
site_id,vendor_id,category,start_date,end_date
S001,V001,Lab,2019-01-01,
S001,V005,RCM,2019-01-01,2022-06-15
S001,V006,RCM,2022-06-15,
...
```

### kpis.csv
```csv
site_id,month,days_ar,denial_rate
S001,2019-01,28.3,5.2
S001,2019-02,27.9,5.4
...
```

## Data Statistics

| Metric | Value |
|--------|-------|
| Total sites | 100 |
| Total vendors | 20 (7 categories) |
| Total contracts | 866 |
| Vendor switches | 166 (over 6 years) |
| Annual switch rate | 4.0% |
| KPI records | 7,200 (72 months × 100 sites) |

## Validation Metrics

Generated data validates against industry benchmarks:

| Metric | Synthetic | Industry |
|--------|-----------|----------|
| Days A/R | 27.3 days | 30-40 days |
| Denial Rate | 5.6% | 7-9% |
| Switch Rate | 4.0% annual | ~5% |

## Note

Full generated data is not included in the repository. Run `generate_all_data.py` to produce outputs, or see [pe-rollup-intelligence-system](https://github.com/ges257/pe-rollup-intelligence-system) for the training data used in the R-GCN model.
