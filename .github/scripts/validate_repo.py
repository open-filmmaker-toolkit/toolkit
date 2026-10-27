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
    subject_ids = [item.get("id") for item in data.get("subjects", []) if isinstance(item, dict)]
    if len(subject_ids) != len(set(subject_ids)):
        fail(f"{name}: duplicate IDs in subjects")
    for subject in data.get("subjects", []):
        if subject.get("personId") and subject["personId"] not in ids["people"]:
            fail(f"{name}: subject {subject.get('id')} personId points to a missing person")
    source_ids = [item.get("id") for item in data.get("sources", []) if isinstance(item, dict)]
    if len(source_ids) != len(set(source_ids)):
        fail(f"{name}: duplicate IDs in sources")
    for source in data.get("sources", []):
        if source.get("elementId") and source["elementId"] not in ids["thirdPartyElements"]:
            fail(f"{name}: source {source.get('id')} elementId points to a missing third-party element")
    comp_ids = [item.get("id") for item in data.get("comps", []) if isinstance(item, dict)]
    if len(comp_ids) != len(set(comp_ids)):
        fail(f"{name}: duplicate IDs in comps")
    grant_ids = [item.get("id") for item in data.get("grants", []) if isinstance(item, dict)]
    if len(grant_ids) != len(set(grant_ids)):
        fail(f"{name}: duplicate IDs in grants")
    narratives = [item for item in data.get("narratives", []) if isinstance(item, dict)]
    narrative_versions = [v for item in narratives for v in item.get("versions", []) if isinstance(v, dict)]
    if len({n.get("id") for n in narratives}) != len(narratives) or len({v.get("id") for v in narrative_versions}) != len(narrative_versions):
        fail(f"{name}: duplicate IDs in narratives or their versions")
    for version in narrative_versions:
        for use in version.get("uses", []):
            if isinstance(use, dict) and use.get("grantId") and use["grantId"] not in set(grant_ids):
                fail(f"{name}: narrative version {version.get('id')} uses points to missing grant {use['grantId']}")
    budget = data.get("budget") if isinstance(data.get("budget"), dict) else {}
    for part, b in [("budget", budget)] + [(f"budget version {v.get('id')}", v) for v in budget.get("versions", []) if isinstance(v, dict)]:
        acc_ids = [a.get("id") for a in b.get("accounts", []) if isinstance(a, dict)]
        line_ids = [l.get("id") for l in b.get("lines", []) if isinstance(l, dict)]
        fringe_ids = [f.get("id") for f in b.get("fringes", []) if isinstance(f, dict)]
        if any(len(x) != len(set(x)) for x in (acc_ids, line_ids, fringe_ids, [m.get("id") for m in b.get("markups", []) if isinstance(m, dict)])):
            fail(f"{name}: duplicate IDs in {part}")
        for line in b.get("lines", []):
            if line.get("accountId") not in acc_ids:
                fail(f"{name}: {part} line {line.get('id')} accountId points to a missing account")
            if line.get("fringeId") and line["fringeId"] not in fringe_ids:
                fail(f"{name}: {part} line {line.get('id')} fringeId points to a missing fringe")
    for fmt in data.get("budgetFormats", []):
        cat_ids = {c.get("id") for c in fmt.get("categories", []) if isinstance(c, dict)} | {""}
        for key in ("accountMap", "lineMap", "markupMap"):
            bad = {v for v in (fmt.get(key) or {}).values() if v not in cat_ids}
            if bad:
                fail(f"{name}: budget format {fmt.get('id')} {key} points to missing categories {sorted(bad)}")
        if fmt.get("grantId") and fmt["grantId"] not in set(grant_ids):
            fail(f"{name}: budget format {fmt.get('id')} grantId points to a missing grant")
    plan = data.get("financePlan") if isinstance(data.get("financePlan"), dict) else {}
    source_ids = [x.get("id") for x in plan.get("sources", []) if isinstance(x, dict)]
    if len(source_ids) != len(set(source_ids)):
        fail(f"{name}: duplicate IDs in financePlan sources")
    for src in plan.get("sources", []):
        if src.get("grantId") and src["grantId"] not in set(grant_ids):
            fail(f"{name}: finance source {src.get('id')} grantId points to a missing grant")
    treatment = data.get("treatment") if isinstance(data.get("treatment"), dict) else {}
    version_ids = [v.get("id") for v in treatment.get("versions", []) if isinstance(v, dict)]
    if len(version_ids) != len(set(version_ids)):
        fail(f"{name}: duplicate IDs in treatment versions")
    deck = data.get("pitchDeck") if isinstance(data.get("pitchDeck"), dict) else {}
    image_ids = {i.get("id") for i in deck.get("images", []) if isinstance(i, dict)}
    slide_ids = [sl.get("id") for sl in deck.get("slides", []) if isinstance(sl, dict)]
    if len(slide_ids) != len(set(slide_ids)) or len(image_ids) != len([i for i in deck.get("images", []) if isinstance(i, dict)]):
        fail(f"{name}: duplicate IDs in pitchDeck slides or images")
    for sl in deck.get("slides", []):
        missing = set(sl.get("imageIds", [])) - image_ids
        if missing:
            fail(f"{name}: slide {sl.get('id')} imageIds points to missing {sorted(missing)}")
    supers = data.get("supers") if isinstance(data.get("supers"), dict) else {}
    super_ids = [entry.get("id") for entry in supers.get("entries", []) if isinstance(entry, dict)]
    if len(super_ids) != len(set(super_ids)):
        fail(f"{name}: duplicate IDs in supers entries")
    for entry in supers.get("entries", []):
        if entry.get("personId") and entry["personId"] not in ids["people"]:
            fail(f"{name}: super {entry.get('id')} personId points to a missing person")
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
