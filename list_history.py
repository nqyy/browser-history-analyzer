import sqlite3
import csv
import datetime
import sys


def find_keyword(URL, title, keywords):
    """ find keyword helper function of history_list """

    for keyword in keywords:
        # case insensitive
        if len(keyword) > 0 and (URL is not None and keyword.lower() in URL.lower()) or (title is not None and keyword.lower() in title.lower()):
            return True
    return False


def list_history(history_path, BROWSER_TYPE=0, start_time="", end_time="", keywords=[]):
    """ list history in chrome """

    c = sqlite3.connect(history_path, timeout=5)
    cursor = c.cursor()

    # tweaking the sqlite3 query
    if BROWSER_TYPE == 0:
        # CHROME
        statement = "SELECT datetime(last_visit_time/1000000-11644473600, \"unixepoch\") as last_visited, url , title FROM urls;"
    if BROWSER_TYPE == 1:
        # SAFARI
        statement = "SELECT datetime(hv.visit_time + 978307200, 'unixepoch', 'localtime') as last_visited, hi.url, hv.title FROM history_visits hv, history_items hi WHERE hv.history_item = hi.id;"
    if BROWSER_TYPE == 2:
        # FIREFOX
        statement = "SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url, moz_places.title FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id;"

    result = cursor.execute(statement)

    csv_file = 'history.csv'

    # deal with the time filter
    try:
        if len(start_time) > 0:
            if (len(start_time) == 10):
                start_timestamp = datetime.datetime.strptime(
                    start_time, "%Y-%m-%d")
            elif (len(start_time) == 19):
                start_timestamp = datetime.datetime.strptime(
                    start_time, "%Y-%m-%d %H:%M:%S")
            else:
                raise Exception
        if len(end_time) > 0:
            if (len(end_time) == 10):
                end_timestamp = datetime.datetime.strptime(
                    end_time, "%Y-%m-%d")
            elif (len(end_time) == 19):
                end_timestamp = datetime.datetime.strptime(
                    end_time, "%Y-%m-%d %H:%M:%S")
            else:
                raise Exception
        if len(start_time) > 0 and len(end_time) > 0:
            if start_timestamp > end_timestamp:
                print("start time cannot be after end time")
                exit(0)
    except:
        print("Input timestamp Error!\nPlease follow format yy-mm-dd (HH:MM:SS)")
        sys.exit(0)

    list_of_tuples = []

    for row in result:
        timestamp = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        URL = row[1]
        title = row[2]

        # deal with keyword filter
        if len(keywords) > 0 and find_keyword(URL, title, keywords) == False:
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
            list_of_tuples.append([str(timestamp), URL, title])
        else:
            list_of_tuples.append(["", URL, title])

    # sort the histories by time
    list_of_tuples.sort(key=lambda tup: tup[0], reverse=True)

    try:
        with open(csv_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Last visit", "URL", "Title"])

            for item in list_of_tuples:
                writer.writerow(item)
    except:
        print("I/O error: ", csv_file)

    print("The history list is saved in history.csv")
