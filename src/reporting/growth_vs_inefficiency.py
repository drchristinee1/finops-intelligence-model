import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "data/sample/api_cost_to_value.csv"
OUTPUT_DIR = "outputs/charts"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "growth_vs_inefficiency.png")


def build_model(df: pd.DataFrame) -> pd.DataFrame:
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

    df["api_calls_per_customer"] = df["monthly_api_calls"] / df["customers"]
    df["total_transactions"] = df["customers"] * df["transactions_per_customer"]
    df["api_calls_per_transaction"] = df["monthly_api_calls"] / df["total_transactions"]
    df["cost_per_transaction"] = df["total_cost"] / df["total_transactions"]
    df["profit_per_transaction"] = (
        df["contribution_margin_per_transaction"] - df["cost_per_transaction"]
    )

    return df


def build_scenarios(base_row: pd.Series) -> pd.DataFrame:
    base = base_row.to_dict()

    scenarios = [
        {
            **base,
            "scenario": "Base Case",
            "monthly_api_calls": base["monthly_api_calls"],
            "customers": base["customers"],
            "transactions_per_customer": base["transactions_per_customer"],
        },
        {
            **base,
            "scenario": "Growth",
            "monthly_api_calls": base["monthly_api_calls"] * 1.4,
            "customers": base["customers"] * 1.4,
            "transactions_per_customer": base["transactions_per_customer"],
        },
        {
            **base,
            "scenario": "Inefficiency",
            "monthly_api_calls": base["monthly_api_calls"] * 1.5,
            "customers": base["customers"],
            "transactions_per_customer": base["transactions_per_customer"],
        },
    ]

    return pd.DataFrame(scenarios)


def plot_chart(df: pd.DataFrame) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    x = df["scenario"]
    y = df["cost_per_transaction"]

    plt.figure(figsize=(8, 5))
    plt.bar(x, y)
    plt.title("Cost per Transaction: Growth vs Inefficiency")
    plt.ylabel("Cost per Transaction ($)")
    plt.xlabel("Scenario")
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)
    plt.close()


def main() -> None:
    base_df = pd.read_csv(INPUT_FILE)
    scenarios_df = build_scenarios(base_df.iloc[0])
    modeled_df = build_model(scenarios_df)

    print(modeled_df[[
        "scenario",
        "monthly_api_calls",
        "customers",
        "total_transactions",
        "api_calls_per_transaction",
        "total_cost",
        "cost_per_transaction",
    ]])

    plot_chart(modeled_df)
    print(f"Chart saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
