#!/usr/bin/env bash
# Assemble the MkDocs source tree from the repository's canonical files.
# The repository stays the single source of truth; this script only copies
# and adjusts links that would otherwise point outside the site.
set -euo pipefail

rm -rf site-src
mkdir -p site-src/assets site-src/stylesheets

cp -r associate-foundations developer-foundations architect-foundations architect-professional guide certificates site-src/
cp -r .github/assets/logos site-src/assets/logos
rm -f site-src/assets/logos/README.md
cp .github/pages/extra.css site-src/stylesheets/extra.css
cp .github/pages/index.md site-src/index.md

# Links that leave the site are pointed at the repository on GitHub;
# repository-root links are pointed at the site's home page.
BLOB="https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main"
find site-src -name '*.md' -exec sed -i \
  -e "s|(../.github/CONTRIBUTING.md#discussions)|(${BLOB}/.github/CONTRIBUTING.md#discussions)|g" \
  -e "s|(../CHANGELOG.md)|(${BLOB}/CHANGELOG.md)|g" \
  -e "s|(../README.md)|(../index.md)|g" \
  {} +
