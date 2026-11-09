"""Checks the repo's rules that can be verified without a browser.

Run locally with: python3 .github/scripts/validate_repo.py
Needs the jsonschema package (pip install jsonschema).
"""
import csv
import html
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
    funder_ids = [f.get("id") for f in data.get("funders", []) if isinstance(f, dict)]
    if len(funder_ids) != len(set(funder_ids)):
        fail(f"{name}: duplicate IDs in funders")
    for funder in data.get("funders", []):
        contact_ids = {c.get("id") for c in funder.get("contacts", []) if isinstance(c, dict)}
        for item in funder.get("interactions", []):
            if item.get("contactId") and item["contactId"] not in contact_ids:
                fail(f"{name}: funder {funder.get('id')} interaction {item.get('id')} contactId points to a missing contact")
        missing = set(funder.get("grantIds", [])) - set(grant_ids)
        if missing:
            fail(f"{name}: funder {funder.get('id')} grantIds points to missing grants {sorted(missing)}")
    cash = data.get("cashFlow") if isinstance(data.get("cashFlow"), dict) else {}
    for key, part in (("accounts", "accounts"), ("lines", "lines"), ("markups", "markups")):
        known = {x.get("id") for x in budget.get(part, []) if isinstance(x, dict)}
        missing = set((cash.get(key) or {}).keys()) - known
        if missing:
            fail(f"{name}: cashFlow {key} points to missing budget {part} {sorted(missing)}")
    day_ids = [x.get("id") for x in data.get("shootDays", []) if isinstance(x, dict)]
    if len(day_ids) != len(set(day_ids)):
        fail(f"{name}: duplicate IDs in shootDays")
    sheet_ids = {x.get("id") for x in data.get("callSheets", []) if isinstance(x, dict)}
    for day in data.get("shootDays", []):
        if day.get("locationId") and day["locationId"] not in ids["locations"]:
            fail(f"{name}: shoot day {day.get('id')} locationId points to a missing location")
        if set(day.get("personIds", [])) - ids["people"]:
            fail(f"{name}: shoot day {day.get('id')} personIds points to missing people")
        if day.get("callSheetId") and day["callSheetId"] not in sheet_ids:
            fail(f"{name}: shoot day {day.get('id')} callSheetId points to a missing call sheet")
    interview_ids = [x.get("id") for x in data.get("interviews", []) if isinstance(x, dict)]
    if len(interview_ids) != len(set(interview_ids)):
        fail(f"{name}: duplicate IDs in interviews")
    for item in data.get("interviews", []):
        if item.get("personId") and item["personId"] not in ids["people"]:
            fail(f"{name}: interview {item.get('id')} personId points to a missing person")
        if item.get("shootDayId") and item["shootDayId"] not in set(day_ids):
            fail(f"{name}: interview {item.get('id')} shootDayId points to a missing shoot day")
        beat_ids = {b.get("id") for b in item.get("beats", []) if isinstance(b, dict)}
        for q in item.get("questions", []):
            if isinstance(q, dict) and q.get("beatId") and q["beatId"] not in beat_ids:
                fail(f"{name}: interview {item.get('id')} question {q.get('id')} beatId points to a missing beat")
    journal_ids = [x.get("id") for x in data.get("journal", []) if isinstance(x, dict)]
    if len(journal_ids) != len(set(journal_ids)):
        fail(f"{name}: duplicate IDs in journal")
    for entry in data.get("journal", []):
        if set(entry.get("personIds", [])) - ids["people"]:
            fail(f"{name}: journal entry {entry.get('id')} personIds points to missing people")
        if set(entry.get("locationIds", [])) - ids["locations"]:
            fail(f"{name}: journal entry {entry.get('id')} locationIds points to missing locations")
        if entry.get("callSheetId") and entry["callSheetId"] not in sheet_ids:
            fail(f"{name}: journal entry {entry.get('id')} callSheetId points to a missing call sheet")
    report_day_ids = {d.get("id") for d in data.get("shootDays", []) if isinstance(d, dict)}
    for coll in ("dailyReports", "expenses", "festivals"):
        listed = [x.get("id") for x in data.get(coll, []) if isinstance(x, dict)]
        if len(listed) != len(set(listed)):
            fail(f"{name}: duplicate IDs in {coll}")
    media_ids = {r.get("id") for r in data.get("mediaReports", []) if isinstance(r, dict)}
    for rep in data.get("dailyReports", []):
        if rep.get("shootDayId") not in report_day_ids:
            fail(f"{name}: daily report {rep.get('id')} shootDayId points to a missing shoot day")
        if rep.get("callSheetId") and rep["callSheetId"] not in sheet_ids:
            fail(f"{name}: daily report {rep.get('id')} callSheetId points to a missing call sheet")
        if set(rep.get("mediaReportIds", [])) - media_ids:
            fail(f"{name}: daily report {rep.get('id')} mediaReportIds points to missing reports")
        for member in rep.get("crew", []):
            if member.get("personId") and member["personId"] not in ids["people"]:
                fail(f"{name}: daily report {rep.get('id')} crew points to a missing person")
    account_ids = {a.get("id") for a in data.get("budget", {}).get("accounts", []) if isinstance(a, dict)}
    asset_ids_all = {a.get("id") for a in data.get("assets", []) if isinstance(a, dict)}
    for exp in data.get("expenses", []):
        if exp.get("accountId") and exp["accountId"] not in account_ids:
            fail(f"{name}: expense {exp.get('id')} accountId points to a missing budget account")
        if exp.get("shootDayId") and exp["shootDayId"] not in report_day_ids:
            fail(f"{name}: expense {exp.get('id')} shootDayId points to a missing shoot day")
        if exp.get("personId") and exp["personId"] not in ids["people"]:
            fail(f"{name}: expense {exp.get('id')} personId points to a missing person")
        if exp.get("receiptAssetId") and exp["receiptAssetId"] not in asset_ids_all:
            fail(f"{name}: expense {exp.get('id')} receiptAssetId points to a missing asset")
    screening_list = [x for x in data.get("screenings", []) if isinstance(x, dict)]
    screening_ids = {x.get("id") for x in screening_list}
    if len(screening_ids) != len(screening_list):
        fail(f"{name}: duplicate IDs in screenings")
    for item in screening_list:
        if item.get("locationId") and item["locationId"] not in ids["locations"]:
            fail(f"{name}: screening {item.get('id')} locationId points to a missing location")
    outlet_list = [x for x in data.get("pressOutlets", []) if isinstance(x, dict)]
    if len({x.get("id") for x in outlet_list}) != len(outlet_list):
        fail(f"{name}: duplicate IDs in pressOutlets")
    for outlet in outlet_list:
        contact_ids = {c.get("id") for c in outlet.get("contacts", []) if isinstance(c, dict)}
        for key in ("screeners", "rsvps", "coverage"):
            for rec in outlet.get(key, []):
                if rec.get("contactId") and rec["contactId"] not in contact_ids:
                    fail(f"{name}: outlet {outlet.get('id')} {key} record {rec.get('id')} contactId points to a missing contact")
        for rec in outlet.get("rsvps", []):
            if rec.get("screeningId") not in screening_ids:
                fail(f"{name}: outlet {outlet.get('id')} rsvp {rec.get('id')} screeningId points to a missing screening")
    partner_list = [x for x in data.get("partners", []) if isinstance(x, dict)]
    if len({x.get("id") for x in partner_list}) != len(partner_list):
        fail(f"{name}: duplicate IDs in partners")
    for partner in partner_list:
        if set(partner.get("screeningIds", [])) - screening_ids:
            fail(f"{name}: partner {partner.get('id')} screeningIds points to missing screenings")
    asset_ids = {a.get("id") for a in data.get("assets", []) if isinstance(a, dict)}
    scout_ids = [x.get("id") for x in data.get("scouts", []) if isinstance(x, dict)]
    if len(scout_ids) != len(set(scout_ids)):
        fail(f"{name}: duplicate IDs in scouts")
    for scout in data.get("scouts", []):
        if scout.get("locationId") not in ids["locations"]:
            fail(f"{name}: scout {scout.get('id')} locationId points to a missing location")
        if set(scout.get("photoIds", [])) - asset_ids:
            fail(f"{name}: scout {scout.get('id')} photoIds points to missing assets")
    budget_line_ids = {l.get("id") for l in (data.get("budget") or {}).get("lines", []) if isinstance(l, dict)}
    day_ids = {d.get("id") for d in data.get("shootDays", []) if isinstance(d, dict)}
    gear = data.get("gear") if isinstance(data.get("gear"), dict) else {}
    gear_ids = [i.get("id") for i in gear.get("items", []) if isinstance(i, dict)]
    if len(gear_ids) != len(set(gear_ids)):
        fail(f"{name}: duplicate IDs in gear items")
    for package in gear.get("packages", []):
        if package.get("shootDayId") and package["shootDayId"] not in day_ids:
            fail(f"{name}: gear package {package.get('id')} shootDayId points to a missing shoot day")
        if set(package.get("itemIds", [])) - set(gear_ids):
            fail(f"{name}: gear package {package.get('id')} itemIds points to missing gear")
    for trip in data.get("trips", []):
        if set(trip.get("personIds", [])) - ids["people"] or set(trip.get("locationIds", [])) - ids["locations"]:
            fail(f"{name}: trip {trip.get('id')} points to missing people or locations")
        for part in trip.get("legs", []) + trip.get("stays", []):
            if set(part.get("personIds", [])) - set(trip.get("personIds", [])):
                fail(f"{name}: trip {trip.get('id')} has travel or a stay for someone not on the trip")
    for plan in data.get("riskPlans", []):
        if set(plan.get("personIds", [])) - ids["people"] or set(plan.get("locationIds", [])) - ids["locations"]:
            fail(f"{name}: risk plan {plan.get('id')} points to missing people or locations")
        for hazard in plan.get("hazards", []):
            if hazard.get("ownerId") and hazard["ownerId"] not in ids["people"]:
                fail(f"{name}: risk plan {plan.get('id')} hazard {hazard.get('id')} ownerId points to a missing person")
    report_ids = {r.get("id") for r in data.get("mediaReports", []) if isinstance(r, dict)}
    if len(report_ids) != len([r for r in data.get("mediaReports", []) if isinstance(r, dict)]):
        fail(f"{name}: duplicate IDs in mediaReports")
    for rep in data.get("mediaReports", []):
        if rep.get("shootDayId") and rep["shootDayId"] not in day_ids:
            fail(f"{name}: report {rep.get('id')} shootDayId points to a missing shoot day")
        if rep.get("callSheetId") and rep["callSheetId"] not in sheet_ids:
            fail(f"{name}: report {rep.get('id')} callSheetId points to a missing call sheet")
        if rep.get("assetId") and rep["assetId"] not in asset_ids:
            fail(f"{name}: report {rep.get('id')} assetId points to a missing asset")
        if rep.get("operatorId") and rep["operatorId"] not in ids["people"]:
            fail(f"{name}: report {rep.get('id')} operatorId points to a missing person")
    for interview in data.get("interviews", []):
        if set(interview.get("mediaReportIds", [])) - report_ids:
            fail(f"{name}: interview {interview.get('id')} mediaReportIds points to missing reports")
        if interview.get("transcriptAssetId") and interview["transcriptAssetId"] not in asset_ids:
            fail(f"{name}: interview {interview.get('id')} transcriptAssetId points to a missing asset")
        if interview.get("locationId") and interview["locationId"] not in ids["locations"]:
            fail(f"{name}: interview {interview.get('id')} locationId points to a missing location")
        beats = {b.get("id") for b in interview.get("beats", [])}
        if {m.get("beatId") for m in interview.get("moments", []) if m.get("beatId")} - beats:
            fail(f"{name}: interview {interview.get('id')} has a moment pointing to a missing beat")
    for clip in [a for a in data.get("assets", []) if isinstance(a, dict) and a.get("type") == "clip"]:
        if set(clip.get("personIds", [])) - ids["people"] or set(clip.get("locationIds", [])) - ids["locations"]:
            fail(f"{name}: clip {clip.get('id')} points to missing people or locations")
        if clip.get("mediaReportId") and clip["mediaReportId"] not in {r.get("id") for r in data.get("mediaReports", []) if isinstance(r, dict)}:
            fail(f"{name}: clip {clip.get('id')} mediaReportId points to a missing report")
    paper = data.get("paperEdit") if isinstance(data.get("paperEdit"), dict) else {}
    interview_ids = {i.get("id") for i in data.get("interviews", []) if isinstance(i, dict)}
    for t in paper.get("transcripts", []):
        if t.get("interviewId") and t["interviewId"] not in interview_ids:
            fail(f"{name}: transcript {t.get('id')} interviewId points to a missing interview")
        if t.get("personId") and t["personId"] not in ids["people"]:
            fail(f"{name}: transcript {t.get('id')} personId points to a missing person")
        if t.get("clipId") and t["clipId"] not in asset_ids:
            fail(f"{name}: transcript {t.get('id')} clipId points to a missing asset")
    for scene in paper.get("scenes", []):
        for bite in scene.get("bites", []):
            if bite.get("out") is not None and bite.get("in") is not None and bite["out"] <= bite["in"]:
                fail(f"{name}: bite {bite.get('id')} ends before it starts")
    line_ids = {l.get("id") for l in (data.get("budget") or {}).get("lines", []) if isinstance(l, dict)}
    for expense in data.get("expenses", []):
        if expense.get("budgetLineId") and expense["budgetLineId"] not in line_ids:
            fail(f"{name}: expense {expense.get('id')} budgetLineId points to a missing budget line")
    for estimate in (data.get("costReport") or {}).get("estimates", []):
        if estimate.get("lineId") and estimate["lineId"] not in line_ids:
            fail(f"{name}: cost report estimate {estimate.get('id')} lineId points to a missing budget line")
    structure = data.get("structure") if isinstance(data.get("structure"), dict) else {}
    act_ids = {a.get("id") for a in structure.get("acts", [])}
    seq_ids = {q.get("id") for q in structure.get("sequences", [])}
    thread_ids = {t.get("id") for t in structure.get("threads", [])}
    card_ids = {c.get("id") for c in structure.get("cards", [])}
    for q in structure.get("sequences", []):
        if q.get("actId") not in act_ids:
            fail(f"{name}: sequence {q.get('id')} actId points to a missing act")
    for c in structure.get("cards", []):
        if (c.get("actId") and c["actId"] not in act_ids) or (c.get("sequenceId") and c["sequenceId"] not in seq_ids) or set(c.get("threadIds", [])) - thread_ids:
            fail(f"{name}: card {c.get('id')} points to a missing act, sequence or thread")
    cut_ids = {c.get("id") for c in data.get("cuts", []) if isinstance(c, dict)}
    if sum(1 for c in data.get("cuts", []) if c.get("locked")) > 1:
        fail(f"{name}: more than one cut is locked")
    for cut in data.get("cuts", []):
        screens = {x.get("id") for x in cut.get("screenings", [])}
        for n in cut.get("notes", []):
            if (n.get("screeningId") and n["screeningId"] not in screens) or (n.get("cardId") and n["cardId"] not in card_ids) or (n.get("carriedToCutId") and n["carriedToCutId"] not in cut_ids):
                fail(f"{name}: cut {cut.get('id')} note {n.get('id')} points to a missing screening, card or cut")
    element_ids = {e.get("id") for e in data.get("thirdPartyElements", []) if isinstance(e, dict)}
    for script in (data.get("clearanceReport") or {}).get("scripts", []):
        segs = {g.get("id") for g in script.get("segments", [])}
        for m in script.get("marks", []):
            if m.get("segId") not in segs or (m.get("personId") and m["personId"] not in ids["people"]) or (m.get("locationId") and m["locationId"] not in ids["locations"]) or (m.get("elementId") and m["elementId"] not in element_ids):
                fail(f"{name}: clearance report mark {m.get('id')} points to a missing line, person, place or element")
    for item in (data.get("chainOfTitle") or {}).get("items", []):
        if set(item.get("contractIds", [])) - {c.get("id") for c in data.get("contracts", [])} or set(item.get("assetIds", [])) - asset_ids:
            fail(f"{name}: chain-of-title item {item.get('key')} points to missing agreements or files")
    press = data.get("pressNotes") if isinstance(data.get("pressNotes"), dict) else {}
    if set(press.get("bioIds", [])) - ids["people"] or set(press.get("stillIds", [])) - asset_ids:
        fail(f"{name}: press notes point to missing people or stills")
    qc = data.get("qc") if isinstance(data.get("qc"), dict) else {}
    master_ids = {v.get("id") for v in qc.get("versions", [])}
    for report in qc.get("reports", []):
        if report.get("versionId") not in master_ids or any(i.get("fixedInId") and i["fixedInId"] not in master_ids for i in report.get("issues", [])):
            fail(f"{name}: QC report {report.get('id')} points to a missing master version")
    contract_ids = {c.get("id") for c in data.get("contracts", [])}
    for statement in data.get("revenueStatements", []):
        if statement.get("contractId") and statement["contractId"] not in contract_ids:
            fail(f"{name}: revenue statement {statement.get('id')} contractId points to a missing contract")
    toc = data.get("theoryOfChange") if isinstance(data.get("theoryOfChange"), dict) else {}
    toc_ids = {k: {x.get("id") for x in toc.get(k, [])} for k in ("audiences", "outcomes")}
    for x in toc.get("activities", []) + toc.get("outcomes", []):
        if set(x.get("audienceIds", [])) - toc_ids["audiences"] or set(x.get("outcomeIds", [])) - toc_ids["outcomes"]:
            fail(f"{name}: theory of change item {x.get('id')} points to a missing audience or outcome")
    indicator_ids = {i.get("id") for i in toc.get("indicators", [])}
    if any(i.get("outcomeId") not in toc_ids["outcomes"] for i in toc.get("indicators", [])):
        fail(f"{name}: an indicator points to a missing outcome")
    impact = data.get("impactReport") if isinstance(data.get("impactReport"), dict) else {}
    if set(impact.get("results", {})) - indicator_ids:
        fail(f"{name}: impact report results point to missing indicators")
    grant_ids = {g.get("id") for g in data.get("grants", [])}
    for gr in data.get("grantReports", []):
        if gr.get("grantId") not in grant_ids:
            fail(f"{name}: grant report {gr.get('id')} points to a missing grant")
    security = data.get("security") if isinstance(data.get("security"), dict) else {}
    if set(security.get("personIds", [])) - ids["people"]:
        fail(f"{name}: security personIds points to missing people")
    for item_id, done in (security.get("done") or {}).items():
        if set(done) - ids["people"]:
            fail(f"{name}: security item {item_id} is marked done by missing people")
    for contract in data.get("contracts", []):
        if contract.get("type") == "deal memo":
            if len(contract.get("personIds", [])) != 1:
                fail(f"{name}: deal memo {contract.get('id')} should name one person")
            if set(contract.get("budgetLineIds", [])) - budget_line_ids:
                fail(f"{name}: deal memo {contract.get('id')} budgetLineIds points to missing budget lines")
        if set(contract.get("shootDayIds", [])) - day_ids:
            fail(f"{name}: contract {contract.get('id')} shootDayIds points to missing shoot days")
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
# XML namespace names look like links but are only labels inside files a tool writes, such as Word documents.
NAMESPACE_HOSTS = {"schemas.openxmlformats.org", "purl.org", "www.w3.org"}
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
        text = page.read_text(encoding="utf-8")
        if 'class="home-link" href="../../index.html"' not in text or 'class="skip-link" href="#main"' not in text:
            fail(f"{rel}/index.html: needs the link back to the toolkit home page and the skip link; copy them from another tool")
        allowed = OPTIONAL_HOSTS.get(rel.as_posix(), set())
        for number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if EXTERNAL.search(line) and not (allowed and re.search(r"\bfetch\s*\(", line) and not re.search(r"XMLHttpRequest|sendBeacon|WebSocket|importScripts|(?:src|action|poster)\s*=|@import|url\(", line, re.I)):
                fail(f"{rel}/index.html:{number}: possible network request or external resource")
            for host in URL_HOST.findall(line) if allowed else []:
                # github.com is only linked to (the guide to shared files), never fetched.
                if host.lower() not in allowed and host.lower() != "github.com" and host.lower() not in NAMESPACE_HOSTS:
                    fail(f"{rel}/index.html:{number}: link to {host} is not an allowed host for this tool")

