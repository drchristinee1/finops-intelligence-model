import pandas as pd

INPUT_FILE = "data/sample/api_cost_to_value.csv"


def build_base_model(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["duration_seconds"] = df["avg_duration_ms"] / 1000
    df["memory_gb"] = df["memory_mb"] / 1024
    df["gb_seconds_per_call"] = df["duration_seconds"] * df["memory_gb"]
    df["total_gb_seconds"] = df["gb_seconds_per_call"] * df["monthly_api_calls"]

    df["request_cost"] = (
        df["monthly_api_calls"] / 1_000_000
    ) * df["cost_per_million_requests"]
    df["compute_cost"] = df["total_gb_seconds"] * df["cost_per_gb_second"]
    df["total_cost"] = df["request_cost"] + df["compute_cost"]

    df["total_transactions"] = df["customers"] * df["transactions_per_customer"]
    df["api_calls_per_transaction"] = df["monthly_api_calls"] / df["total_transactions"]
    df["cost_per_transaction"] = df["total_cost"] / df["total_transactions"]

    return df


def build_commitment_view(base_row: pd.Series) -> pd.DataFrame:
    monthly_api_calls = float(base_row["monthly_api_calls"])
    total_cost = float(base_row["total_cost"])

    # Simple MVP assumption:
    # 70% of base usage is safe baseline for commitment
    baseline_ratio = 0.70
    baseline_api_calls = monthly_api_calls * baseline_ratio
    variable_api_calls = monthly_api_calls - baseline_api_calls

    cost_per_api_call = total_cost / monthly_api_calls

    baseline_cost = baseline_api_calls * cost_per_api_call
    variable_cost = variable_api_calls * cost_per_api_call

    # Example estimated discount for committed usage
    commitment_discount = 0.30
    committed_cost = baseline_cost * (1 - commitment_discount)
    savings_from_commitment = baseline_cost - committed_cost

    rows = [
        {
            "metric": "monthly_api_calls",
            "value": monthly_api_calls,
        },
        {
            "metric": "baseline_api_calls",
            "value": baseline_api_calls,
        },
        {
            "metric": "variable_api_calls",
            "value": variable_api_calls,
        },
        {
            "metric": "baseline_cost_candidate",
            "value": baseline_cost,
        },
        {
            "metric": "variable_cost_on_demand",
            "value": variable_cost,
        },
        {
            "metric": "committed_cost_estimate",
            "value": committed_cost,
        },
        {
            "metric": "estimated_monthly_savings",
            "value": savings_from_commitment,
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    df = pd.read_csv(INPUT_FILE)
    modeled = build_base_model(df)
    commitment_view = build_commitment_view(modeled.iloc[0])

    print("=== Base model ===")
    print(modeled[[
        "monthly_api_calls",
        "total_cost",
        "total_transactions",
        "api_calls_per_transaction",
        "cost_per_transaction",
    ]].T)

    print("\n=== Commitment layer ===")
    print(commitment_view)


if __name__ == "__main__":
    main()
