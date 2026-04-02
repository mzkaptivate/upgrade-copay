"""
Zarena's 90-Day Calendar — Google Calendar Builder
April 1 – June 29, 2026  (90 days, Week 1 of cycle)

SETUP:
  1. Place service_account.json in this directory
  2. Share your Google Calendar with the service account email
  3. pip3 install -r requirements.txt
  4. python3 build_calendar.py
"""

import datetime
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

CALENDAR_ID = "mattiewhitfield@gmail.com"
TIMEZONE = "America/Chicago"      # Central Time

SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# ---------------------------------------------------------------------------
# COLOR IDs (Google Calendar)
# 1=Lavender  2=Sage(green)  3=Grape(purple)  4=Flamingo(pink)
# 5=Banana    6=Tangerine(orange)  7=Peacock(blue)  8=Graphite(gray)
# 9=Blueberry(dark blue)  10=Basil(dark green)  11=Tomato(red)
# ---------------------------------------------------------------------------
COLOR_HEALTH   = "4"   # Flamingo (fuschia)  — movement / yoga / gym / pilates / walk
COLOR_ZELLEVON = "9"   # Blueberry           — ZelleVon AI Systems
COLOR_MANIFEST = "2"   # Sage (green)        — She Manifest Co. (money activities)
COLOR_CONTENT  = "6"   # Tangerine (orange)  — content filming / posting / editing
COLOR_WRITING  = "1"   # Lavender            — writing / journaling / scripts / copy
COLOR_WINDDOWN = "5"   # Banana (yellow)     — wind-down ritual / sleep


# ---------------------------------------------------------------------------
# HELPER — build an event dict
# ---------------------------------------------------------------------------

def make_event(date: datetime.date, start_time: str, end_time: str,
               title: str, color_id: str = None, description: str = ""):
    """
    date       : datetime.date object
    start_time : "HH:MM"  (24-hour)
    end_time   : "HH:MM"  (24-hour)
    """
    start_dt = f"{date.isoformat()}T{start_time}:00"
    end_dt   = f"{date.isoformat()}T{end_time}:00"

    event = {
        "summary": title,
        "start":   {"dateTime": start_dt, "timeZone": TIMEZONE},
        "end":     {"dateTime": end_dt,   "timeZone": TIMEZONE},
    }
    if description:
        event["description"] = description
    if color_id:
        event["colorId"] = color_id
    return event


# ---------------------------------------------------------------------------
# DAILY TEMPLATES — each returns a list of event dicts for a given date
# ---------------------------------------------------------------------------

