#!/usr/bin/env sh

URL="$1"
INTERVAL=2 # seconds between checks

if [[ -z "$URL" ]]; then
  echo "Usage: $0 <url>"
  exit 1
fi

echo "Waiting for $URL to become available..."

while ! curl --output /dev/null --silent --fail "$URL"; do
  printf '.'
  sleep "$INTERVAL"
done

open "$URL"
