"""
generate_vendors.py -- create vendor catalog with real names

Author: Gregory Schwartz
Date: December 2025
"""

import numpy as np
import pandas as pd


# pricing rules by category
PRICING_RULES = {
    'Lab': {'base': 8000, 'tier_delta': 500},
    'RCM': {'base': 2500, 'tier_delta': 500},
    'Telephony': {'base': 600, 'tier_delta': 200},
    'Scheduling': {'base': 400, 'tier_delta': 100},
    'Clearinghouse': {'base': 200, 'tier_delta': 100},
    'IT_MSP': {'base': 1500, 'tier_delta': 500},
    'Supplies': {'base': 1200, 'tier_delta': 300},
}


def get_vendor_catalog():
    """Return list of vendor dictionaries from LLM research."""
    vendors = [
        # lab vendors
        {'vendor_id': 'V001', 'name': 'National Dental Labs', 'category': 'Lab', 'tier': 2},
        {'vendor_id': 'V002', 'name': 'Glidewell', 'category': 'Lab', 'tier': 3},
        {'vendor_id': 'V003', 'name': 'DDS Lab', 'category': 'Lab', 'tier': 1},
        {'vendor_id': 'V004', 'name': 'NDX', 'category': 'Lab', 'tier': 2},

        # rcm vendors
        {'vendor_id': 'V005', 'name': 'Apex Dental Billing', 'category': 'RCM', 'tier': 2},
        {'vendor_id': 'V006', 'name': 'EOS Healthcare', 'category': 'RCM', 'tier': 3},
        {'vendor_id': 'V007', 'name': 'Dental Billing Solutions', 'category': 'RCM', 'tier': 1},

        # telephony vendors
        {'vendor_id': 'V008', 'name': 'Weave', 'category': 'Telephony', 'tier': 3},
        {'vendor_id': 'V009', 'name': 'Solutionreach', 'category': 'Telephony', 'tier': 2},
        {'vendor_id': 'V010', 'name': 'Dental Phone Pro', 'category': 'Telephony', 'tier': 1},

        # scheduling vendors
        {'vendor_id': 'V011', 'name': 'Lighthouse 360', 'category': 'Scheduling', 'tier': 2},
        {'vendor_id': 'V012', 'name': 'Dental Intelligence', 'category': 'Scheduling', 'tier': 3},
        {'vendor_id': 'V013', 'name': 'Simple Scheduler', 'category': 'Scheduling', 'tier': 1},

        # clearinghouse vendors
        {'vendor_id': 'V014', 'name': 'DentalXChange', 'category': 'Clearinghouse', 'tier': 2},
        {'vendor_id': 'V015', 'name': 'NEA Fast Attach', 'category': 'Clearinghouse', 'tier': 2},

        # it msp vendors
        {'vendor_id': 'V016', 'name': 'Dental IT Solutions', 'category': 'IT_MSP', 'tier': 2},
        {'vendor_id': 'V017', 'name': 'MicroMD IT', 'category': 'IT_MSP', 'tier': 3},
        {'vendor_id': 'V018', 'name': 'Tech4Dentists', 'category': 'IT_MSP', 'tier': 1},

        # supplies vendors
        {'vendor_id': 'V019', 'name': 'Patterson Dental', 'category': 'Supplies', 'tier': 2},
        {'vendor_id': 'V020', 'name': 'Benco Dental', 'category': 'Supplies', 'tier': 2},
    ]
    return vendors


def calculate_price(category, tier):
    """Calculate monthly price based on category and tier."""
    rules = PRICING_RULES[category]
    base = rules['base']
    delta = rules['tier_delta']

    if tier == 1:
        return base - delta
    elif tier == 2:
        return base
    else:
        return base + delta  # premium tier


def generate_vendors(seed=42):
    """Generate vendor catalog dataframe."""
    np.random.seed(seed)

    vendor_list = get_vendor_catalog()
    vendors_df = pd.DataFrame(vendor_list)

    # add pricing column
    prices = []
    for idx, row in vendors_df.iterrows():
        price = calculate_price(row['category'], row['tier'])
        prices.append(price)

    vendors_df['monthly_price_per_site'] = prices

    return vendors_df


def save_vendors(vendors_df, output_path='data/generated/vendors.csv'):
    """Save vendors to csv file."""
    vendors_df.to_csv(output_path, index=False)
    print(f'Saved {len(vendors_df)} vendors to {output_path}')


if __name__ == '__main__':
    vendors = generate_vendors(seed=42)

    print('=== Vendor Generation Summary ===')
    print(f'Total vendors: {len(vendors)}')

    print(f'\nVendors per category:')
    print(vendors['category'].value_counts().sort_index())

    print(f'\nTier distribution:')
    print(vendors['tier'].value_counts().sort_index())

    print(f'\nAll vendors:')
    print(vendors.to_string(index=False))

    save_vendors(vendors)
