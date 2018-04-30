# Browser to suport: chrome, firefox, safari
# Supporting Functionality:
# statistics, history with timestamp filter, keyword filter

import os
from os.path import expanduser
import fnmatch
import sys

from statistic import history_statistics
from list_history import list_history

def find_files(pattern, path):
    """ find the files following specific pattern in path """

    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

#================================================================================
# start of function

#-------------------------------------------------------------------------------
# parsing of the config file to perform the right operation
try:
    s = open("configuration.config","r")
except:
    sys.exit("File 'configuration.config' is missing")

settings = s.readlines()
i = 0
for line in settings:
    settings[i] = line[line.index(":") + 2: -1]
    i+=1

# all the config settings
browser_config = settings[0]
path_config = settings[1]
statistics_config = settings[2]
plot_config = settings[3]
plot_number_config = settings[4]
historylist_config = settings[5]
starttime_config = settings[6]
endtime_config = settings[7]
keywords_config = settings[8]

# put keywords into keywords
keywords_list = []
keywords_list = keywords_config.split(" ")
keywords = []
for item in keywords_list:
    if len(item) > 0:
        keywords.append(item)

#-------------------------------------------------------------------------------
# start the finding of the related history file
BROWSER_TYPE = -1
if browser_config == 'chrome':
    BROWSER_TYPE = 0
elif browser_config == 'safari':
    BROWSER_TYPE = 1
elif browser_config == 'firefox':
    BROWSER_TYPE = 2
else:
    print("Browser not valid")
    sys.exit(70)

home_dir = expanduser(path_config)

find_string = ""
if BROWSER_TYPE == 0:
    find_string = "find " + home_dir + " -type d -iname \"*chrome*\" > dir.txt"

if BROWSER_TYPE == 1:
    find_string = "find " + home_dir + " -type d -iname \"*safari*\" > dir.txt"

if BROWSER_TYPE == 2:
    find_string = "find " + home_dir + " -type d -iname \"*firefox*\" > dir.txt"

print("searching for related path ...")
os.system(find_string)

dir_list = []
f = open('dir.txt', 'r')

for line in f:
    dir_list.append(line.strip())

print(dir_list)

history_pattern = ""
if BROWSER_TYPE == 0:
    # format of chrome history
    history_pattern = '*History'
if BROWSER_TYPE == 1:
    # format of safari history
    history_pattern = '*History.db'
if BROWSER_TYPE == 2:
    # format of firefox history
    history_pattern = '*places.sqlite'


history_list = []
for item in dir_list:
    new_list = find_files(history_pattern, item)
    if len(new_list) > 0:
        for path in new_list:
            history_list.append(path)

if len(history_list) < 1:
    print("no valid history file found")
    sys.exit(0)

print("\n\n")
for i in range(len(history_list)):
    print(str(i+1) + ": " + history_list[i])

chosen = "-1"

try:
    chosen = input(
        "\nplease select the history from the following list to explore: ")
    print(history_list[int(chosen)-1] + " chosen")
except:
    print("\nError: invalid input!")
    sys.exit(0)

# the history pass can be specified here!
# history_path = /path/you/found
history_path = history_list[int(chosen)-1]

#-------------------------------------------------------------------------------
# statistics
if statistics_config == 'true':
    if plot_config == 'true':
        history_statistics(history_path, BROWSER_TYPE, True, int(plot_number_config))
    else:
        history_statistics(history_path, BROWSER_TYPE, False)

# hitory list
if historylist_config == 'true':
    list_history(history_path, BROWSER_TYPE, starttime_config, endtime_config, keywords)
