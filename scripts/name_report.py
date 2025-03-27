#!/usr/bin/env python3

import argparse
import curses
import datetime
from pymongo import MongoClient

# Define column positions (adjust as needed)
START_COL = 0
DURATION_COL = 45
NAME_COL = 60
MAX_START_WIDTH = 42
MAX_DURATION_WIDTH = 15

def format_duration(start, end):
    """Return a human-readable duration between two datetime objects."""
    delta = end - start
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    else:
        return f"{minutes}m {seconds}s"

def relative_time(dt):
    """Return a rough relative time string (e.g., 'ago 2d', 'ago 3M', 'ago 1y') for a datetime dt compared to now (UTC)."""
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - dt
    if diff.total_seconds() < 0:
        return "in the future"
    if diff.days >= 365:
        years = diff.days // 365
        return f"ago {years}y"
    elif diff.days >= 30:
        months = diff.days // 30
        return f"ago {months}M"
    elif diff.days >= 1:
        return f"ago {diff.days}d"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"ago {hours}h"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"ago {minutes}m"
    else:
        return f"ago {diff.seconds}s"

def make_aware(dt):
    """Ensure dt is offset-aware (assume UTC if naive)."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt

def main(stdscr, collection):
    curses.curs_set(0)
    current_index = 0

    # Fetch all reports from the collection.
    reports = list(collection.find())
    if not reports:
        stdscr.addstr(0, 0, "No reports found.")
        stdscr.refresh()
        stdscr.getch()
        return

    while True:
        stdscr.clear()
        # Title line
        stdscr.addstr(0, 0, "Game Reports (arrow keys: navigate, Enter: edit name, ESC or q: exit)")

        # Header row with column names
        stdscr.addstr(1, START_COL, "Start Time".ljust(MAX_START_WIDTH))
        stdscr.addstr(1, DURATION_COL, "Duration".ljust(MAX_DURATION_WIDTH))
        stdscr.addstr(1, NAME_COL, "Name")

        # Data rows starting at row 2.
        for idx, report in enumerate(reports):
            row = idx + 2
            try:
                start = report.get("start_time")
                end = report.get("end_time")
                
                if start is None:
                    start_display = "N/A"
                    rel = ""
                else:
                    if isinstance(start, str):
                        start = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
                    else:
                        start = make_aware(start)
                    start_display = start.isoformat()
                    rel = relative_time(start)
                start_str = f"{start_display} ({rel})"
                start_str = start_str[:MAX_START_WIDTH]

                if end is None:
                    duration = "N/A"
                else:
                    if isinstance(end, str):
                        end = datetime.datetime.fromisoformat(end.replace("Z", "+00:00"))
                    else:
                        end = make_aware(end)
                    duration = format_duration(start, end)
                duration_str = duration[:MAX_DURATION_WIDTH]

                name_str = report.get("report_name", "")
            except Exception as e:
                start_str = "Error"
                duration_str = "Error"
                name_str = f"Error: {e}"
            
            attr = curses.A_REVERSE if idx == current_index else curses.A_NORMAL
            stdscr.addstr(row, START_COL, start_str.ljust(MAX_START_WIDTH), attr)
            stdscr.addstr(row, DURATION_COL, duration_str.ljust(MAX_DURATION_WIDTH), attr)
            stdscr.addstr(row, NAME_COL, name_str, attr)
        
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_index = (current_index - 1) % len(reports)
        elif key == curses.KEY_DOWN:
            current_index = (current_index + 1) % len(reports)
        elif key in [27, ord('q')]:  # ESC or q
            break
        elif key in [10, 13]:  # Enter key to edit the report name.
            curses.echo()
            prompt = "Enter new report name: "
            stdscr.addstr(len(reports)+3, 0, prompt)
            stdscr.clrtoeol()
            new_name = stdscr.getstr(len(reports)+3, len(prompt)).decode('utf-8')
            curses.noecho()
            report_to_update = reports[current_index]
            report_to_update["report_name"] = new_name
            collection.update_one({"_id": report_to_update["_id"]}, {"$set": {"report_name": new_name}})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Curses CLI for MongoDB game reports")
    parser.add_argument("ip", nargs="?", default="localhost",
                        help="MongoDB IP address (default: localhost)")
    parser.add_argument("--collection", default="game_report",
                        help="MongoDB collection name (default: game_report)")
    args = parser.parse_args()
    
    mongo_uri = f"mongodb://{args.ip}:27017"
    client = MongoClient(mongo_uri)
    db = client["rcll"]
    collection = db[args.collection]
    
    curses.wrapper(lambda stdscr: main(stdscr, collection))
