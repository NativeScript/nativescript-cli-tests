import csv
import json
import os
import urllib2

URL = 'http://plugins.nativescript.org/api/getPlugins/all'
RAW_CSV_PATH = os.path.join('verified_plugins', 'data', 'plugins_raw.csv')
CSV_PATH = os.path.join('verified_plugins', 'data', 'plugins.csv')
CSV_PATH_NO_DEMOS = os.path.join('verified_plugins', 'data', 'plugins_no_demos.csv')


def csv_writer(data, path):
    """
    Write data to a CSV file path
    :param data: DAta to write.
    :param path: File path.
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            try:
                writer.writerow(line)
            except:
                print 'Failed to write line: '
                print line


def generate_raw_csv():
    summary = []
    response = urllib2.urlopen(URL)
    data = json.load(response)
    for plugin in data:
        id = plugin.get('id')
        name = plugin.get('name')
        repo = plugin.get('repo_url')
        if repo is not None:
            repo = 'https://github.com/' + plugin.get('repo_url')
        author = plugin.get('author').get('name')
        details_url = 'http://plugins.nativescript.org/api/getPlugin/' + id
        details_response = urllib2.urlopen(details_url)
        details = json.load(details_response)[0]
        os_support = details.get('os_support')
        android_support = False
        ios_support = False
        if os_support.get('android') is True:
            android_support = True
        if os_support.get('ios') is True:
            ios_support = True
        npm_downloads = details.get('npm_downloads')
        git_stars = details.get('git_stars')
        demo_url_raw = details.get('demo_url')
        if demo_url_raw is None:
            demo_url = ''
            if repo is not None:
                demo_url = repo + '/tree/master/demo'
                try:
                    urllib2.urlopen(demo_url).code
                except urllib2.HTTPError:
                    demo_url = ''
        elif '/master/demo' in demo_url_raw:
            demo_url = demo_url_raw.replace('/master/demo', '/tree/master/demo')
            try:
                urllib2.urlopen(demo_url).code
            except urllib2.HTTPError:
                demo_url = ''
        if demo_url is '':
            if repo is not None:
                demo_url = repo + '-demo'
                try:
                    urllib2.urlopen(demo_url).code
                except urllib2.HTTPError:
                    demo_url = ''

        try:
            if demo_url == '':
                print '[ERROR] Demo repo not found for ' + name
            else:
                print '[INFO] Demo app for {0} is available at {1}'.format(name, demo_url)
            raw = [name, repo, author, android_support, ios_support, npm_downloads, git_stars, demo_url]
            summary.append(raw)
        except:
            print 'Failed to get data for {0}'.format(name)

    summary.sort(key=lambda x: x[5], reverse=True)
    csv_writer(summary, RAW_CSV_PATH)


def generate_csv():
    verified = []
    no_demos = []
    raw_data = csv.reader(open(RAW_CSV_PATH, 'rb'), delimiter=',')
    for line in raw_data:
        if line[7] is not '':
            verified.append(line)
        else:
            no_demos.append(line)

    csv_writer(verified, CSV_PATH)
    csv_writer(no_demos, CSV_PATH_NO_DEMOS)


if __name__ == '__main__':
    generate_raw_csv()
    generate_csv()
