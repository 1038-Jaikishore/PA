# Volume 1 Report

## Overview
- CMS datasets: 9 / 9
- Synthea datasets: 21 / 21
- Supplemental aligned datasets: 2 / 2
- Core datasets: 30
- Physical data files: 32

## Discovered Relationships & findings
- CMS relationships discovered matching LCD -> Article -> HCPCS/ICD10 structures.
- Synthea keys like patient_id, encounter_id detected.
- Internal synthetic codes (DIAGxx/PROCxxxx) successfully identified and flagged.
- Normalization functions implemented for ICD10/HCPCS.
- Aligned cases audited for validation without mutating raw structures.
- Raw datasets remain perfectly intact.
