"""
simulate_switches.py -- simulate vendor switches 2019-2024

Author: Gregory Schwartz
Date: December 2025
"""

import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# mechanism multipliers
INTEGRATION_MULTIPLIERS = {0: 2.0, 1: 1.3, 2: 0.7}


def calculate_switch_probability(integration_quality, months_since_change, base_annual=0.05):
    """Calculate monthly switch probability using causal mechanisms."""

    # convert annual to monthly
    base_monthly = 1 - (1 - base_annual) ** (1 / 12)

    # integration multiplier
    integration_mult = INTEGRATION_MULTIPLIERS.get(integration_quality, 1.0)

    # fatigue multiplier
    if months_since_change < 12:
        fatigue_mult = 0.3  # too soon again
    elif months_since_change < 24:
        fatigue_mult = 0.7
    else:
        fatigue_mult = 1.0  # ok to switch

    prob = base_monthly * integration_mult * fatigue_mult
    return min(prob, 1.0)


def get_integration_quality(site_id, vendor_id, integration_df):
    """Look up integration quality for a site-vendor pair."""
    match = integration_df[
        (integration_df['site_id'] == site_id) &
        (integration_df['vendor_id'] == vendor_id)
    ]
    if len(match) > 0:
        return match.iloc[0]['integration_quality']
    return 0


def select_new_vendor(site_id, category, current_vendor, vendors_df, integration_df):
    """Select a new vendor when switching occurs."""

    # get candidates excluding current
    category_vendors = vendors_df[vendors_df['category'] == category]
    candidates = category_vendors[category_vendors['vendor_id'] != current_vendor]

    if len(candidates) == 0:
        return None  # no alternatives

    scores = []
    vendor_ids = []

    for idx, vendor in candidates.iterrows():
        vendor_id = vendor['vendor_id']
        tier = vendor['tier']
        quality = get_integration_quality(site_id, vendor_id, integration_df)

        score = np.exp(0.5 * quality + 0.3 * tier)
        scores.append(score)
        vendor_ids.append(vendor_id)

    # softmax selection
    scores = np.array(scores)
    probs = scores / scores.sum()

    selected_idx = np.random.choice(len(vendor_ids), p=probs)
    return vendor_ids[selected_idx]


def simulate_switches(sites_df, vendors_df, integration_df, initial_state_df,
                      start_date='2019-01-01', end_date='2024-12-31', seed=42):
    """Simulate vendor switches over time period."""
    np.random.seed(seed)

    sim_start = datetime.strptime(start_date, '%Y-%m-%d')
    sim_end = datetime.strptime(end_date, '%Y-%m-%d')

    # generate monthly timesteps
    months = []
    current = sim_start
    while current <= sim_end:
        months.append(current)
        current = current + relativedelta(months=1)

    # initialize state from initial contracts
    current_state = {}
    for idx, row in initial_state_df.iterrows():
        key = (row['site_id'], row['category'])
        current_state[key] = {
            'vendor_id': row['vendor_id'],
            'start_date': datetime.strptime(row['contract_start_date'], '%Y-%m-%d'),
            'last_change': datetime.strptime(row['contract_start_date'], '%Y-%m-%d')
        }

    # contract history
    contracts = []

    # add initial contracts
    for key, state in current_state.items():
        site_id, category = key
        contracts.append({
            'site_id': site_id,
            'category': category,
            'vendor_id': state['vendor_id'],
            'contract_start_date': state['start_date'].strftime('%Y-%m-%d'),
            'contract_end_date': None
        })

    # simulate each month
    categories = vendors_df['category'].unique()

    for month_idx, month in enumerate(months):
        if month_idx == 0:
            continue  # skip first month

        for site_id in sites_df['site_id']:
            for category in categories:
                key = (site_id, category)
                state = current_state[key]

                current_vendor = state['vendor_id']
                last_change = state['last_change']

                # get current integration quality
                quality = get_integration_quality(site_id, current_vendor, integration_df)

                # calculate months since change
                months_since = (month.year - last_change.year) * 12
                months_since += month.month - last_change.month

                # calculate switch probability
                prob = calculate_switch_probability(quality, months_since)

                # decide if switch happens
                if np.random.random() < prob:
                    new_vendor = select_new_vendor(
                        site_id, category, current_vendor, vendors_df, integration_df
                    )

                    if new_vendor is None:
                        continue

                    # end current contract
                    for contract in reversed(contracts):
                        if (contract['site_id'] == site_id and
                            contract['category'] == category and
                            contract['vendor_id'] == current_vendor and
                            contract['contract_end_date'] is None):
                            contract['contract_end_date'] = month.strftime('%Y-%m-%d')
                            break

                    # add new contract
                    contracts.append({
                        'site_id': site_id,
                        'category': category,
                        'vendor_id': new_vendor,
                        'contract_start_date': month.strftime('%Y-%m-%d'),
                        'contract_end_date': None
                    })

                    # update state
                    current_state[key] = {
                        'vendor_id': new_vendor,
                        'start_date': month,
                        'last_change': month
                    }

    # build output dataframe
    contracts_df = pd.DataFrame(contracts)
    contract_ids = [f'C{i + 1:05d}' for i in range(len(contracts_df))]
    contracts_df.insert(0, 'contract_id', contract_ids)

    return contracts_df


def save_contracts(contracts_df, output_path='data/generated/contracts_2019_2024.csv'):
    """Save contracts to csv."""
    contracts_df.to_csv(output_path, index=False)
    print(f'Saved {len(contracts_df)} contract records to {output_path}')


if __name__ == '__main__':
    sites = pd.read_csv('data/generated/sites.csv')
    vendors = pd.read_csv('data/generated/vendors.csv')
    integration_matrix = pd.read_csv('data/generated/integration_matrix.csv')
    initial_state = pd.read_csv('data/generated/initial_state_2019.csv')

    print('=== Simulating Switches (2019-2024) ===')
    contracts = simulate_switches(
        sites, vendors, integration_matrix, initial_state,
        start_date='2019-01-01', end_date='2024-12-31', seed=42
    )

    switches = len(contracts) - 700
    print(f'\nTotal contracts: {len(contracts)}')
    print(f'Initial: 700')
    print(f'Switches: {switches}')

    save_contracts(contracts)
