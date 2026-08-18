# VOLUME_3_CMS_POLICY_RELATIONSHIP_ENGINE.md

# Volume 3 — Deterministic CMS Relationship Engine & Policy Explorer

## STRICT EXECUTION RULE

Execute ONLY Volume 3.

Do not implement RAG, criteria extraction, evidence matching, triage, or external PDF evaluation.

When complete, STOP and say:

**"Volume 3 completed. Please review the Policy Explorer and real MongoDB ID trace, then tell me when to proceed to Volume 4."**

## GOAL

Build the deterministic CMS policy resolver using only the 9 CMS MongoDB collections.

The LLM must NOT choose the policy.

## INPUT

Resolver accepts:

```json
{
  "icd10": "...",
  "hcpcs_cpt": "..."
}
```

No hardcoded defaults.

## TASK 1 — ICD-10 → ARTICLE

Query:

```text
cms_icd_covered_articles
```

Return all matching Article ID/version pairs and relationship MongoDB `_id`s.

Also query:

```text
cms_icd_noncovered_articles
```

and report any explicit non-covered mappings.

## TASK 2 — HCPCS/CPT → ARTICLE

Query:

```text
cms_article_hcpcs
```

Return all Article ID/version pairs and relationship MongoDB `_id`s.

## TASK 3 — INTERSECTION

Compute:

```text
Covered ICD Article set
∩
HCPCS Article set
```

Do not select the first row.

If no intersection:

```json
{
  "status": "NO_ARTICLE_INTERSECTION"
}
```

If multiple intersections exist, return/rank deterministically using real version/status information.

## TASK 4 — ARTICLE MASTER

Fetch from:

```text
cms_articles
```

Return:
- article_id
- article_version
- display_id
- title
- status
- MongoDB `_id`

## TASK 5 — ARTICLE → LCD

Use:

```text
cms_related_documents
```

Resolve actual related LCD IDs/version fields.

Then fetch LCD from:

```text
cms_lcd
```

Return:
- LCD ID
- LCD version
- title
- policy text fields
- MongoDB `_id`
- relationship MongoDB `_id`

## TASK 6 — LCD/ARTICLE → NCD

Use:

```text
cms_related_ncd
```

For every NCD candidate:
1. read `r_ncd_id`/version
2. reject `0`, `"0"`, null, empty unless a real NCD master record exists
3. verify candidate in `cms_ncd`
4. only then return it

If none:

```json
{
  "ncd_status": "NO_RELATED_NCD"
}
```

## TASK 7 — CONTRACTOR

Use:

```text
cms_contractors
```

Resolve contractor information where the relationship is actually supported.

Do not fabricate jurisdiction or contractor.

Jurisdiction is not required for this volume unless present in the 9-file corpus.

## TASK 8 — API

Create:

```text
POST /api/policies/resolve
```

Return a complete trace:

```json
{
  "input": {},
  "covered_icd_matches": [],
  "noncovered_icd_matches": [],
  "hcpcs_matches": [],
  "intersection": [],
  "selected_article": {},
  "related_lcds": [],
  "selected_lcd": {},
  "related_ncds": [],
  "selected_ncd": null,
  "contractor": null,
  "mongo_ids": {},
  "warnings": []
}
```

## TASK 9 — POLICY EXPLORER FRONTEND

Build a polished Liquid Glass `PolicyExplorer`.

Inputs:
- ICD-10
- CPT/HCPCS

Button:
- Resolve Policy

Visual trace:

```text
ICD-10 ─────────┐
                ├── Article ──→ LCD ──→ NCD
CPT/HCPCS ──────┘
```

Show:
- covered ICD matches
- non-covered ICD matches
- HCPCS matches
- intersection
- selected Article
- related LCD
- valid NCD or "No related NCD"
- contractor if available
- real MongoDB `_id`s

No fake values.

## TESTS

Test:
- valid intersection
- no ICD match
- no HCPCS match
- no intersection
- multiple intersections
- Article without LCD
- NCD candidate = 0/null
- valid NCD
- non-covered ICD relationship

## REQUIRED REPORT

Create:

```text
backend/reports/VOLUME_3_REPORT.md
```

Include actual field names and successful relationship traces.

## COMPLETION GATE

Volume 3 is complete only if:
- ICD → Article works
- HCPCS → Article works
- intersection works
- Article → LCD works
- NCD candidates are validated against NCD master
- actual MongoDB `_id`s are returned
- frontend Policy Explorer uses live backend results
- no RAG exists yet
- no evidence/triage exists yet

Then STOP.
