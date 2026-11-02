import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

BASE = "https://www.safe182.go.kr/api/lcm/"
# (API 주소, 저장할 파일 이름)
TARGETS = [
    ("amberList.do", "amber.json"),      # 목록 1: 실종경보
    ("findChildList.do", "child.json"),  # 목록 2: 실종아동 등
]
ROW_SIZE = 100      # 명세상 최대 100
MAX_PAGES = 10      # 일일 조회 건수 초과(코드 80)를 막기 위한 안전장치

esntl_id = os.environ.get("ESNTL_ID", "").strip()
auth_key = os.environ.get("AUTH_KEY", "").strip()

if not esntl_id or not auth_key:
    sys.exit("ESNTL_ID 또는 AUTH_KEY 환경변수(Secrets)가 비어 있습니다.")


def call(api, page):
    body = urllib.parse.urlencode({
        "esntlId": esntl_id,
        "authKey": auth_key,
        "rowSize": str(ROW_SIZE),
        "page": str(page),
    }).encode("utf-8")
    req = urllib.request.Request(BASE + api, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as res:
        raw = res.read().decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError("JSON이 아닌 응답: " + raw[:200])


def fetch_all(api):
    items, total = [], None
    for page in range(1, MAX_PAGES + 1):
        data = call(api, page)
        if str(data.get("result")) != "00":
            # 80: 일일 조회 건수 초과, 99: 필수항목 누락 또는 아이디/인증키 오류
            raise RuntimeError("result=%s msg=%s" % (data.get("result"), data.get("msg")))
        if total is None:
            total = int(data.get("totalCount", 0))
        batch = data.get("list") or []
        items.extend(batch)
        print("  page", page, ":", len(batch), "건")
        if not batch or len(items) >= total:
            break
    return items, total


KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y-%m-%d")


def mask_name(name):
    name = (name or "").strip()
    if len(name) <= 1:
        return name
    if len(name) == 2:
        return name[0] + "○"
    return name[0] + "○" * (len(name) - 2) + name[-1]


def slim(item):
    """공개 저장소에 올리므로 분석에 필요한 항목만 남기고 이름은 가려서 저장."""
    return {
        "nm": mask_name(item.get("nm")),
        "age": item.get("age"),
        "occrde": item.get("occrde"),
        "sexdstnDscd": item.get("sexdstnDscd"),
        "occrAdres": item.get("occrAdres"),
        "writngTrgetDscd": item.get("writngTrgetDscd"),
    }


def key_of(r):
    return "|".join(str(r.get(k)) for k in ("nm", "age", "occrde", "sexdstnDscd", "occrAdres"))


def merge(outfile, fresh):
    """기존 파일 + 이번에 받은 목록을 합쳐서 사라진 건도 남긴다."""
    old = []
    if os.path.exists(outfile):
        try:
            with open(outfile, encoding="utf-8") as f:
                old = json.load(f)
        except Exception:
            old = []
    merged = {}
    for r in old:
        base = slim(r)
        base["_firstSeen"] = r.get("_firstSeen", TODAY)
        base["_lastSeen"] = r.get("_lastSeen", r.get("_firstSeen", TODAY))
        merged[key_of(base)] = base
    new_count = 0
    for r in fresh:
        base = slim(r)
        k = key_of(base)
        if k in merged:
            merged[k]["_lastSeen"] = TODAY
        else:
            base["_firstSeen"] = TODAY
            base["_lastSeen"] = TODAY
            merged[k] = base
            new_count += 1
    return list(merged.values()), new_count


ok = 0
for api, outfile in TARGETS:
    print(api)
    try:
        items, total = fetch_all(api)
    except Exception as e:
        print("  실패:", e)
        continue
    merged, new_count = merge(outfile, items)
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print("  이번에 받은 건수:", len(items), "/ 전체", total, "건")
    print("  새로 추가:", new_count, "건, 누적 저장:", outfile, len(merged), "건")
    ok += 1

if ok == 0:
    sys.exit("모든 API 호출이 실패했습니다.")
