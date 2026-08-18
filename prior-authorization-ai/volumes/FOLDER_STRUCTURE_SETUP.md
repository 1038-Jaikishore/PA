# FOLDER_STRUCTURE_SETUP.md

# AntiGravity Setup Prompt — Create Project Structure Only

Create a brand-new project for an AI-assisted Prior Authorization Triage and Policy Companion.

## STRICT RULES

- DO NOT implement business logic yet.
- DO NOT import any data into MongoDB yet.
- DO NOT run RAG yet.
- DO NOT build the evaluation engine yet.
- DO NOT fabricate or create mock medical data.
- DO NOT create hardcoded CMS Article/LCD/NCD IDs.
- DO NOT create Synthea-derived demo cases yet.
- ONLY create the folder/file skeleton and minimum bootstrapping needed for the project to run.
- Preserve secrets in `.env`; never commit `.env`.
- Create `.env.example` with variable names only.
- After the structure is created, STOP and tell me exactly where to place the CMS and Synthea datasets.

## TECH STACK

Frontend:
- React
- TypeScript
- Vite
- Professional Liquid Glass UI

Backend:
- Python
- FastAPI
- Pydantic

Database:
- MongoDB Atlas

AI:
- OpenAI API
- OpenAI embeddings later for Policy RAG

## CREATE THIS STRUCTURE

```text
prior-authorization-ai/
│
├── README.md
├── .gitignore
├── .env.example
│
├── backend/
│   ├── .env
│   ├── requirements.txt
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── constants.py
│   │   ├── db/
│   │   │   ├── mongodb.py
│   │   │   ├── collections.py
│   │   │   └── indexes.py
│   │   ├── models/
│   │   │   ├── patient.py
│   │   │   ├── prior_auth.py
│   │   │   ├── cms_policy.py
│   │   │   ├── evidence.py
│   │   │   └── evaluation.py
│   │   ├── repositories/
│   │   │   ├── synthea_repository.py
│   │   │   ├── cms_repository.py
│   │   │   └── case_repository.py
│   │   ├── services/
│   │   │   ├── synthea_service.py
│   │   │   ├── pdf_extraction_service.py
│   │   │   ├── code_normalizer.py
│   │   │   ├── cms_relationship_service.py
│   │   │   ├── policy_resolution_service.py
│   │   │   ├── policy_rag_service.py
│   │   │   ├── criteria_service.py
│   │   │   ├── evidence_matching_service.py
│   │   │   └── triage_service.py
│   │   ├── rag/
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   └── vector_index.py
│   │   ├── api/
│   │   │   ├── health.py
│   │   │   ├── datasets.py
│   │   │   ├── patients.py
│   │   │   ├── upload.py
│   │   │   ├── policies.py
│   │   │   └── evaluations.py
│   │   └── utils/
│   │       ├── ids.py
│   │       ├── dates.py
│   │       └── provenance.py
│   │
│   ├── scripts/
│   │   ├── audit_datasets.py
│   │   ├── import_cms.py
│   │   ├── import_synthea.py
│   │   ├── create_indexes.py
│   │   ├── validate_relationships.py
│   │   └── build_rag_index.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   │   ├── cms/
│   │   │   └── synthea/
│   │   ├── normalized/
│   │   │   ├── cms/
│   │   │   └── synthea/
│   │   └── uploads/
│   │
│   ├── reports/
│   └── tests/
│
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── api/
        │   └── client.ts
        ├── components/
        │   ├── glass/
        │   │   ├── GlassCard.tsx
        │   │   ├── GlassPanel.tsx
        │   │   ├── GlassButton.tsx
        │   │   └── GlassBadge.tsx
        │   ├── navigation/
        │   │   └── Sidebar.tsx
        │   ├── policy/
        │   │   ├── PolicyTrace.tsx
        │   │   ├── PolicyCard.tsx
        │   │   └── CriteriaCard.tsx
        │   └── evaluation/
        │       ├── EvidenceRow.tsx
        │       └── TriageResult.tsx
        ├── pages/
        │   ├── Dashboard.tsx
        │   ├── DataStatus.tsx
        │   ├── SyntheaCases.tsx
        │   ├── PatientCase.tsx
        │   ├── UploadCase.tsx
        │   ├── PolicyExplorer.tsx
        │   └── Evaluation.tsx
        ├── hooks/
        ├── types/
        ├── utils/
        └── styles/
            └── global.css
```

## DATASET LOCATIONS I WILL POPULATE MANUALLY

After creating the structure, I will place the 9 CMS coverage-policy files inside:

```text
backend/data/raw/cms/
```

Expected CMS files:

```text
Article.csv
ICD10_Covered_MEJ.csv
ICD10_NonCovered_MEJ.csv
Article_HCPCS.csv
Related_Documents.csv
lcd.csv
Related_NCD.csv
NCD.csv
Contractor.csv
```

I will place the 21 Synthea files inside:

```text
backend/data/raw/synthea/
```

Expected Synthea files:

```text
patients.csv
conditions.csv
medications.csv
procedures.csv
diagnostic_results.csv
vital_signs.csv
encounters.csv
allergies.csv
immunizations.csv
care_plans.csv
social_history.csv
surgeries.csv
functional_status.csv
clinical_assessments.csv
family_history.csv
referrals.csv
medical_equipment.csv
claims.csv
coverage.csv
authorization_requests.csv
providers.csv
```

## ENVIRONMENT FILE

Create:

```text
backend/.env
```

but leave secrets for me to fill manually.

Create `.env.example` with:

```env
MONGODB_URI=
MONGODB_DATABASE=prior_authorization
OPENAI_API_KEY=
OPENAI_MODEL=
OPENAI_EMBEDDING_MODEL=
```

Ensure `.gitignore` includes:

```gitignore
.env
.env.*
!.env.example
__pycache__/
*.pyc
node_modules/
dist/
backend/data/uploads/*
```

Do NOT put credentials into source code.

## FRONTEND SHELL

Create only the initial Liquid Glass application shell.

Required navigation:

- Dashboard
- Data Status
- Synthea Cases
- Upload Patient
- Policy Explorer
- Evaluation

The visual language should use:
- frosted translucent surfaces
- subtle backdrop blur
- thin glass borders
- large rounded corners
- restrained shadows
- smooth hover transitions
- professional spacing
- accessible contrast
- responsive desktop-first layout

Do not display fake policy/evaluation data.

For unfinished features display:

```text
Not available yet — implemented in a later volume.
```

## MINIMUM BACKEND BOOTSTRAP

Create:

```text
GET /api/health
```

with a response similar to:

```json
{
  "status": "healthy",
  "backend": "FastAPI",
  "database": "not_initialized",
  "version": "1.0"
}
```

Do not connect/import MongoDB data in this setup step.

## COMPLETION

Verify:
- project structure exists
- FastAPI starts
- React starts
- frontend can call `/api/health`
- all frontend routes render
- no mock medical data exists
- no dataset has been imported
- no RAG exists
- no evaluation engine exists

Then STOP.

Tell me:

**"Folder structure setup completed. Add the 9 CMS files to `backend/data/raw/cms/` and the 21 Synthea files to `backend/data/raw/synthea/`. Then start Volume 1."**
