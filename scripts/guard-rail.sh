#!/bin/bash
set -e
echo "🛡️  Sentinel Guard-Rail: Starting Verification..."

echo "1. Running Verification Script..."
python3 scripts/verify.py

echo "2. Running Tests..."
if command -v pnpm &> /dev/null; then
    pnpm test
else
    npm test
fi

echo "✅ Guard-Rail Passed!"
