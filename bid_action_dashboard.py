import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="공고털이",
    page_icon="🥷",
    layout="wide"
)

# ── 가상 데이터 ────────────────────────────────────────────────
@st.cache_data
def load_data():
    today = datetime.today()
    return pd.DataFrame([
        {
            "우선순위": 1,
            "공고명": "국방과학연구소 AI GPU 서버 구축",
            "발주기관": "국방과학연구소",
            "지역": "대전",
            "기초금액": 850000000,
            "마감일": today + timedelta(days=2),
            "ai_매칭": "지원가능",
            "필요액션": "가격 검토 필요",
            "보류사유": None,
            "관심": True,
            "ai_요약": "H100 GPU 8장 이상 탑재 서버 납품. NVLink 지원 필수. 납품 후 6개월 유지보수 포함.",
            "요건": {
                "GPU 사양 (H100 이상)": {"보유": "H100 SXM5", "충족": True, "근거": "2조 GPU 규격"},
                "NVLink 지원": {"보유": "지원", "충족": True, "근거": "3조 연결 규격"},
                "납품 실적 3건 이상": {"보유": "5건", "충족": True, "근거": "4조 자격 요건"},
                "유지보수 인력 2인 이상": {"보유": "1인", "충족": False, "근거": "5조 유지보수 조항"},
                "보안 적합성 인증": {"보유": "미보유", "충족": False, "근거": "6조 보안 요건"},
            },
            "서류체크": {"사업자등록증": True, "GPU납품실적": True, "보안인증서": False, "유지보수계획서": False},
            "확인필요조건": ["유지보수 인력 1인 추가 확보 필요", "보안 적합성 인증 취득 여부 확인"],
            "유사낙찰률": 89.2,
            "유사낙찰가범위": "748,000,000 ~ 772,000,000원",
            "경쟁강도": "높음",
        },
        {
            "우선순위": 2,
            "공고명": "한국전자통신연구원 딥러닝 연산 장비 도입",
            "발주기관": "ETRI",
            "지역": "대전",
            "기초금액": 520000000,
            "마감일": today + timedelta(days=3),
            "ai_매칭": "지원가능",
            "필요액션": "오늘 서류 확인",
            "보류사유": None,
            "관심": True,
            "ai_요약": "A100 또는 동급 이상 GPU 클러스터 구성. InfiniBand 네트워크 포함. 설치 및 세팅 포함.",
            "요건": {
                "GPU 사양 (A100 이상)": {"보유": "H100 SXM5", "충족": True, "근거": "2조 장비 규격"},
                "InfiniBand 지원": {"보유": "지원", "충족": True, "근거": "3조 네트워크"},
                "클러스터 구성 경험": {"보유": "3건", "충족": True, "근거": "4조 실적"},
                "설치 인력 보유": {"보유": "2인", "충족": True, "근거": "5조 설치 조항"},
                "납품 후 테스트 지원": {"보유": "가능", "충족": True, "근거": "6조 검수"},
            },
            "서류체크": {"사업자등록증": True, "납품실적": True, "설치계획서": True, "보험증권": False},
            "확인필요조건": ["보험증권 갱신 필요"],
            "유사낙찰률": 91.5,
            "유사낙찰가범위": "470,000,000 ~ 485,000,000원",
            "경쟁강도": "보통",
        },
        {
            "우선순위": 3,
            "공고명": "서울시 스마트시티 AI 인프라 구축",
            "발주기관": "서울특별시",
            "지역": "서울",
            "기초금액": 1200000000,
            "마감일": today + timedelta(days=5),
            "ai_매칭": "검토 필요",
            "필요액션": "요건 재확인",
            "보류사유": None,
            "관심": False,
            "ai_요약": "엣지 AI 서버 및 GPU 인프라 통합 구축. 중소기업 참여 제한 없음. 컨소시엄 가능.",
            "요건": {
                "엣지 AI 서버 납품 실적": {"보유": "1건", "충족": False, "근거": "3조 실적 요건"},
                "GPU 서버 구축 실적": {"보유": "5건", "충족": True, "근거": "4조 실적"},
                "컨소시엄 구성 가능": {"보유": "가능", "충족": True, "근거": "2조 참가 자격"},
                "보안 인증 (CC인증)": {"보유": "미보유", "충족": False, "근거": "5조 보안"},
                "유지보수 3년 이상": {"보유": "1년", "충족": False, "근거": "6조 유지보수"},
            },
            "서류체크": {"사업자등록증": True, "실적증명서": True, "CC인증서": False, "컨소시엄동의서": False},
            "확인필요조건": ["CC인증 취득 또는 컨소시엄 파트너 필요", "유지보수 기간 요건 확인"],
            "유사낙찰률": 85.3,
            "유사낙찰가범위": "1,010,000,000 ~ 1,040,000,000원",
            "경쟁강도": "높음",
        },
        {
            "우선순위": 4,
            "공고명": "중소벤처기업부 AI 바우처 GPU 장비",
            "발주기관": "중소벤처기업부",
            "지역": "세종",
            "기초금액": 180000000,
            "마감일": today + timedelta(days=6),
            "ai_매칭": "지원가능",
            "필요액션": "참여 가능성 높음",
            "보류사유": None,
            "관심": True,
            "ai_요약": "중소기업 AI 바우처 지원용 GPU 서버 납품. RTX 4090 또는 A6000급. 소량 납품.",
            "요건": {
                "GPU 사양 (RTX4090/A6000)": {"보유": "A6000", "충족": True, "근거": "2조 규격"},
                "납품 실적 1건 이상": {"보유": "5건", "충족": True, "근거": "3조 자격"},
                "중소기업 확인서": {"보유": "보유", "충족": True, "근거": "4조 참가 자격"},
                "AS 1년 보증": {"보유": "2년", "충족": True, "근거": "5조 AS"},
                "세금계산서 발행 가능": {"보유": "가능", "충족": True, "근거": "6조 계약"},
            },
            "서류체크": {"사업자등록증": True, "중소기업확인서": True, "납품실적": True, "AS계획서": True},
            "확인필요조건": [],
            "유사낙찰률": 94.1,
            "유사낙찰가범위": "167,000,000 ~ 172,000,000원",
            "경쟁강도": "낮음",
        },
        {
            "우선순위": 5,
            "공고명": "국가정보원 보안 AI 서버 도입",
            "발주기관": "국가정보원",
            "지역": "서울",
            "기초금액": 950000000,
            "마감일": today + timedelta(days=8),
            "ai_매칭": "보류",
            "필요액션": "참여 보류",
            "보류사유": "보안 인증 미충족",
            "관심": False,
            "ai_요약": "보안 특수 목적 AI 서버. 국정원 보안 적합성 검증 필수. 납품 업체 사전 등록 필요.",
            "요건": {
                "국정원 보안 적합성": {"보유": "미보유", "충족": False, "근거": "2조 필수 요건"},
                "납품업체 사전 등록": {"보유": "미등록", "충족": False, "근거": "3조 자격"},
                "GPU 사양": {"보유": "H100", "충족": True, "근거": "4조 장비"},
                "보안 서약서": {"보유": "가능", "충족": True, "근거": "5조"},
                "비밀취급인가": {"보유": "미보유", "충족": False, "근거": "6조"},
            },
            "서류체크": {"사업자등록증": True, "보안적합성인증": False, "비밀취급인가": False, "사전등록증": False},
            "확인필요조건": ["보안 적합성 인증 없으면 참여 불가", "납품업체 사전 등록 6개월 소요"],
            "유사낙찰률": 88.0,
            "유사낙찰가범위": "836,000,000 ~ 855,000,000원",
            "경쟁강도": "높음",
        },
    ])

