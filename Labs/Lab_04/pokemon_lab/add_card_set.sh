#!/usr/bin/env bash
set -euo pipefail

read -rp "TCG Card Set ID (e.g., base1, base4): " SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

mkdir -p card_set_lookup

echo "Fetching card data for set '$SET_ID'..."
OUT="card_set_lookup/${SET_ID}.json"
BASE_URL="https://api.pokemontcg.io/v2/cards"

if [[ -n "${POKEMON_TCG_API_KEY:-}" ]]; then
    curl -sSf -G "$BASE_URL" \
        --data-urlencode "q=set.id:${SET_ID}" \
        -H "X-Api-Key: ${POKEMON_TCG_API_KEY}" \
        -o "$OUT"
else
    curl -sSf -G "$BASE_URL" \
        --data-urlencode "q=set.id:${SET_ID}" \
        -o "$OUT"
fi

echo "Saved to $OUT"
