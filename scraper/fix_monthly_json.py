import json
import glob
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

monthly_dir = r"C:\Users\dell\Forex News\scraper\news\monthly"
json_files = glob.glob(os.path.join(monthly_dir, "*.json"))

karachi_tz = ZoneInfo("Asia/Karachi")
kolkata_tz = ZoneInfo("Asia/Kolkata")

total_converted = 0

for filepath in json_files:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    changed = False
    for item in data:
        if item.get("timezone") == "Asia/Karachi":
            date_str = item.get("date")
            time_str = item.get("time")
            
            if not date_str or not time_str or time_str.lower() in ["all day", "tentative"]:
                item["timezone"] = "Asia/Kolkata"
                changed = True
                continue
                
            try:
                # Parse the time in Karachi timezone
                day, month, year = map(int, date_str.split("/"))
                hour, minute = map(int, time_str.split(":"))
                
                dt_karachi = datetime(year, month, day, hour, minute, tzinfo=karachi_tz)
                
                # Convert to Kolkata timezone
                dt_kolkata = dt_karachi.astimezone(kolkata_tz)
                
                # Update item
                item["date"] = dt_kolkata.strftime("%d/%m/%Y")
                item["day"] = dt_kolkata.strftime("%a")
                item["time"] = dt_kolkata.strftime("%H:%M")
                item["timezone"] = "Asia/Kolkata"
                
                changed = True
                total_converted += 1
            except Exception as e:
                print(f"Error converting {date_str} {time_str}: {e}")
                
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
print(f"Conversion complete. Converted {total_converted} events to Asia/Kolkata.")
