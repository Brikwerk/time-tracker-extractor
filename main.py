import argparse
from pprint import pprint
import datetime
import json
import time

from clockify import Clockify
from toggl import Toggl
from utils import get_last_friday_or_wednesday, get_iso_timestamp


parser = argparse.ArgumentParser(
    description='Get total times from Clockify or Toggl')
parser.add_argument('--start_time', type=str, default=None,
                    help='Start date in YYYY-MM-DD format. Defaults to today')
parser.add_argument('--end_time', type=str, default=None,
                    help='End date in YYYY-MM-DD format. Defaults to 22/06/21')
parser.add_argument('--token_file', type=str, default='tokens.json',
                    help='Location of JSON file containing API tokens')
parser.add_argument('--csv_file', type=str, default='times.csv',
                    help='Output location of CSV file containing user times')


def get_clockify_times(clockify_tokens: list, intervals: list) -> dict:
    times = {'map': {}}
    for token in clockify_tokens:
        clockify = Clockify(token)
        workspace_ids, workspace_map = clockify.get_workspace_ids()

        times['map'] = {**times['map'], **workspace_map}

        for workspace_id in workspace_ids:
            times[workspace_id] = {}
            for start, end in intervals:
                time.sleep(0.15) # To respect rate-limiting

                start_iso = get_iso_timestamp(start)
                end_iso = get_iso_timestamp(end)

                report = clockify.get_workspace_summary_report(
                    workspace_id, end_iso, start_iso)

                times[workspace_id][start_iso] = {
                    'users': {},
                    'total': report['totals'][0]['totalTime'] / 3600,
                    'interval_end': end_iso
                }
                
                users_report = report['groupOne']
                for user in users_report:
                    name = user['name']
                    duration = user['duration'] / 3600
                    times[workspace_id][start_iso]['users'][name] = duration
    
    return times


def get_toggl_times(toggl_tokens: list, intervals: list) -> dict:
    times = {'map': {}}
    for token in toggl_tokens:
        toggl = Toggl(token)
        workspace_ids, workspace_map = toggl.get_workspace_ids()

        times['map'] = {**times['map'], **workspace_map}

        for workspace_id in workspace_ids:
            times[workspace_id] = {}
            for start, end in intervals:
                time.sleep(0.15) # To respect rate-limiting

                start_iso = get_iso_timestamp(start)
                end_iso = get_iso_timestamp(end)

                report = toggl.get_workspace_summary_report(
                    workspace_id, start_iso, end_iso)

                times[workspace_id][start_iso] = {
                    'users': {},
                    'total': report['total_grand'] / (3600 * 1000),
                    'interval_end': end_iso
                }
                
                users_report = report['data']
                for user in users_report:
                    name = user['title']['user']
                    duration = user['time'] / (3600 * 1000)
                    times[workspace_id][start_iso]['users'][name] = duration
    
    return times


def two_decimals(num: float):
    if type(num) == str:
        return num
    else:
        return f"{num:.2f}"


def times_to_csv(times: dict) -> str:
    csv = ""

    for workspace_id, workspace_data in times.items():
        if workspace_id == 'map': continue

        organized = {
            'Team': times['map'][workspace_id],
            'Times': [],
            'Totals': [],
        }
        for date, date_data in workspace_data.items():
            organized['Totals'].append(date_data['total'])
            organized['Times'].append(date)
            for username, time in date_data['users'].items():
                if username not in organized.keys():
                    organized[username] = [time]
                else:
                    organized[username].append(time)
    
        for key, value in organized.items():
            if type(value) == list:
                csv += f"{key},{','.join(map(two_decimals, value))}\n"
            else:
                csv += f"{key},{value}\n"
        csv += ",\n"
    
    return csv


if __name__ == "__main__":
    args = parser.parse_args()
    
    with open(args.token_file, 'r') as f:
        tokens = json.load(f)

    if args.start_time is None:
        start_time = datetime.datetime.today()
    else:
        start_time = datetime.datetime.strptime(args.start_time, "%Y-%m-%d")
    
    if args.end_time is None:
        end_time = datetime.datetime(2022, 6, 21)
    else:
        end_time = datetime.datetime.strptime(args.end_time, "%Y-%m-%d")

    # Collect all datetime intervals
    intervals = []
    interval_start = start_time
    interval_end = get_last_friday_or_wednesday(
        interval_start - datetime.timedelta(days=1))
    while interval_end > end_time:
        intervals.append((interval_start, interval_end))
        interval_start = interval_end
        interval_end = get_last_friday_or_wednesday(
            interval_start - datetime.timedelta(days=1))
    

    clockify_times = get_clockify_times(tokens['clockify_tokens'], intervals)
    clockify_csv = times_to_csv(clockify_times)

    toggl_times = get_toggl_times(tokens['toggl_tokens'], intervals)
    toggl_csv = times_to_csv(toggl_times)

    csv = clockify_csv + toggl_csv

    with open(args.csv_file, 'w') as f:
        f.write(csv)
