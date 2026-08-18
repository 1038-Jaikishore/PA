# VOLUME_2_MONGODB_INGESTION_AND_PATIENT_GRAPH.md

# Volume 2 — MongoDB Ingestion, Indexes, Synthea Patient Graph & Progress UI

## STRICT EXECUTION RULE

Execute ONLY Volume 2.

Do not implement the CMS policy resolver, RAG, criteria extraction, evidence matching, triage, or external PDF evaluation yet.

When complete, STOP and say:

**"Volume 2 completed. Please review MongoDB/Data Status and Synthea patient views, then tell me when to proceed to Volume 3."**

## GOAL

Import the validated 9 CMS + 21 Synthea datasets into the existing MongoDB Atlas database and prove that Synthea patient relationships work.

## ENVIRONMENT

Use existing environment variables:

```env
MONGODB_URI=
MONGODB_DATABASE=prior_authorization
```

Never print/log the URI or credentials.

## TASK 1 — CONNECT TO MONGODB

Implement/refine:

```text
backend/app/db/mongodb.py
backend/app/db/collections.py
backend/app/db/indexes.py
```

Use one configured database.

Do not create a second competing database.

## TASK 2 — IMPORT 9 CMS DATASETS

Implement:

```text
backend/scripts/import_cms.py
```

Recommended collection names:

```text
cms_articles
cms_icd_covered_articles
cms_icd_noncovered_articles
cms_article_hcpcs
cms_related_documents
cms_lcd
cms_related_ncd
cms_ncd
cms_contractors
```

Preserve:
- original source fields
- original source values
- source filename
- import timestamp if helpful

Do not fabricate relationships.

## TASK 3 — IMPORT 21 SYNTHEA DATASETS

Implement:

```text
backend/scripts/import_synthea.py
```

Recommended collections:

```text
synthea_patients
synthea_conditions
synthea_medications
synthea_procedures
synthea_diagnostic_results
synthea_vital_signs
synthea_encounters
synthea_allergies
synthea_immunizations
synthea_care_plans
synthea_social_history
synthea_surgeries
synthea_functional_status
synthea_clinical_assessments
synthea_family_history
synthea_referrals
synthea_medical_equipment
synthea_claims
synthea_coverage
synthea_authorization_requests
synthea_providers
```

If useful, add normalized fields such as:

```json
{
  "procedure_code": "CPT27447",
  "normalized_cpt": "27447"
}
```

Do not replace original values.

## TASK 4 — VALIDATE IMPORT COUNTS

For every collection compare:
- CSV source rows
- MongoDB imported documents

Do not silently drop malformed rows.

Any rejected rows must be reported.

## TASK 5 — CREATE INDEXES

Create indexes only after inspecting actual schemas.

Likely useful fields:

```text
patient_id
encounter_id
provider_id
article_id
article_version
lcd_id
lcd_version
r_article_id
r_ncd_id
icd10_code_id
hcpc_code_id
contractor_id
```

Document every created index.

## TASK 6 — BUILD SYNTHEA PATIENT GRAPH

Implement repository/service APIs using `patient_id`.

Required endpoints:

```text
GET /api/patients
GET /api/patients/{patient_id}
GET /api/patients/{patient_id}/clinical-context
```

A patient clinical context should aggregate real records from:

```text
conditions
procedures
medications
diagnostic_results
vital_signs
encounters
allergies
care_plans
social_history
surgeries
functional_status
clinical_assessments
family_history
referrals
medical_equipment
claims
coverage
providers
```

Preserve source collection and MongoDB `_id` for provenance.

Do not interpret `DIAGxx/PROCxxxx` as CMS codes.

## TASK 7 — FRONTEND

Update Dashboard/Data Status:

```text
MongoDB           Connected
CMS Collections   9 / 9
Synthea           21 / 21
Patient Graph     Ready
CMS Policy Engine Not Started
RAG               Not Started
Evaluation        Not Started
```

Build/refine `SyntheaCases.tsx`.

Show:
- patient list
- basic demographics
- linked-record counts

Build/refine `PatientCase.tsx`.

Liquid Glass sections:
- Overview
- Conditions
- Procedures
- Medications
- Diagnostics
- Functional Status
- Clinical Assessments
- Coverage
- Timeline

All displayed values must come from MongoDB.

## REQUIRED REPORT

Create:

```text
backend/reports/VOLUME_2_REPORT.md
```

Include:
- database used
- collections created
- document counts
- indexes
- any rejected rows
- Synthea join keys
- 5 tested patient IDs and linked-record counts

## COMPLETION GATE

Volume 2 is complete only if:
- MongoDB connects
- all 30 datasets are imported successfully or every exception is documented
- collection counts are validated
- indexes exist
- at least 5 patients resolve across related Synthea collections
- frontend displays real MongoDB data
- no CMS policy resolver exists yet
- no RAG/evaluation exists yet

Then STOP.
