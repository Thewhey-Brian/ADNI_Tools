# ADNI_Tools: Creating Map For ADNI Dataset!
## Introduction
ADNI is a longitudinal multisite study of mild cognitive impairment (MCI) and AD with clinical, imaging, genetic, and biomedical biomarkers. This study was initiated in 2004 and has been extended for 20 years by several phases. The first phase, called ADNI1 (2004-2010), recruited 800 participants, including 200 elderly controls, 400 MCI, and 200 AD. At this phase, brain imaging was measured by structure MRI and PET. The study was extended to phase ADNI-GO in 2009 (2009-2011), where an additional 200 early MCI patients were included. During this phase, the MR protocols were revised. The following phase ADNI2 (2011-2016), recruited additional 550 participants, where 150 were elderly controls, 100 were early MCI, 150 l were ate MCI, and 150 were AD. At the ADNI2 phase, researchers additionally measured amyloid PET with Florbetapir for all ADNI-GO and ADNI2 patients. Next, the ADNI3 (2016-2022) further recruited 133 elderly controls, 151 MCI, and 87 AD participants. During this phase, additional brain scan detecting tau PET was included. The ADNI_Tools provides a convenient way to create a map for the massive dataset, mapping the table names on the website, table names after downloading, variables in each table, and the version/time for each table. 

## Requirements
1. Valid user account for ADNI website.
2. Several Local Inputs:
   - The desired download location (for temperary files and outputs storage).
   - Username of ADNI.
   - Password of ADNI.
3. Required modules in [requirements.txt](https://github.com/Thewhey-Brian/ADNI_Tools/blob/master/requirements.txt).

## Installation
You can use Git to clone the repository from GitHub to install the latest version:
```
git clone https://github.com/Thewhey-Brian/ADNI_Tools.git
cd ADNI_Tools
pip install -r requirements.txt (or pip3 install -r requirements.txt for Python 3)
python3 adni_map.py
```

## Output
A csv file with general dictionary information for ADNI database.
 |      file_label      |          file_name         |    file_version   |         vars           | 
 | -------------------- | -------------------------  | ----------------- | --------------------------- |
 | ADSP Phenotype Harmonization Consortium (PHC) - Composite Cognitive Scores Dictionary [ADNI1,GO,2,3]|ADSP_PHC_COGN_DICT_10_05_22.csv|2022-10-05|['ID', 'FLDNAME', 'TBLNAME', 'CRFNAME', 'QUESTION', 'TEXT', 'STATUS', 'DEPRULE']|
 |ADSP Phenotype Harmonization Consortium (PHC) - Composite Cognitive Scores Methods (PDF)|PDF file skipped|2022-10-05| |
 |ADSP Phenotype Harmonization Consortium (PHC) - Composite Cognitive Scores [ADNI1,GO,2,3]|ADSP_PHC_COGN_10_05_22.csv|2022-10-05|['RID', 'SUBJID', 'PHASE', 'VISCODE', 'VISCODE2', 'EXAMDATE', 'PHC_VISIT', 'PHC_Sex', 'PHC_Education', 'PHC_Ethnicity', 'PHC_Race’]|

## Note:
If your internet connection is unstable, you could break down the full table into several smaller tables (by changing the start and end points of the for loop in [adni_map.py](https://github.com/Thewhey-Brian/ADNI_Tools/blob/master/adni_map.py)).
 
