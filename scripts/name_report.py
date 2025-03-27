#!/usr/bin/env python3
import argparse
import curses
import datetime
from pymongo import MongoClient

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
    """Return a rough relative time string (e.g., 'ago 2d', 'ago 3M', 'ago 1y') compared to now (UTC)."""
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
    """Ensure a datetime is timezone-aware (assume UTC if naive)."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt

def compute_row(report):
    """Convert a MongoDB report into a list of strings for each column."""
    try:
        start = report.get("start_time")
        end = report.get("end_time")
        if start is None:
            start_str = "N/A"
        else:
            if isinstance(start, str):
                start = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
            else:
                start = make_aware(start)
            start_str = start.isoformat() + " (" + relative_time(start) + ")"
        if end is None:
            duration = "N/A"
        else:
            if isinstance(end, str):
                end = datetime.datetime.fromisoformat(end.replace("Z", "+00:00"))
            else:
                end = make_aware(end)
            duration = format_duration(start, end)
        name = report.get("report_name", "")
        return [start_str, duration, name]
    except Exception as e:
        return ["Error", "Error", f"Error: {e}"]

def safe_addstr(win, y, x, s, attr=curses.A_NORMAL):
    """
    Safely add string s at (y, x) in win.
    If x is negative, trim the string.
    If the string exceeds the available width, truncate it.
    """
    max_y, max_x = win.getmaxyx()
    if y < 0 or y >= max_y:
        return
    if x < 0:
        s = s[-x:]
        x = 0
    if x + len(s) > max_x:
        s = s[:max_x - x]
    try:
        win.addstr(y, x, s, attr)
    except curses.error:
        pass

def display_table(stdscr, titles, rows, reports, collection):
    """
    Display a table with headers and rows.
    Supports vertical and horizontal scrolling.
    Press Enter to edit the "Name" field of the selected row.
    """
    curses.curs_set(0)
    current_row = 0
    scroll_x = 0

    def calculate_column_widths():
        cols = list(zip(*([titles] + rows)))
        widths = [max(len(str(item)) for item in col) + 2 for col in cols]
        return widths

    def draw_table():
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        col_widths = calculate_column_widths()
        total_width = sum(col_widths)

        # Draw header in row 0 with horizontal scrolling.
        x_pos = -scroll_x
        for title, width in zip(titles, col_widths):
            safe_addstr(stdscr, 0, x_pos, title.center(width), curses.A_REVERSE)
            x_pos += width

        # Determine vertical visible rows (header occupies row 0).
        visible_rows = max_y - 1
        start_index = 0 if current_row < visible_rows else current_row - visible_rows + 1

        for i in range(start_index, min(len(rows), start_index + visible_rows)):
            row_data = rows[i]
            x_pos = -scroll_x
            attr = curses.A_REVERSE if i == current_row else curses.A_NORMAL
            for cell, width in zip(row_data, col_widths):
                safe_addstr(stdscr, i - start_index + 1, x_pos, str(cell).center(width), attr)
                x_pos += width

        stdscr.refresh()

    while True:
        draw_table()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(rows) - 1:
            current_row += 1
        elif key == curses.KEY_LEFT and scroll_x > 0:
            scroll_x = max(0, scroll_x - 10)
        elif key == curses.KEY_RIGHT:
            _, max_x = stdscr.getmaxyx()
            total_width = sum(calculate_column_widths())
            if scroll_x < total_width - max_x:
                scroll_x += 10
        elif key in [10, 13]:  # Enter key to edit "Name"
            curses.echo()
            max_y, _ = stdscr.getmaxyx()
            prompt = "Enter new report name: "
            safe_addstr(stdscr, max_y - 1, 0, prompt)
            stdscr.clrtoeol()
            new_name = stdscr.getstr(max_y - 1, len(prompt)).decode('utf-8')
            curses.noecho()
            report = reports[current_row]
            report["report_name"] = new_name
            collection.update_one({"_id": report["_id"]}, {"$set": {"report_name": new_name}})
            rows[current_row][2] = new_name
        elif key == 27:  # ESC key
            break

def main(stdscr, collection):
    reports = list(collection.find())
    if not reports:
        safe_addstr(stdscr, 0, 0, "No reports found. Press any key.")
        stdscr.getch()
        return
    rows = [compute_row(r) for r in reports]
    titles = ["Start Time", "Duration", "Name"]
    display_table(stdscr, titles, rows, reports, collection)

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
    
    curses.wrapper(main, collection)
