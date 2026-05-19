import streamlit as st

st.set_page_config(
    page_title="입찰 AI 대시보드",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 전역 CSS ──────────────────────────────────────────────────────────────────
# 남색 팔레트: 메인 #0a1628 / 사이드바 #081020 / 카드 #0f1e36 / 서브카드 #0c1830
st.markdown("""
<style>
/* ── 기본 배경/폰트 ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a1628 !important;
    color: #cdd8ee;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
}
[data-testid="stSidebar"] {
    background-color: #081020 !important;
    border-right: 1px solid #162240;
}
[data-testid="stSidebar"] * { color: #8aa0c0 !important; font-size: 12px !important; }

/* ── 사이드바 헤더 ── */
.sidebar-title {
    font-size: 11px !important; font-weight: 700;
    color: #c0d0e8 !important;
    line-height: 1.5; margin-bottom: 3px;
}
.sidebar-sub {
    font-size: 10px !important; color: #4a6080 !important; margin-bottom: 16px;
}
.sidebar-divider { border-top: 1px solid #162240; margin: 8px 0 12px; }

/* ── Streamlit 사이드바 버튼 (네비) ── */
div[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    background: transparent !important;
    border: none !important;
    color: #6a88aa !important;
    border-radius: 5px !important;
    font-size: 11px !important;
    padding: 6px 10px !important;
    text-align: left !important;
    width: 100% !important;
    justify-content: flex-start !important;
    font-weight: 400 !important;
}
div[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: #101e38 !important;
    color: #a0c0e0 !important;
    border: none !important;
}

/* ── 회사 정보 ── */
.sidebar-company {
    font-size: 10px !important; color: #3a5070 !important;
    margin-top: 18px; padding-top: 12px;
    border-top: 1px solid #162240;
    line-height: 1.7;
}
.sidebar-company strong { color: #7090b0 !important; font-size: 11px !important; }

/* ── 페이지 헤더 ── */
.page-header { margin-bottom: 4px; }
.page-header h2 {
    font-size: 17px; font-weight: 700; color: #d0dcf0; margin: 0;
}
.page-subtext { font-size: 11px; color: #4a6080; margin-top: 3px; }

/* ── 지표 카드 ── */
.metric-card {
    background: #0f1e36; border: 1px solid #1a3060;
    border-radius: 9px; padding: 14px 18px;
}
.metric-label { font-size: 10px; color: #4a6080; margin-bottom: 5px; }
.metric-value { font-size: 28px; font-weight: 800; line-height: 1; }
.mv-red    { color: #e84040; }
.mv-amber  { color: #d89010; }
.mv-gray   { color: #7080a0; }
.mv-blue   { color: #3a8ef0; }

/* ── 섹션 제목 ── */
.section-title {
    font-size: 13px; font-weight: 700; color: #a0b8d8;
    margin: 20px 0 10px;
    display: flex; align-items: center; gap: 6px;
}

/* ── 공고 테이블 ── */
.bid-table {
    width: 100%; border-collapse: collapse;
    background: #0f1e36; border-radius: 9px; overflow: hidden;
}
.bid-table th {
    padding: 8px 12px; font-size: 10px; color: #4a6080;
    font-weight: 600; background: #0c1830;
    border-bottom: 1px solid #1a3060; text-align: left;
}
.bid-table td {
    padding: 9px 12px; font-size: 11px; color: #a0b8d0;
    border-bottom: 1px solid #122040; vertical-align: middle;
}
.bid-table tr:last-child td { border-bottom: none; }
.bid-table tr:hover td { background: #122040; }

/* ── 배지 ── */
.badge {
    display: inline-block; padding: 2px 8px;
    border-radius: 99px; font-size: 10px; font-weight: 700;
    white-space: nowrap;
}
.badge-green  { background: #0e2e1c; color: #2ecc60; border: 1px solid #1a5030; }
.badge-amber  { background: #2e1e04; color: #d89010; border: 1px solid #5a3a08; }
.badge-red    { background: #2e0c0c; color: #e84040; border: 1px solid #5a1818; }
.badge-gray   { background: #101828; color: #6080a0; border: 1px solid #1e3050; }
.badge-blue   { background: #081a38; color: #3a8ef0; border: 1px solid #123470; }

/* ── 마감 D-day ── */
.dday {
    display: inline-block; padding: 2px 7px;
    border-radius: 5px; font-size: 10px; font-weight: 700;
}
.dday-urgent { background: #2e0c0c; color: #e84040; }
.dday-warn   { background: #2e1e04; color: #d89010; }
.dday-safe   { background: #081838; color: #3a8ef0; }

/* ── 카드 (일반) ── */
.content-card {
    background: #0f1e36; border: 1px solid #1a3060;
    border-radius: 9px; padding: 16px 18px; margin-bottom: 12px;
}
.content-card h4 {
    font-size: 12px; font-weight: 600; color: #8aaac8;
    margin: 0 0 12px;
}

/* ── 액션 아이템 ── */
.action-item {
    padding: 9px 12px; border-radius: 7px;
    border-left: 3px solid; margin-bottom: 7px;
    background: #0c1830;
}
.action-item .action-team {
    font-size: 9px; font-weight: 700;
    text-transform: uppercase; margin-bottom: 3px; letter-spacing: .05em;
}
.action-item .action-text { font-size: 11px; color: #8aaac0; line-height: 1.5; }
.action-item .action-sub  { font-size: 10px; color: #3a5070; margin-top: 2px; }

.ai-bid   { border-color: #3a8ef0; }
.ai-bid   .action-team { color: #3a8ef0; }
.ai-ops   { border-color: #20a860; }
.ai-ops   .action-team { color: #20a860; }
.ai-fin   { border-color: #d89010; }
.ai-fin   .action-team { color: #d89010; }
.ai-admin { border-color: #8860d8; }
.ai-admin .action-team { color: #8860d8; }

/* ── chunk 뷰어 ── */
.chunk-item {
    border-radius: 7px; border-left: 3px solid;
    padding: 9px 12px; margin-bottom: 7px;
    background: #0c1830;
}
.chunk-meta { font-size: 9px; color: #3a8ef0; font-family: monospace; margin-bottom: 4px; }
.chunk-text { font-size: 11px; color: #8aaac0; line-height: 1.6; }
.hl-green { color: #2ecc60; font-weight: 600; }
.hl-amber { color: #d89010; font-weight: 600; }
.hl-blue  { color: #3a8ef0; font-weight: 600; }
.chunk-ok   { border-color: #20a860; }
.chunk-warn { border-color: #d89010; }
.chunk-info { border-color: #3a8ef0; }

/* ── 매칭 행 ── */
.match-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 7px 10px; border-radius: 6px;
    background: #0c1830; margin-bottom: 4px; font-size: 11px;
}
.match-label { color: #5070a0; }
.match-ok    { color: #2ecc60; font-weight: 600; }
.match-warn  { color: #d89010; font-weight: 600; }
.match-no    { color: #e84040; font-weight: 600; }

/* ── 폼 요소 ── */
.form-input {
    width: 100%; padding: 7px 10px;
    background: #0c1830; border: 1px solid #1a3060;
    border-radius: 6px; color: #a0b8d0;
    font-size: 11px; margin-bottom: 9px; box-sizing: border-box;
}
.form-input.disabled { color: #304060; }

/* ── 지역 그리드 ── */
.region-grid { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 7px; }
.region-tag {
    padding: 4px 10px; border-radius: 5px;
    font-size: 11px; cursor: pointer;
    border: 1px solid #1a3060; color: #4a6080; background: #0c1830;
}
.region-tag.on {
    background: #081838; border-color: #1a4480;
    color: #3a8ef0; font-weight: 600;
}

/* ── 실적 행 ── */
.record-row {
    display: grid; grid-template-columns: 1fr 80px 60px 30px;
    gap: 8px; align-items: center;
    padding: 7px 10px; background: #0c1830;
    border-radius: 6px; margin-bottom: 4px; font-size: 11px;
}
.record-del { color: #e84040; cursor: pointer; text-align: right; }

/* ── ACL 매트릭스 ── */
.acl-table {
    width: 100%; border-collapse: collapse;
    background: #0f1e36; border-radius: 9px; overflow: hidden;
}
.acl-table th {
    padding: 8px 10px; font-size: 10px;
    background: #0c1830; color: #4a6080;
    border-bottom: 1px solid #1a3060; text-align: center;
}
.acl-table th:first-child { text-align: left; }
.acl-table td {
    padding: 8px 10px; font-size: 11px; color: #8aaac0;
    border-bottom: 1px solid #122040; text-align: center;
}
.acl-table td:first-child { text-align: left; }
.acl-table tr:last-child td { border-bottom: none; }
.acl-ok   { color: #2ecc60; font-size: 14px; }
.acl-off  { color: #1a3060; font-size: 14px; }
.acl-part { color: #7080a0; font-size: 14px; }

/* ── 팀원 행 ── */
.member-row {
    display: grid; grid-template-columns: 30px 1fr 110px 110px 90px 30px;
    gap: 8px; align-items: center;
    padding: 9px 12px; background: #0c1830;
    border-radius: 7px; margin-bottom: 5px; font-size: 11px;
}
.avatar {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700;
}
.av-admin { background: #1e1038; color: #8860d8; }
.av-bid   { background: #081838; color: #3a8ef0; }
.av-ops   { background: #081e10; color: #20a860; }
.av-fin   { background: #281800; color: #d89010; }
.av-gen   { background: #101828; color: #5070a0; }

/* ── 인라인 구분선 ── */
.hdivider { border-top: 1px solid #122040; margin: 12px 0; }

/* ── Streamlit 버튼 (메인 영역) ── */
div[data-testid="stMain"] div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid #1a3060 !important;
    color: #6090b8 !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    padding: 5px 14px !important;
}
div[data-testid="stMain"] div[data-testid="stButton"] > button:hover {
    background: #101e38 !important;
    color: #90b8d8 !important;
    border-color: #2a4a80 !important;
}

/* ── Streamlit 기본 텍스트 요소 크기 ── */
.stTextInput input, .stSelectbox select, .stRadio label,
[data-testid="stRadio"] label { font-size: 11px !important; }
.stTextInput label, .stSelectbox label { font-size: 10px !important; color: #4a6080 !important; }

/* ── 여백 ── */
.block-container { padding-top: 48px !important; padding-bottom: 16px !important; }
section[data-testid="stSidebar"] > div { padding-top: 18px !important; }
</style>
""", unsafe_allow_html=True)


# ── session_state 초기화 ───────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "dashboard"


def nav(p):
    st.session_state.page = p


# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">Azure 기반 공공조달<br>시설관리 입찰 대응 AI E2E 시스템</div>
    <div class="sidebar-sub">End-to-End 입찰 자동화</div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    pages = [
        ("dashboard",    "데일리 액션 대시보드"),
        ("bid_search",   "공고 검색"),
        ("bid_detail",   "공고 상세 / 근거 뷰어"),
        ("action",       "오늘의 액션"),
        ("profile",      "회사 프로필"),
        ("team",         "팀 관리 / ACL"),
        ("settings",     "설정"),
    ]

    for key, label in pages:
        active = "active" if st.session_state.page == key else ""
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            nav(key)

    st.markdown("""
    <div class="sidebar-company">
        <strong>삼구아이앤씨(주)</strong><br>
        업종: FM·아웃소싱·시설관리<br>
        지역: 전국 주요 거점
    </div>
    """, unsafe_allow_html=True)


# ── 헬퍼 ─────────────────────────────────────────────────────────────────────
def badge(text, kind="gray"):
    return f'<span class="badge badge-{kind}">{text}</span>'

def dday(text, level="safe"):
    return f'<span class="dday dday-{level}">{text}</span>'

def section(icon, title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 1. 데일리 액션 대시보드
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    st.markdown("""
    <div class="page-header">
        <h2>데일리 액션 대시보드</h2>
        <div class="page-subtext">2026년 5월 18일 (월) · 오늘 수집 기준 5건</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "긴급 처리 (D-3)", "2", "mv-red"),
        (c2, "검토 추천 (4-7일)", "2", "mv-amber"),
        (c3, "보류 추천", "1", "mv-gray"),
        (c4, "전체 확인 공고", "5", "mv-blue"),
    ]
    for col, label, val, cls in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value {cls}">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    section("📌", "오늘 우선 확인해야 할 공고")

    bids = [
        ("#1", "2026년 OO구 공공시설 청소 용역",   "20260518-001", "OO구청",  "D-1",  "3,9*,***,***", "지원 가능", "green",  "urgent"),
        ("#2", "OO공단 시설관리 위탁 운영 용역",    "20260518-004", "OO공단",  "D-2", "11*,***,***,***", "보류",     "gray",   "urgent"),
        ("#3", "OO교육청 환경정비 용역",             "20260518-005", "OO교육청","D-3",  "5*,***,***,***", "검토 필요","amber",  "urgent"),
        ("#4", "OO병원 환경미화 용역 입찰",          "20260518-002", "OO병원",  "D-7",  "8*,***,***,***", "검토 필요","amber",  "warn"),
        ("#5", "OO시 행정복지센터 청소 용역",        "20260518-003", "OO시",    "D-14", "2*,***,***,***", "지원 가능","green",  "safe"),
    ]

    header = """
    <table class="bid-table">
    <thead><tr>
        <th>우선순위</th><th>공고명</th><th>공고번호</th>
        <th>수요기관</th><th>마감일</th><th>AI 입찰가 (추정)</th><th>AI 매칭 결과</th>
    </tr></thead><tbody>
    """
    rows = ""
    for rank, name, num, org, dd, price, verdict, vkind, dlevel in bids:
        rank_color = "#f04040" if rank in ("#1","#2","#3") else "#6a7a92"
        rows += f"""<tr>
            <td style="color:{rank_color};font-weight:700">{rank}</td>
            <td style="color:#d0daf0;font-weight:500">{name}</td>
            <td style="color:#4a5a72;font-size:12px">{num}</td>
            <td>{org}</td>
            <td>{dday(dd, dlevel)}</td>
            <td style="font-family:monospace;color:#8aaac8">{price}원 추정</td>
            <td>{badge(verdict, vkind)}</td>
        </tr>"""
    st.markdown(header + rows + "</tbody></table>", unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        section("⚡", "오늘의 해야 할 일 (5)")
        actions = [
            ("ai-bid",   "입찰/영업팀", "OO구 청소 용역 — 참가자격 서류 확인 (D-1)", "20260518-001"),
            ("ai-ops",   "운영팀",     "상주 인력 1명 투입 가능 여부 확인",           "20260518-001"),
            ("ai-fin",   "재무팀",     "입찰보증금 5% 산정 및 가용 예산 확인",        "20260518-001"),
            ("ai-admin", "총무팀",     "직접생산확인증명서 발급 요청",                 "20260518-001"),
            ("ai-bid",   "입찰/영업팀","OO교육청 환경정비 — 실적 요건 재검토",        "20260518-005"),
        ]
        for cls, team, text, num in actions:
            st.markdown(f"""
            <div class="action-item {cls}">
                <div class="action-team">{team}</div>
                <div class="action-text">{text}</div>
                <div class="action-sub">{num}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        section("📧", "매일 아침 8:00 이메일 보고서")
        st.markdown("""
        <div class="content-card">
            <h4>자동 발송 설정</h4>
            <div class="match-row">
                <span class="match-label">발송 시각</span>
                <span class="match-ok">매일 08:00</span>
            </div>
            <div class="match-row">
                <span class="match-label">수신자</span>
                <span style="color:#8aaac8">입찰팀장, 대표</span>
            </div>
            <div class="match-row">
                <span class="match-label">포함 내용</span>
                <span style="color:#8aaac8">긴급 공고 · 오늘의 액션</span>
            </div>
            <div class="match-row">
                <span class="match-label">Teams 알림</span>
                <span class="match-ok">연동됨</span>
            </div>
            <div class="match-row">
                <span class="match-label">마지막 발송</span>
                <span style="color:#3a5a7a">2026-05-18 08:00</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("지금 즉시 발송")


# ══════════════════════════════════════════════════════════════════════════════
# 2. 공고 검색
# ══════════════════════════════════════════════════════════════════════════════
def page_bid_search():
    st.markdown("""
    <div class="page-header">
        <h2>공고 검색</h2>
        <div class="page-subtext">나라장터 연동 · 실시간 수집</div>
    </div>
    """, unsafe_allow_html=True)

    col_q, col_btn = st.columns([4, 1])
    with col_q:
        st.text_input("", placeholder="공고명, 기관명, 공고번호로 검색...", label_visibility="collapsed")
    with col_btn:
        st.button("🔍 검색", use_container_width=True)

    cf1, cf2, cf3, cf4 = st.columns(4)
    with cf1:
        st.selectbox("판정 필터", ["전체", "지원 가능", "검토 필요", "보류"], label_visibility="collapsed")
    with cf2:
        st.selectbox("마감일", ["전체", "D-3 이내", "D-7 이내", "D-14 이내"], label_visibility="collapsed")
    with cf3:
        st.selectbox("금액 범위", ["전체", "1억 미만", "1~5억", "5억 이상"], label_visibility="collapsed")
    with cf4:
        st.selectbox("지역", ["전체", "서울", "경기", "인천"], label_visibility="collapsed")

    section("📄", "검색 결과 (5건)")

    bids = [
        ("2026년 OO구 공공시설 청소 용역",   "20260518-001", "OO구청", "D-1",  "42,000,000", "지원 가능", "green",  "urgent"),
        ("OO공단 시설관리 위탁 운영 용역",    "20260518-004", "OO공단", "D-2", "120,000,000", "보류",     "gray",   "urgent"),
        ("OO교육청 환경정비 용역",             "20260518-005", "OO교육청","D-3", "55,000,000", "검토 필요","amber",  "urgent"),
        ("OO병원 환경미화 용역 입찰",          "20260518-002", "OO병원", "D-7", "85,000,000", "검토 필요","amber",  "warn"),
        ("OO시 행정복지센터 청소 용역",        "20260518-003", "OO시",   "D-14","31,000,000", "지원 가능","green",  "safe"),
    ]

    header = """
    <table class="bid-table"><thead><tr>
        <th>공고명</th><th>공고번호</th><th>수요기관</th>
        <th>마감일</th><th>추정가격</th><th>AI 매칭</th>
    </tr></thead><tbody>
    """
    rows = ""
    for name, num, org, dd, price, verdict, vkind, dlevel in bids:
        rows += f"""<tr>
            <td style="color:#d0daf0;font-weight:500">{name}</td>
            <td style="color:#4a5a72;font-size:12px">{num}</td>
            <td>{org}</td>
            <td>{dday(dd, dlevel)}</td>
            <td>{price}원</td>
            <td>{badge(verdict, vkind)}</td>
        </tr>"""
    st.markdown(header + rows + "</tbody></table>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. 공고 상세 / 근거 뷰어
# ══════════════════════════════════════════════════════════════════════════════
def page_bid_detail():
    st.markdown("""
    <div class="page-header">
        <h2>공고 상세 / 근거 뷰어</h2>
        <div class="page-subtext">OO구 공공시설 청소 용역 · chunk/rule 기반 분석</div>
    </div>
    """, unsafe_allow_html=True)

    # 헤더 정보
    hc1, hc2, hc3, hc4 = st.columns([3, 1, 1, 1])
    with hc1:
        st.markdown("""
        <div class="content-card" style="margin-bottom:0">
            <div style="font-size:16px;font-weight:700;color:#e0eaff;margin-bottom:8px">
                2026년 OO구 공공시설 청소 용역
            </div>
            <div style="font-size:12px;color:#6a7a92;line-height:1.9">
                📌 수요기관: OO구청 &nbsp;|&nbsp; 🔢 공고번호: 20260518-001
            </div>
        </div>
        """, unsafe_allow_html=True)
    with hc2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">마감일</div>
            <div class="metric-value mv-red" style="font-size:20px">D-1</div>
            <div style="font-size:11px;color:#6a7a92;margin-top:4px">2026-05-19</div>
        </div>
        """, unsafe_allow_html=True)
    with hc3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AI 입찰가 (추정)</div>
            <div style="font-size:14px;font-weight:700;color:#8aaac8;margin-top:4px;font-family:monospace">3,9*,***,***원대</div>
        </div>
        """, unsafe_allow_html=True)
    with hc4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AI 판정</div>
            <div style="margin-top:6px">{badge('지원 가능','green')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        section("📏", "공고 상세")
        rc1, rc2 = st.columns(2)
        rules = [
            (rc1, "마감일",      "2026-05-19",      "#f04040"),
            (rc2, "계약기간",    "2026-07~2027-06", "#c0d0e8"),
            (rc1, "입찰보증금",  "입찰금액의 5%",   "#e8a020"),
            (rc2, "계약보증금",  "계약금액의 10%",  "#c0d0e8"),
            (rc1, "투입 인력",   "상주 1명 이상",   "#c0d0e8"),
            (rc2, "지역 제한",   "서울시 (보유)",   "#34d870"),
        ]
        for col, k, v, color in rules:
            with col:
                st.markdown(f"""
                <div class="content-card" style="padding:12px 14px;margin-bottom:8px">
                    <div style="font-size:11px;color:#6a7a92;margin-bottom:4px">{k}</div>
                    <div style="font-size:13px;font-weight:600;color:{color}">{v}</div>
                </div>
                """, unsafe_allow_html=True)

        section("🗂️", "분석 요약")
        chunks = [
            ("chunk", "[chunk_042, line 12–15]", "ok",
             '수행 업종: <span class="hl-green">건물위생관리업</span>, <span class="hl-green">시설경비업</span> 보유 자격과 일치.'),
            ("chunk", "[chunk_058, line 3–5]", "warn",
             '입찰보증금 <span class="hl-amber">5%</span> 납부 필요 — 재무팀 가용 예산 확인 필요.'),
            ("chunk", "[chunk_071, line 7–9]", "ok",
             '최근 3년 내 유사 실적 1건 이상 — <span class="hl-green">2024년 OO청사 용역 실적 적용 가능</span>.'),
            ("chunk", "[chunk_089, line 1–4]", "info",
             '상주 인력 <span class="hl-blue">1명 이상</span> — 현장 교대근무 가능 여부 운영팀 확인 필요.'),
        ]
        for _, meta, cls, text in chunks:
            st.markdown(f"""
            <div class="chunk-item chunk-{cls}">
                <div class="chunk-meta">{meta}</div>
                <div class="chunk-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

        section("💬", "RAG 질문하기")
        st.text_input("", placeholder="예: 소방시설 자격이 꼭 필요한가요?", label_visibility="collapsed", key="rag_input")
        st.button("질문 전송", key="rag_send")
        st.markdown('<div style="font-size:11px;color:#4a5a72;margin-top:4px">3순위 확장 — Azure AI Search 기반 RAG</div>', unsafe_allow_html=True)

    with right:
        section("🏢", "회사 프로필 매칭")
        matches = [
            ("건물위생관리업",  "✅ 보유",         "match-ok"),
            ("시설경비업",      "✅ 보유",         "match-ok"),
            ("전기안전관리업",  "✅ 보유",         "match-ok"),
            ("소방시설관리업",  "⚠️ 미보유(필수 아님)", "match-warn"),
            ("유사 실적 (3년)", "✅ 1건 적용",     "match-ok"),
            ("지역 요건 (서울)","✅ 충족",         "match-ok"),
            ("상주 인력 (1명)", "⚠️ 운영팀 확인", "match-warn"),
        ]
        for label, status, cls in matches:
            st.markdown(f"""
            <div class="match-row">
                <span class="match-label">{label}</span>
                <span class="{cls}">{status}</span>
            </div>
            """, unsafe_allow_html=True)

        section("✅", "부서별 오늘의 액션")
        actions = [
            ("ai-bid",   "입찰/영업팀", "참가자격 서류 최종 확인 · 실적증명서 발급"),
            ("ai-ops",   "운영팀",      "상주 인력 투입 가능 여부 · 교대근무 일정"),
            ("ai-fin",   "재무팀",      "입찰보증금 5% 산정 · 계약보증금 검토"),
            ("ai-admin", "총무팀",      "직접생산확인증명서, 실적증명서 준비"),
        ]
        for cls, team, text in actions:
            st.markdown(f"""
            <div class="action-item {cls}">
                <div class="action-team">{team}</div>
                <div class="action-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        bc1, bc2, bc3 = st.columns(3)
        with bc1: st.button("Teams 전송", key="teams_btn")
        with bc2: st.button("HWP 원문", key="hwp_btn")
        with bc3: st.button("나라장터", key="g2b_btn")


# ══════════════════════════════════════════════════════════════════════════════
# 4. 오늘의 액션
# ══════════════════════════════════════════════════════════════════════════════
def page_action():
    st.markdown("""
    <div class="page-header">
        <h2>오늘의 액션</h2>
        <div class="page-subtext">2026년 5월 18일 (월) · LLM 자동 생성</div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("", ["👤 개인용 모드", "🏢 기업용 모드"], horizontal=True, label_visibility="collapsed")

    sc1, sc2, sc3 = st.columns(3)
    for col, val, label, color in [
        (sc1, "9", "전체 액션",   "#c0d0e8"),
        (sc2, "3", "완료",        "#34d870"),
        (sc3, "6", "남은 액션",   "#f04040"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color}">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if "개인용" in mode:
        section("👤", "오늘 내가 할 일")
        personal_actions = [
            (False, "ai-bid",   "참가자격 서류 최종 확인 — 직접생산확인증명서 발급 요청",   "OO구 공공시설 청소 용역", "D-1", "urgent"),
            (False, "ai-fin",   "입찰보증금 5% 가용 여부 확인 및 준비",                      "OO구 공공시설 청소 용역", "D-1", "urgent"),
            (False, "ai-bid",   "OO교육청 — 소방시설관리업 자격 보완 가능 여부 검토",        "OO교육청 환경정비 용역",  "D-3", "urgent"),
            (False, "ai-ops",   "상주 인력 투입 가능 여부 확인 및 운영팀 협의",              "OO구 공공시설 청소 용역", "D-1", "urgent"),
            (False, "ai-admin", "실적증명서 발급 요청 및 제출서류 준비",                      "OO구 공공시설 청소 용역", "D-1", "urgent"),
            (True,  "ai-bid",   "나라장터 신규 공고 수집 확인",                               "시스템 자동 수집",        "",    "safe"),
            (True,  "ai-bid",   "기장군청 청사관리 — 지원 가능 판정 확인",                   "기장군청 청사관리 용역",  "",    "safe"),
            (False, "ai-fin",   "OO병원 환경미화 — 예산 검토 (D-7)",                          "OO병원 환경미화 용역",    "D-7", "warn"),
            (False, "ai-admin", "OO시 행정복지센터 — 제출서류 사전 확인 (D-14)",              "OO시 행정복지센터 청소",  "D-14","safe"),
        ]
        for done, cls, text, bid, dd, dlevel in personal_actions:
            done_style = "text-decoration:line-through;color:#4a5a72;" if done else ""
            dd_html = f" &nbsp;{dday(dd, dlevel)}" if dd else ""
            checkmark = "✅ " if done else "◻️ "
            st.markdown(f"""
            <div class="action-item {cls}" style="{'opacity:.6' if done else ''}">
                <div class="action-team">{'완료' if done else '미완료'}</div>
                <div class="action-text" style="{done_style}">{checkmark}{text}{dd_html}</div>
                <div class="action-sub">{bid}</div>
            </div>
            """, unsafe_allow_html=True)

    else:  # 기업용
        section("🏢", "팀별 오늘 액션")

        team_actions = {
            "입찰/영업팀": {
                "color": "#4a9eff", "cls": "ai-bid",
                "items": [
                    (False, "OO구 청소 용역 — 참가자격 및 유사 실적 서류 확인", "D-1", "urgent"),
                    (False, "OO교육청 용역 입찰 참여 여부 최종 결정",           "D-3", "urgent"),
                ]
            },
            "운영팀": {
                "color": "#30c080", "cls": "ai-ops",
                "items": [
                    (False, "상주 인력 1명 투입 가능 여부 확인 · 교대근무 일정", "D-1", "urgent"),
                ]
            },
            "재무팀": {
                "color": "#e8a020", "cls": "ai-fin",
                "items": [
                    (True,  "입찰보증금 가용 예산 확인 완료", "", "safe"),
                ]
            },
            "총무팀": {
                "color": "#a080e8", "cls": "ai-admin",
                "items": [
                    (False, "직접생산확인증명서, 실적증명서 발급 요청", "D-1", "urgent"),
                    (True,  "사업자등록증 사본 준비 완료",               "", "safe"),
                ]
            },
        }

        for team, data in team_actions.items():
            st.markdown(f"""
            <div style="font-size:13px;font-weight:700;color:{data['color']};
                margin:16px 0 8px;padding-bottom:6px;border-bottom:1px solid #1e2840">
                {team}
            </div>
            """, unsafe_allow_html=True)
            for done, text, dd, dlevel in data["items"]:
                done_style = "text-decoration:line-through;color:#4a5a72;" if done else ""
                dd_html = f" &nbsp;{dday(dd, dlevel)}" if dd else ""
                checkmark = "✅ " if done else "◻️ "
                st.markdown(f"""
                <div class="action-item {data['cls']}" style="{'opacity:.6' if done else ''}">
                    <div class="action-text" style="{done_style}">{checkmark}{text}{dd_html}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.button("부서별 액션 Teams 전송", key="biz_teams")


# ══════════════════════════════════════════════════════════════════════════════
# 5. 회사 프로필
# ══════════════════════════════════════════════════════════════════════════════
def page_profile():
    st.markdown("""
    <div class="page-header">
        <h2>회사 프로필 설정</h2>
        <div class="page-subtext">입력 정보는 공고 매칭 시 자동 비교에 활용됩니다 · 삼구아이앤씨(주)</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 매칭 커버리지 + 회사 소개 요약 ──
    cov_col, info_col = st.columns([2, 3])
    with cov_col:
        st.markdown("""
        <div class="content-card" style="display:flex;align-items:center;gap:16px;padding:12px 16px">
            <div>
                <div style="font-size:10px;color:#4a6080">현재 매칭 커버리지</div>
                <div style="font-size:24px;font-weight:800;color:#2ecc60">94%</div>
            </div>
            <div style="flex:1">
                <div style="height:8px;background:#0a1828;border-radius:99px;overflow:hidden">
                    <div style="width:94%;height:100%;background:#1a9e60;border-radius:99px"></div>
                </div>
                <div style="font-size:10px;color:#3a5070;margin-top:4px">전국 영업망 · 다수 자격 보유로 높은 커버리지</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with info_col:
        st.markdown("""
        <div class="content-card" style="padding:12px 16px">
            <div style="font-size:10px;color:#4a6080;margin-bottom:6px;font-weight:600">기업 개요</div>
            <div style="font-size:11px;color:#8aaac0;line-height:1.8">
                청사 시설관리 · 아웃소싱 · FM 서비스 전문 대형 기업 &nbsp;|&nbsp;
                사업시설 유지·관리 서비스업 &nbsp;|&nbsp;
                <span style="color:#2ecc60;font-weight:600">중견기업</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 기본 정보 ──
    section("", "기본 정보")
    pc1, pc2 = st.columns(2)
    with pc1:
        st.text_input("회사명", value="삼구아이앤씨(주)")
        st.text_input("대표자명", value="김형규")
    with pc2:
        st.text_input("사업자등록번호", value="220-81-01574", disabled=True)
        st.text_input("설립연도", value="1976년 (업력 51년차)")
    st.text_input("본사 주소 (지역 요건 자동 판단)", value="서울특별시 중구 청계천로 100 시그니쳐타워 동관 6층")

    # ── 사업 영역 ──
    section("", "주요 사업 영역")
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px">
        <div class="content-card" style="padding:10px 14px;margin-bottom:0;text-align:center">
            <div style="font-size:10px;color:#4a6080;margin-bottom:4px">사업 분야 1</div>
            <div style="font-size:12px;font-weight:600;color:#8aaac8">청사 시설관리</div>
            <div style="font-size:10px;color:#3a5070;margin-top:3px">공공기관 · 정부청사</div>
        </div>
        <div class="content-card" style="padding:10px 14px;margin-bottom:0;text-align:center">
            <div style="font-size:10px;color:#4a6080;margin-bottom:4px">사업 분야 2</div>
            <div style="font-size:12px;font-weight:600;color:#8aaac8">아웃소싱 서비스</div>
            <div style="font-size:10px;color:#3a5070;margin-top:3px">HR · 경비 · 미화</div>
        </div>
        <div class="content-card" style="padding:10px 14px;margin-bottom:0;text-align:center">
            <div style="font-size:10px;color:#4a6080;margin-bottom:4px">사업 분야 3</div>
            <div style="font-size:12px;font-weight:600;color:#8aaac8">FM 통합서비스</div>
            <div style="font-size:10px;color:#3a5070;margin-top:3px">빌딩 · 산업 · 공공</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 보유 자격 ──
    section("", "보유 자격 / 업종 등록")
    st.markdown("""
    <div style="display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px">
        <span class="badge badge-blue">건물위생관리업</span>
        <span class="badge badge-blue">건물시설관리업</span>
        <span class="badge badge-blue">시설경비업</span>
        <span class="badge badge-blue">소방시설관리업</span>
        <span class="badge badge-blue">전기안전관리업</span>
        <span class="badge badge-blue">고압가스안전관리업</span>
        <span class="badge badge-blue">승강기유지관리업</span>
        <span class="badge badge-blue">직업소개사업</span>
        <span class="badge badge-blue">경비업(일반경비)</span>
    </div>
    <div style="font-size:10px;color:#3a5070">
        미보유 자격이 필수인 공고는 자동으로 '보류' 판정됩니다
    </div>
    """, unsafe_allow_html=True)
    st.button("+ 자격 추가", key="add_qual")

    # ── 영업 가능 지역 ──
    section("", "영업 가능 지역")
    all_regions = ["서울", "경기", "인천", "부산", "대구", "광주", "대전", "울산", "세종", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]
    active_regions = ["서울", "경기", "인천", "부산", "대구", "광주", "대전", "울산", "세종", "충북", "충남", "경남", "경북"]
    tags = "".join([
        f'<span class="region-tag {"on" if r in active_regions else ""}">{r}</span>'
        for r in all_regions
    ])
    st.markdown(f'<div class="region-grid">{tags}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#3a5070;margin-top:6px">전국 주요 거점 영업망 보유 · 지역 제한 공고 자동 필터링</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    ec1, ec2 = st.columns(2)
    with ec1:
        section("", "주요 수행 실적")
        st.markdown("""
        <div class="record-row" style="background:#0c1830;font-size:10px;color:#3a5070;font-weight:600">
            <span>용역명</span><span>발주처</span><span>연도</span><span></span>
        </div>
        """, unsafe_allow_html=True)
        records = [
            ("정부청사 시설관리 용역",        "조달청",           "2024"),
            ("공공기관 청사 FM 서비스",        "한국지역정보개발원","2023"),
            ("대형 공공건물 위생·경비 용역",   "서울특별시",       "2023"),
            ("공단 시설물 통합관리 용역",       "한국도로공사",     "2022"),
            ("국가기관 아웃소싱 서비스",        "행정안전부",       "2022"),
        ]
        for name, org, year in records:
            st.markdown(f"""
            <div class="record-row">
                <span style="color:#8aaac0">{name}</span>
                <span style="color:#4a6080">{org}</span>
                <span style="color:#4a6080">{year}</span>
                <span class="record-del">O</span>
            </div>
            """, unsafe_allow_html=True)
        st.button("+ 실적 추가", key="add_record")

    with ec2:
        section("", "보유 인력 규모")
        staff = [
            ("시설관리 인력",   "3,200명 이상"),
            ("경비·보안 인력",  "2,100명 이상"),
            ("미화·위생 인력",  "4,500명 이상"),
            ("전기·기계 기술자","480명"),
            ("소방설비 기술자", "210명"),
            ("관리·지원 인력",  "320명"),
        ]
        for k, v in staff:
            st.markdown(f"""
            <div class="match-row">
                <span class="match-label">{k}</span>
                <span style="color:#8aaac8;font-weight:600">{v}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<div class="hdivider"></div>', unsafe_allow_html=True)
        equip = [
            ("청소·방역 장비",   "1,800식"),
            ("전기설비 장비",    "650식"),
            ("소방점검 장비",    "420식"),
            ("승강기 유지보수",  "전국 거점"),
        ]
        for k, v in equip:
            st.markdown(f"""
            <div class="match-row">
                <span class="match-label">{k}</span>
                <span style="color:#8aaac8;font-weight:600">{v}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    sb1, sb2, _ = st.columns([1, 2, 4])
    with sb1:
        st.button("취소", key="cancel_profile")
    with sb2:
        st.button("저장 및 매칭 재실행", key="save_profile")


# ══════════════════════════════════════════════════════════════════════════════
# 6. 팀 관리 / ACL
# ══════════════════════════════════════════════════════════════════════════════
def page_team():
    st.markdown("""
    <div class="page-header">
        <h2>팀 관리 / ACL 권한</h2>
        <div class="page-subtext">역할별로 볼 수 있는 공고·액션 범위가 달라집니다</div>
    </div>
    """, unsafe_allow_html=True)

    th1, th2 = st.columns([5, 1])
    with th2:
        st.button("+ 멤버 초대", key="invite_member")

    section("", "멤버 목록")
    members = [
        ("주재륜", "관리자",     "Admin",       "av-admin", "방금 전"),
        ("정해원", "입찰/영업팀","Bid Manager", "av-bid",   "1시간 전"),
        ("송채원", "운영팀",     "Operations",  "av-ops",   "3시간 전"),
        ("서수민", "재무팀",     "Finance",     "av-fin",   "어제"),
        ("유선희", "총무팀",     "Viewer",      "av-gen",   "2일 전"),
    ]
    for name, team, role, av_cls, last in members:
        role_badge_map = {
            "Admin":       "badge-red",
            "Bid Manager": "badge-blue",
            "Operations":  "badge-green",
            "Finance":     "badge-amber",
            "Viewer":      "badge-gray",
        }
        st.markdown(f"""
        <div class="member-row">
            <div class="avatar {av_cls}">{name[:2]}</div>
            <span style="color:#c0d0e8;font-weight:500">{name}</span>
            <span>{badge(team, 'gray')}</span>
            <span>{badge(role, role_badge_map[role])}</span>
            <span style="color:#5a6a82;font-size:12px">{last}</span>
            <span style="color:#4a5a72;font-size:16px">⋯</span>
        </div>
        """, unsafe_allow_html=True)

    section("", "역할별 접근 권한 매트릭스")
    acl_data = [
        ("전체 공고 목록",       True,  True,  False, False, False),
        ("지원 가능성 판정",     True,  True,  False, False, True),
        ("chunk 근거 상세",      True,  True,  False, False, False),
        ("운영팀 액션",          True,  True,  True,  False, False),
        ("금액 / 보증금 정보",   True,  True,  False, True,  False),
        ("제출서류 목록",        True,  True,  False, False, True),
        ("회사 프로필 편집",     True,  False, False, False, False),
        ("팀 관리 / ACL 편집",  True,  False, False, False, False),
    ]

    def acl_icon(v, partial=False):
        if partial: return '<span class="acl-part">◑</span>'
        return '<span class="acl-ok">✔</span>' if v else '<span class="acl-off">✕</span>'

    partial_cases = {("지원 가능성 판정", 4), ("제출서류 목록", 4)}

    header_row = """
    <table class="acl-table"><thead><tr>
        <th style="width:28%">접근 범위</th>
        <th><span style="color:#a080e8">Admin</span></th>
        <th><span style="color:#4a9eff">Bid Mgr</span></th>
        <th><span style="color:#30c080">Operations</span></th>
        <th><span style="color:#e8a020">Finance</span></th>
        <th><span style="color:#7a8aaa">Viewer</span></th>
    </tr></thead><tbody>
    """
    rows = ""
    for row in acl_data:
        label = row[0]
        cells = ""
        for i, v in enumerate(row[1:]):
            is_partial = (label, i) in partial_cases
            cells += f"<td>{acl_icon(v, is_partial and v)}</td>"
        rows += f"<tr><td>{label}</td>{cells}</tr>"
    st.markdown(header_row + rows + "</tbody></table>", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:20px;margin-top:10px;font-size:12px;color:#5a6a82">
        <span><span style="color:#34d870">✔</span> 접근 허용</span>
        <span><span style="color:#9090b0">◑</span> 요약만</span>
        <span><span style="color:#2a3548">✕</span> 접근 불가</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#2a1a00;border:1px solid #6a4010;border-radius:10px;padding:14px 18px;
        display:flex;gap:14px;align-items:flex-start">
        <span style="font-size:20px">☁️</span>
        <div style="font-size:13px;color:#c0a060;line-height:1.7">
            <strong style="color:#e8c080">Entra ID 연동 (확장 항목)</strong><br>
            확장 시 Entra ID 그룹과 매핑하여 회사 조직도 기반 권한 자동 부여,
            감사 로그, 부서별 문서 접근 제어가 가능합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 7. 설정 (로그인 / 로그아웃 / 회원가입)
# ══════════════════════════════════════════════════════════════════════════════
def page_settings():
    st.markdown("""
    <div class="page-header">
        <h2>설정</h2>
        <div class="page-subtext">계정 관리 · 로그인 / 로그아웃 · 회원가입</div>
    </div>
    """, unsafe_allow_html=True)

    # 로그인 상태 초기화
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"

    if st.session_state.logged_in:
        # ── 로그인 상태 ──
        st.markdown(f"""
        <div class="content-card" style="max-width:420px">
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px">
                <div class="avatar av-admin" style="width:44px;height:44px;font-size:14px">
                    {st.session_state.get('username','사용자')[:2]}
                </div>
                <div>
                    <div style="font-size:13px;font-weight:600;color:#c0d0e8">
                        {st.session_state.get('username','사용자')}
                    </div>
                    <div style="font-size:10px;color:#4a6080;margin-top:2px">
                        {st.session_state.get('user_email','user@example.com')}
                    </div>
                </div>
            </div>
            <div class="hdivider"></div>
            <div class="match-row" style="margin-bottom:4px">
                <span class="match-label">소속</span>
                <span style="color:#8aaac8">삼구아이앤씨(주)</span>
            </div>
            <div class="match-row" style="margin-bottom:4px">
                <span class="match-label">역할</span>
                <span style="color:#8aaac8">{st.session_state.get('user_role','Viewer')}</span>
            </div>
            <div class="match-row">
                <span class="match-label">마지막 로그인</span>
                <span style="color:#4a6080">2026-05-18 09:12</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if st.button("로그아웃", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_email = ""
            st.session_state.user_role = ""
            st.rerun()

    else:
        # ── 탭 선택 (로그인 / 회원가입) ──
        tab_cols = st.columns([1, 1, 4])
        with tab_cols[0]:
            if st.button("로그인", key="tab_login"):
                st.session_state.auth_tab = "login"
        with tab_cols[1]:
            if st.button("회원가입", key="tab_signup"):
                st.session_state.auth_tab = "signup"

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.session_state.auth_tab == "login":
            # ── 로그인 폼 ──
            st.markdown("""
            <div style="font-size:13px;font-weight:600;color:#8aaac8;
                margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid #1a3060">
                로그인
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                email_in = st.text_input("이메일", placeholder="example@samgu.co.kr")
                pw_in    = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력")
                role_in  = st.selectbox("역할 선택", ["Admin", "Bid Manager", "Operations", "Finance", "Viewer"])
                submitted = st.form_submit_button("로그인")

                if submitted:
                    if email_in and pw_in:
                        st.session_state.logged_in   = True
                        st.session_state.username    = email_in.split("@")[0]
                        st.session_state.user_email  = email_in
                        st.session_state.user_role   = role_in
                        st.rerun()
                    else:
                        st.markdown('<div style="color:#e84040;font-size:11px;margin-top:4px">이메일과 비밀번호를 입력해주세요.</div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="font-size:10px;color:#3a5070;margin-top:10px">
                비밀번호를 잊으셨나요? &nbsp;
                <span style="color:#3a8ef0;cursor:pointer">재설정 요청</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── 회원가입 폼 ──
            st.markdown("""
            <div style="font-size:13px;font-weight:600;color:#8aaac8;
                margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid #1a3060">
                회원가입
            </div>
            """, unsafe_allow_html=True)

            with st.form("signup_form"):
                su_name  = st.text_input("이름", placeholder="홍길동")
                su_email = st.text_input("이메일", placeholder="example@samgu.co.kr")
                su_dept  = st.selectbox("소속 팀", ["입찰/영업팀", "운영팀", "재무팀", "총무팀", "기타"])
                su_role  = st.selectbox("요청 역할", ["Bid Manager", "Operations", "Finance", "Viewer"])
                su_pw    = st.text_input("비밀번호", type="password", placeholder="8자 이상")
                su_pw2   = st.text_input("비밀번호 확인", type="password", placeholder="동일하게 입력")
                submitted2 = st.form_submit_button("가입 신청")

                if submitted2:
                    if not su_name or not su_email or not su_pw:
                        st.markdown('<div style="color:#e84040;font-size:11px;margin-top:4px">모든 항목을 입력해주세요.</div>', unsafe_allow_html=True)
                    elif su_pw != su_pw2:
                        st.markdown('<div style="color:#e84040;font-size:11px;margin-top:4px">비밀번호가 일치하지 않습니다.</div>', unsafe_allow_html=True)
                    elif len(su_pw) < 8:
                        st.markdown('<div style="color:#e84040;font-size:11px;margin-top:4px">비밀번호는 8자 이상이어야 합니다.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background:#0e2e1c;border:1px solid #1a5030;border-radius:8px;
                            padding:12px 16px;font-size:11px;color:#2ecc60;margin-top:8px">
                            {su_name}님의 가입 신청이 완료되었습니다.<br>
                            관리자 승인 후 로그인이 가능합니다.
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("""
            <div style="font-size:10px;color:#3a5070;margin-top:10px">
                이미 계정이 있으신가요? 로그인 탭을 이용해주세요.
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 라우터
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state.page

if page == "dashboard":
    page_dashboard()
elif page == "bid_search":
    page_bid_search()
elif page == "bid_detail":
    page_bid_detail()
elif page == "action":
    page_action()
elif page == "profile":
    page_profile()
elif page == "team":
    page_team()
elif page == "settings":
    page_settings()
