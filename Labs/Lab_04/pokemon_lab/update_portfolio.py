#!/usr/bin/env python3
from __future__ import annotations

import sys
import json
from pathlib import Path
from typing import List

import pandas as pd


def _load_lookup_data(lookup_dir: str | Path) -> pd.DataFrame:
    lookup_dir = Path(lookup_dir)
    all_lookup_df: List[pd.DataFrame] = []

    for p in sorted(lookup_dir.glob("*.json")):
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)

        raw = data.get("data", [])
        if not raw:
            continue

        df = pd.json_normalize(raw)

        holo = df.get("tcgplayer.prices.holofoil.market")
        normal = df.get("tcgplayer.prices.normal.market")

        if holo is None and normal is None:
            price = pd.Series(0.0, index=df.index, dtype="float64")
        else:
            price = (holo if holo is not None else pd.Series([None] * len(df)))
            if normal is not None:
                price = price.fillna(normal)
            price = price.fillna(0.0).astype("float64")

        df["card_market_value"] = price

        df = df.rename(
            columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name",
            }
        )

        required_cols = [
            "card_id",
            "card_name",
            "card_number",
            "set_id",
            "set_name",
            "card_market_value",
        ]

        present = [c for c in required_cols if c in df.columns]
        df = df[present].copy()
        all_lookup_df.append(df)

    if not all_lookup_df:
        return pd.DataFrame(
            columns=[
                "card_id",
                "card_name",
                "card_number",
                "set_id",
                "set_name",
                "card_market_value",
            ]
        )

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    if "card_market_value" in lookup_df.columns:
        lookup_df = lookup_df.sort_values(
            by=["card_market_value"], ascending=False, kind="mergesort"
        )

    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first").reset_index(drop=True)
    return lookup_df


def _load_inventory_data(inventory_dir: str | Path) -> pd.DataFrame:
    inventory_dir = Path(inventory_dir)
    inventory_data: List[pd.DataFrame] = []

    for p in sorted(inventory_dir.glob("*.csv")):
        df = pd.read_csv(p)
        inventory_data.append(df)

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    for col in ("set_id", "card_number"):
        if col not in inventory_df.columns:
            inventory_df[col] = ""

    inventory_df["set_id"] = inventory_df["set_id"].astype(str).str.strip()
    inventory_df["card_number"] = inventory_df["card_number"].astype(str).str.strip()
    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"]

    return inventory_df


def update_portfolio(inventory_dir: str | Path, lookup_dir: str | Path, output_file: str | Path) -> None:
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "set_id",
        "set_name",
        "card_number",
        "card_name",
        "card_id",
        "card_market_value",
    ]

    if inventory_df.empty:
        print("No inventory found; writing empty portfolio CSV.", file=sys.stderr)
        pd.DataFrame(columns=final_cols).to_csv(output_file, index=False)
        return

    needed_lookup_cols = [
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]
    for col in needed_lookup_cols:
        if col not in lookup_df.columns:
            lookup_df[col] = pd.Series(dtype="object" if col != "card_market_value" else "float64")

    merged = pd.merge(
        inventory_df,
        lookup_df[needed_lookup_cols],
        on="card_id",
        how="left",
        suffixes=("", "_lkp"),
    )

    if "card_market_value" in merged.columns:
        merged["card_market_value"] = merged["card_market_value"].fillna(0.0).astype("float64")
    if "set_name" in merged.columns:
        merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")
    if "card_name" in merged.columns:
        merged["card_name"] = merged["card_name"].fillna("")

    for col in ("binder_name", "page_number", "slot_number"):
        if col not in merged.columns:
            merged[col] = ""

    merged["index"] = (
        merged["binder_name"].astype(str).str.strip()
        + "-"
        + merged["page_number"].astype(str).str.strip()
        + "-"
        + merged["slot_number"].astype(str).str.strip()
    )

    for col in final_cols:
        if col not in merged.columns:
            merged[col] = "" if col != "card_market_value" else 0.0

    out_df = merged[final_cols].copy()
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_file, index=False)
    print(f"Wrote portfolio to {output_file}")


def main() -> None:
    update_portfolio(
        inventory_dir=Path("./card_inventory/"),
        lookup_dir=Path("./card_set_lookup/"),
        output_file=Path("card_portfolio.csv"),
    )


def test() -> None:
    update_portfolio(
        inventory_dir=Path("./card_inventory_test/"),
        lookup_dir=Path("./card_set_lookup_test/"),
        output_file=Path("test_card_portfolio.csv"),
    )


if __name__ == "__main__":
    print("Starting update_portfolio.py in Test Mode...", file=sys.stderr)
    test()
