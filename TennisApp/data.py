import urllib
import csv

from bs4 import BeautifulSoup

__author__ = 'pradyumnad'


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
        if (len(parts) > 4):
            field_names.append(parts[2])
            player1[parts[2]] = parts[0] + " | " + parts[1]
            player2[parts[2]] = parts[3] + " | " + parts[4]
        else:
            field_names.append(parts[1])
            player1[parts[1]] = parts[0]
            player2[parts[1]] = parts[2]

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
        parts = div.get_text(" | ", strip=True).split(" | ")
        if (len(parts) > 4):
            field_names.append(parts[2])
        else:
            field_names.append(parts[1])

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

    csvfile = open('data/us_open.csv', 'w')
    field_names = match_field_names('http://www.usopen.org/en_US/scores/stats/day20/1701ms.html')
    print(field_names)
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    csv.writer(csvfile).writerow(field_names)
    for iurl in usopen_urls:
        player1, player2 = extract_match_details(us_url + iurl)
        writer.writerow(player1)
        writer.writerow(player2)


if __name__ == '__main__':
    # extract_match_details('http://www.ausopen.com/en_AU/scores/stats/day19/1701ms.html')
    # extract_match_details('http://www.ausopen.com/en_AU/scores/stats/day18/2701ms.html')
    aus_open()
    us_open()
