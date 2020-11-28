###### FSDB IGC

A simple script to take igc files nominated in a FSDB file and rename them with the pilots name. Creates folders for each task with cleanly named trackfiles.
It also creates a zip file for each task. 
The zip file is suitable for bulk uploading to airScore.


Requirements:
- Python 3.6
- lxml (install with 'pip install lxml')

Usage: python fsdb_igc.py /path/to/fsdbfile.fsdb

In the dir where the fsdb file is stored, fsdb_igc will expect to find sub dirs with tracklogs. The sub dir names and tracklog names need to be as they are specified in the fsdb file.
fsdb_igc will create an output dir with zip files in the root and sub dirs (named as above) with the clean tracklog files inside.