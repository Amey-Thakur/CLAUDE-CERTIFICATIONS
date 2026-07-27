# Security policy

This is a documentation repository. It ships one maintenance script, `scripts/update_resources.py`, which downloads PDFs from fixed official URLs over HTTPS using the Python standard library.

## Reporting

If you find a security problem, such as a mirrored file that appears tampered with, a link that redirects somewhere malicious, or an issue in the maintenance script, report it privately through [GitHub security advisories](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/security/advisories/new) rather than a public issue. Reports are reviewed promptly.

## Verifying mirrored documents

Every mirrored PDF's source URL is listed in [guide/official-sources.md](guide/official-sources.md). If you want certainty, download the document from the official source and compare hashes. If a mirrored file ever differs from its official source, treat the official source as correct and please report the discrepancy.