def monday_events(date: datetime.date):
    """Moon Day — Light/Reset"""
    return [
        make_event(date, "07:30", "08:45", "🚗 Travel to Yoga",           COLOR_HEALTH),
        make_event(date, "09:00", "10:00", "🧘 Yoga Class",               COLOR_HEALTH),
        make_event(date, "10:00", "10:15", "🚗 Travel Home from Yoga",    COLOR_HEALTH),
        make_event(date, "10:15", "13:00", "🏠 Home Reset + Cleaning"),
        make_event(date, "13:00", "14:00", "🥗 Lunch + Reset"),
        make_event(date, "14:00", "17:00", "✨ Soft Life Block — Errands / Self-Care / Walk"),
        make_event(date, "18:00", "19:30", "🍽️ Dinner"),
        make_event(date, "19:00", "21:00", "✍️ Content Writing — Scripts / Captions / Copy / Blogs",
                   COLOR_WRITING,
                   "Faceless Pages content writing block"),
        make_event(date, "21:00", "22:30", "🌙 Wind-Down Ritual",          COLOR_WINDDOWN),
        make_event(date, "22:30", "23:00", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


def tuesday_events(date: datetime.date):
    """Mars Day — Heavy"""
    return [
        make_event(date, "07:30", "08:15", "☀️ Wake + Tea + Journal",      COLOR_WRITING),
        make_event(date, "08:15", "08:30", "🚗 Travel to Gym",             COLOR_HEALTH),
        make_event(date, "08:30", "09:00", "🏋️ Gym",                      COLOR_HEALTH),
        make_event(date, "09:00", "09:15", "🚗 Travel Home from Gym",      COLOR_HEALTH),
        make_event(date, "09:15", "09:45", "🚿 Get Ready + Breakfast"),
        make_event(date, "09:45", "10:00", "📋 Light Admin"),
        make_event(date, "10:00", "13:00", "💻 ZelleVon AI Systems — Work Block 1",
                   COLOR_ZELLEVON,
                   "Pomodoro 25/5 · 6 sprints · ZelleVon AI Systems"),
        make_event(date, "13:00", "14:00", "🥗 Lunch + Reset"),
        make_event(date, "14:00", "17:00", "✍️ Content Writing — Work Block 2",
                   COLOR_WRITING,
                   "Scripts, captions, copy, blogs — Faceless Pages"),
        make_event(date, "17:00", "18:00", "🚶 Walk",                      COLOR_HEALTH),
        make_event(date, "18:30", "19:45", "🍽️ Dinner"),
        make_event(date, "20:00", "21:00", "📓 Journaling",                COLOR_WRITING),
        make_event(date, "21:00", "22:30", "🌙 Wind-Down Ritual",          COLOR_WINDDOWN),
        make_event(date, "22:30", "23:00", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


def wednesday_events(date: datetime.date):
    """Mercury Day — Heavy / Filming"""
    return [
        make_event(date, "07:30", "08:30", "☀️ Wake + Tea + Journal",      COLOR_WRITING),
        make_event(date, "08:30", "10:30", "🎥 Beauty Prep + Filming — Get Ready Content",
                   COLOR_CONTENT,
                   "On-camera get-ready content for all platforms"),
        make_event(date, "10:30", "11:00", "🍳 Breakfast"),
        make_event(date, "11:00", "13:00", "🎬 Main Filming Block — Primary Content",
                   COLOR_CONTENT,
                   "Primary content for all platforms"),
        make_event(date, "13:00", "14:00", "🥗 Lunch + Reset"),
        make_event(date, "14:00", "17:00", "🎞️ Afternoon Filming + Editing — B-Roll / Review / Light Edit",
                   COLOR_CONTENT,
                   "B-roll, review, light edit"),
        make_event(date, "17:00", "18:00", "🚶 Walk",                      COLOR_HEALTH),
        make_event(date, "18:00", "19:00", "🍽️ Early Dinner"),
        make_event(date, "19:00", "21:00", "💜 Healing Block"),
        make_event(date, "21:00", "22:30", "🌙 Wind-Down",                 COLOR_WINDDOWN),
        make_event(date, "22:30", "23:00", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


def thursday_events(date: datetime.date):
    """Jupiter Day — Heavy (Pilates shift)"""
    return [
        make_event(date, "07:30", "08:30", "☀️ Wake + Tea + Journal",      COLOR_WRITING),
        make_event(date, "09:00", "09:30", "🚗 Travel to Reformer Pilates", COLOR_HEALTH),
        make_event(date, "09:30", "10:30", "🧘 Reformer Pilates Class",    COLOR_HEALTH),
        make_event(date, "10:30", "11:00", "🚗 Travel Home from Pilates",  COLOR_HEALTH),
        make_event(date, "11:00", "11:30", "🚿 Get Ready + Breakfast + Light Admin"),
        make_event(date, "11:30", "14:00", "🌙 She Manifest Co. — Work Block 1",
                   COLOR_MANIFEST,
                   "Pomodoro 25/5 · Spiritual content, teaching, moon circle content"),
        make_event(date, "14:00", "15:00", "🥗 Lunch + Reset"),
        make_event(date, "15:00", "18:00", "🎞️ Deep Video Editing — Work Block 2",
                   COLOR_CONTENT,
                   "Deep video editing session"),
        make_event(date, "18:30", "19:45", "🍽️ Dinner"),
        make_event(date, "20:00", "21:00", "📓 Journaling",                COLOR_WRITING),
        make_event(date, "21:00", "22:30", "🌙 Wind-Down Ritual",          COLOR_WINDDOWN),
        make_event(date, "22:30", "23:00", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


def friday_events(date: datetime.date):
    """Venus Day — Light / Posting"""
    return [
        make_event(date, "07:30", "08:45", "☀️ Wake + Tea",                COLOR_WRITING),
        make_event(date, "08:45", "09:00", "🚗 Travel to Gym",             COLOR_HEALTH),
        make_event(date, "09:00", "10:00", "🏋️ Gym",                      COLOR_HEALTH),
        make_event(date, "10:00", "10:15", "🚗 Travel Home from Gym",      COLOR_HEALTH),
        make_event(date, "10:15", "11:00", "🌸 Self-Care + Breakfast"),
        make_event(date, "11:00", "13:00", "📲 Content Posting + Engagement",
                   COLOR_CONTENT,
                   "Schedule, publish, community engagement — all platforms"),
        make_event(date, "13:00", "14:00", "🥗 Lunch"),
        make_event(date, "14:00", "15:00", "📖 Rest + Journal",            COLOR_WRITING),
        make_event(date, "15:00", "17:00", "💬 Respond + Engage — Comments / DMs / Analytics",
                   COLOR_CONTENT),
        make_event(date, "18:00", "19:00", "🍽️ Early Dinner"),
        make_event(date, "19:00", "21:00", "💜 Healing Block"),
        make_event(date, "21:00", "22:30", "🌙 Wind-Down",                 COLOR_WINDDOWN),
        make_event(date, "22:30", "23:00", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


def saturday_events(date: datetime.date):
    """Saturn Day — Soft"""
    return [
        make_event(date, "08:00", "09:00", "☀️ Wake + Tea"),
        make_event(date, "09:30", "10:00", "🚗 Travel to Yoga Series",     COLOR_HEALTH),
        make_event(date, "10:00", "11:15", "🧘 Yoga Series",               COLOR_HEALTH),
        make_event(date, "11:15", "11:45", "🚗 Travel Home from Yoga",     COLOR_HEALTH),
        make_event(date, "12:00", "14:00", "🛒 Lunch + Errands"),
        make_event(date, "15:00", "17:00", "🌿 Nature + Family"),
        make_event(date, "18:00", "19:30", "🍽️ Dinner"),
        make_event(date, "20:00", "22:00", "📖 Relax + Journal",           COLOR_WRITING),
        make_event(date, "22:30", "23:00", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


def sunday_events(date: datetime.date):
    """Sun Day — Vision"""
    return [
        make_event(date, "08:00", "09:00", "🌅 Morning Reflection"),
        make_event(date, "09:00", "10:00", "🧘 Yoga + Meditation",         COLOR_HEALTH),
        make_event(date, "10:00", "12:00", "📋 Weekly Planning + Vision"),
        make_event(date, "12:00", "13:00", "🥗 Lunch"),
        make_event(date, "13:00", "15:00", "🎨 Creative + Vision Work"),
        make_event(date, "15:00", "17:00", "📦 Prep + Organize"),
        make_event(date, "17:00", "18:00", "🚶 Walk",                      COLOR_HEALTH),
        make_event(date, "18:00", "19:00", "🍽️ Dinner"),
        make_event(date, "20:00", "21:30", "🌙 Reflection Ritual"),
        make_event(date, "22:00", "22:30", "😴 Sleep",                     COLOR_WINDDOWN),
    ]


# ---------------------------------------------------------------------------
# MAP weekday → template function
# ---------------------------------------------------------------------------

DAY_TEMPLATES = {
    0: monday_events,
    1: tuesday_events,
    2: wednesday_events,
    3: thursday_events,
    4: friday_events,
    5: saturday_events,
    6: sunday_events,
}

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ---------------------------------------------------------------------------
# GOOGLE CALENDAR AUTH
# ---------------------------------------------------------------------------

def get_calendar_service():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"\n❌  {SERVICE_ACCOUNT_FILE} not found.")
        print("    Place your service_account.json file in this folder.")
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("calendar", "v3", credentials=creds)


# ---------------------------------------------------------------------------
# MAIN — build and push 90 days: April 1 – June 29, 2026
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Zarena's 90-Day Calendar — Apr 1 – Jun 29, 2026")
    print("=" * 60)

    # ------------------------------------------------------------------
    # ⚠️  CONFIRMATION WARNINGS printed before pushing
    # ------------------------------------------------------------------
    print("\nSchedule: Saturday Yoga Series + Friday Gym confirmed.")
    print("Timezone: Central (America/Chicago)")
    print()
    answer = input("Type YES to continue pushing to Google Calendar, or NO to exit: ").strip().upper()
    if answer != "YES":
        print("Exiting. No events were created.")
        sys.exit(0)

    # ------------------------------------------------------------------
    # Connect
    # ------------------------------------------------------------------
    print("\nConnecting to Google Calendar...")
    service = get_calendar_service()
    print("Connected.\n")

    # ------------------------------------------------------------------
    # Iterate 90 days: April 1 – June 29, 2026
    # ------------------------------------------------------------------
    start_date = datetime.date(2026, 4, 1)
    total_created = 0
    errors = []

    for offset in range(90):
        date = start_date + datetime.timedelta(days=offset)
        weekday = date.weekday()           # 0=Mon … 6=Sun
        template_fn = DAY_TEMPLATES[weekday]
        events = template_fn(date)

        label = date.strftime("%b %d")
        print(f"{label} ({DAY_NAMES[weekday]:<9}) — {len(events)} events", end="")

        day_count = 0
        for event in events:
            try:
                service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
                day_count += 1
            except HttpError as e:
                errors.append(f"  {label} '{event['summary']}': {e}")
                print("✗", end="", flush=True)

        total_created += day_count
        print(f" — {day_count} pushed ✓")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"  ✅  Done! {total_created} events pushed to Google Calendar.")
    print(f"       90-day cycle: April 1 – June 29, 2026")
    if errors:
        print(f"\n  ⚠️  {len(errors)} error(s):")
        for e in errors:
            print(e)
    print("=" * 60)


if __name__ == "__main__":
    main()
