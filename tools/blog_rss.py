# 블로그 RSS를 읽어 blog.json(최근 글 5개)을 만듦 — 앱 「입시 정보 > 최근 올라온 글」이 읽는 파일
import json, re, sys, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
RSS = "https://rss.blog.naver.com/kwon_th.xml"
req = urllib.request.Request(RSS, headers={"User-Agent": "Mozilla/5.0 (uridongne-ipsi blog list)"})
xml = urllib.request.urlopen(req, timeout=30).read()
root = ET.fromstring(xml)
items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    link = re.sub(r"\?.*$", "", (it.findtext("link") or "").strip())
    if not title or not link:
        continue
    try:
        date = parsedate_to_datetime(it.findtext("pubDate") or "").isoformat()
    except Exception:
        date = ""
    items.append({"title": title, "link": link, "date": date, "cat": (it.findtext("category") or "").strip()})
items.sort(key=lambda x: x["date"], reverse=True)
items = items[:5]
if not items:
    sys.exit("RSS에서 글을 찾지 못함 — blog.json을 그대로 둠")
try:
    old = json.load(open("blog.json", encoding="utf-8")).get("items")
except Exception:
    old = None
if old == items:
    print("바뀐 글 없음"); sys.exit(0)
json.dump({"items": items}, open("blog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("blog.json 갱신:", items[0]["title"])