# Plain templates: spreadsheets and Word documents only, each listed in templates/README.md.
# Word files must not carry macros or links to anything outside the file.
TEMPLATES = ROOT / "templates"
template_readme = TEMPLATES / "README.md"
listed = template_readme.read_text(encoding="utf-8") if template_readme.is_file() else ""
if not listed:
    fail("templates: missing README.md")
for path in sorted(p for p in TEMPLATES.rglob("*") if p.is_file()) if TEMPLATES.is_dir() else []:
    rel = path.relative_to(ROOT)
    if path.name == "README.md":
        continue
    if path.suffix.lower() not in (".csv", ".docx"):
        fail(f"{rel}: templates must be .csv or .docx files")
        continue
    if f"({path.relative_to(TEMPLATES).as_posix()})" not in listed:
        fail(f"{rel}: not listed in templates/README.md")
    # Legal forms (CC0) carry the not-legal-advice notice and say where they were written for.
    if path.parent.name == "legal-forms" and path.suffix.lower() == ".docx":
        try:
            with zipfile.ZipFile(path) as docx:
                text = re.sub(r"<[^>]+>", "", docx.read("word/document.xml").decode("utf-8", "replace"))
            if "Not legal advice" not in text or "Written for" not in text:
                fail(f"{rel}: legal forms need the not-legal-advice notice and a 'Written for' line at the top")
        except (zipfile.BadZipFile, KeyError):
            pass
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

