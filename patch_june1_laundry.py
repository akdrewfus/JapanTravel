import json

path = r'C:\Users\ak\OneDrive\Documents\claude-projects\japan\itinerary.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

day = next(d for d in data['days'] if d['date'] == '2026-06-01')

# ── 1. Remove Shinjuku Gyoen (was index 0) ────────────────────────────────────
assert day['stops'][0]['name'] == 'Shinjuku Gyoen National Garden', \
    f"Unexpected stop 0: {day['stops'][0]['name']}"
day['stops'].pop(0)

# ── 2. Insert 39 Laundry as new index 0 ──────────────────────────────────────
# 3 Chome-5-8 Hatchobori, Chuo City, Tokyo 104-0032
laundry_stop = {
    "name": "39 Laundry — Hatchobori",
    "lat": 35.6742,
    "lng": 139.7750,
    "type": "activity",
    "time": "08:30",
    "notes": (
        "Morning laundry run — 2 loads while Shinjuku day prep happens. "
        "Self-service laundromat at 3 Chome-5-8 Hatchobori, Chuo City. "
        "~15 min walk southeast from the hotel. "
        "Washer cycles ~30–35 min, dryer ~40–45 min per load; "
        "plan for 90 min total including walk time. "
        "Head back to the hotel around 10:00–10:30 before setting off to Shinjuku."
    ),
    "photo": "",
    "visited": False
}
day['stops'].insert(0, laundry_stop)

# ── 3. Insert hotel return as new index 1 ─────────────────────────────────────
# Courtyard by Marriott Tokyo Station (Kyobashi 2-1-3, Chuo-ku)
hotel_return_stop = {
    "name": "Courtyard by Marriott Tokyo Station (return)",
    "lat": 35.6793,
    "lng": 139.7681,
    "type": "hotel",
    "time": "10:30",
    "notes": (
        "Back at the hotel after laundry. "
        "Drop off clean clothes, freshen up, grab bags for a full Shinjuku day. "
        "Head to Tokyo Station to catch the Marunouchi Line for Shinjuku."
    ),
    "photo": "",
    "visited": False
}
day['stops'].insert(1, hotel_return_stop)

# ── 4. Fix stale Omoide Yokocho notes (now index 4) ──────────────────────────
# After the two inserts: 0=Laundry, 1=Hotel, 2=Kura Sushi, 3=Omoide, 4=Godzilla...
# Wait — original stops after Gyoen removal:
#   0: Kura Sushi, 1: Omoide Yokocho, 2: Godzilla, 3: DQ, 4: Cosplay, 5: Tsurutontan
# After two inserts at 0 and 1:
#   0: Laundry, 1: Hotel, 2: Kura Sushi, 3: Omoide, 4: Godzilla, 5: DQ, 6: Cosplay, 7: Tsurutontan
omoide = day['stops'][3]
assert 'Omoide' in omoide['name'], f"Unexpected stop 3: {omoide['name']}"
omoide['notes'] = (
    "Short walk east from Kura Sushi (~5 min). "
    "Narrow grid of tiny yakitori stalls wedged between the JR tracks — "
    "look for the green and red lanterns. Walk-through and photo stop "
    "rather than a full meal (lunch at Kura Sushi is handled). "
    "Soak in the atmosphere before heading east into Kabukicho."
)

# ── 5. Rebuild transit legs 0–2, keep 2–3 (now 3–4) ─────────────────────────
old_transit = day['transit']
# old: [0] Tokyo Stn→Gyoemmae, [1] Gyoen→Kura Sushi, [2] Kura→Omoide/etc, [3] Shinjuku return
# keep [2] and [3]

new_transit = [
    {
        "from": "Courtyard by Marriott Tokyo Station",
        "to": "39 Laundry — Hatchobori",
        "method": "Walk",
        "duration": "~15 min",
        "cost": "Free",
        "notes": (
            "Head southeast from the hotel — Hatchobori is just across the Kanda River. "
            "Walk past the Showa-dori intersection; 39 Laundry is on Hatchobori 3-chome."
        )
    },
    {
        "from": "39 Laundry — Hatchobori",
        "to": "Courtyard by Marriott Tokyo Station",
        "method": "Walk",
        "duration": "~15 min",
        "cost": "Free",
        "notes": "Same route back. Return to hotel ~10:00–10:30, freshen up, then head to Tokyo Station."
    },
    {
        "from": "Tokyo Station",
        "to": "Shinjuku Station",
        "method": "Marunouchi Line (Red)",
        "duration": "20 min",
        "cost": "¥210",
        "notes": (
            "Direct from Tokyo Station. Well after morning rush — trains are comfortable by 11:00 AM. "
            "Exit West or South at Shinjuku; Kura Sushi Nishishinjuku is a 3-min walk west."
        )
    },
    old_transit[2],   # Kura Sushi → Omoide / Godzilla / DQ
    old_transit[3],   # Shinjuku → Tokyo Station return
]
day['transit'] = new_transit

# ── 6. Update metadata ────────────────────────────────────────────────────────
day['suggestedStart'] = "08:30"

day['startReason'] = (
    "Early start for laundry — walk to 39 Laundry at 8:30 AM before the machines fill up. "
    "Back at the hotel by 10:30, then depart to Shinjuku for a full afternoon."
)

day['rushHourNote'] = (
    "The 8:30 AM laundry walk is on foot — no train needed. "
    "By the time you board the Marunouchi Line to Shinjuku (~11:00 AM), "
    "Monday rush hour is fully over and trains are comfortable."
)

day['dayNotes'] = (
    "Morning laundry run to 39 Laundry in Hatchobori — get two loads done early "
    "while prepping for a full Shinjuku day. Back at the hotel by 10:30, "
    "then it's a direct Marunouchi Line ride to Shinjuku. "
    "Kaiten sushi lunch at Kura Sushi (west side of the station) — "
    "Sadie will love the Bikkura-Pon capsule lottery every 5 plates. "
    "Short walk east through Memory Lane (Omoide Yokocho), then into Kabukicho "
    "for the Godzilla Head and Don Quijote. "
    "The 5 PM cosplay adventure is the centrepiece of the day. "
    "Tsurutontan udon is 4 mins away — effortless post-cosplay dinner."
)

# ── 7. Write back ─────────────────────────────────────────────────────────────
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# ── 8. Verify ─────────────────────────────────────────────────────────────────
with open(path, 'r', encoding='utf-8') as f:
    check = json.load(f)
june1 = next(d for d in check['days'] if d['date'] == '2026-06-01')

print("suggestedStart:", june1['suggestedStart'])
print()
print("Stops:")
for i, s in enumerate(june1['stops']):
    print(f"  [{i}] {s['time']} -- {s['name']}")
print()
print("Transit:")
for i, t in enumerate(june1['transit']):
    print(f"  [{i}] {t['from']} -> {t['to']} ({t['method']}, {t['duration']})")
