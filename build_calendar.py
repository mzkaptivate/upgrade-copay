"""
Zarena's 90-Day Calendar — April 2026 Google Calendar Builder
Week 1 of 90-day cycle.

SETUP:
  1. Go to https://console.cloud.google.com/
  2. Create a project, enable "Google Calendar API"
  3. Create OAuth 2.0 credentials (Desktop app), download as credentials.json
  4. Place credentials.json in this directory
  5. pip install -r requirements.txt
  6. python build_calendar.py

  On first run, a browser window opens for Google sign-in.
  A token.json will be saved so you won't be re-prompted.

FLAGS FOR ZARENA:
  - Saturday gym and yoga OVERLAP (see notes in SATURDAY template below).
    The script creates BOTH blocks but marks them with a note.
    Please confirm which Saturdays are gym-only vs yoga-only.
  - Friday yoga TIME is unconfirmed. Currently set to 8:30–9:00am.
    Please confirm the actual class time.
"""

import datetime
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

CALENDAR_ID = "primary"          # Change to a specific calendar ID if needed
TIMEZONE = "America/Los_Angeles"  # Change to Zarena's timezone

# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# ---------------------------------------------------------------------------
# COLOR IDs (Google Calendar)
# 1=Lavender  2=Sage(green)  3=Grape(purple)  4=Flamingo(pink)
# 5=Banana    6=Tangerine(orange)  7=Peacock(blue)  8=Graphite(gray)
# 9=Blueberry(dark blue)  10=Basil(dark green)  11=Tomato(red)
# ---------------------------------------------------------------------------
COLOR_HEALTH   = "2"   # Sage green  — movement / yoga / gym / pilates / walk
COLOR_ZELLEVON = "9"   # Blueberry   — ZelleVon AI Systems
COLOR_MANIFEST = "4"   # Flamingo    — She Manifest Co.
COLOR_CONTENT  = "6"   # Tangerine   — content filming / posting / editing
COLOR_WRITING  = "3"   # Grape       — writing / journaling / scripts / copy
COLOR_WINDDOWN = "8"   # Graphite    — wind-down ritual / sleep


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
        make_event(date, "07:30", "08:15", "☀️ Wake + Tea",                COLOR_WRITING),
        make_event(date, "08:15", "08:30", "🚗 Travel to Gentle Yoga",     COLOR_HEALTH),
        make_event(date, "08:30", "09:00", "🧘 Gentle Yoga ⚠️ TIME TBC",  COLOR_HEALTH,
                   "⚠️ CONFIRM WITH ZARENA: exact class time still needed. Travel is 15 min each way."),
        make_event(date, "09:00", "09:15", "🚗 Travel Home from Yoga",     COLOR_HEALTH),
        make_event(date, "09:00", "10:00", "🌸 Self-Care + Breakfast"),
        make_event(date, "10:00", "13:00", "📲 Content Posting + Engagement",
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
    """Saturn Day — Soft
    ⚠️ FLAG: Gym (9:30–10:30am) and Yoga Series (10:00–11:15am) overlap.
    Both are included below. Zarena should confirm which applies each Saturday
    or whether they alternate.
    """
    return [
        make_event(date, "08:00", "09:00", "☀️ Wake + Tea"),
        # --- GYM block (confirm with Zarena) ---
        make_event(date, "09:00", "09:30", "🚗 Travel to Gym ⚠️ CONFIRM",  COLOR_HEALTH,
                   "⚠️ CONFIRM WITH ZARENA: Saturday gym and yoga overlap. "
                   "Gym travel 15 min each way. Confirm if gym or yoga (or alternating)."),
        make_event(date, "09:30", "10:30", "🏋️ Gym ⚠️ OVERLAP — CONFIRM",  COLOR_HEALTH,
                   "⚠️ OVERLAP: Yoga Series starts 10:00am. Confirm with Zarena which applies this Saturday."),
        # --- YOGA SERIES block ---
        make_event(date, "09:30", "10:00", "🚗 Travel to Yoga Series ⚠️ CONFIRM", COLOR_HEALTH,
                   "⚠️ CONFIRM WITH ZARENA: 30 min travel to Yoga Series. "
                   "This overlaps with gym block — clarify schedule."),
        make_event(date, "10:00", "11:15", "🧘 Yoga Series ⚠️ OVERLAP — CONFIRM", COLOR_HEALTH,
                   "⚠️ OVERLAP: Gym block runs 9:30–10:30am. Confirm with Zarena."),
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
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("\n❌  credentials.json not found.")
                print("    1. Go to https://console.cloud.google.com/")
                print("    2. Enable Google Calendar API")
                print("    3. Create OAuth 2.0 credentials (Desktop app)")
                print("    4. Download as credentials.json and place it here")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


# ---------------------------------------------------------------------------
# MAIN — build and push all April 2026 events
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Zarena's 90-Day Calendar — April 2026 Builder")
    print("=" * 60)

    # ------------------------------------------------------------------
    # ⚠️  CONFIRMATION WARNINGS printed before pushing
    # ------------------------------------------------------------------
    print("\n⚠️  BEFORE PUSHING — Please confirm with Zarena:")
    print("  1. Saturday schedule: Gym (9:30–10:30am) and Yoga Series")
    print("     (10:00–11:15am) OVERLAP. The script creates both blocks")
    print("     on all 4 Saturdays (Apr 4, 11, 18, 25) and flags them.")
    print("     Update the script once Zarena clarifies the Saturday plan.")
    print()
    print("  2. Friday yoga time is UNCONFIRMED.")
    print("     Currently set to 8:30–9:00am as a placeholder.")
    print("     Update friday_events() once confirmed.")
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
    # Iterate April 1–30, 2026
    # ------------------------------------------------------------------
    total_created = 0
    errors = []

    for day_num in range(1, 31):
        date = datetime.date(2026, 4, day_num)
        weekday = date.weekday()           # 0=Mon … 6=Sun
        template_fn = DAY_TEMPLATES[weekday]
        events = template_fn(date)

        print(f"April {day_num:2d} ({DAY_NAMES[weekday]}) — {len(events)} events", end="")

        day_count = 0
        for event in events:
            try:
                service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
                day_count += 1
            except HttpError as e:
                errors.append(f"  April {day_num} '{event['summary']}': {e}")
                print("✗", end="", flush=True)

        total_created += day_count
        print(f" — {day_count} pushed ✓")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"  ✅  Done! {total_created} events pushed to Google Calendar.")
    if errors:
        print(f"\n  ⚠️  {len(errors)} error(s):")
        for e in errors:
            print(e)
    print()
    print("  Reminders:")
    print("  • Saturday gym/yoga overlap — confirm with Zarena")
    print("  • Friday yoga time — confirm with Zarena")
    print("  • Adjust TIMEZONE in script if needed (currently:", TIMEZONE + ")")
    print("=" * 60)


if __name__ == "__main__":
    main()
