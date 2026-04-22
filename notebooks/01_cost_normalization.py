import pandas as pd

# Load data
df = pd.read_csv('../data/sample/api_cost_to_value.csv')

# Step 1: Convert units
df['duration_seconds'] = df['avg_duration_ms'] / 1000
df['memory_gb'] = df['memory_mb'] / 1024

# Step 2: Compute GB-seconds
df['gb_seconds_per_call'] = df['duration_seconds'] * df['memory_gb']
df['total_gb_seconds'] = df['gb_seconds_per_call'] * df['monthly_api_calls']

# Step 3: Compute costs
df['request_cost'] = (df['monthly_api_calls'] / 1_000_000) * df['cost_per_million_requests']
df['compute_cost'] = df['total_gb_seconds'] * df['cost_per_gb_second']
df['total_cost'] = df['request_cost'] + df['compute_cost']

# Step 4: Workload behavior
df['api_calls_per_customer'] = df['monthly_api_calls'] / df['customers']
df['total_transactions'] = df['customers'] * df['transactions_per_customer']
df['api_calls_per_transaction'] = df['monthly_api_calls'] / df['total_transactions']

# Step 5: Business value
df['cost_per_transaction'] = df['total_cost'] / df['total_transactions']
df['profit_per_transaction'] = df['contribution_margin_per_transaction'] - df['cost_per_transaction']

print(df.T)
