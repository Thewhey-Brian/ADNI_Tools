# ADNI_MAP: Map for ADNI!
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

## Note:
If your internet connection is unstable, you could break down the full table into several smaller tables (by changing the start and end points of the for loop in [adni_map.py](https://github.com/Thewhey-Brian/ADNI_Tools/blob/master/adni_map.py)).
 
