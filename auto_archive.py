######################################################################
# IMPORT MODULES
######################################################################

import os
import argparse
import re
import datetime
from pathlib import Path
import shutil

######################################################################
# ARCHIVE FILES
######################################################################

dir_to_archive_help="Specify directory for which the content will be copied to a dated archive subfolder.\
In particular, all files in the diectory specified will be organized by the month and year they were last changed and copied to an \
<directory>/archive/<month>_<year> subdirectory. The code will use existing subdirectories whenever they\
exist."

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("dir_to_archive", help=dir_to_archive_help,
                    type=str)
args = parser.parse_args()
dir_to_archive = args.dir_to_archive

# get all paths in directory specified by user
files_path = [os.path.join(dir_to_archive,x) for x in os.listdir(dir_to_archive)]

# make empty dict to store files by month and year they were last changed
date_files_dict = {}
# loop over file to make dictionary filled with dates and corresponding files
for file in files_path:
    # check if path is file
    if Path(file).is_file():
        # if file get month and year it was last edited
        secs_since_epoch = os.path.getmtime(files_path[0])
        date_str = datetime.datetime.fromtimestamp(secs_since_epoch).strftime('%b%Y').lower()
        # save path to list in dictionary organized by edit date
        if date_str in date_files_dict:
            file_list = date_files_dict[date_str]
            file_list.append(file)
            date_files_dict[date_str] = file_list
        else:
            file_list = [file]
            date_files_dict[date_str] = file_list
date_files_dict

# program which creates a new diectory new_dir in root directory if new_dir does not exist
def create_dir_if_not_exist(path):
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)

# create archive folder if it does not exist
archive_subdir_path = os.path.join(dir_to_archive,'archives')
create_dir_if_not_exist(archive_subdir_path)

# loop over dictionary keys, making archive folders as necessary and copying files to archive
not_archived=[]
archived=[]
for key in date_files_dict:
    month_year_path = os.path.join(archive_subdir_path,key)
    create_dir_if_not_exist(month_year_path)
    for file in date_files_dict[key]:
        # check if file exists in archive already
        file_name = os.path.basename(file)
        new_path = os.path.join(month_year_path,file_name)
        is_exist = os.path.exists(new_path)
        # if yes, skip and add to list to print
        if is_exist:
            not_archived.append(file)
        # if no, copy file to archive
        else:
            archived.append(new_path)
            shutil.copy2(file,month_year_path)

######################################################################
# PRINT SOME DIAGNOSTIC OUTPUT
######################################################################


# print files that were archived
if len(archived)!=0:
    print('The following files were copied to these new locations:')
    for file in archived:
        print(file)
    print('End of list of that were archived. A total of ' + str(len(archived)) + ' files were archived.')
else:
    print('No files were moved to the archives subfolder.')

# print files that were not archived
if len(not_archived)!=0:
    print('The following files already existed in the archives subfolder and were not copied:')
    for file in not_archived:
        print(file)
    print('End of list of files not archived due to already existing in the correct archives subfolder.')
    print('A total of ' + str(len(not_archived)) + ' files were not archived.')
else:
    print('Every file was archived (none were skipped because they already existed in the archives subfolder).')
