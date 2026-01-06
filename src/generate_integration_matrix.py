"""
generate_integration_matrix.py -- create site x vendor integration quality

Author: Gregory Schwartz
Date: December 2025
"""

import numpy as np
import pandas as pd


# ehr capability scores from research
EHR_SCORES = {
    'Dentrix': 0.9,
    'OpenDental': 0.8,
    'Eaglesoft': 0.7,
    'Curve': 0.6,
    'Other': 0.3,
}


def get_fixed_integration(category, vendor_id, ehr):
    """Return integration quality for fixed-pattern categories."""

    # lab always partial csv
    if category == 'Lab':
        return 1  # stl file upload

    # telephony always full api
    if category == 'Telephony':
        return 2  # call pop needs

    # scheduling always full api
    if category == 'Scheduling':
        if vendor_id == 'V012' and ehr == 'Denticon':
            return 0  # competitive issue
        return 2

    # supplies always partial csv
    if category == 'Supplies':
        return 1

    return None  # not a fixed category


def get_it_msp_integration(vendor_id, ehr):
    """Return integration for IT MSP based on ownership."""

    # henry schein owns dentrix
    if vendor_id == 'V016':
        if ehr in ['Dentrix', 'Dentrix Ascend', 'Dentrix Enterprise']:
            return 2
        return 1

    # pact one has monitoring
    if vendor_id == 'V017':
        if ehr in ['Dentrix', 'OpenDental', 'Eaglesoft', 'Curve']:
            return 2
        return 1

    return 1  # default partial


def get_rcm_integration(tier, ehr):
    """Return probabilistic integration for RCM."""
    major_ehrs = ['Dentrix', 'OpenDental', 'Eaglesoft', 'Denticon']

    # tier 1 with major ehrs
    if tier == 1 and ehr in major_ehrs:
        rand = np.random.random()
        if rand < 0.80:
            return 2
        elif rand < 0.95:
            return 1
        return 0

    # other cases
    rand = np.random.random()
    if rand < 0.40:
        return 2
    elif rand < 0.70:
        return 1
    return 0


def get_clearinghouse_integration(vendor_id, ehr):
    """Return integration for clearinghouse vendors."""

    # dentalxchange full service
    if vendor_id == 'V014':
        if ehr in ['OpenDental', 'Eaglesoft', 'Curve', 'Denticon']:
            return 2
        return 1  # dentrix competitive

    # nea fastattach attachment only
    if vendor_id == 'V015':
        return 1

    return 1


def assign_integration_quality(category, vendor_id, tier, ehr):
    """Determine integration quality for a site-vendor pair."""

    # check fixed patterns first
    fixed = get_fixed_integration(category, vendor_id, ehr)
    if fixed is not None:
        return fixed

    # handle variable patterns
    if category == 'IT_MSP':
        return get_it_msp_integration(vendor_id, ehr)

    if category == 'RCM':
        return get_rcm_integration(tier, ehr)

    if category == 'Clearinghouse':
        return get_clearinghouse_integration(vendor_id, ehr)

    return 1  # fallback


def generate_integration_matrix(sites_df, vendors_df, seed=42):
    """Generate integration quality for all site-vendor pairs."""
    np.random.seed(seed)

    records = []

    for site_idx, site in sites_df.iterrows():
        site_id = site['site_id']
        ehr = site['ehr_system']

        for vendor_idx, vendor in vendors_df.iterrows():
            vendor_id = vendor['vendor_id']
            category = vendor['category']
            tier = vendor['tier']

            quality = assign_integration_quality(category, vendor_id, tier, ehr)

            records.append({
                'site_id': site_id,
                'vendor_id': vendor_id,
                'integration_quality': quality
            })

    integration_df = pd.DataFrame(records)
    return integration_df


def save_integration_matrix(integration_df, output_path='data/generated/integration_matrix.csv'):
    """Save integration matrix to csv."""
    integration_df.to_csv(output_path, index=False)
    print(f'Saved {len(integration_df)} integration records to {output_path}')


if __name__ == '__main__':
    sites = pd.read_csv('data/generated/sites.csv')
    vendors = pd.read_csv('data/generated/vendors.csv')

    integration_matrix = generate_integration_matrix(sites, vendors, seed=42)

    print('=== Integration Matrix Summary ===')
    print(f'Total pairs: {len(integration_matrix)}')

    print(f'\nIntegration quality distribution:')
    quality_counts = integration_matrix['integration_quality'].value_counts().sort_index()
    labels = {0: 'None (manual)', 1: 'Partial (CSV)', 2: 'Full (API)'}

    for quality, count in quality_counts.items():
        pct = 100 * count / len(integration_matrix)
        print(f'  {quality} ({labels[quality]:15s}): {count:4d} ({pct:5.1f}%)')

    save_integration_matrix(integration_matrix)
