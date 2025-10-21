#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import pandas as pd


def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        print(f"Error: '{portfolio_file}' not found.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("Portfolio is empty. No data to summarize.")
        return

    if "card_market_value" not in df.columns:
        print("Error: 'card_market_value' column missing.", file=sys.stderr)
        sys.exit(1)

    total_portfolio_value = float(df["card_market_value"].fillna(0.0).sum())

    idx = df["card_market_value"].fillna(0.0).idxmax()
    most_valuable_card = df.loc[idx]

    name = str(most_valuable_card.get("card_name", ""))
    cid = str(most_valuable_card.get("card_id", ""))
    value = float(most_valuable_card.get("card_market_value", 0.0))

    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(f"Most Valuable Card: {name} ({cid}) — ${value:,.2f}")


def main() -> None:
    generate_summary("card_portfolio.csv")


def test() -> None:
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    test()
