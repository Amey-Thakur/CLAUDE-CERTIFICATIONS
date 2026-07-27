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

# The certificates page opens with an HTML-centered header that GitHub
# renders but MkDocs does not; swap it for a site-native markdown header.
n=$(grep -n -m1 '</div>' site-src/certificates/README.md | cut -d: -f1)
{ cat .github/pages/certificates-header.md; tail -n +$((n + 1)) site-src/certificates/README.md; } > site-src/certificates/README.md.tmp
mv site-src/certificates/README.md.tmp site-src/certificates/README.md

# YouTube thumbnail links become real embedded players on the site;
# GitHub keeps the clickable thumbnails, which it renders and iframes it does not.
PYBIN=""
for candidate in python3 python py; do
  if "$candidate" -c "import sys" >/dev/null 2>&1; then PYBIN="$candidate"; break; fi
done
"$PYBIN" - <<'PY'
import re
from pathlib import Path
pattern = re.compile(r'\[!\[([^\]]*)\]\(https://img\.youtube\.com/vi/([\w-]+)/hqdefault\.jpg\)\]\(https://www\.youtube\.com/watch\?v=[\w-]+\)')
def repl(m):
    title, vid = m.group(1), m.group(2)
    return (f'<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
            f'title="{title}" frameborder="0" loading="lazy" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
            f'allowfullscreen></iframe></div>')
for md in Path('site-src').rglob('*.md'):
    t = md.read_text(encoding='utf-8')
    new = pattern.sub(repl, t)
    if new != t:
        md.write_text(new, encoding='utf-8')
PY

# GitHub-friendly <details> blocks become Material's native collapsible
# callouts on the site, so the markdown inside them renders properly.
PYBIN=""
for candidate in python3 python py; do
  if "$candidate" -c "import sys" >/dev/null 2>&1; then PYBIN="$candidate"; break; fi
done
"$PYBIN" - <<'PY'
import re
from pathlib import Path
pattern = re.compile(r'<details><summary>(.*?)</summary>\n\n(.*?)\n\n</details>', re.S)
def repl(m):
    title, body = m.group(1), m.group(2)
    indented = '\n'.join('    ' + line if line.strip() else '' for line in body.split('\n'))
    return f'??? success "{title}"\n\n{indented}'
for md in Path('site-src').rglob('*.md'):
    t = md.read_text(encoding='utf-8')
    new = pattern.sub(repl, t)
    if new != t:
        md.write_text(new, encoding='utf-8')
PY

# Search engines get a per-page meta description, injected here so the
# repository markdown stays clean, and a robots.txt pointing at the sitemap.
PYBIN=""
for candidate in python3 python py; do
  if "$candidate" -c "import sys" >/dev/null 2>&1; then PYBIN="$candidate"; break; fi
done
"$PYBIN" - <<'PY'
import json
from pathlib import Path
for rel, desc in json.loads(Path('.github/pages/descriptions.json').read_text(encoding='utf-8')).items():
    p = Path('site-src') / rel
    text = p.read_text(encoding='utf-8')
    if not text.startswith('---'):
        # Quoted: descriptions contain colons, which are YAML mapping syntax unquoted.
        safe = desc.replace('"', "'")
        p.write_text(f'---\ndescription: "{safe}"\n---\n\n{text}', encoding='utf-8')
PY
printf 'User-agent: *\nAllow: /\nSitemap: https://amey-thakur.github.io/CLAUDE-CERTIFICATIONS/sitemap.xml\n' > site-src/robots.txt

# Links that leave the site are pointed at the repository on GitHub;
# repository-root links are pointed at the site's home page.
BLOB="https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main"
find site-src -name '*.md' -exec sed -i \
  -e "s|(../.github/CONTRIBUTING.md#discussions)|(${BLOB}/.github/CONTRIBUTING.md#discussions)|g" \
  -e "s|(../README.md)|(../index.md)|g" \
  {} +
