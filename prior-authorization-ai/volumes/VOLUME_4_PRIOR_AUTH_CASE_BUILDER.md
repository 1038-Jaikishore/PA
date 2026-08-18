# VOLUME_4_PRIOR_AUTH_CASE_BUILDER.md

# Volume 4 — Synthea Prior Authorization Case Builder & CMS Connection

## STRICT EXECUTION RULE

Execute ONLY Volume 4.

Do not build Policy RAG, criteria extraction, evidence matching, triage, or external PDF mode yet.

When complete, STOP and say:

**"Volume 4 completed. Please review Synthea case creation and CMS policy resolution, then tell me when to proceed to Volume 5."**

## GOAL

Connect a selected Synthea patient to a policy-compatible prior authorization request and prove:

```text
patient
→ ICD-10 + CPT/HCPCS
→ CMS Article
→ LCD
```

## CRITICAL DATA RULE

Do NOT directly treat:

```text
DIAGxx
PROCxxxx
```

from synthetic authorization/claim data as CMS ICD-10 or CPT/HCPCS.

Use real standardized codes from appropriate sources or clearly defined policy-aligned demo mappings.

Never hardcode Article/LCD/NCD.

## TASK 1 — CASE MODEL

Create a structured case model:

```json
{
  "case_id": "...",
  "patient_id": "...",
  "diagnosis": {
    "original_code": "...",
    "normalized_icd10": "...",
    "description": "...",
    "source": "..."
  },
  "requested_service": {
    "original_code": "...",
    "normalized_hcpcs_cpt": "...",
    "description": "...",
    "source": "..."
  },
  "clinical_context": {},
  "provenance": []
}
```

## TASK 2 — SELECT/BUILD POLICY-COMPATIBLE CASES

Use actual Synthea clinical records.

If the original authorization request uses an internal code, do not pretend it is standardized.

Support explicit policy-aligned demo cases for development/testing, but clearly mark them as:

```text
POLICY_ALIGNED_SYNTHETIC_CASE
```

The case should provide only:
- patient_id
- real ICD-10
- real CPT/HCPCS
- provenance

The CMS resolver must still dynamically discover Article/LCD/NCD.

## TASK 3 — CLINICAL CONTEXT

For selected patient, aggregate evidence from MongoDB:
- conditions
- procedures
- medications
- diagnostic results
- functional status
- clinical assessments
- surgeries
- care plans
- other relevant patient records

Preserve collection and MongoDB `_id`.

## TASK 4 — CONNECT TO CMS RESOLVER

Pass only:

```json
{
  "icd10": "...",
  "hcpcs_cpt": "..."
}
```

to the Volume 3 policy resolver.

Store the returned relationship trace with the case.

## TASK 5 — APIS

Create/refine endpoints such as:

```text
POST /api/prior-auth/cases
GET /api/prior-auth/cases/{case_id}
POST /api/prior-auth/cases/{case_id}/resolve-policy
```

Adapt to existing route conventions if necessary.

## TASK 6 — FRONTEND

On `PatientCase.tsx` add:

```text
Create Prior Authorization Case
```

Case builder should show:
- patient
- diagnosis
- ICD-10
- requested service
- CPT/HCPCS
- provenance
- evidence counts

Button:

```text
Resolve CMS Policy
```

Then show the real policy trace from Volume 3.

Use Liquid Glass cards and stepper/timeline.

## TASK 7 — VALIDATION

Test several policy-compatible Synthea cases.

At least one must successfully resolve:

```text
Patient
→ ICD/CPT
→ Article
→ LCD
```

Do not evaluate criteria yet.

## REQUIRED REPORT

Create:

```text
backend/reports/VOLUME_4_REPORT.md
```

Include:
- case schema
- standardized-code sources
- internal synthetic-code handling
- tested case IDs
- policy resolution results
- any data alignment limitations

## COMPLETION GATE

Volume 4 is complete only if:
- Synthea patient context is linked to a case
- cases use real ICD-10 + CPT/HCPCS
- DIAGxx/PROCxxxx are never sent to CMS resolver
- CMS policy resolves dynamically
- frontend displays real patient + real CMS trace
- no RAG/criteria/evidence evaluation exists yet

Then STOP.
