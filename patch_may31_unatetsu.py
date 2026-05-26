import json

path = r'C:\Users\ak\OneDrive\Documents\claude-projects\japan\itinerary.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

day = next(d for d in data['days'] if d['date'] == '2026-05-31')

# ── 1. Verify we're touching the right stop ───────────────────────────────────
assert day['stops'][1]['name'] == 'Unatoto Asakusa', \
    f"Unexpected stop 1: {day['stops'][1]['name']}"

# ── 2. Replace stop[1] with Asakusa Unatetsu Kokusai-dori ────────────────────
# Address: 1-43-7 Asakusa, Taito-ku, Tokyo  |  on Kokusai-dori (International St)
# Hours: 11:30–22:00, closed Tuesdays — Sunday May 31 is fine
day['stops'][1] = {
    "name": "Asakusa Unatetsu — Kokusai-dori",
    "lat": 35.7110,
    "lng": 139.7952,
    "type": "food",
    "time": "12:00",
    "notes": (
        "~8 min walk south from Kama-Asa. "
        "Long-standing Asakusa institution serving traditional grilled eel (unagi) — "
        "order the unaju (lacquered box) for the full experience. "
        "Eel is grilled over charcoal, steamed, then glazed in house tare. "
        "Address: 1-43-7 Asakusa, Taito-ku, on Kokusai-dori (International Street). "
        "Open 11:30–22:00; closed Tuesdays (Sunday May 31 is fine)."
    ),
    "photo": "",
    "visited": False
}

# ── 3. Update transit[1] — label still accurate, just tighten the 'to' field ─
assert 'Kappabashi' in day['transit'][1]['from'], \
    f"Unexpected transit[1] from: {day['transit'][1]['from']}"
day['transit'][1]['to'] = 'Asakusa Unatetsu (Kokusai-dori)'
day['transit'][1]['notes'] = (
    'Easy flat walk south from Kappabashi into Asakusa. '
    'Unatetsu is on Kokusai-dori — head south on Kappabashi-dori, '
    'then east along Kokusai-dori. About 8 min.'
)

# ── 4. Write back ─────────────────────────────────────────────────────────────
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done. May 31 stop[1]:')
s = day['stops'][1]
print(f"  {s['time']} -- {s['name']}")
print(f"  lat: {s['lat']}, lng: {s['lng']}")
print(f"  notes: {s['notes'][:80]}...")
print()
print('Transit[1]:')
t = day['transit'][1]
print(f"  {t['from']} -> {t['to']} ({t['method']})")
