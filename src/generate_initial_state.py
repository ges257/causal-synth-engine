"""
generate_initial_state.py -- create baseline contracts for 2019-01-01

Author: Gregory Schwartz
Date: December 2025
"""

import numpy as np
import pandas as pd


def calculate_selection_score(integration_quality, tier):
    """Calculate vendor selection weight."""
    score = np.exp(0.5 * integration_quality + 0.3 * tier)  # softmax weights
    return score


def select_vendor_for_category(site_id, category, vendors_df, integration_df):
    """Select one vendor for a site in a category using softmax."""

    # get vendors in this category
    category_vendors = vendors_df[vendors_df['category'] == category]

    # get integration data for this site
    site_integrations = integration_df[integration_df['site_id'] == site_id]

    scores = []
    vendor_ids = []

    for idx, vendor in category_vendors.iterrows():
        vendor_id = vendor['vendor_id']
        tier = vendor['tier']

        # find integration quality
        match = site_integrations[site_integrations['vendor_id'] == vendor_id]
        if len(match) > 0:
            quality = match.iloc[0]['integration_quality']
        else:
            quality = 0

        score = calculate_selection_score(quality, tier)
        scores.append(score)
        vendor_ids.append(vendor_id)

    # convert to probabilities
    scores = np.array(scores)
    probs = scores / scores.sum()

    # sample vendor
    selected_idx = np.random.choice(len(vendor_ids), p=probs)
    return vendor_ids[selected_idx]


def generate_initial_state(sites_df, vendors_df, integration_df, seed=42):
    """Generate initial contracts as of 2019-01-01."""
    np.random.seed(seed)

    categories = vendors_df['category'].unique()
    contracts = []

    for site_idx, site in sites_df.iterrows():
        site_id = site['site_id']

        for category in categories:
            vendor_id = select_vendor_for_category(
                site_id, category, vendors_df, integration_df
            )

            contracts.append({
                'site_id': site_id,
                'category': category,
                'vendor_id': vendor_id,
                'contract_start_date': '2019-01-01'
            })

    initial_df = pd.DataFrame(contracts)
    return initial_df


def save_initial_state(initial_df, output_path='data/generated/initial_state_2019.csv'):
    """Save initial state to csv."""
    initial_df.to_csv(output_path, index=False)
    print(f'Saved {len(initial_df)} initial contracts to {output_path}')


if __name__ == '__main__':
    sites = pd.read_csv('data/generated/sites.csv')
    vendors = pd.read_csv('data/generated/vendors.csv')
    integration_matrix = pd.read_csv('data/generated/integration_matrix.csv')

    initial_state = generate_initial_state(sites, vendors, integration_matrix, seed=42)

    print('=== Initial State Summary (2019-01-01) ===')
    print(f'Total contracts: {len(initial_state)}')
    print(f'Expected: {len(sites)} sites x 7 categories = {len(sites) * 7}')

    contracts_per_site = initial_state.groupby('site_id').size()
    print(f'\nAll sites have 7 contracts: {(contracts_per_site == 7).all()}')

    save_initial_state(initial_state)
