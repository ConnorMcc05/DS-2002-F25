#!/usr/bin/env python3
from __future__ import annotations

import sys

import update_portfolio
import generate_summary


def run_production_pipeline() -> None:
    print("Starting production pipeline...", file=sys.stderr)

    print("ETL: updating portfolio (card_portfolio.csv)...", file=sys.stderr)
    update_portfolio.main()

    print("Reporting: generating summary from card_portfolio.csv...", file=sys.stderr)
    generate_summary.main()

    print("Pipeline complete.", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()
