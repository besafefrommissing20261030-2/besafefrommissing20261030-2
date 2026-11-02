import json
import os
import sys
import urllib.parse
import urllib.request

URL = "https://www.safe182.go.kr/api/lcm/amberList.do"

esntl_id = os.environ.get("ESNTL_ID", "").strip()
auth_key = os.environ.get("AUTH_KEY", "").strip()

if not esntl_id or not auth_key:
    sys.exit("ESNTL_ID 또는 AUTH_KEY 환경변수(Secrets)가 비어 있습니다.")

body = urllib.parse.urlencode({
    "esntlId": esntl_id,
    "authKey": auth_key,
    "rowSize": "100",
    "page": "1",
}).encode("utf-8")

req = urllib.request.Request(URL, data=body, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")

with urllib.request.urlopen(req, timeout=30) as res:
    raw = res.read().decode("utf-8")

try:
    data = json.loads(raw)
except json.JSONDecodeError:
    sys.exit("JSON이 아닌 응답이 왔습니다. 앞부분: " + raw[:200])

# 오류 응답 예: {"result":"99","msg":"사용자아이디와 인증키가 올바르지 않습니다."}
if "list" not in data:
    sys.exit("데이터가 없습니다. 서버 응답: " + json.dumps(data, ensure_ascii=False)[:300])

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data["list"], f, ensure_ascii=False, indent=2)

print("저장 완료:", len(data["list"]), "건")
