import os
from os import path

"""
Quick check across all folders in current directory for any unfinished downloads.
(i.e. files ending with the '.crdownload' extension)

To run this program:
 1. Place the Python script in the directory
 at the same level as the folders that you would like to check
 2. Run the following command:
 $ python checkcrdl.py

NOTE: This script does not handle nested subdirectories
(working off the assumption that the download/bucketing script ran prior
only creates folders that directly contain all downloaded inspection reports)
"""

def checkcrdl():
    # Assign directory
    directory = os.getcwd()
    total = 0
    dircount = 0
    # Iterate over files in directory
    for name in os.listdir(directory):
        if not os.path.isfile(name):
            dircount += 1
            count = 0
            for fname in os.listdir(name):
                if fname.endswith('.crdownload'):
                    count += 1
            if count > 0:
                print(f"Found {count} unfinished downloads in {name}")
            total += count
    
    print(f"TOTAL: FOUND {total} UNFINISHED DOWNLOADS ACROSS {dircount} FOLDERS")



if __name__ == "__main__":
    checkcrdl()