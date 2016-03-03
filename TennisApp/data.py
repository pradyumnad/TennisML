import re
import urllib
import csv

from bs4 import BeautifulSoup
import pandas

__author__ = 'pradyumnad'


def normalized(val1, val2):
    if " " in val1:
        parts1 = val1.split(" ")
        parts2 = val2.split(" ")

        if parts1[1] == "MPH" or parts1[1] == "KMH":
            return parts1[0], parts2[0]
        else:
            m1 = re.search('([0-9])+(\s)*%', val1)
            m2 = re.search('([0-9])+(\s)*%', val2)

            tmp1 = int(m1.group(0).strip(" %"))
            tmp2 = int(m2.group(0).strip(" %"))
            return tmp1 / 100.0, tmp2 / 100.0
    else:
        val1_temp = float(val1)
        val2_temp = float(val2)

        val1norm = val1_temp / (val1_temp + val2_temp)
        val2norm = val2_temp / (val1_temp + val2_temp)
        return val1norm, val2norm


def extract_match_details(match_url):
    print(match_url)
    sock = urllib.urlopen(match_url)
    html_lines = sock.readlines()
    match_html = ' '.join(map(str, html_lines))

    soup = BeautifulSoup(match_html, "html.parser")
    summary = soup.find(id='summary')

    match_stats = summary.find(id='match-stats')

    stats_table = match_stats.findAll("div", class_="statsTable")[0]
    # print(stats_table.prettify())

    player1 = {}
    player2 = {}
    field_names = []

    for div in stats_table.find_all(class_=['header', 'row']):
        parts = div.get_text(" | ", strip=True).split(" | ")
        # print(parts, len(parts))
        if len(parts) > 4:
            field_names.append(parts[2])
            player1[parts[2]] = parts[0] + " | " + parts[1]
            player2[parts[2]] = parts[3] + " | " + parts[4]
        else:
            field_names.append(parts[1])
            player1[parts[1]] = parts[0]
            player2[parts[1]] = parts[2]

            if parts[1] != "Stats":
                field_norm = parts[1] + " Norm"
                field_names.append(field_norm)
                val1, val2 = normalized(parts[0], parts[2])
                player1[field_norm] = val1
                player2[field_norm] = val2

    field_names.append("url")
    player1["url"] = match_url
    player2["url"] = match_url

    return player1, player2


def match_field_names(match_url):
    sock = urllib.urlopen(match_url)
    html_lines = sock.readlines()
    match_html = ' '.join(map(str, html_lines))

    # print(match_html)

    soup = BeautifulSoup(match_html, "html.parser")
    summary = soup.find(id='summary')

    match_stats = summary.find(id='match-stats')

    stats_table = match_stats.findAll("div", class_="statsTable")[0]
    # print(stats_table.prettify())

    field_names = []

    for div in stats_table.find_all(class_=['header', 'row']):
        field = ""
        parts = div.get_text(" | ", strip=True).split(" | ")
        if (len(parts) > 4):
            field = parts[2]
        else:
            field = parts[1]
        field_names.append(field)
        if field != "Stats":
            field_names.append(field + " Norm")

    field_names.append("url")

    return field_names


def aus_open():
    aus_url = "http://www.ausopen.com"
    ausopen_urls = ["/en_AU/scores/stats/day19/1701ms.html", "/en_AU/scores/stats/day18/2701ms.html",
                    "/en_AU/scores/stats/day18/3601ms.html", "/en_AU/scores/stats/day17/4601ms.html",
                    "/en_AU/scores/stats/day19/5501ms.html", "/en_AU/scores/stats/day18/21601ms.html",
                    "/en_AU/scores/stats/day18/22601ms.html", "/en_AU/scores/stats/day18/23501ms.html",
                    "/en_AU/scores/stats/day18/24501ms.html", "/en_AU/scores/stats/day18/31301ms.html",
                    "/en_AU/scores/stats/day18/32201ms.html", "/en_AU/scores/stats/day18/33301ms.html",
                    "/en_AU/scores/stats/day18/34201ms.html", "/en_AU/scores/stats/day18/35401ms.html",
                    "/en_AU/scores/stats/day16/36101ms.html", "/en_AU/scores/stats/day18/44401ms.html"]

    csvfile = open('data/au_open.csv', 'w')
    field_names = match_field_names('http://www.ausopen.com/en_AU/scores/stats/day19/1701ms.html')
    print(field_names)
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    csv.writer(csvfile).writerow(field_names)
    for iurl in ausopen_urls:
        player1, player2 = extract_match_details(aus_url + iurl)
        writer.writerow(player1)
        writer.writerow(player2)


def us_open():
    us_url = "http://www.usopen.org"
    usopen_urls = ["/en_US/scores/stats/day20/1701ms.html", "/en_US/scores/stats/day19/2701ms.html",
                   "/en_US/scores/stats/day19/3601ms.html", "/en_US/scores/stats/day20/4601ms.html",
                   "/en_US/scores/stats/day18/5501ms.html", "/en_US/scores/stats/day20/21601ms.html",
                   "/en_US/scores/stats/day20/22601ms.html", "/en_US/scores/stats/day20/23501ms.html",
                   "/en_US/scores/stats/day19/24501ms.html", "/en_US/scores/stats/day20/31301ms.html",
                   "/en_US/scores/stats/day20/32201ms.html", "/en_US/scores/stats/day20/33301ms.html",
                   "/en_US/scores/stats/day20/34201ms.html", "/en_US/scores/stats/day20/35401ms.html",
                   "/en_US/scores/stats/day20/36101ms.html", "/en_US/scores/stats/day20/46201ms.html",
                   "/en_US/scores/stats/day19/51301ms.html", "/en_US/scores/stats/day19/52301ms.html"]

    field_names = match_field_names('http://www.usopen.org/en_US/scores/stats/day20/1701ms.html')
    print(field_names)

    csvfile = open('data/us_open.csv', 'w')
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    csv.writer(csvfile).writerow(field_names)
    for iurl in usopen_urls:
        player1, player2 = extract_match_details(us_url + iurl)
        writer.writerow(player1)
        writer.writerow(player2)

def prepare_data():
    global train, train_target, test, test_target
    df1 = pandas.read_csv("data/us_open_final.csv")
    df2 = pandas.read_csv("data/au_open_final.csv")
    frames = [
        df1[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm', 'Won']],
        df2[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm', 'Won']]
    ]
    df = pandas.concat(frames)
    N = len(df[1:])
    # tennis_data = df[['1st serve points won Norm', '2nd serve points won Norm', 'Break points won Norm', 'Won']]
    print("Total Data : ", N)
    split = int(N * 0.6)
    train = df.sample(n=split)
    train_target = train['Won']
    test = df.drop(train.index)
    test_target = test['Won']
    return train, train_target, test, test_target

if __name__ == '__main__':
    # extract_match_details('http://www.ausopen.com/en_AU/scores/stats/day19/1701ms.html')
    # extract_match_details('http://www.ausopen.com/en_AU/scores/stats/day18/2701ms.html')
    aus_open()
    us_open()
