"""
generate_sites.py -- create synthetic dental practice sites

Author: Gregory Schwartz
Date: December 2025
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_sites(n_sites=100, seed=42):
    """Generate n_sites synthetic dental practices."""
    np.random.seed(seed)

    # create site ids
    site_ids = [f'S{i + 1:03d}' for i in range(n_sites)]

    # region distribution matches US dental density
    regions = np.random.choice(
        ['Northeast', 'South', 'West', 'Midwest'],
        size=n_sites,
        p=[0.25, 0.35, 0.20, 0.20]
    )

    # ehr market shares from industry
    ehr_systems = np.random.choice(
        ['Dentrix', 'OpenDental', 'Eaglesoft', 'Curve', 'Other'],
        size=n_sites,
        p=[0.35, 0.25, 0.20, 0.10, 0.10]
    )

    # dates joined throughout 2019
    start_date = datetime(2019, 1, 1)
    days_in_year = 364  # maybe use 365?

    dates_joined = []
    for i in range(n_sites):
        random_days = int(np.random.uniform(0, days_in_year))
        join_date = start_date + timedelta(days=random_days)
        dates_joined.append(join_date.strftime('%Y-%m-%d'))

    # revenue uses lognormal
    annual_revenues = np.random.lognormal(mean=14.5, sigma=0.3, size=n_sites)  # params from paper
    annual_revenues = np.round(annual_revenues, -3).astype(int)

    # build dataframe
    sites_df = pd.DataFrame({
        'site_id': site_ids,
        'region': regions,
        'ehr_system': ehr_systems,
        'date_joined': dates_joined,
        'annual_revenue': annual_revenues
    })

    return sites_df


def save_sites(sites_df, output_path='data/generated/sites.csv'):
    """Save sites to csv file."""
    sites_df.to_csv(output_path, index=False)
    print(f'Saved {len(sites_df)} sites to {output_path}')


if __name__ == '__main__':
    sites = generate_sites(n_sites=100, seed=42)

    print('=== Site Generation Summary ===')
    print(f'Total sites: {len(sites)}')

    print(f'\nRegion distribution:')
    print(sites['region'].value_counts().sort_index())

    print(f'\nEHR distribution:')
    print(sites['ehr_system'].value_counts())

    print(f'\nRevenue statistics:')
    print(f'  Median: ${sites["annual_revenue"].median():,.0f}')
    print(f'  Mean:   ${sites["annual_revenue"].mean():,.0f}')

    print(f'\nFirst 5 sites:')
    print(sites.head())

    save_sites(sites)
