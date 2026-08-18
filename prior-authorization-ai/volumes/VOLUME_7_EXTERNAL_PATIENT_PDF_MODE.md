# VOLUME_7_EXTERNAL_PATIENT_PDF_MODE.md

# Volume 7 — External Patient PDF Intake, Extraction & PDF-Only Evaluation

## STRICT EXECUTION RULE

Execute ONLY Volume 7.

Do not perform broad final UI redesign or unrelated architectural changes.

When complete, STOP and say:

**"Volume 7 completed. Please review external PDF intake and PDF-only evaluation, then tell me when to proceed to Volume 8."**

## GOAL

Allow a user to upload a patient/prior-authorization PDF even if that patient does NOT exist in Synthea.

The system must support:

```text
MODE A
PDF matches Synthea
→ PDF evidence + Synthea evidence

MODE B
PDF does not match Synthea
→ PDF evidence only
```

Synthea is optional support, not a mandatory patient identity source.

## TASK 1 — PDF UPLOAD

Create/refine:

```text
POST /api/upload
```

Accept PDF only with safe size/type validation.

Store temporary upload under:

```text
backend/data/uploads/
```

Do not commit uploads.

## TASK 2 — TEXT EXTRACTION

Extract readable text using a suitable Python PDF library.

Do not use OCR unless necessary.

Preserve source filename and page/provenance information when feasible.

## TASK 3 — CLINICAL EXTRACTION

Use deterministic parsing + OpenAI structured extraction as appropriate.

Extract:

```text
patient identifiers if present
name
DOB/age
sex
diagnosis
ICD-10
requested service
CPT/HCPCS
laterality
symptoms
duration
functional limitations
medications
previous treatment
physical therapy
injections
imaging
lab results
clinical findings
contraindications
provider/facility
location if present
```

Never fabricate missing facts.

If code is explicitly documented:
- mark source = DOCUMENTED

If code is inferred from narrative:
- mark source = MODEL_INFERRED
- include confidence
- preserve supporting source text

## TASK 4 — OPTIONAL SYNTHEA MATCH

Try deterministic patient matching only if enough identifiers exist.

Preferred:
- patient_id/member ID
- strong exact identifiers
- name + DOB only if appropriate

If no match:

```json
{
  "synthea_match": false,
  "patient_source": "PDF_ONLY"
}
```

Continue evaluation.

Do not fail merely because Synthea has no patient.

## TASK 5 — CMS POLICY RESOLUTION

Use extracted normalized:

```text
ICD-10
+
CPT/HCPCS
```

with the existing Volume 3 resolver.

Do not provide Article/LCD/NCD manually.

## TASK 6 — EVIDENCE MODE

If Synthea match exists:
- combine PDF evidence + Synthea evidence
- retain provenance and indicate source

If no match:
- use PDF evidence only

Missing information becomes:

```text
UNCLEAR
```

not automatically NOT_MET.

## TASK 7 — FRONTEND

Build a polished Liquid Glass `UploadCase.tsx`.

Drag-and-drop PDF upload.

Progress stepper:

```text
Uploading
↓
Extracting Clinical Data
↓
Validating Codes
↓
Searching Synthea
↓
Resolving CMS Policy
↓
Running Policy RAG
↓
Matching Evidence
↓
Generating Triage
```

After extraction show editable/reviewable structured information before running evaluation if appropriate.

Clearly display:

```text
Patient Source:
Synthea + PDF
```

or:

```text
Patient Source:
Uploaded PDF Only
```

## TASK 8 — TESTS

Test:
- PDF with explicit ICD/CPT
- PDF without Synthea match
- PDF with Synthea match
- missing ICD
- missing CPT
- inferred code with provenance
- missing clinical evidence
- invalid PDF
- policy not found

## REQUIRED REPORT

Create:

```text
backend/reports/VOLUME_7_REPORT.md
```

## COMPLETION GATE

Volume 7 is complete only if:
- external PDFs can be uploaded
- structured clinical extraction works
- Synthea matching is optional
- PDF-only evaluation continues without Synthea
- CMS policy is still resolved from real MongoDB relationships
- missing evidence becomes UNCLEAR
- frontend clearly shows source/provenance

Then STOP.
