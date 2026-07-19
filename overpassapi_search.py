import csv
import json
import time
import random
import requests
from datetime import datetime

# ==========================================
# 設定
# ==========================================
OVERPASS_URL = "https://overpass.private.coffee/api/interpreter"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
USER_AGENT = "KyotoTourismExporter/2.2"

# 拡張性の高いリスト形式のクエリ定義
QUERIES = [
    ("観光施設", '[out:json][timeout:600];area["name:ja"="京都市"]->.searchArea;(node["tourism"~"attraction|museum|viewpoint|artwork|gallery|zoo|aquarium|theme_park|information"](area.searchArea);way["tourism"~"attraction|museum|viewpoint|artwork|gallery|zoo|aquarium|theme_park|information"](area.searchArea);relation["tourism"~"attraction|museum|viewpoint|artwork|gallery|zoo|aquarium|theme_park|information"](area.searchArea););out center;'),
    ("寺社", '[out:json][timeout:600];area["name:ja"="京都市"]->.searchArea;(node["amenity"="place_of_worship"](area.searchArea);way["amenity"="place_of_worship"](area.searchArea);relation["amenity"="place_of_worship"](area.searchArea););out center;'),
    ("史跡", '[out:json][timeout:600];area["name:ja"="京都市"]->.searchArea;(node["historic"~"castle|monument|memorial|ruins|building|archaeological_site"](area.searchArea);way["historic"~"castle|monument|memorial|ruins|building|archaeological_site"](area.searchArea);relation["historic"~"castle|monument|memorial|ruins|building|archaeological_site"](area.searchArea););out center;'),
    ("庭園・公園", '[out:json][timeout:600];area["name:ja"="京都市"]->.searchArea;(node["leisure"~"garden|park"](area.searchArea);way["leisure"~"garden|park"](area.searchArea);relation["leisure"~"garden|park"](area.searchArea););out center;'),
    ("自然", '[out:json][timeout:600];area["name:ja"="京都市"]->.searchArea;(node["natural"~"peak|spring|waterfall|cave_entrance"](area.searchArea);way["natural"~"peak|spring|waterfall|cave_entrance"](area.searchArea);relation["natural"~"peak|spring|waterfall|cave_entrance"](area.searchArea););out center;')
]

def fetch_with_retry(session, query, category_name, max_retries=5):
    for i in range(max_retries):
        try:
            print(f"[{category_name}] 取得中... (試行 {i+1})")
            response = session.post(OVERPASS_URL, data={"data": query}, timeout=300)
            if response.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(response=response)
            response.raise_for_status()
            return response.json().get("elements", [])
        except Exception as e:
            wait = (2 ** i) + random.uniform(1, 3)
            print(f"警告: {category_name}取得失敗: {e}。{wait:.2f}秒待機...")
            time.sleep(wait)
    return []

def save_csv(records, filename):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "name_ja", "name_en", "tourism", "amenity", "historic", "leisure", "natural",
                         "lat", "lon", "osm_type", "osm_id", "url", "website", "wikipedia", "wikidata", "tags_json"])
        for r in records:
            writer.writerow([r["name"], r["name_ja"], r["name_en"], r["tourism"], r["amenity"], r["historic"],
                             r["leisure"], r["natural"], r["lat"], r["lon"], r["osm_type"], r["osm_id"],
                             r["url"], r["website"], r["wikipedia"], r["wikidata"], json.dumps(r["tags"], ensure_ascii=False)])

def save_geojson(records, filename):
    features = []
    for r in records:
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
            "properties": {k: v for k, v in r.items() if k not in ["lat", "lon"]}
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False, indent=2)

def main():
    all_elements = []
    with requests.Session() as session:
        session.headers.update({"User-Agent": USER_AGENT})
        for name, query in QUERIES:
            elements = fetch_with_retry(session, query, name)
            all_elements.extend(elements)
            print(f"[{name}] 完了: {len(elements)} 件")

    records = []
    for elem in all_elements:
        tags = elem.get("tags", {})
        lat = elem.get("lat") or elem.get("center", {}).get("lat")
        lon = elem.get("lon") or elem.get("center", {}).get("lon")
        if lat is None or lon is None: continue

        records.append({
            "name": tags.get("name:ja") or tags.get("name") or "名称不明",
            "name_ja": tags.get("name:ja", ""),
            "name_en": tags.get("name:en", ""),
            "tourism": tags.get("tourism", ""),
            "amenity": tags.get("amenity", ""),
            "historic": tags.get("historic", ""),
            "leisure": tags.get("leisure", ""),
            "natural": tags.get("natural", ""),
            "lat": lat, "lon": lon,
            "osm_type": elem["type"], "osm_id": elem["id"],
            "url": f"https://www.openstreetmap.org/{elem['type']}/{elem['id']}",
            "website": tags.get("website") or tags.get("contact:website") or "",
            "wikipedia": tags.get("wikipedia", ""),
            "wikidata": tags.get("wikidata", ""),
            "tags": tags
        })

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    save_csv(records, f"kyoto_data_{ts}.csv")
    save_geojson(records, f"kyoto_data_{ts}.geojson")
    print(f"全 {len(records)} 件を保存しました。")

if __name__ == "__main__":
    main()
