# VOLUME_1_FOUNDATION_AND_DATA_AUDIT.md

# Volume 1 — Foundation, Dataset Audit, Normalization Contract & Progress UI

## STRICT EXECUTION RULE

Execute ONLY Volume 1.

Do not start MongoDB ingestion, patient graph construction, CMS relationship resolution, RAG, evidence matching, triage, or PDF evaluation.

When every completion gate below passes, STOP and say:

**"Volume 1 completed. Please review the Data Status UI and reports, then tell me when to proceed to Volume 2."**

## GOAL

Validate the project foundation and audit all 30 source datasets before any database ingestion.

At this point I will already have manually placed:

```text
9 CMS files     → backend/data/raw/cms/
21 Synthea files → backend/data/raw/synthea/
```

Raw files are READ-ONLY.

## TASK 1 — VERIFY FOUNDATION

Verify:
- FastAPI starts
- React/Vite starts
- frontend calls backend health endpoint
- configuration loads from environment variables
- no secrets are hardcoded
- `.env` is ignored by Git
- `.env.example` contains variable names only

## TASK 2 — AUDIT ALL DATASETS

Implement/refine:

```text
backend/scripts/audit_datasets.py
```

Audit every file under:

```text
backend/data/raw/cms/
backend/data/raw/synthea/
```

For every dataset report:
- file name
- detected format
- encoding
- row count
- column count
- exact column names
- inferred types
- null counts
- duplicate rows
- candidate primary/business keys
- candidate relationship keys
- malformed rows
- sample values
- suspicious internal codes
- data-quality warnings

Do not silently repair raw files.

## TASK 3 — CMS FIELD DISCOVERY

For the 9 CMS files, explicitly discover the real fields corresponding to:

```text
article_id
article_version
display_id
icd10_code_id
hcpc_code_id
lcd_id
lcd_version
r_article_id
r_article_version
r_lcd_id
r_ncd_id
r_ncd_version
contractor_id
```

Do not guess field names.

Create a relationship report that identifies the likely chain:

```text
ICD10_Covered_MEJ
        ↓
      Article

Article_HCPCS
        ↓
      Article

Article
        ↓
Related_Documents
        ↓
       LCD
        ↓
 Related_NCD
        ↓
       NCD

LCD
 ↓
Contractor
```

## TASK 4 — SYNTHEA FIELD DISCOVERY

Identify actual Synthea linkage fields including:

```text
patient_id
encounter_id
provider_id
condition_id
procedure_id
claim_id
authorization_id
```

Identify which datasets use real standard codes and which use internal synthetic codes.

Specifically detect internal values such as:

```text
DIAGxx
PROCxxxx
```

and mark them:

```text
INTERNAL_SYNTHETIC_CODE
```

Do not treat them as CMS ICD-10 or HCPCS/CPT codes.

## TASK 5 — NORMALIZATION CONTRACT

Create normalization helpers/specifications but DO NOT change raw files.

Examples:

```text
m17.11      → M17.11
CPT27447    → 27447
CPT 27447   → 27447
HCPCS:J7325 → J7325
```

Store normalized outputs only under:

```text
backend/data/normalized/cms/
backend/data/normalized/synthea/
```

if normalized files are needed.

Never overwrite raw files.

## TASK 6 — PROFESSIONAL LIQUID GLASS FRONTEND

Improve the Liquid Glass frontend so Volume 1 progress is visible.

`DataStatus.tsx` must show:

```text
CMS datasets
9 / 9 detected

Synthea datasets
21 / 21 detected
```

Each dataset card/table row should show:
- detected/not detected
- row count
- column count
- likely primary key
- relationship fields
- warnings
- normalization status

Clicking/expanding a dataset may show sample schema information.

No fake medical outcomes.

Dashboard status should show:

```text
Backend            Connected
Dataset Audit      Complete
MongoDB Import     Not Started
Patient Graph      Not Started
CMS Policy Engine  Not Started
RAG                Not Started
Evaluation         Not Started
```

## REQUIRED REPORTS

Create:

```text
backend/reports/VOLUME_1_REPORT.md
backend/reports/dataset_audit.json
backend/reports/dataset_audit.md
backend/reports/relationship_report.md
backend/reports/data_quality_report.md
```

## TESTS

Add tests for:
- file detection
- schema discovery
- code normalization
- no mutation of raw datasets

## COMPLETION GATE

Volume 1 is complete only if:
- exactly 9 CMS files are detected
- exactly 21 Synthea files are detected
- schemas are audited
- relationship candidates are documented
- internal `DIAGxx/PROCxxxx` style codes are flagged
- raw files remain unchanged
- frontend Data Status displays real audit information
- no MongoDB import has occurred
- no RAG/evaluation logic has been started

Then STOP.
