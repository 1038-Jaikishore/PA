# VOLUME_6_EVIDENCE_MATCHING_AND_TRIAGE.md

# Volume 6 — Evidence Matching, Deterministic Triage & Professional Review UI

## STRICT EXECUTION RULE

Execute ONLY Volume 6.

Do not add external PDF-only patient intake yet.

When complete, STOP and say:

**"Volume 6 completed. Please review the evidence matching and triage results, then tell me when to proceed to Volume 7."**

## GOAL

Compare structured policy criteria from Volume 5 against real Synthea patient evidence and generate a deterministic triage recommendation.

## TASK 1 — EVIDENCE MATCHING

For each criterion search relevant Synthea MongoDB collections by `patient_id`.

Potential evidence sources:
- conditions
- procedures
- medications
- diagnostic_results
- vital_signs
- functional_status
- clinical_assessments
- surgeries
- care_plans
- encounters
- other relevant collections

Preserve:
- source collection
- MongoDB `_id`
- field/value
- date if present
- provenance

## ALLOWED STATUSES

Use ONLY:

```text
MET
NOT_MET
UNCLEAR
```

### MET
Only when explicit supporting evidence exists.

### NOT_MET
Only when explicit evidence shows the requirement is not satisfied.

### UNCLEAR
Use when:
- information is missing
- evidence is incomplete
- evidence is ambiguous
- evidence conflicts
- documentation is insufficient

CRITICAL:

```text
MISSING EVIDENCE != NOT_MET
```

## TASK 2 — EVIDENCE RESULT SCHEMA

Example:

```json
{
  "criterion_id": "C1",
  "requirement": "...",
  "status": "MET",
  "patient_evidence": [
    {
      "collection": "synthea_diagnostic_results",
      "mongo_id": "...",
      "field": "...",
      "value": "...",
      "date": "..."
    }
  ],
  "policy_source": {},
  "reason": "..."
}
```

## TASK 3 — TRIAGE ENGINE

The final recommendation must be deterministic.

Suggested rules:

```text
All mandatory criteria MET
→ APPROVE_RECOMMENDATION

One or more mandatory criteria UNCLEAR
→ REQUEST_MORE_INFORMATION

One or more critical criteria explicitly NOT_MET
→ NURSE_REVIEW

Policy unresolved / conflicting policy state
→ MANUAL_REVIEW
```

OpenAI may generate a human-readable explanation AFTER the deterministic result is known.

OpenAI must not choose the triage result.

## TASK 4 — API

Add/refine evaluation endpoint:

```text
POST /api/evaluations/{case_id}/run
GET /api/evaluations/{case_id}
```

Return:
- patient/case summary
- CMS relationship trace
- selected policy
- RAG criteria
- evidence result for every criterion
- summary counts
- deterministic triage
- warnings/missing information

## TASK 5 — FRONTEND

Build/refine professional Liquid Glass `Evaluation.tsx`.

Top summary:

```text
Prior Authorization Review

Recommendation
REQUEST MORE INFORMATION

Criteria Summary
7 MET
2 UNCLEAR
0 NOT MET
```

Policy trace:
- Article
- LCD
- NCD if valid
- real MongoDB IDs

Criteria cards:

```text
✓ MET
Functional limitation documented

Patient Evidence
...

Policy Requirement
...

Source
...
```

```text
? UNCLEAR
Required therapy duration

Missing Information
...
```

Include Human Review section.

## TASK 6 — FAILURE BEHAVIOR

Never hide:
- missing patient evidence
- unresolved policy
- non-covered ICD conflicts
- missing NCD
- ambiguous Article matches

Return explicit statuses/warnings.

## TESTS

Test:
- all MET
- some UNCLEAR
- explicit NOT_MET
- missing evidence
- unresolved policy
- deterministic repeatability
- provenance on every criterion

## REQUIRED REPORT

Create:

```text
backend/reports/VOLUME_6_REPORT.md
```

## COMPLETION GATE

Volume 6 is complete only if:
- every criterion gets MET/NOT_MET/UNCLEAR
- evidence comes from real Synthea MongoDB documents
- policy source is preserved
- triage is deterministic
- frontend shows traceable review results
- no external PDF mode exists yet

Then STOP.
