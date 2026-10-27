#!/usr/bin/env bash
# Render .github/og-card/card.html to assets/og-image.png (1200×630 link-preview image).
# Usage (from anywhere): .github/og-card/render.sh
set -euo pipefail

cd "$(dirname "$0")/../.."
PORT=8799
OUT=assets/og-image.png

CHROME=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then CHROME="$c"; break; fi
done
[ -n "$CHROME" ] || { echo "Chrome/Chromium not found" >&2; exit 1; }

# card.html loads the profile photo by relative path, so serve the repo over HTTP
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER' EXIT
sleep 1

"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1200,630 --virtual-time-budget=8000 \
    --screenshot="$OUT" "http://localhost:$PORT/.github/og-card/card.html" 2>/dev/null

echo "Wrote $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"
