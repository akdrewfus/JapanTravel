import json

path = r'C:\Users\ak\OneDrive\Documents\claude-projects\japan\itinerary.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for day in data['days']:
    if 'instagramPosts' not in day:
        day['instagramPosts'] = []
    for stop in day.get('stops', []):
        if 'visited' not in stop:
            stop['visited'] = False

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done — added visited/instagramPosts fields.")
