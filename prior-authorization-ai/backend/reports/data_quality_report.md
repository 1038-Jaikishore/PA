# Data Quality Report

### lcd.csv
- 10 duplicate rows found.
### Related_Documents.csv
- 6 duplicate rows found.
### ICD10_Covered_MEJ.csv
- 4 duplicate rows found.
### Article_HCPCS.csv
- 30 duplicate rows found.
### claims.csv
- Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'procedure_code'. Marked as INTERNAL_SYNTHETIC_CODE.
- Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'diagnosis_code'. Marked as INTERNAL_SYNTHETIC_CODE.
### diagnostic_results.csv
- Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'result_id'. Marked as INTERNAL_SYNTHETIC_CODE.
### authorization_requests.csv
- Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'requested_procedure_code'. Marked as INTERNAL_SYNTHETIC_CODE.
- Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'diagnosis_code'. Marked as INTERNAL_SYNTHETIC_CODE.
### encounters.csv
- Internal synthetic codes (DIAGxx/PROCxxxx) found in column 'primary_diagnosis_code'. Marked as INTERNAL_SYNTHETIC_CODE.
