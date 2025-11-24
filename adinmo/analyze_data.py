#!/usr/bin/env python3
"""
Adinmo Data Analysis Script
Analyzes CSV sample files to extract schema information, statistics, and relationships.
"""

import pandas as pd
import os
import json
from pathlib import Path
from collections import defaultdict

# Base path for data files
BASE_PATH = "/home/lryan/work/wmd/data-models/seeds/adinmo"

FILES = {
    'bids': 'sample_bids.csv',
    'iap': 'sample_iap.csv',
    'impressions': 'sample_impressions.csv',
    'sessions': 'sample_sessions.csv',
    'tracker_events': 'sample_tracker_events.csv',
    'attributed_installs': 'sample_attributed_installs.csviuliana.berzuntanu@brainpool.ai'
}

def analyze_file(table_name, filename):
    """Analyze a single CSV file and extract schema information."""
    print(f"\n{'='*80}")
    print(f"Analyzing: {table_name}")
    print(f"{'='*80}")
    
    filepath = os.path.join(BASE_PATH, filename)
    
    # Read first 100 rows for analysis
    df = pd.read_csv(filepath, nrows=100)
    
    analysis = {
        'table_name': table_name,
        'total_columns': len(df.columns),
        'columns': {},
        'sample_row_count': len(df),
        'common_keys': []
    }
    
    # Analyze each column
    for col in df.columns:
        col_data = df[col]
        
        col_analysis = {
            'dtype': str(col_data.dtype),
            'null_count': int(col_data.isnull().sum()),
            'null_percentage': float(col_data.isnull().sum() / len(df) * 100),
            'unique_count': int(col_data.nunique()),
            'sample_values': []
        }
        
        # Get sample non-null values
        non_null_values = col_data.dropna().head(5).tolist()
        col_analysis['sample_values'] = [str(v)[:100] for v in non_null_values]
        
        analysis['columns'][col] = col_analysis
    
    # Identify common linking keys
    if 'ANON_DEVICE_ID' in df.columns:
        analysis['common_keys'].append('ANON_DEVICE_ID')
    if 'SESSION_ID' in df.columns:
        analysis['common_keys'].append('SESSION_ID')
    if 'GAME_ID' in df.columns:
        analysis['common_keys'].append('GAME_ID')
    
    # Print summary
    print(f"Total Columns: {analysis['total_columns']}")
    print(f"Sample Rows: {analysis['sample_row_count']}")
    print(f"Common Keys: {', '.join(analysis['common_keys'])}")
    print(f"\nColumn Summary:")
    print(f"{'Column':<40} {'Type':<15} {'Nulls':<8} {'Unique':<8}")
    print(f"{'-'*80}")
    
    for col, info in list(analysis['columns'].items())[:20]:  # First 20 columns
        print(f"{col:<40} {info['dtype']:<15} {info['null_count']:<8} {info['unique_count']:<8}")
    
    if len(analysis['columns']) > 20:
        print(f"... and {len(analysis['columns']) - 20} more columns")
    
    return analysis

def main():
    """Main analysis function."""
    all_analyses = {}
    
    print("Adinmo Data Analysis")
    print("=" * 80)
    
    for table_name, filename in FILES.items():
        try:
            analysis = analyze_file(table_name, filename)
            all_analyses[table_name] = analysis
        except Exception as e:
            print(f"Error analyzing {table_name}: {e}")
    
    # Save full analysis to JSON
    output_path = "/home/lryan/work/wmd/schemas/adinmo/data_analysis.json"
    with open(output_path, 'w') as f:
        json.dump(all_analyses, f, indent=2)
    
    print(f"\n\nFull analysis saved to: {output_path}")
    
    # Identify common fields across tables
    print(f"\n{'='*80}")
    print("Common Fields Across Tables")
    print(f"{'='*80}")
    
    all_columns = defaultdict(list)
    for table_name, analysis in all_analyses.items():
        for col in analysis['columns'].keys():
            all_columns[col].append(table_name)
    
    # Find columns that appear in multiple tables
    common_cols = {col: tables for col, tables in all_columns.items() if len(tables) > 1}
    
    for col, tables in sorted(common_cols.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{col:<40} -> {', '.join(tables)}")

if __name__ == "__main__":
    main()

