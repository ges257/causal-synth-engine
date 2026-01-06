"""
generate_kpis.py -- generate monthly KPI time series

Author: Gregory Schwartz
Date: December 2025
"""

import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def assign_vendor_effects(vendors_df, seed=42):
    """Assign KPI effects to each vendor based on tier."""
    np.random.seed(seed)

    effects = {}

    for idx, vendor in vendors_df.iterrows():
        vendor_id = vendor['vendor_id']
        category = vendor['category']
        tier = vendor['tier']

        # tier effect: tier3=-1, tier2=0, tier1=+1
        tier_effect = 2 - tier  # simple formula

        # rcm has larger impact
        if category == 'RCM':
            days_ar = tier_effect * 3.0 * 1.5
            denial = tier_effect * 0.5 * 1.5
        else:
            days_ar = tier_effect * 3.0
            denial = tier_effect * 0.5

        # add noise
        days_ar += np.random.normal(0, 0.5)
        denial += np.random.normal(0, 0.1)

        effects[vendor_id] = {
            'days_ar_effect': days_ar,
            'denial_rate_effect': denial
        }

    return effects


def assign_site_baselines(sites_df, seed=42):
    """Assign baseline KPIs for each site."""
    np.random.seed(seed + 1)  # different seed

    baselines = {}

    for idx, site in sites_df.iterrows():
        site_id = site['site_id']

        baselines[site_id] = {
            'baseline_days_ar': np.random.uniform(30, 40),
            'baseline_denial_rate': np.random.uniform(5, 9)
        }

    return baselines


def get_active_vendor(site_id, category, month, contracts_df):
    """Find the active vendor for a site-category at a given month."""

    site_contracts = contracts_df[
        (contracts_df['site_id'] == site_id) &
        (contracts_df['category'] == category)
    ]

    for idx, contract in site_contracts.iterrows():
        start = datetime.strptime(contract['contract_start_date'], '%Y-%m-%d')

        end_str = contract['contract_end_date']
        if pd.notna(end_str):
            end = datetime.strptime(end_str, '%Y-%m-%d')
        else:
            end = datetime(2099, 12, 31)

        if start <= month <= end:
            return contract['vendor_id']

    return None


def calculate_integration_bonus(vendor_id, site_id, integration_df, vendor_effects):
    """Calculate integration bonus for a vendor."""

    match = integration_df[
        (integration_df['site_id'] == site_id) &
        (integration_df['vendor_id'] == vendor_id)
    ]

    if len(match) == 0:
        return 0.0, 0.0

    quality = match.iloc[0]['integration_quality']
    effects = vendor_effects[vendor_id]

    # bonus factor based on quality
    if quality == 2:
        factor = -0.5  # api reduces friction
    elif quality == 1:
        factor = -0.2
    else:
        factor = 0.0

    days_bonus = factor * abs(effects['days_ar_effect'])
    denial_bonus = factor * abs(effects['denial_rate_effect'])

    return days_bonus, denial_bonus


def generate_kpis(sites_df, vendors_df, integration_df, contracts_df,
                  start_date='2019-01-01', end_date='2024-12-31', seed=42):
    """Generate monthly KPIs for all sites."""
    np.random.seed(seed)

    vendor_effects = assign_vendor_effects(vendors_df, seed)
    site_baselines = assign_site_baselines(sites_df, seed)

    sim_start = datetime.strptime(start_date, '%Y-%m-%d')
    sim_end = datetime.strptime(end_date, '%Y-%m-%d')

    # generate months
    months = []
    current = sim_start
    while current <= sim_end:
        months.append(current)
        current = current + relativedelta(months=1)

    categories = vendors_df['category'].unique()
    records = []

    for site_id in sites_df['site_id']:
        baseline = site_baselines[site_id]
        baseline_ar = baseline['baseline_days_ar']
        baseline_denial = baseline['baseline_denial_rate']

        for month in months:
            # find active vendors
            active_vendors = {}
            for category in categories:
                vendor_id = get_active_vendor(site_id, category, month, contracts_df)
                if vendor_id:
                    active_vendors[category] = vendor_id

            # sum vendor effects
            total_ar_effect = 0.0
            total_denial_effect = 0.0

            for category, vendor_id in active_vendors.items():
                effects = vendor_effects[vendor_id]
                total_ar_effect += effects['days_ar_effect']
                total_denial_effect += effects['denial_rate_effect']

            # sum integration bonuses
            total_ar_bonus = 0.0
            total_denial_bonus = 0.0

            for category, vendor_id in active_vendors.items():
                ar_bonus, denial_bonus = calculate_integration_bonus(
                    vendor_id, site_id, integration_df, vendor_effects
                )
                total_ar_bonus += ar_bonus
                total_denial_bonus += denial_bonus

            # seasonality
            month_num = month.month
            season_ar = 2.0 * np.sin(2 * np.pi * month_num / 12)
            season_denial = 0.3 * np.sin(2 * np.pi * month_num / 12)

            # noise
            noise_ar = np.random.normal(0, 1.5)
            noise_denial = np.random.normal(0, 0.3)

            # final values
            days_ar = (baseline_ar + total_ar_effect + total_ar_bonus +
                       season_ar + noise_ar)
            denial_rate = (baseline_denial + total_denial_effect + total_denial_bonus +
                           season_denial + noise_denial)

            # clamp to realistic
            days_ar = max(15, min(60, days_ar))
            denial_rate = max(0, min(20, denial_rate))

            records.append({
                'site_id': site_id,
                'month': month.strftime('%Y-%m-%d'),
                'days_ar': round(days_ar, 2),
                'denial_rate': round(denial_rate, 2)
            })

    kpis_df = pd.DataFrame(records)
    return kpis_df


def save_kpis(kpis_df, output_path='data/generated/kpis.csv'):
    """Save KPIs to csv."""
    kpis_df.to_csv(output_path, index=False)
    print(f'Saved {len(kpis_df)} KPI records to {output_path}')


if __name__ == '__main__':
    sites = pd.read_csv('data/generated/sites.csv')
    vendors = pd.read_csv('data/generated/vendors.csv')
    integration_matrix = pd.read_csv('data/generated/integration_matrix.csv')
    contracts = pd.read_csv('data/generated/contracts_2019_2024.csv')

    print('=== Generating KPIs (2019-2024) ===')
    kpis = generate_kpis(
        sites, vendors, integration_matrix, contracts,
        start_date='2019-01-01', end_date='2024-12-31', seed=42
    )

    print(f'\nTotal KPI records: {len(kpis)}')
    print(f'Days A/R mean: {kpis["days_ar"].mean():.2f}')
    print(f'Denial Rate mean: {kpis["denial_rate"].mean():.2f}%')

    save_kpis(kpis)
