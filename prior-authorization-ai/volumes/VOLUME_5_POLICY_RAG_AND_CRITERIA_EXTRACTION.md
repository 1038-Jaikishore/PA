# VOLUME_5_POLICY_RAG_AND_CRITERIA_EXTRACTION.md

# Volume 5 — Policy RAG, OpenAI Embeddings, Retrieval & Structured Criteria

## STRICT EXECUTION RULE

Execute ONLY Volume 5.

Do not implement final evidence matching, triage, or external PDF mode.

When complete, STOP and say:

**"Volume 5 completed. Please review the RAG retrieval and policy criteria UI, then tell me when to proceed to Volume 6."**

## GOAL

Use RAG only AFTER the correct CMS policy has been resolved structurally.

Architecture:

```text
ICD + CPT
↓
MongoDB relationship engine
↓
Article/LCD/NCD resolved
↓
real policy text
↓
RAG
↓
relevant sections
↓
OpenAI
↓
structured policy criteria
```

## CRITICAL RULE

RAG/LLM must NOT guess Article/LCD/NCD IDs.

## TASK 1 — POLICY TEXT EXTRACTION

From the selected policy documents, extract useful text fields such as:
- coverage indications
- limitations
- medical necessity
- documentation requirements
- coding guidance
- diagnosis support/non-support
- relevant NCD text when applicable

Preserve:
- policy type
- policy ID
- version
- source collection
- MongoDB `_id`
- section name

## TASK 2 — CHUNKING

Implement:

```text
backend/app/rag/chunker.py
```

Create policy-aware chunks.

Do not mix unrelated policy documents.

Metadata must include:

```json
{
  "policy_type": "LCD",
  "policy_id": "...",
  "policy_version": "...",
  "section": "...",
  "source_mongo_id": "...",
  "text": "..."
}
```

## TASK 3 — EMBEDDINGS

Use OpenAI embeddings.

Environment variables only:

```env
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL=
```

Never log API keys.

## TASK 4 — VECTOR SEARCH

Prefer MongoDB Atlas Vector Search if available in the configured cluster.

If unavailable, implement the cleanest supported fallback without changing the architecture.

Do not duplicate the entire CMS database unnecessarily.

## TASK 5 — RETRIEVAL

Retrieve policy chunks for topics such as:
- medical necessity
- diagnosis criteria
- conservative therapy
- functional limitation
- imaging
- treatment history
- documentation
- frequency
- limitations

The retriever must remain scoped to the already-resolved policy.

## TASK 6 — CRITERIA EXTRACTION

Use OpenAI to convert retrieved policy text into structured criteria.

Schema:

```json
{
  "criteria": [
    {
      "criterion_id": "C1",
      "category": "functional_limitation",
      "requirement": "...",
      "required": true,
      "source_policy_type": "LCD",
      "source_policy_id": "...",
      "source_section": "...",
      "source_text": "..."
    }
  ]
}
```

Possible categories:
- diagnosis
- symptoms
- severity
- duration
- functional_limitation
- conservative_treatment
- medication
- physical_therapy
- injection
- imaging
- laboratory
- contraindication
- documentation
- frequency
- coding_requirement

Do not invent criteria outside retrieved policy text.

## TASK 7 — FRONTEND

In Policy Explorer / Case page add a Liquid Glass:

```text
Policy RAG
```

section showing:
- indexed policy
- retrieved chunks
- section name
- relevance score if available
- source policy
- source MongoDB ID

Add:

```text
Extracted Coverage Criteria
```

cards with:
- criterion ID
- category
- requirement
- required/conditional
- policy citation/provenance

No patient matching yet.

## TESTS

Test:
- retrieval stays within resolved policy
- criteria have source provenance
- missing policy text produces explicit error
- LLM output schema validation
- no policy ID guessing

## REQUIRED REPORT

Create:

```text
backend/reports/VOLUME_5_REPORT.md
```

## COMPLETION GATE

Volume 5 is complete only if:
- real resolved policy text is chunked
- embeddings/index work
- relevant sections can be retrieved
- structured criteria are extracted
- every criterion has provenance
- frontend shows RAG results
- no final patient evidence statuses or triage exist yet

Then STOP.
