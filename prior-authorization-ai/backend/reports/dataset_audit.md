# Dataset Audit Report

## CMS
### NCD.csv
- Rows: 345
- Columns: 15
- Primary Keys Candidates: document_id, title
- Relationship Keys: document_id, document_display_id
- Warnings: 

### lcd.csv
- Rows: 1137
- Columns: 1780
- Primary Keys Candidates: 
- Relationship Keys: lcd_id, lcd_version, display_id
- Warnings: 10 duplicate rows found.

### Related_Documents.csv
- Rows: 2807
- Columns: 12
- Primary Keys Candidates: 
- Relationship Keys: lcd_id, lcd_version, r_article_id, r_article_version, r_lcd_id, r_lcd_version, r_contractor_id, source_id
- Warnings: 6 duplicate rows found.

### Article_cleaned.csv
- Rows: 463
- Columns: 16
- Primary Keys Candidates: article_id
- Relationship Keys: article_id, article_version, display_id, article_type, article_type_description, article_eff_date, article_end_date, article_pub_date, reference_article
- Warnings: 

### Related_NCD.csv
- Rows: 1419
- Columns: 7
- Primary Keys Candidates: 
- Relationship Keys: lcd_id, lcd_version, r_ncd_id, r_ncd_version
- Warnings: 

### ICD10_Covered_MEJ.csv
- Rows: 57533
- Columns: 10
- Primary Keys Candidates: 
- Relationship Keys: article_id, article_version, icd10_code_id, icd10_code_version
- Warnings: 4 duplicate rows found.

### Article_HCPCS.csv
- Rows: 22234
- Columns: 9
- Primary Keys Candidates: 
- Relationship Keys: article_id, article_version, hcpc_code_id, hcpc_code_version, hcpc_code_group
- Warnings: 30 duplicate rows found.

### ICD10_NonCovered_MEJ.csv
- Rows: 47885
- Columns: 10
- Primary Keys Candidates: 
- Relationship Keys: article_id, article_version, icd10_code_id, icd10_code_version
- Warnings: 

### Contractor.csv
- Rows: 144
- Columns: 6
- Primary Keys Candidates: contractor_id
- Relationship Keys: contractor_id, contract_type_id, contract_subtype_id
- Warnings: 

## SYNTHEA
### clinical_assessments.csv
- Rows: 60
- Columns: 8
- Primary Keys Candidates: assessment_id
- Relationship Keys: assessment_id, patient_id
- Warnings: 

### medications.csv
- Rows: 100
- Columns: 8
- Primary Keys Candidates: medication_id
- Relationship Keys: medication_id, patient_id
- Warnings: 

### providers.csv
- Rows: 15
- Columns: 9
- Primary Keys Candidates: provider_id, first_name, last_name, npi, contact_number
- Relationship Keys: provider_id
- Warnings: 

### coverage.csv
- Rows: 30
- Columns: 12
- Primary Keys Candidates: patient_id, plan_id
- Relationship Keys: patient_id, plan_id
- Warnings: 

### referrals.csv
- Rows: 50
- Columns: 9
- Primary Keys Candidates: referral_id
- Relationship Keys: referral_id, patient_id, referring_provider_id, specialist_provider_id
- Warnings: 

### claims.csv
- Rows: 100
- Columns: 15
- Primary Keys Candidates: claim_id, procedure_code, amount_billed, amount_paid
- Relationship Keys: claim_id, patient_id, provider_id, procedure_code, diagnosis_code
- Warnings: Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'procedure_code'. Marked as INTERNAL_SYNTHETIC_CODE., Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'diagnosis_code'. Marked as INTERNAL_SYNTHETIC_CODE.

### diagnostic_results.csv
- Rows: 80
- Columns: 8
- Primary Keys Candidates: result_id
- Relationship Keys: result_id, patient_id
- Warnings: Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'result_id'. Marked as INTERNAL_SYNTHETIC_CODE.

### care_plans.csv
- Rows: 40
- Columns: 10
- Primary Keys Candidates: plan_id
- Relationship Keys: plan_id, patient_id, provider_id
- Warnings: 

### allergies.csv
- Rows: 40
- Columns: 8
- Primary Keys Candidates: allergy_id
- Relationship Keys: allergy_id, patient_id
- Warnings: 

### procedures.csv
- Rows: 60
- Columns: 8
- Primary Keys Candidates: procedure_record_id, procedure_date
- Relationship Keys: procedure_record_id, patient_id, provider_id, procedure_code
- Warnings: 

### authorization_requests.csv
- Rows: 50
- Columns: 16
- Primary Keys Candidates: request_id, requested_procedure_code, supporting_evidence_url
- Relationship Keys: request_id, patient_id, provider_id, requested_procedure_code, diagnosis_code, provider_justification
- Warnings: Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'requested_procedure_code'. Marked as INTERNAL_SYNTHETIC_CODE., Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'diagnosis_code'. Marked as INTERNAL_SYNTHETIC_CODE.

### conditions.csv
- Rows: 80
- Columns: 8
- Primary Keys Candidates: condition_id, onset_date
- Relationship Keys: condition_id, patient_id, diagnosis_code, condition_type
- Warnings: 

### encounters.csv
- Rows: 80
- Columns: 9
- Primary Keys Candidates: encounter_id
- Relationship Keys: encounter_id, patient_id, provider_id, encounter_date, encounter_type, primary_diagnosis_code
- Warnings: Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'primary_diagnosis_code'. Marked as INTERNAL_SYNTHETIC_CODE.

### medical_equipment.csv
- Rows: 40
- Columns: 8
- Primary Keys Candidates: equipment_id
- Relationship Keys: equipment_id, patient_id
- Warnings: 

### immunizations.csv
- Rows: 60
- Columns: 7
- Primary Keys Candidates: immunization_id
- Relationship Keys: immunization_id, patient_id
- Warnings: 

### functional_status.csv
- Rows: 60
- Columns: 9
- Primary Keys Candidates: status_id
- Relationship Keys: status_id, patient_id
- Warnings: 

### patients.csv
- Rows: 40
- Columns: 9
- Primary Keys Candidates: patient_id, first_name, last_name, member_id, summary_card_text
- Relationship Keys: patient_id, member_id
- Warnings: 

### social_history.csv
- Rows: 30
- Columns: 8
- Primary Keys Candidates: social_history_id, patient_id
- Relationship Keys: social_history_id, patient_id
- Warnings: 

### surgeries.csv
- Rows: 50
- Columns: 8
- Primary Keys Candidates: surgery_id
- Relationship Keys: surgery_id, patient_id, provider_id
- Warnings: 

### family_history.csv
- Rows: 40
- Columns: 6
- Primary Keys Candidates: history_id
- Relationship Keys: history_id, patient_id, condition
- Warnings: 

### vital_signs.csv
- Rows: 100
- Columns: 9
- Primary Keys Candidates: vital_id
- Relationship Keys: vital_id, patient_id
- Warnings: 

## ALIGNED_CASES
### synthea_condition_additions_for_policy_demo.csv
- Rows: 12
- Columns: 6
- Primary Keys Candidates: case_id
- Relationship Keys: case_id, patient_id, icd10_code
- Warnings: 

### synthea_cms_policy_aligned_cases.csv
- Rows: 12
- Columns: 17
- Primary Keys Candidates: case_id
- Relationship Keys: case_id, patient_id, patient_name, icd10_code, cpt_hcpcs_code, cms_article_id, cms_article_version, cms_article_title, lcd_id, lcd_version, lcd_title, ncd_status
- Warnings: 

