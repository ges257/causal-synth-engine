"""
generate_all_data.py -- master pipeline for synthetic data generation

Author: Gregory Schwartz
Date: December 2025

Usage:
    python3 generate_all_data.py --seed 42 --n_sites 100
"""

import argparse
import os
import sys
from pathlib import Path

# add src to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_sites import generate_sites, save_sites
from generate_vendors import generate_vendors, save_vendors
from generate_integration_matrix import generate_integration_matrix, save_integration_matrix
from generate_initial_state import generate_initial_state, save_initial_state
from simulate_switches import simulate_switches, save_contracts
from generate_kpis import generate_kpis, save_kpis


def run_pipeline(seed=42, n_sites=100, output_dir='../data/generated'):
    """Run the full synthetic data generation pipeline."""

    print('=' * 70)
    print('SYNTHETIC DATA GENERATION PIPELINE')
    print('=' * 70)
    print(f'Seed: {seed}')
    print(f'Sites: {n_sites}')
    print(f'Output: {output_dir}')
    print('=' * 70)

    os.makedirs(output_dir, exist_ok=True)

    # step 1: sites
    print('\n[Step 1/6] Generating sites...')
    sites = generate_sites(n_sites=n_sites, seed=seed)
    save_sites(sites, f'{output_dir}/sites.csv')

    # step 2: vendors
    print('\n[Step 2/6] Generating vendors...')
    vendors = generate_vendors(seed=seed)
    save_vendors(vendors, f'{output_dir}/vendors.csv')

    # step 3: integration matrix
    print('\n[Step 3/6] Generating integration matrix...')
    integration_matrix = generate_integration_matrix(sites, vendors, seed=seed)
    save_integration_matrix(integration_matrix, f'{output_dir}/integration_matrix.csv')

    # step 4: initial state
    print('\n[Step 4/6] Generating initial state (2019-01-01)...')
    initial_state = generate_initial_state(sites, vendors, integration_matrix, seed=seed)
    save_initial_state(initial_state, f'{output_dir}/initial_state_2019.csv')

    # step 5: simulate switches
    print('\n[Step 5/6] Simulating vendor switches (2019-2024)...')
    contracts = simulate_switches(
        sites, vendors, integration_matrix, initial_state,
        start_date='2019-01-01', end_date='2024-12-31', seed=seed
    )
    save_contracts(contracts, f'{output_dir}/contracts_2019_2024.csv')

    # step 6: generate kpis
    print('\n[Step 6/6] Generating KPIs...')
    kpis = generate_kpis(
        sites, vendors, integration_matrix, contracts,
        start_date='2019-01-01', end_date='2024-12-31', seed=seed
    )
    save_kpis(kpis, f'{output_dir}/kpis.csv')

    # summary
    print('\n' + '=' * 70)
    print('PIPELINE COMPLETE')
    print('=' * 70)
    print(f'\nGenerated datasets:')
    print(f'  sites.csv:               {len(sites):5d} rows')
    print(f'  vendors.csv:             {len(vendors):5d} rows')
    print(f'  integration_matrix.csv:  {len(integration_matrix):5d} rows')
    print(f'  initial_state_2019.csv:  {len(initial_state):5d} rows')
    print(f'  contracts_2019_2024.csv: {len(contracts):5d} rows')
    print(f'  kpis.csv:                {len(kpis):5d} rows')

    switches = len(contracts) - len(initial_state)
    print(f'\nKey Statistics:')
    print(f'  Total switches (2019-2024): {switches}')
    print(f'  Annual switch rate: {switches / len(initial_state) / 6 * 100:.1f}%')
    print(f'  Days A/R mean: {kpis["days_ar"].mean():.2f} days')
    print(f'  Denial Rate mean: {kpis["denial_rate"].mean():.2f}%')
    print('=' * 70)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synthetic data')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--n_sites', type=int, default=100, help='Number of sites')
    parser.add_argument('--output', type=str, default='../data/generated', help='Output directory')

    args = parser.parse_args()

    run_pipeline(seed=args.seed, n_sites=args.n_sites, output_dir=args.output)
