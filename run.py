# Browser to suport: chrome, firefox, safari
# Functionality to support: statistics, history with timestamp filter, keyword filter


import os
from os.path import expanduser
import fnmatch
import sys
import sqlite3
import matplotlib.pyplot as plt

import operator
from collections import OrderedDict
import csv
import datetime

def find_files(pattern, path):
    """ find the files following specific pattern in path """

    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def parse_url(url):
    """ parse the URL to a readable format """

    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print ("URL format error")


def history_statistics(history_path):
    """ output the history statistics of chrome """

    c = sqlite3.connect(history_path, timeout=5)
    cursor = c.cursor()
    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)

    results = cursor.fetchall()

    # deal with URL counts
    counts = {}
    for url, count in results:
        url = parse_url(url)
        if url in counts:
            counts[url] += 1
        else:
            counts[url] = 1

    counts_sorted = OrderedDict(
        sorted(counts.items(), key=operator.itemgetter(1), reverse=True))

    # output the result to the csv file
    csv_file = 'statistics.csv'
    try:
        with open(csv_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Website", "Counts"])
            for key, value in counts_sorted.items():
                count = str(value)
                writer.writerow([key, count])
    except:
        print("I/O error: ", csv_file)

    print("The statistics of the history is saved in statistics.csv")


def history_list(history_path, start_time = "", end_time = "", keyword = ""):
    """ list history in chrome """

    c = sqlite3.connect(history_path, timeout=5)
    cursor = c.cursor()
    statement = "SELECT datetime(last_visit_time/1000000-11644473600, \"unixepoch\") as last_visited, url , title FROM urls;"
    result = cursor.execute(statement)

    csv_file = 'history.csv'

    # deal with the time filter
    try:
        if len(start_time) > 0:
            if (len(start_time) == 10):
                start_timestamp = datetime.datetime.strptime(start_time, "%Y-%m-%d")
            elif (len(start_time) == 19):
                start_timestamp = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            else:
                raise Exception
        if len(end_time) > 0:
            if (len(end_time) == 10):
                end_timestamp = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            elif (len(end_time) == 19):
                end_timestamp = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            else:
                raise Exception
        if len(start_time) > 0 and len(end_time) > 0:
            if start_timestamp > end_timestamp:
                print("start time cannot be after end time")
                exit(0)
    except:
        print("Input timestamp Error!\nPlease follow format yy-mm-dd (HH:MM:SS)")
        sys.exit(0)

    # output the result to the csv file
    # try:
    with open(csv_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Last visit", "URL", "Title"])
        for row in result:
            timestamp = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            URL = row[1]
            title = row[2]

            # deal with keyword filter
            if len(keyword) > 0:
                # case insensitive
                if keyword.lower() not in URL.lower() and keyword.lower() not in title.lower():
                    continue

            # deal with time stamp filter
            if len(start_time) > 0:
                if timestamp < start_timestamp:
                    continue
            if len(end_time) > 0:
                if timestamp > end_timestamp:
                    continue

            # output the result to the csv file
            # deal with some 1601-01-01 00:00:00 issue
            if timestamp != datetime.datetime.strptime("1601-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"):
                writer.writerow([str(timestamp), URL, title])
            else:
                writer.writerow(["", URL, title])
    # except:
    #     print("I/O error: ", csv_file)

    print("The history list is saved in history.csv")

#================================================================================
# start of function


# home_dir = expanduser("~")
# find_string = "find " + home_dir + " -type d -iname \"*chrome*\" > dir.txt"
# print("searching for related path ...")
# os.system(find_string)

# dir_list = []
# f = open('dir.txt', 'r')

# for line in f:
#     dir_list.append(line.strip())

# # print(dir_list)
# history_list = []
# for item in dir_list:
#     new_list = find_files('*History', item)
#     if len(new_list) > 0:
#         for path in new_list:
#             history_list.append(path)

# if len(history_list) < 1:
#     print("no valid chrome history found")
#     sys.exit(0)
# print("\n\n")
# for i in range(len(history_list)):
#     print(str(i+1) + ": " + history_list[i])

# chosen = "-1"

# try:
#     chosen = input(
#         "\nplease select the history from the following list to explore: ")
#     print(history_list[int(chosen)-1] + " chosen")
# except:
#     print("\nError: invalid input!")
#     sys.exit(0)

# history_path = history_list[int(chosen)-1]

history_path = "/Users/tchi/Library/Application Support/Google/Chrome/Profile 2/History"

# history_statistics(history_path)
history_list(history_path)
