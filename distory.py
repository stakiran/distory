# -*- coding: utf-8 -*-

import csv
import datetime
import os
import sys
import time

def abort(msg):
    print('Error!: {0}'.format(msg))
    exit(1)

def list2file(filepath, ls):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.writelines(['{:}\n'.format(line) for line in ls] )

def dtstr2dt(dtstr):
    """ @param A YYMMDD string. """
    return datetime.datetime(int('20'+dtstr[0:2]), int(dtstr[2:4]), int(dtstr[4:6]))

def dt2unixtime_micro(dt):
    unixtime_second = time.mktime(dt.timetuple())
    unixtime_micro_str = '{}000000'.format(int(unixtime_second))
    unixtime_micro = int(unixtime_micro_str)
    return unixtime_micro

def unixtime_micro_str2dt(unixtime_micro_str):
    unixtime_second = int(unixtime_micro_str[:-6])
    dt = datetime.datetime.fromtimestamp(unixtime_second)
    return dt

def walk_dt(dt, days):
    """ @return A new dt object with walked +n days. """
    return dt + datetime.timedelta(days=days)

def dt2japanese_readable(dt):
    weekdays = ['月','火','水','木','金','土','日']
    idx = dt.weekday()
    wdstr = weekdays[idx]

    datestr = dt.strftime("%Y/%m/%d")
    timestr = dt.strftime("%H:%M:%S")

    ret = '{:}({:}) {:}'.format(datestr, wdstr, timestr)
    return ret

def dt2japanese_readable_without_time(dt):
    dtstr = dt2japanese_readable(dt)
    unneed_tail_length = len(' hh:mm:ss')
    return dtstr[:-1*unneed_tail_length]

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-p', '--profile-name', type=str, default=None, required=True,
        help='Your firefox profile name. (Ex: XXXXXX.Username)')

    parser.add_argument('-d', '--date', type=str, default=None, required=True,
        help='A date you want to extract on. (Ex: 190214)')

    parser.add_argument('--md', default=False, action='store_true',
        help='If given, convert (DATE).csv to (DATE).md.')

    parser.add_argument('--bookmark', default=False, action='store_true',
        help='If given, export bookmark with dateAdded based instead of history with last_visit_date based.')

    parser.add_argument('--debug', default=False, action='store_true',
        help='If given, show the commandline only. This option is invalid in no --md.')

    args = parser.parse_args()
    return args

COMMANDLINE_EXPORT_HISTORY = 'sqlite3 -readonly -csv "%appdata%\\Mozilla\\Firefox\\Profiles\\{profile_name}\\places.sqlite" "SELECT title,url,last_visit_date FROM moz_places WHERE last_visit_date BETWEEN {range_start} AND {range_end};" > {target_datestr}.csv'
COMMANDLINE_EXPORT_BOOKMARK = 'sqlite3 -readonly -csv "%appdata%\\Mozilla\\Firefox\\Profiles\\{profile_name}\\places.sqlite" "SELECT moz_bookmarks.title, moz_places.url, moz_bookmarks.dateAdded FROM moz_bookmarks INNER JOIN moz_places ON moz_bookmarks.fk = moz_places.id WHERE moz_bookmarks.dateAdded BETWEEN {range_start} AND {range_end};" > {target_datestr}_bookmark.csv'

args = parse_arguments()

profile_name = args.profile_name

dtstr = args.date
dt_start = dtstr2dt(dtstr)
dt_end = walk_dt(dt_start, days=1)

ut_start = dt2unixtime_micro(dt_start)
ut_end = dt2unixtime_micro(dt_end)

if not(args.md):
    commandline_template = COMMANDLINE_EXPORT_HISTORY
    if args.bookmark:
        commandline_template = COMMANDLINE_EXPORT_BOOKMARK

    commandline_params = {
        'profile_name' : profile_name,
        'range_start' : ut_start,
        'range_end' : ut_end,
        'target_datestr' : dtstr,
    }
    commandline = commandline_template.format(**commandline_params)

    print(commandline)
    if args.debug:
        exit(0)
    returncode = os.system(commandline)
    exit(returncode)

target_filename = '{}.csv'.format(dtstr)
output_filename = '{}.md'.format(dtstr)
if args.bookmark:
    target_filename = '{}_bookmark.csv'.format(dtstr)
    output_filename = '{}_bookmark.md'.format(dtstr)

# Create csv_lines with csv lib because easy handling of "comma in element".
# csv_lines = [
#     ['element1','element2',...],
#     ['element1','element2',...],
#     ...
# ]
csv_lines = []
with open(target_filename, encoding='utf8', mode='r') as f:
    for row in csv.reader(f):
        csv_lines.append(row)

# Convert csv_lines to md_lines.
md_lines = []
historycount = 0
for i,csv_line_with_list in enumerate(csv_lines):
    historycount = i+1

    title, url, unixtime_micro_str = csv_line_with_list
    dt = unixtime_micro_str2dt(unixtime_micro_str)
    dtstr_readable = dt2japanese_readable(dt)

    # Completion title of specific urls
    if len(title)==0:
        title = '<<< Untitled >>>'

    md_line = '- {} [{}]({})'.format(
        dtstr_readable, title, url
    )

    md_lines.append(md_line)

caption = dt2japanese_readable_without_time(dtstr2dt(dtstr))
md_lines.insert(0, '# {} {} counts'.format(caption, historycount))
list2file(output_filename, md_lines)