# The home page (index.html) lists every tool, in step with TOOLS.md, and follows the same offline rules.
hub_path = ROOT / "index.html"
if not hub_path.is_file():
    fail("index.html: the home page is missing")
else:
    hub = hub_path.read_text(encoding="utf-8")
    if EXTERNAL.search(hub):
        fail("index.html: loads something from the network; the home page must work offline like the tools")
    tools_md = (ROOT / "TOOLS.md").read_text(encoding="utf-8")
    for slug in sorted(p.name for p in (ROOT / "tools").iterdir() if p.is_dir()):
        if f'href="tools/{slug}/index.html"' not in hub:
            fail(f"index.html: doesn't link to tools/{slug}/index.html")
    for name, use in re.findall(r"^\| \[([^\]]+)\]\(tools/[^)]+\) \| (.+?) \| First version \|$", tools_md, re.M):
        if html.escape(name) not in hub or html.escape(use) not in hub:
            fail(f"index.html: the {name} card doesn't match its line in TOOLS.md")
    for issue in re.findall(r"Planned, \[#(\d+)\]", tools_md):
        if f"/issues/{issue}\"" not in hub:
            fail(f"index.html: planned tool #{issue} from TOOLS.md is missing")
    # Each stage's count, and the total, match the tool cards on the page.
    for stage in re.findall(r'<section[^>]*>\s*<div class="stage-head">.*?</section>', hub, re.S):
        cards = stage.count('<li class="tool"')
        m = re.search(r'<span class="tally">(\d+) tools?</span>', stage)
        name = re.search(r'<h2[^>]*>([^<]+)</h2>', stage)
        if not m or int(m.group(1)) != cards:
            fail(f"index.html: the {name.group(1) if name else 'stage'} count should say {cards} tool{'' if cards == 1 else 's'}")
    total = len(re.findall(r'<li class="tool"', hub))
    if f"<p>{total} tools.</p>" not in hub:
        fail(f"index.html: the tool count above the stages should say {total} tools.")
    for href in re.findall(r'href="((?:tools|templates|samples|docs)/[^"#]*)"', hub):
        if not (ROOT / href).exists():
            fail(f"index.html: links to {href}, which doesn't exist")

# Shared code is copied into each page; the copies must match shared/.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_shared  # noqa: E402

for page in sync_shared.check():
    fail(f"{page}: its copy of the shared code is out of date. Run python3 .github/scripts/sync_shared.py")
for tool in sorted((ROOT / "tools").glob("*/index.html")):
    if "/* oft-shared:tool begin." not in tool.read_text(encoding="utf-8"):
        fail(f"{tool.relative_to(ROOT)}: doesn't include the shared tool code from shared/tool.js")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Schema, sample files, tool rules, templates and the home page all check out.")
