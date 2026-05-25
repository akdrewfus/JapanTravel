import json

path = r'C:\Users\ak\OneDrive\Documents\claude-projects\japan\itinerary.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

day = next(d for d in data['days'] if d['date'] == '2026-06-01')

# ── 1. New stop: YAKINIKU LIKE Shinjuku Minamiguchi ──────────────────────────
# Address: 2-1-13 Shinjuku, Shinjuku-ku (south of Shinjuku Station South Exit)
yakiniku_like = {
    "name": "YAKINIKU LIKE — Shinjuku Minamiguchi",
    "lat": 35.6876,
    "lng": 139.7002,
    "type": "food",
    "time": "12:00",
    "notes": "Solo-style yakiniku — every seat has its own individual grill. High-quality beef sets at accessible prices. Great for a quick, satisfying lunch. Located just south of Shinjuku Station's South Exit (Minamiguchi).",
    "photo": "",
    "visited": False
}

# Insert after Shinjuku Gyoen (index 0), before Omoide Yokocho (index 1)
day['stops'].insert(1, yakiniku_like)

# ── 2. Adjust Omoide Yokocho (now index 2) ───────────────────────────────────
# Time: 12:30 → 13:15 (post-lunch walk-through rather than meal stop)
# Notes: clarify it's an atmospheric walk now that lunch is done
omoide = day['stops'][2]
omoide['time'] = '13:15'
omoide['notes'] = (
    "Walk north from YAKINIKU LIKE, 5 min. "
    "Narrow grid of tiny yakitori stalls wedged between the train tracks — "
    "look for the green and red lanterns. This is a walk-through and photo stop "
    "rather than a full meal (lunch is handled). Soak in the atmosphere."
)

# ── 3. Shift Godzilla Head to 14:15, Don Quijote to 14:45 ───────────────────
# (gives a comfortable 1 hr at Omoide + walk, and 30 min at each landmark before cosplay)
day['stops'][3]['time'] = '14:15'   # Godzilla Head
day['stops'][4]['time'] = '14:45'   # Don Quijote

# ── 4. Update dayNotes ────────────────────────────────────────────────────────
day['dayNotes'] = (
    "Full day in Shinjuku. Lunch at YAKINIKU LIKE near the South Exit, "
    "then stroll north through the lantern-lit alley of Omoide Yokocho before "
    "hitting Kabukicho for the Godzilla Head and Don Quijote. "
    "The cosplay adventure at 5 PM is the centrepiece — everything else builds around it. "
    "Tsurutontan is 4 mins from the Godzilla Head so dinner is effortless post-cosplay."
)

# ── 5. Update transit ─────────────────────────────────────────────────────────
# Replace the single "Gyoen → Omoide Yokocho" step with two steps
old_transit = day['transit']
new_transit_steps = [
    {
        "from": "Shinjuku Gyoen",
        "to": "YAKINIKU LIKE (Shinjuku South Exit)",
        "method": "Walk",
        "duration": "~12 min",
        "cost": "Free",
        "notes": "Head west/northwest from the garden exit toward Shinjuku Station. "
                 "YAKINIKU LIKE Minamiguchi is just south of the station's South Exit."
    },
    {
        "from": "YAKINIKU LIKE",
        "to": "Omoide Yokocho → Godzilla Head → Don Quijote",
        "method": "Walk",
        "duration": "5 min → 10 min → 3 min",
        "cost": "Free",
        "notes": "Walk north past the JR tracks to Omoide Yokocho (Memory Lane). "
                 "Continue east through Kabukicho to the Godzilla Head (Shinjuku Toho Bldg), "
                 "then 2 mins to Don Quijote."
    }
]

# Find and replace the Gyoen→Omoide step (was index 1)
day['transit'] = [old_transit[0]] + new_transit_steps + [old_transit[2]]

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done — June 1 updated.")

# Quick verification
with open(path, 'r', encoding='utf-8') as f:
    check = json.load(f)
june1 = next(d for d in check['days'] if d['date'] == '2026-06-01')
print("\nStops:")
for s in june1['stops']:
    print(f"  {s['time']} — {s['name']}")
print("\nTransit:")
for t in june1['transit']:
    print(f"  {t['from']} → {t['to']} ({t['method']})")
