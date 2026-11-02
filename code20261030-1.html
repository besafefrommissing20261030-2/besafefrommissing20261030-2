<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>실종 위험 예측 프로젝트</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f4f6f9;
      color: #222;
    }

    header {
      background: #243b55;
      color: white;
      padding: 55px 20px;
      text-align: center;
    }

    main {
      max-width: 900px;
      margin: 40px auto;
      padding: 30px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 3px 12px #00000010;
    }

    h2 {
      color: #243b55;
    }

    .table-wrap {
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 15px;
    }

    th, td {
      padding: 10px 12px;
      border-bottom: 1px solid #e3e7ee;
      text-align: center;
      white-space: nowrap;
    }

    th {
      background: #243b55;
      color: white;
      font-weight: 600;
    }

    tbody tr:nth-child(even) {
      background: #f7f9fc;
    }

    #status {
      color: #666;
      font-size: 14px;
      margin: 8px 0 14px;
    }

    footer {
      text-align: center;
      padding: 25px;
      color: #777;
      font-size: 14px;
    }
  </style>
</head>
<body>

  <header>
    <h1>실종 위험 예측 프로젝트</h1>
    <p>공공데이터를 활용한 지역별 실종 위험 분석</p>
  </header>

  <main>
    <h2>프로젝트 소개</h2>
    <p>
      본 프로젝트는 실종 관련 공공데이터를 활용하여
      지역과 시간에 따른 실종 발생 위험을 분석하고
      예측하는 것을 목표로 합니다.
    </p>

    <h2>분석 목적</h2>
    <p>
      실종 위험이 상대적으로 높은 시간과 지역을 파악하여
      예방 활동과 안전 관리에 활용할 수 있는 정보를
      제공하고자 합니다.
    </p>

    <h2>활용 데이터</h2>
    <p>
      경찰청 안전Dream에서 제공하는 실종 관련 공공데이터를
      활용합니다.
    </p>

    <h2>실종 정보 목록</h2>
    <div id="status">불러오는 중...</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>이름</th>
            <th>나이</th>
            <th>시간(24시)</th>
            <th>성별</th>
            <th>장소(시)</th>
            <th>장소(군)</th>
            <th>장소(동)</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </main>

  <footer>
    © 2026 Missing Risk Prediction Project
  </footer>

  <script>
    // ---- 설정 ----
    const DATA_URL = "data.json";   // 같은 폴더의 JSON 파일 (아래 설명 참고)
    const MASK_NAME = true;         // true: 이름 가운데 글자를 ○로 가림 (김○수)

    // API 응답의 필드 이름. 실제 응답과 다르면 여기만 고치세요.
    const FIELD = {
      name: "nm",
      age: "age",             // 당시 나이. 현재 나이는 "ageNow"
      occurred: "occrde",     // 발생일시
      gender: "sexdstnDscd",
      address: "occrAdres"    // "서울특별시 강남구 역삼동 ..." 형태
    };

    // 파일이 없을 때 보여줄 예시 데이터 (가상의 값)
    const SAMPLE = [
      { nm: "홍길동", age: 7,  occrde: "202610301430", sexdstnDscd: "남자", occrAdres: "서울특별시 강남구 역삼동" },
      { nm: "김영희", age: 82, occrde: "202610311905", sexdstnDscd: "여자", occrAdres: "부산광역시 해운대구 우동" }
    ];

    // ---- 가공 함수 ----
    function maskName(name) {
      if (!MASK_NAME || !name) return name || "-";
      if (name.length <= 2) return name[0] + "○";
      return name[0] + "○".repeat(name.length - 2) + name[name.length - 1];
    }

    // "202610301430" -> "14:30", 날짜만 있으면 "-"
    function formatTime(v) {
      const s = String(v || "").replace(/\D/g, "");
      if (s.length >= 12) return s.slice(8, 10) + ":" + s.slice(10, 12);
      return "-";
    }

    function splitAddress(addr) {
      const p = String(addr || "").trim().split(/\s+/);
      return { si: p[0] || "-", gun: p[1] || "-", dong: p[2] || "-" };
    }

    function render(list) {
      const tbody = document.getElementById("tbody");
      tbody.innerHTML = "";
      list.forEach(item => {
        const loc = splitAddress(item[FIELD.address]);
        const cells = [
          maskName(item[FIELD.name]),
          item[FIELD.age] ?? "-",
          formatTime(item[FIELD.occurred]),
          item[FIELD.gender] || "-",
          loc.si, loc.gun, loc.dong
        ];
        const tr = document.createElement("tr");
        cells.forEach(c => {
          const td = document.createElement("td");
          td.textContent = c;   // textContent로 넣어 안전하게 표시
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }

    async function load() {
      const status = document.getElementById("status");
      try {
        const res = await fetch(DATA_URL);
        if (!res.ok) throw new Error(res.status);
        const json = await res.json();
        const list = Array.isArray(json) ? json : (json.list || []);
        render(list);
        status.textContent = "총 " + list.length + "건";
      } catch (e) {
        render(SAMPLE);
        status.textContent = "data.json을 찾지 못해 예시 데이터를 표시합니다.";
      }
    }

    load();
  </script>

</body>
</html>
