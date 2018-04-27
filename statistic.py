import sqlite3
import csv
from collections import OrderedDict
import operator
import matplotlib.pyplot as plt


def plot(counts_sorted, number=10):
    """ plot the pie chart of the frequent visited website """

    plt.figure(1, figsize=(10, 10))
    plt.title('Top $n Sites Visited'.replace('$n', str(number)))
    # the count is sizes, the url is labels
    labels = []
    sizes = []

    count = 0
    for key, value in counts_sorted.items():
        labels.append(key)
        sizes.append(value)
        count += 1
        if count >= number:
            break

    # make the plot, save it and show it
    plt.pie(sizes, autopct='%1.1f%%', labels=labels)
    plt.savefig("statistics.jpg")
    print("The statistics plot is saved as statistics.jpg")
    plt.show()


def parse_url(url):
    """ parse the URL to a readable format """

    try:
        # parse the URL to a better form
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print ("URL format error")


def history_statistics(history_path, BROWSER_TYPE = 0, plot_graph=False, number=10):
    """ output the history statistics of chrome """

    c = sqlite3.connect(history_path, timeout=5)
    cursor = c.cursor()
    # tweaking the sqlite3 query
    if BROWSER_TYPE == 0:
        # chrome
        select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    if BROWSER_TYPE == 1:
        # safari
        select_statement = "SELECT history_items.url, history_items.visit_count FROM history_items, history_visits WHERE history_items.id = history_visits.id;"
    if BROWSER_TYPE == 2:
        # firefox
        select_statement = "SELECT moz_places.url, moz_places.visit_count FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id"

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

    if plot_graph:
        plot(counts_sorted, number)

    print("The statistics of the history is saved in statistics.csv")
