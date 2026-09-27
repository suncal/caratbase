#!/usr/bin/env bash
# Full rebuild in the order the generators depend on each other.
# history -> prices -> pages -> long tail -> static schema -> syntax gate -> asset stamps
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/sync_prices.py
python3 tools/design/home.py   > /dev/null
python3 tools/design/pages.py  > /dev/null
python3 tools/genpages.py
python3 tools/schema.py
python3 tools/checkjs.py          # gates the build: a broken inline script fails silently otherwise
bash scripts/bump-assets.sh    > /dev/null
python3 tools/spelling.py --check

echo "build complete"
