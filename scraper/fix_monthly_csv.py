import csv
import glob
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

monthly_dir = r"C:\Users\dell\Forex News\scraper\news\monthly"
csv_files = glob.glob(os.path.join(monthly_dir, "*.csv"))

karachi_tz = ZoneInfo("Asia/Karachi")
kolkata_tz = ZoneInfo("Asia/Kolkata")

total_converted = 0

for filepath in csv_files:
    # Read the data
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
        
    changed = False
    for row in rows:
        if row.get("timezone") == "Asia/Karachi":
            date_str = row.get("date", "")
            time_str = row.get("time", "")
            
            if not date_str or not time_str or time_str.lower() in ["all day", "tentative"]:
                row["timezone"] = "Asia/Kolkata"
                changed = True
                continue
                
            try:
                # Parse the time in Karachi timezone
                day, month, year = map(int, date_str.split("/"))
                hour, minute = map(int, time_str.split(":"))
                
                dt_karachi = datetime(year, month, day, hour, minute, tzinfo=karachi_tz)
                
                # Convert to Kolkata timezone
                dt_kolkata = dt_karachi.astimezone(kolkata_tz)
                
                # Update row
                row["date"] = dt_kolkata.strftime("%d/%m/%Y")
                row["day"] = dt_kolkata.strftime("%a")
                row["time"] = dt_kolkata.strftime("%H:%M")
                row["timezone"] = "Asia/Kolkata"
                
                changed = True
                total_converted += 1
            except Exception as e:
                print(f"Error converting {date_str} {time_str}: {e}")
                
    # Write back if changed
    if changed:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
print(f"CSV Conversion complete. Converted {total_converted} events to Asia/Kolkata.")
