"""Checks the repo's rules that can be verified without a browser.

Run locally with: python3 .github/scripts/validate_repo.py
Needs the jsonschema package (pip install jsonschema).
"""
import csv
import io
import json
import re
import sys
import zipfile
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
    for collection in ("people", "locations", "thirdPartyElements", "contracts", "assets", "callSheets"):
        values = [item.get("id") for item in data.get(collection, []) if isinstance(item, dict)]
        if len(values) != len(set(values)):
            fail(f"{name}: duplicate IDs in {collection}")
        ids[collection] = set(values)
    for contract in data.get("contracts", []):
        for field, target in REFERENCES.items():
            missing = set(contract.get(field, [])) - ids[target]
            if missing:
                fail(f"{name}: contract {contract.get('id')} {field} points to missing {sorted(missing)}")
    for sheet in data.get("callSheets", []):
        if sheet.get("locationId") and sheet["locationId"] not in ids["locations"]:
            fail(f"{name}: call sheet {sheet.get('id')} locationId points to a missing location")
        for member in sheet.get("crew", []):
            if member.get("personId") not in ids["people"]:
                fail(f"{name}: call sheet {sheet.get('id')} crew points to missing person {member.get('personId')}")
    credits = data.get("credits") if isinstance(data.get("credits"), dict) else {}
    entry_ids = [entry.get("id") for entry in credits.get("entries", []) if isinstance(entry, dict)]
    if len(entry_ids) != len(set(entry_ids)):
        fail(f"{name}: duplicate IDs in credits entries")
    for entry in credits.get("entries", []):
        missing = set(entry.get("personIds", [])) - ids["people"]
        if missing:
            fail(f"{name}: credit {entry.get('id')} personIds points to missing {sorted(missing)}")
    missing = set(credits.get("notCredited", [])) - ids["people"]
    if missing:
        fail(f"{name}: credits notCredited points to missing {sorted(missing)}")
    for element in data.get("thirdPartyElements", []):
        missing = set(element.get("contractIds", [])) - ids["contracts"]
        if missing:
            fail(f"{name}: element {element.get('id')} contractIds points to missing {sorted(missing)}")

# Tools must work offline: no external scripts, styles, fonts, images or requests.
# The only exception: a tool may reach specific hosts, but only from a button the user
# clicks. Everything else in the tool must stay offline.
OPTIONAL_HOSTS = {
    "tools/call-sheet": {"photon.komoot.io", "api.open-meteo.com"},
}
URL_HOST = re.compile(r"https?://([^/\s\"'`)<>]+)", re.IGNORECASE)
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
        allowed = OPTIONAL_HOSTS.get(rel.as_posix(), set())
        for number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if EXTERNAL.search(line) and not (allowed and re.search(r"\bfetch\s*\(", line) and not re.search(r"XMLHttpRequest|sendBeacon|WebSocket|importScripts|(?:src|action|poster)\s*=|@import|url\(", line, re.I)):
                fail(f"{rel}/index.html:{number}: possible network request or external resource")
            for host in URL_HOST.findall(line) if allowed else []:
                if host.lower() not in allowed:
                    fail(f"{rel}/index.html:{number}: link to {host} is not an allowed host for this tool")

# Plain templates: spreadsheets and Word documents only, each listed in templates/README.md.
# Word files must not carry macros or links to anything outside the file.
TEMPLATES = ROOT / "templates"
template_readme = TEMPLATES / "README.md"
listed = template_readme.read_text(encoding="utf-8") if template_readme.is_file() else ""
if not listed:
    fail("templates: missing README.md")
for path in sorted(TEMPLATES.iterdir()) if TEMPLATES.is_dir() else []:
    rel = path.relative_to(ROOT)
    if path.name == "README.md":
        continue
    if path.suffix.lower() not in (".csv", ".docx"):
        fail(f"{rel}: templates must be .csv or .docx files")
        continue
    if f"({path.name})" not in listed:
        fail(f"{rel}: not listed in templates/README.md")
    if path.suffix.lower() == ".csv":
        try:
            rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8-sig"))))
        except (UnicodeDecodeError, csv.Error) as exc:
            fail(f"{rel}: can't be read as a UTF-8 CSV file ({exc})")
            continue
        if not rows or not any(cell.strip() for cell in rows[0]):
            fail(f"{rel}: has no heading row")
    else:
        try:
            with zipfile.ZipFile(path) as docx:
                names = docx.namelist()
                if "word/document.xml" not in names:
                    fail(f"{rel}: isn't a Word document")
                if any(re.search(r"vbaProject|activeX|\.bin$", n, re.I) for n in names):
                    fail(f"{rel}: contains macros or embedded programs")
                for part in (n for n in names if n.endswith(".rels")):
                    if re.search(r'TargetMode\s*=\s*"External"', docx.read(part).decode("utf-8", "replace")):
                        fail(f"{rel}: links to something outside the file ({part})")
        except zipfile.BadZipFile:
            fail(f"{rel}: isn't a valid Word document")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Schema, sample files, tool rules and templates all check out.")
