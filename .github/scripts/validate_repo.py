"""Checks the repo's rules that can be verified without a browser.

Run locally with: python3 .github/scripts/validate_repo.py
Needs the jsonschema package (pip install jsonschema).
"""
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
errors = []


def fail(message):
    errors.append(message)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"{path.relative_to(ROOT)}: can't be read as JSON ({exc})")
        return None


schema = load(ROOT / "schemas" / "project-v1.schema.json")
validator = None
if schema is not None:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

REFERENCES = {
    "personIds": "people",
    "locationIds": "locations",
    "thirdPartyElementIds": "thirdPartyElements",
    "assetIds": "assets",
}

for sample in sorted((ROOT / "samples").glob("*.oft.json")):
    name = sample.relative_to(ROOT)
    data = load(sample)
    if data is None or validator is None:
        continue
    for err in validator.iter_errors(data):
        fail(f"{name}: {'/'.join(map(str, err.absolute_path)) or 'file'}: {err.message}")
    ids = {}
    for collection in ("people", "locations", "thirdPartyElements", "contracts", "assets"):
        values = [item.get("id") for item in data.get(collection, []) if isinstance(item, dict)]
        if len(values) != len(set(values)):
            fail(f"{name}: duplicate IDs in {collection}")
        ids[collection] = set(values)
    for contract in data.get("contracts", []):
        for field, target in REFERENCES.items():
            missing = set(contract.get(field, [])) - ids[target]
            if missing:
                fail(f"{name}: contract {contract.get('id')} {field} points to missing {sorted(missing)}")
    for element in data.get("thirdPartyElements", []):
        missing = set(element.get("contractIds", [])) - ids["contracts"]
        if missing:
            fail(f"{name}: element {element.get('id')} contractIds points to missing {sorted(missing)}")

# Tools must work offline: no external scripts, styles, fonts, images or requests.
EXTERNAL = re.compile(
    r"""(?:\b(?:src|action|poster)\s*=\s*["']?\s*(?:https?:)?//"""
    r"""|<link\b[^>]*\bhref\s*=\s*["']?\s*(?:https?:)?//"""
    r"""|@import\s+(?:url\()?["']?(?:https?:)?//"""
    r"""|url\(\s*["']?(?:https?:)?//"""
    r"""|\bfetch\s*\(|XMLHttpRequest|\bsendBeacon\b|\bnew\s+WebSocket\b|\bimportScripts\b)""",
    re.IGNORECASE,
)
for tool in sorted((ROOT / "tools").iterdir()):
    if not tool.is_dir():
        continue
    rel = tool.relative_to(ROOT)
    for required in ("index.html", "README.md"):
        if not (tool / required).is_file():
            fail(f"{rel}: missing {required}")
    page = tool / "index.html"
    if page.is_file():
        for number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if EXTERNAL.search(line):
                fail(f"{rel}/index.html:{number}: possible network request or external resource")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Schema, sample files and tool rules all check out.")
