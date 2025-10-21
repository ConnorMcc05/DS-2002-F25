#!/usr/bin/env bash
set -euo pipefail

echo "Refreshing all card sets in card_set_lookup/..."

for FILE in card_set_lookup/*.json; do
  [ -e "$FILE" ] || { echo "No JSON files found in card_set_lookup/."; break; }
  SET_ID=$(basename "$FILE" .json)
  echo "Updating set '$SET_ID'..."
  BASE_URL="https://api.pokemontcg.io/v2/cards"

  if [[ -n "${POKEMON_TCG_API_KEY:-}" ]]; then
    curl -sSf -G "$BASE_URL" \
      --data-urlencode "q=set.id:${SET_ID}" \
      -H "X-Api-Key: ${POKEMON_TCG_API_KEY}" \
      -o "$FILE"
  else
    curl -sSf -G "$BASE_URL" \
      --data-urlencode "q=set.id:${SET_ID}" \
      -o "$FILE"
  fi

  echo "Wrote refreshed data to $FILE"
done

echo "All card sets have been refreshed."
