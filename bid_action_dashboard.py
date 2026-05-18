import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 페이지 설정 ────────────────────────────────────────────────
st.set_page_config(
    page_title="공공조달 입찰 분석 AI ETE 시스템",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 공통 CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Noto Sans KR', sans-serif;
    background: #f5f4f0;
}
[data-testid="stSidebar"] { background: #1a1918 !important; }
[data-testid="stSidebar"] * { color: #d4d3ce !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 13px; }
[data-testid="stSidebar"] hr { border-color: #333; }

h1 { font-size: 20px !important; font-weight: 700 !important; margin-bottom: 2px !important; }
h2 { font-size: 15px !important; font-weight: 600 !important; }
h3 { font-size: 13px !important; font-weight: 600 !important; }

.card {
    background: #fff; border: 1px solid #e0dfd8;
    border-radius: 10px; padding: 16px; margin-bottom: 12px;
}
.kpi { background: #f0efe9; border-radius: 8px; padding: 14px 16px; }
.kpi-l { font-size: 11px; color: #6b6a65; margin-bottom: 4px; }
.kpi-v { font-size: 28px; font-weight: 700; }
.green { color: #1f6b2e; } .amber { color: #7a4d0a; }
.red   { color: #8b2020; } .blue  { color: #1a56a0; }

.badge { display:inline-block; font-size:10px; padding:2px 8px;
         border-radius:999px; font-weight:600; white-space:nowrap; }
.bg   { background:#e6f4ea; color:#1f6b2e; }
.ba   { background:#fdf3e0; color:#7a4d0a; }
.br   { background:#fdeaea; color:#8b2020; }
.bb   { background:#e8f0fb; color:#1a56a0; }
.bgray{ background:#f0efe9; color:#444; }

.ok   { background:#e6f4ea; color:#1f6b2e; font-size:10px; padding:1px 6px; border-radius:4px; display:inline-block; }
.warn { background:#fdf3e0; color:#7a4d0a; font-size:10px; padding:1px 6px; border-radius:4px; display:inline-block; }
.ng   { background:#fdeaea; color:#8b2020; font-size:10px; padding:1px 6px; border-radius:4px; display:inline-block; }

.ar { display:flex; align-items:center; gap:10px; padding:8px 0;
      border-bottom:1px solid #f5f4f0; font-size:12px; }
.ar:last-child { border-bottom:none; }
.dr { width:8px; height:8px; border-radius:50%; background:#e24b4a; flex-shrink:0; display:inline-block; }
.da { width:8px; height:8px; border-radius:50%; background:#ef9f27; flex-shrink:0; display:inline-block; }
.dg { width:8px; height:8px; border-radius:50%; background:#3b8a4a; flex-shrink:0; display:inline-block; }

.tbl { width:100%; border-collapse:collapse; font-size:12px; }
.tbl th { padding:7px 10px; text-align:left; font-size:11px; font-weight:600;
          color:#6b6a65; border-bottom:1px solid #e0dfd8; background:#f8f7f3; }
.tbl td { padding:8px 10px; border-bottom:1px solid #f0efe9; color:#1a1918; }
.tbl tr:last-child td { border-bottom:none; }
.tbl tr:hover td { background:#fafaf7; }

.profit { background:#f0efe9; border:1px solid #e0dfd8; border-radius:8px; padding:14px; text-align:center; }
.profit-l { font-size:10px; color:#6b6a65; margin-bottom:4px; }
.profit-v { font-size:17px; font-weight:700; color:#1a56a0; }
.profit-s { font-size:10px; color:#9e9d98; margin-top:3px; }

.pr { display:flex; justify-content:space-between; align-items:center;
      padding:8px 0; border-bottom:1px solid #f5f4f0; font-size:12px; }
.pr:last-child { border-bottom:none; }
.pr-l { font-size:11px; color:#6b6a65; }

.email-box { background:#fff; border:1px solid #e0dfd8; border-radius:10px; padding:16px 20px; }
.email-title { font-size:15px; font-weight:700; margin-bottom:4px; }
.email-sub   { font-size:11px; color:#6b6a65; margin-bottom:14px; }
.email-item  { background:#f8f7f3; border-radius:8px; padding:12px 14px; margin-bottom:8px; }
.email-item-t{ font-size:13px; font-weight:600; margin-bottom:3px; }
.email-item-s{ font-size:11px; color:#6b6a65; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 더미 데이터
# ══════════════════════════════════════════════════════════════
NOTICES = [
    {"id":"20260518-001","title":"2026년 OO구 공공시설 청소 용역","org":"OO구청","demand_org":"OO구청",
     "type":"용역","region":"서울","amount":42_000_000,"base":44_100_000,"min_rate":87.5,
     "dday":1,"bid_start":"2026-05-10","bid_end":"2026-05-19","open_dt":"2026-05-20",
     "open_place":"나라장터 전자개찰","competition":"제한경쟁",
     "rc":"ok","lc":"ok","pc":"ok","dc":"warn","dlv":"ok","status":"지원 가능","score":82,
     "avg_rate":88.4,"case_count":23,"bid_low":36_120_000,"bid_high":39_480_000,"comp_level":"중","comp_cnt":7,
     "docs":["사업실적 증명서","법인 등기부등본","직접생산확인증명서","면허증 사본"],
     "docs_done":[True,True,False,False],
     "reqs":[
         {"item":"지역 조건","required":"서울 소재","company":"서울 소재","status":"ok","compete":"낮음","source":"공고문 3p"},
         {"item":"면허/업종","required":"청소업 면허","company":"보유","status":"ok","compete":"중간","source":"공고문 2p"},
         {"item":"사업 실적","required":"3억↑ (최근3년)","company":"4.2억","status":"ok","compete":"중간","source":"첨부1 p2"},
         {"item":"직접생산확인","required":"필요","company":"확인 필요","status":"warn","compete":"—","source":"첨부2 p1"},
         {"item":"납기 수행","required":"90일","company":"가능","status":"ok","compete":"—","source":"공고문 4p"},
     ]},
    {"id":"20260518-002","title":"OO병원 환경미화 용역 입찰","org":"OO의료원","demand_org":"OO병원",
     "type":"용역","region":"경기","amount":85_000_000,"base":89_250_000,"min_rate":86.0,
     "dday":7,"bid_start":"2026-05-12","bid_end":"2026-05-25","open_dt":"2026-05-27",
     "open_place":"나라장터 전자개찰","competition":"일반경쟁",
     "rc":"ok","lc":"ok","pc":"warn","dc":"ok","dlv":"warn","status":"검토 필요","score":61,
     "avg_rate":85.1,"case_count":11,"bid_low":69_200_000,"bid_high":74_500_000,"comp_level":"상","comp_cnt":12,
     "docs":["사업실적 증명서","법인 등기부등본","면허증 사본"],
     "docs_done":[False,True,False],
     "reqs":[
         {"item":"지역 조건","required":"경기 소재","company":"서울 소재","status":"warn","compete":"—","source":"공고문 2p"},
         {"item":"면허/업종","required":"청소업 면허","company":"보유","status":"ok","compete":"중간","source":"공고문 2p"},
         {"item":"사업 실적","required":"5억↑ (최근3년)","company":"4.2억","status":"warn","compete":"높음","source":"첨부1 p3"},
         {"item":"납기 수행","required":"60일","company":"가능(빠듯)","status":"warn","compete":"—","source":"공고문 4p"},
     ]},
    {"id":"20260518-003","title":"OO시 행정복지센터 청소 용역","org":"OO시청","demand_org":"OO시",
     "type":"용역","region":"서울","amount":31_000_000,"base":32_550_000,"min_rate":88.0,
     "dday":14,"bid_start":"2026-05-15","bid_end":"2026-06-02","open_dt":"2026-06-04",
     "open_place":"나라장터 전자개찰","competition":"제한경쟁",
     "rc":"ok","lc":"ok","pc":"ok","dc":"ok","dlv":"ok","status":"지원 가능","score":91,
     "avg_rate":91.2,"case_count":31,"bid_low":27_500_000,"bid_high":29_800_000,"comp_level":"하","comp_cnt":4,
     "docs":["사업실적 증명서","법인 등기부등본","면허증 사본","직접생산확인증명서"],
     "docs_done":[True,True,True,False],
     "reqs":[
         {"item":"지역 조건","required":"서울 소재","company":"서울 소재","status":"ok","compete":"낮음","source":"공고문 2p"},
         {"item":"면허/업종","required":"청소업 면허","company":"보유","status":"ok","compete":"낮음","source":"공고문 2p"},
         {"item":"사업 실적","required":"2억↑ (최근3년)","company":"4.2억","status":"ok","compete":"낮음","source":"첨부1 p2"},
         {"item":"직접생산확인","required":"필요","company":"미준비","status":"warn","compete":"—","source":"첨부2 p1"},
         {"item":"납기 수행","required":"120일","company":"가능","status":"ok","compete":"—","source":"공고문 4p"},
     ]},
    {"id":"20260518-004","title":"OO공단 시설관리 위탁 운영 용역","org":"OO공단","demand_org":"OO공단",
     "type":"용역","region":"경기","amount":120_000_000,"base":126_000_000,"min_rate":85.0,
     "dday":2,"bid_start":"2026-05-08","bid_end":"2026-05-20","open_dt":"2026-05-22",
     "open_place":"나라장터 전자개찰","competition":"제한경쟁",
     "rc":"ng","lc":"ok","pc":"ng","dc":"ok","dlv":"ok","status":"보류","score":38,
     "avg_rate":87.0,"case_count":8,"bid_low":99_000_000,"bid_high":106_000_000,"comp_level":"상","comp_cnt":14,
     "docs":["사업실적 증명서","면허증 사본"],
     "docs_done":[True,False],
     "reqs":[
         {"item":"지역 조건","required":"경기 소재","company":"서울 소재","status":"ng","compete":"—","source":"공고문 2p"},
         {"item":"면허/업종","required":"시설관리 면허","company":"보유","status":"ok","compete":"높음","source":"공고문 2p"},
         {"item":"사업 실적","required":"10억↑ (최근3년)","company":"4.2억","status":"ng","compete":"높음","source":"첨부1 p4"},
     ]},
    {"id":"20260518-005","title":"OO교육청 환경정비 용역","org":"OO교육청","demand_org":"OO교육청",
     "type":"용역","region":"서울","amount":55_000_000,"base":57_750_000,"min_rate":87.0,
     "dday":3,"bid_start":"2026-05-14","bid_end":"2026-05-21","open_dt":"2026-05-23",
     "open_place":"나라장터 전자개찰","competition":"일반경쟁",
     "rc":"ok","lc":"ok","pc":"warn","dc":"warn","dlv":"ok","status":"검토 필요","score":58,
     "avg_rate":89.3,"case_count":17,"bid_low":47_200_000,"bid_high":50_600_000,"comp_level":"중","comp_cnt":9,
     "docs":["사업실적 증명서","직접생산확인증명서","면허증 사본"],
     "docs_done":[False,False,False],
     "reqs":[
         {"item":"지역 조건","required":"서울 소재","company":"서울 소재","status":"ok","compete":"낮음","source":"공고문 2p"},
         {"item":"면허/업종","required":"청소업 면허","company":"보유","status":"ok","compete":"중간","source":"공고문 2p"},
         {"item":"사업 실적","required":"4억↑ (최근3년)","company":"4.2억","status":"warn","compete":"높음","source":"첨부1 p3"},
         {"item":"직접생산확인","required":"필요","company":"미준비","status":"warn","compete":"—","source":"첨부2 p1"},
     ]},
]

ACTIONS = [
    {"dot":"r","text":"[N001] OO구 청소 용역 마감 D-1 — 서류 제출 완료 확인","tag":"긴급"},
    {"dot":"r","text":"직접생산확인증명서 유효기간 만료 임박 확인 필요","tag":"서류"},
    {"dot":"a","text":"[N005] OO교육청 환경정비 마감 D-3 — 적합도 검토","tag":"검토"},
    {"dot":"a","text":"OO병원 환경미화 지역 조건 원문 추가 확인","tag":"확인"},
    {"dot":"g","text":"사업실적 증명서 갱신 완료","tag":"완료"},
]

COMPANY = {
    "name":"(주)청명서비스",
    "industry":"청소업 / 시설관리업",
    "product_no":"4111010101",
    "product_name":"청소 및 위생 관련 서비스",
    "region":"서울특별시",
    "budget_min":10_000_000,
    "budget_max":150_000_000,
}

# ── 헬퍼 ──────────────────────────────────────────────────────
def chip(val):
    m = {"ok":'<span class="ok">충족</span>',
         "warn":'<span class="warn">확인 필요</span>',
         "ng":'<span class="ng">미충족</span>'}
    return m.get(val, "")

def badge(status):
    m = {"지원 가능":"bg","검토 필요":"ba","보류":"br"}
    return f'<span class="badge {m.get(status,"bgray")}">{status}</span>'

def dday_badge(d):
    cls = "br" if d <= 2 else ("ba" if d <= 7 else "bb")
    return f'<span class="badge {cls}">D-{d}</span>'


# ══════════════════════════════════════════════════════════════
# 사이드바
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🏛️ ")
    st.caption("공공조달 입찰 분석 AI ETE 시스템")
    st.divider()
    menu = st.radio("", [
        "📋 데일리 액션 대시보드",
        "🔍 공고 검색",
        "⭐ 관심 공고",
        "🎯 요건 매칭",
        "🏢 회사 프로필",
    ], label_visibility="collapsed")
    st.divider()
    st.caption(f"**{COMPANY['name']}**")
    st.caption(f"업종: {COMPANY['industry']}")
    st.caption(f"지역: {COMPANY['region']}")


# ══════════════════════════════════════════════════════════════
# 화면 1 — 데일리 액션 대시보드
# ══════════════════════════════════════════════════════════════
if menu == "📋 데일리 액션 대시보드":
    st.markdown("# 📋 데일리 액션 대시보드")
    st.caption("2026년 5월 18일 (월) · 오늘 수집 기준 5건")

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("긴급 처리 (D-3)","2","red"),
        ("검토 추천 (4~7일)","2","amber"),
        ("보류 추천","1",""),
        ("전체 확인 공고","5","blue"),
    ]
    for col, (label, val, color) in zip([k1,k2,k3,k4], kpis):
        with col:
            st.markdown(
                f'<div class="kpi"><div class="kpi-l">{label}</div>'
                f'<div class="kpi-v {color}">{val}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # 오늘 우선 확인 공고
    st.markdown("#### 오늘 우선 확인해야 할 공고")
    tbl = """<div class="card"><table class="tbl"><thead><tr>
        <th>우선순위</th><th>공고명</th><th>공고번호</th><th>수요기관</th>
        <th>마감일</th><th>추정가격</th><th>AI 매칭 결과</th>
    </tr></thead><tbody>"""
    for i, n in enumerate(sorted(NOTICES, key=lambda x: x["dday"]), 1):
        pc = "#e24b4a" if i<=2 else ("#ef9f27" if i<=4 else "#888")
        tbl += f"""<tr>
            <td><span style="font-weight:700;color:{pc}">#{i}</span></td>
            <td style="font-weight:500">{n['title']}</td>
            <td style="font-family:monospace;font-size:10px;color:#6b6a65">{n['id']}</td>
            <td>{n['demand_org']}</td>
            <td>{dday_badge(n['dday'])}</td>
            <td>{n['amount']:,.0f}원</td>
            <td>{badge(n['status'])}</td>
        </tr>"""
    tbl += "</tbody></table></div>"
    st.markdown(tbl, unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("#### ⚡ 오늘의 해야 할 일 (5)")
        rows = "".join(
            f'<div class="ar"><span class="d{a["dot"]}"></span>'
            f'<span style="flex:1">{a["text"]}</span>'
            f'<span style="font-size:10px;color:#9e9d98;background:#f0efe9;padding:1px 7px;border-radius:999px">{a["tag"]}</span></div>'
            for a in ACTIONS
        )
        st.markdown(f'<div class="card">{rows}</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown("#### 📧 매일 아침 8:00 이메일 보고서")
        st.markdown("""
        <div class="email-box">
            <div style="font-size:11px;color:#6b6a65;margin-bottom:8px">📎 나라장터 맞춤 공고 알림 예시</div>
            <div class="email-title">오늘의 나라장터 공고 — 5건</div>
            <div class="email-sub">2026-05-18 (월) 08:00 발송</div>
            <div class="email-item">
                <div class="email-item-t">2026년 OO구 공공시설 청소 용역</div>
                <div class="email-item-s">용역 · 서울 · 42,000,000원 · <span style="color:#8b2020;font-weight:600">D-1</span></div>
            </div>
            <div class="email-item">
                <div class="email-item-t">OO교육청 환경정비 용역</div>
                <div class="email-item-s">용역 · 서울 · 55,000,000원 · D-3</div>
            </div>
            <div style="text-align:center;font-size:12px;color:#1a56a0;margin-top:8px">+ 3건 더 보기 →</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        email_val = st.text_input("이메일 주소", placeholder="example@company.com", label_visibility="collapsed")
        if st.button("매일 아침 보고서 받기", use_container_width=True):
            st.success("✅ 등록 완료!" if email_val else "이메일을 입력해주세요.")


# ══════════════════════════════════════════════════════════════
# 화면 2 — 공고 검색
# ══════════════════════════════════════════════════════════════
elif menu == "🔍 공고 검색":
    st.markdown("# 🔍 공고 검색")

    f1, f2, f3 = st.columns(3)
    with f1: type_f  = st.multiselect("업무구분", ["용역","물품","공사"], default=["용역"])
    with f2: region_f= st.multiselect("지역구분", ["서울","경기","부산","인천"], default=["서울","경기"])
    with f3: status_f= st.selectbox("AI 매칭 결과", ["전체","지원 가능","검토 필요","보류"])

    st.markdown("**자주 찾는 공고 모아보기**")
    qc = st.columns(6)
    for col, label in zip(qc, ["3일 이내 마감","전국무관","제한경쟁","수의계약","일반경쟁","최신순"]):
        with col: st.button(label, use_container_width=True)

    st.markdown("**업종 대표 키워드**")
    kc = st.columns(5)
    for col, kw in zip(kc, ["청소용역","경비용역","소프트웨어개발","시스템 유지보수","전기공사"]):
        with col: st.button(kw, use_container_width=True)

    st.markdown("**발주기관으로 찾기**")
    oc = st.columns(5)
    for col, org in zip(oc, ["경찰청","서울특별시","국방과학연구소","조달청","교육청"]):
        with col: st.button(org, use_container_width=True)

    st.divider()

    filtered = [n for n in NOTICES
                if (not type_f or n["type"] in type_f)
                and (not region_f or n["region"] in region_f)
                and (status_f == "전체" or n["status"] == status_f)]
    filtered.sort(key=lambda x: x["dday"])

    st.markdown(f"**검색 결과 {len(filtered)}건**")
    if filtered:
        tbl = """<div class="card"><table class="tbl"><thead><tr>
            <th>공고명</th><th>업무구분</th><th>지역</th><th>추정가격</th>
            <th>마감</th><th>경쟁유형</th><th>AI 매칭</th>
        </tr></thead><tbody>"""
        for n in filtered:
            tbl += f"""<tr>
                <td style="font-weight:500">{n['title']}</td>
                <td><span class="badge bgray">{n['type']}</span></td>
                <td>{n['region']}</td>
                <td>{n['amount']:,.0f}원</td>
                <td>{dday_badge(n['dday'])}</td>
                <td style="font-size:11px;color:#6b6a65">{n['competition']}</td>
                <td>{badge(n['status'])}</td>
            </tr>"""
        tbl += "</tbody></table></div>"
        st.markdown(tbl, unsafe_allow_html=True)
    else:
        st.info("검색 결과가 없습니다.")


# ══════════════════════════════════════════════════════════════
# 화면 3 — 관심 공고 (공고 상세)
# ══════════════════════════════════════════════════════════════
elif menu == "⭐ 관심 공고":
    st.markdown("# ⭐ 관심 공고")

    sel = st.selectbox("공고 선택", [n["title"] for n in NOTICES], label_visibility="collapsed")
    n = next(x for x in NOTICES if x["title"] == sel)

    hc1, hc2 = st.columns([5,1])
    with hc1:
        st.markdown(f"### {n['title']}")
        st.caption(f"공고번호: {n['id']} · {n['org']}")
    with hc2:
        st.markdown(f"<div style='text-align:right;margin-top:12px'>{badge(n['status'])}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 📄 공고 기본 정보")
        rows = [("공고일자",n["bid_start"]),("입찰 시작",n["bid_start"]),
                ("입찰 마감",n["bid_end"]),("개찰일시",n["open_dt"]),
                ("개찰장소",n["open_place"]),("공고기관",n["org"]),
                ("수요기관",n["demand_org"]),("입찰조건",n["competition"])]
        html = '<div class="card">' + "".join(
            f'<div class="pr"><span class="pr-l">{l}</span><span style="font-weight:500">{v}</span></div>'
            for l, v in rows) + '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with col2:
        st.markdown("##### 💰 금액 정보")
        amt_rows = [("추정가격",f"{n['amount']:,.0f}원"),
                    ("기초금액",f"{n['base']:,.0f}원"),
                    ("낙찰하한율",f"{n['min_rate']}%")]
        html = '<div class="card">' + "".join(
            f'<div class="pr"><span class="pr-l">{l}</span><span style="font-weight:500">{v}</span></div>'
            for l, v in amt_rows) + '</div>'
        st.markdown(html, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="profit" style="margin-bottom:8px">
            <div class="profit-l">AI 예측 입찰가 범위</div>
            <div class="profit-v">{n['bid_low']:,.0f} ~ {n['bid_high']:,.0f}원</div>
            <div class="profit-s">평균 낙찰율 {n['avg_rate']}% 기준 · 유사 사례 {n['case_count']}건</div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div class="profit">
                <div class="profit-l">평균 낙찰율</div>
                <div class="profit-v" style="font-size:22px">{n['avg_rate']}%</div>
            </div>
            <div class="profit">
                <div class="profit-l">경쟁 강도</div>
                <div class="profit-v" style="font-size:22px;color:#7a4d0a">{n['comp_level']}</div>
                <div class="profit-s">평균 {n['comp_cnt']}개사</div>
            </div>
        </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("##### 📎 첨부파일")
        st.markdown("""<div class="card">
            <div class="pr"><span>📄 입찰공고문.pdf</span><span style="font-size:11px;color:#1a56a0">다운로드</span></div>
            <div class="pr"><span>📄 규격서_첨부1.hwpx</span><span style="font-size:11px;color:#1a56a0">다운로드</span></div>
            <div class="pr"><span>📄 규격서_첨부2.pdf</span><span style="font-size:11px;color:#1a56a0">다운로드</span></div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown("##### 🔗 비슷한 공고")
        sims = [x for x in NOTICES if x["id"] != n["id"] and x["type"] == n["type"]][:3]
        sim_html = '<div class="card">' + "".join(
            f'<div class="pr"><span style="font-size:12px">{s["title"]}</span>{dday_badge(s["dday"])}</div>'
            for s in sims) + '</div>'
        st.markdown(sim_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 화면 4 — 요건 매칭
# ══════════════════════════════════════════════════════════════
elif menu == "🎯 요건 매칭":
    st.markdown("# 🎯 요건 매칭")
    st.caption("AI가 첨부파일을 분석하여 우리 회사 조건과 비교합니다. 원문을 반드시 확인하세요.")

    sel = st.selectbox("분석할 공고", [n["title"] for n in NOTICES], label_visibility="collapsed")
    n = next(x for x in NOTICES if x["title"] == sel)

    st.markdown(f"**{n['title']}** &nbsp; {badge(n['status'])}", unsafe_allow_html=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    col_t, col_c = st.columns([3, 2])

    with col_t:
        st.markdown("##### 요건 항목 분석표")
        tbl = """<div class="card"><table class="tbl"><thead><tr>
            <th>요건 항목</th><th>공고 요건 (AI 추출)</th><th>우리 회사 보유</th>
            <th>충족 상태</th><th>경쟁 강도</th><th>근거 (원문)</th>
        </tr></thead><tbody>"""
        for r in n["reqs"]:
            tbl += f"""<tr>
                <td style="font-weight:500">{r['item']}</td>
                <td style="font-size:11px">{r['required']}</td>
                <td style="font-size:11px">{r['company']}</td>
                <td>{chip(r['status'])}</td>
                <td style="font-size:11px;color:#6b6a65">{r['compete']}</td>
                <td style="font-size:10px;color:#1a56a0;cursor:pointer">{r['source']}</td>
            </tr>"""
        tbl += "</tbody></table></div>"
        st.markdown(tbl, unsafe_allow_html=True)
        st.warning("⚠️ AI 분석 결과는 참고용입니다. 최종 판단은 반드시 원문을 확인하세요.")

    with col_c:
        st.markdown("##### 통합 매칭 결과")
        score = n["score"]
        ok_cnt   = sum(1 for r in n["reqs"] if r["status"]=="ok")
        warn_cnt = sum(1 for r in n["reqs"] if r["status"]=="warn")
        ng_cnt   = sum(1 for r in n["reqs"] if r["status"]=="ng")

        fig = go.Figure(go.Pie(
            values=[ok_cnt, warn_cnt, ng_cnt],
            labels=["충족","확인 필요","미충족"],
            hole=0.65,
            marker_colors=["#1f6b2e","#ef9f27","#e24b4a"],
            textinfo="none",
            hovertemplate="%{label}: %{value}건<extra></extra>",
        ))
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25,
                        xanchor="center", x=0.5, font=dict(size=11)),
            margin=dict(t=10, b=50, l=10, r=10), height=230,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text=f"<b>{score}점</b>", x=0.5, y=0.5,
                              font_size=24, showarrow=False)],
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        # 다음 액션 추천
        if score >= 80:
            msg = "✅ <b>지원 가능</b> — 서류 준비 후 바로 지원을 권장합니다."
            bg, border = "#e6f4ea", "#1f6b2e"
        elif score >= 50:
            msg = "⚠️ <b>검토 필요</b> — 확인 필요 항목 해소 후 판단하세요."
            bg, border = "#fdf3e0", "#ef9f27"
        else:
            msg = "🚫 <b>보류 권장</b> — 요건 미충족 항목이 많아 이번 입찰은 보류를 권장합니다."
            bg, border = "#fdeaea", "#e24b4a"

        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:8px;
                    padding:12px 14px;font-size:12px;line-height:1.8;margin-top:4px">
            {msg}<br>
            <span style="font-size:11px;color:#6b6a65">충족 {ok_cnt}건 · 확인필요 {warn_cnt}건 · 미충족 {ng_cnt}건</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 화면 5 — 회사 프로필
# ══════════════════════════════════════════════════════════════
elif menu == "🏢 회사 프로필":
    st.markdown("# 🏢 회사 프로필")
    st.caption("요건 매칭 및 AI 분석의 기준값으로 사용됩니다.")

    col_p, col_s = st.columns([3, 2])

    with col_p:
        st.markdown("##### 기본 정보")
        with st.form("profile_form"):
            st.text_input("회사명", value=COMPANY["name"])
            st.text_input("업종", value=COMPANY["industry"])
            st.text_input("세부품명번호", value=COMPANY["product_no"])
            st.text_input("품명", value=COMPANY["product_name"])
            st.selectbox("지역", ["서울특별시","경기도","부산광역시","인천광역시"], index=0)
            st.markdown("**예산 금액대**")
            bc1, bc2 = st.columns(2)
            with bc1: st.number_input("최소 (원)", value=COMPANY["budget_min"], step=1_000_000, format="%d")
            with bc2: st.number_input("최대 (원)", value=COMPANY["budget_max"], step=1_000_000, format="%d")
            st.form_submit_button("저장", use_container_width=True)

    with col_s:
        st.markdown("##### 보유 현황 (요건 매칭 기준값)")
        st.markdown("""<div class="card">
            <div class="pr"><span class="pr-l">사업 실적</span><span style="font-weight:500">4.2억 (최근 3년)</span></div>
            <div class="pr"><span class="pr-l">보유 면허</span><span style="font-weight:500">청소업, 시설관리업</span></div>
            <div class="pr"><span class="pr-l">직접생산확인증명서</span><span class="warn">확인 필요</span></div>
            <div class="pr"><span class="pr-l">최대 수행 납기</span><span style="font-weight:500">120일</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("##### 설정")
        st.markdown("""<div class="card">
            <div class="pr"><span class="pr-l">이메일 알림</span><span class="ok">활성화</span></div>
            <div class="pr"><span class="pr-l">알림 시간</span><span style="font-weight:500">매일 08:00</span></div>
            <div class="pr"><span class="pr-l">계정 상태</span><span class="ok">로그인 중</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("##### 계정")
        st.button("회원 정보 수정", use_container_width=True)
        st.button("로그아웃", use_container_width=True)