df = load_data()
today = datetime.today()

if "company" not in st.session_state:
    st.session_state.company = {
        "회사명": "테크비전 주식회사",
        "업종": "IT장비납품",
        "세부품명번호": "2127-0001",
        "품명": "GPU 서버",
        "지역": "서울",
        "예산금액대": "1억 ~ 10억",
    }

if "관심공고" not in st.session_state:
    st.session_state.관심공고 = list(df[df["관심"] == True]["공고명"])

# ── 사이드바 ───────────────────────────────────────────────────
with st.sidebar:
    st.title("🥷 공고털이")
    st.caption(datetime.today().strftime('%Y-%m-%d'))
    st.divider()
    menu = st.radio(
        "메뉴",
        ["오늘의 액션", "공고 검색", "관심 공고", "요건 매칭", "회사 프로필", "설정"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption(f"👤 {st.session_state.company['회사명']}")
    st.caption(f"📍 {st.session_state.company['지역']} | {st.session_state.company['업종']}")

# ══════════════════════════════════════════════════════════════
# 1. 오늘의 액션
# ══════════════════════════════════════════════════════════════
if menu == "오늘의 액션":
    st.header(f"오늘의 액션 · {datetime.today().strftime('%Y-%m-%d')}")

    긴급 = df[df["마감일"] <= today + timedelta(days=3)]
    검토 = df[(df["마감일"] > today + timedelta(days=3)) & (df["마감일"] <= today + timedelta(days=7))]
    보류 = df[df["ai_매칭"] == "보류"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 긴급 처리", f"{len(긴급)}건", "마감 D-3")
    c2.metric("🟡 검토 추천", f"{len(검토)}건", "마감 4~7일")
    c3.metric("⚪ 보류 추천", f"{len(보류)}건", "요건 미충족")
    c4.metric("📋 전체 공고", f"{len(df)}건", "오늘 수집 기준")

    st.divider()
    st.subheader("오늘 우선 확인해야 할 공고")

    header = st.columns([1, 4, 2, 2, 2, 2])
    header[0].markdown("**순위**")
    header[1].markdown("**공고명**")
    header[2].markdown("**발주기관**")
    header[3].markdown("**마감일**")
    header[4].markdown("**필요 액션**")
    header[5].markdown("**AI 매칭**")
    st.divider()

    for _, row in df.sort_values("우선순위").iterrows():
        dday = (row["마감일"] - today).days
        cols = st.columns([1, 4, 2, 2, 2, 2])
        cols[0].markdown(f"**{row['우선순위']}**")
        cols[1].markdown(row["공고명"])
        cols[2].markdown(row["발주기관"])
        cols[3].markdown(f"{'🔴' if dday <= 2 else '🟡' if dday <= 5 else '⚪'} D-{dday}")
        cols[4].markdown(row["필요액션"])
        if row["ai_매칭"] == "지원가능":
            cols[5].success("지원가능")
        elif row["ai_매칭"] == "검토 필요":
            cols[5].warning("검토 필요")
        else:
            cols[5].error("보류")

    st.divider()
    st.subheader("오늘 해야 할 일")
    할일 = {"제안서 검토": 2, "제출 서류": 4, "실적 증명": 3, "기술지원": 1, "원문 확인": 2}
    cols = st.columns(len(할일))
    for i, (k, v) in enumerate(할일.items()):
        cols[i].metric(k, f"{v}건")

# ══════════════════════════════════════════════════════════════
# 2. 공고 검색
# ══════════════════════════════════════════════════════════════
elif menu == "공고 검색":
    st.header("공고 검색")
    st.caption("나라장터 공고를 검색합니다 (현재 데모 데이터 기준)")

    col1, col2, col3 = st.columns(3)
    keyword = col1.text_input("검색어", placeholder="예: GPU, 서버, AI")
    filter_매칭 = col2.selectbox("AI 매칭", ["전체", "지원가능", "검토 필요", "보류"])
    filter_경쟁 = col3.selectbox("경쟁 강도", ["전체", "낮음", "보통", "높음"])

    filtered = df.copy()
    if keyword:
        filtered = filtered[
            filtered["공고명"].str.contains(keyword) |
            filtered["발주기관"].str.contains(keyword)
        ]
    if filter_매칭 != "전체":
        filtered = filtered[filtered["ai_매칭"] == filter_매칭]
    if filter_경쟁 != "전체":
        filtered = filtered[filtered["경쟁강도"] == filter_경쟁]

    st.caption(f"검색 결과 {len(filtered)}건")
    st.divider()

    for _, row in filtered.iterrows():
        dday = (row["마감일"] - today).days
        with st.expander(f"{row['공고명']} | {row['발주기관']} | {int(row['기초금액']/100000000)}억 | D-{dday}"):
            st.markdown(f"**AI 요약:** {row['ai_요약']}")
            st.markdown(f"**경쟁강도:** {row['경쟁강도']} | **AI 매칭:** {row['ai_매칭']}")
            is_관심 = row["공고명"] in st.session_state.관심공고
            if st.button("⭐ 관심 해제" if is_관심 else "☆ 관심 등록", key=f"s_{row['공고명']}"):
                if is_관심:
                    st.session_state.관심공고.remove(row["공고명"])
                else:
                    st.session_state.관심공고.append(row["공고명"])
                st.rerun()

# ══════════════════════════════════════════════════════════════
# 3. 관심 공고
# ══════════════════════════════════════════════════════════════
elif menu == "관심 공고":
    st.header("관심 공고")
    관심df = df[df["공고명"].isin(st.session_state.관심공고)]

    if len(관심df) == 0:
        st.info("등록된 관심 공고가 없습니다. 공고 검색에서 등록하세요.")
    else:
        for _, row in 관심df.iterrows():
            dday = (row["마감일"] - today).days
            with st.expander(f"⭐ {row['공고명']} | {row['발주기관']} | D-{dday} | {row['ai_매칭']}"):
                left, right = st.columns(2)
                with left:
                    st.markdown("**📝 공고 요약**")
                    st.info(row["ai_요약"])
                    st.markdown(f"**기초금액:** {int(row['기초금액']/100000000)}억원")
                    st.markdown(f"**마감일:** {row['마감일'].strftime('%Y-%m-%d')} (D-{dday})")
                    st.markdown(f"**경쟁강도:** {row['경쟁강도']}")
                with right:
                    st.markdown("**📄 제출 서류**")
                    for 서류, 준비 in row["서류체크"].items():
                        st.markdown(f"{'✅' if 준비 else '❌'} {서류}")
                    if row["확인필요조건"]:
                        st.markdown("**⚠️ 확인 필요**")
                        for 조건 in row["확인필요조건"]:
                            st.warning(조건)
                st.markdown(f"**유사 낙찰률:** {row['유사낙찰률']}% | **낙찰가 범위:** {row['유사낙찰가범위']}")
                st.caption("※ 참고용 지표이며 실제 투찰가는 담당자가 판단하세요.")
                if st.button("⭐ 관심 해제", key=f"r_{row['공고명']}"):
                    st.session_state.관심공고.remove(row["공고명"])
                    st.rerun()

# ══════════════════════════════════════════════════════════════
# 4. 요건 매칭
# ══════════════════════════════════════════════════════════════
elif menu == "요건 매칭":
    st.header("요건 매칭")
    공고선택 = st.selectbox("공고 선택", df["공고명"].tolist())
    row = df[df["공고명"] == 공고선택].iloc[0]
    st.divider()

    left, right = st.columns([3, 2])
    with left:
        st.subheader("요건 항목표")
        요건df = pd.DataFrame([
            {
                "요건 항목": k,
                "우리 회사 보유": v["보유"],
                "충족 여부": "✅ 충족" if v["충족"] else "❌ 미충족",
                "경쟁 강도": row["경쟁강도"],
                "근거 (원문)": v["근거"],
            }
            for k, v in row["요건"].items()
        ])
        st.dataframe(요건df, use_container_width=True, hide_index=True)

    with right:
        st.subheader("통합 매칭 결과")
        총 = len(row["요건"])
        충족 = sum(1 for v in row["요건"].values() if v["충족"])
        미충족 = 총 - 충족
        pct = int(충족 / 총 * 100)

        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        ax.pie(
            [충족, 미충족],
            colors=["#4dabf7", "#dee2e6"],
            startangle=90,
            wedgeprops={"width": 0.5}
        )
        ax.text(0, 0, f"{pct}%", ha="center", va="center", fontsize=26, fontweight="bold")
        fig.patch.set_alpha(0)
        st.pyplot(fig)

        if pct >= 80:
            st.success(f"✅ 매칭률 {pct}% — 참여 권장")
            st.markdown("**다음 액션:** 서류 준비 후 입찰 등록")
        elif pct >= 50:
            st.warning(f"🟡 매칭률 {pct}% — 신중 검토 필요")
            st.markdown("**다음 액션:** 미충족 요건 보완 가능 여부 확인")
        else:
            st.error(f"❌ 매칭률 {pct}% — 참여 보류 권장")
            st.markdown("**다음 액션:** 요건 충족 후 재검토")

        st.caption(f"충족 {충족} / 미충족 {미충족} / 전체 {총}건")
        st.caption("※ AI 분석 결과이며 최종 판단은 담당자가 확인하세요.")

# ══════════════════════════════════════════════════════════════
# 5. 회사 프로필
# ══════════════════════════════════════════════════════════════
elif menu == "회사 프로필":
    st.header("회사 프로필")
    st.caption("입력된 정보를 기준으로 AI가 공고 매칭을 수행합니다.")
    st.divider()

    c = st.session_state.company
    col1, col2 = st.columns(2)
    with col1:
        c["회사명"] = st.text_input("회사명", value=c["회사명"])
        c["업종"] = st.text_input("업종", value=c["업종"])
        c["세부품명번호"] = st.text_input("세부품명번호", value=c["세부품명번호"])
    with col2:
        c["품명"] = st.text_input("품명", value=c["품명"])
        c["지역"] = st.selectbox("지역", ["서울", "경기", "대전", "부산", "기타"],
            index=["서울", "경기", "대전", "부산", "기타"].index(c["지역"]))
        c["예산금액대"] = st.selectbox("예산 금액대", ["1천만 ~ 1억", "1억 ~ 10억", "10억 이상"],
            index=["1천만 ~ 1억", "1억 ~ 10억", "10억 이상"].index(c["예산금액대"]))

    if st.button("저장", use_container_width=True):
        st.session_state.company = c
        st.success("저장되었습니다.")

# ══════════════════════════════════════════════════════════════
# 6. 설정
# ══════════════════════════════════════════════════════════════
elif menu == "설정":
    st.header("설정")
    st.divider()

    st.subheader("로그인")
    st.text_input("이메일", placeholder="example@company.com")
    st.text_input("비밀번호", type="password", placeholder="••••••••")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("로그인", use_container_width=True):
            st.success("로그인되었습니다. (데모)")
    with col2:
        if st.button("로그아웃", use_container_width=True):
            st.info("로그아웃되었습니다. (데모)")

    st.divider()
    st.subheader("회원가입")
    st.text_input("이름", placeholder="홍길동")
    st.text_input("회사명", placeholder="테크비전 주식회사")
    st.text_input("가입 이메일", placeholder="example@company.com")
    st.text_input("가입 비밀번호", type="password", placeholder="••••••••")
    if st.button("회원가입", use_container_width=True):
        st.success("가입이 완료되었습니다. (데모)")

    st.divider()
    st.caption("※ 이 대시보드는 참고용이며 최종 입찰 판단은 담당자가 직접 확인하세요.")
