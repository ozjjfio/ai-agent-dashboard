import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from datetime import datetime, timedelta
import random

# ── 한글 폰트 설정 ──────────────────────────────────────────────
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="AI Bid Action Agent",
    page_icon="📋",
    layout="wide"
)

# ── 가상 데이터 생성 ────────────────────────────────────────────
@st.cache_data
def load_data():
    today = datetime.today()
    data = [
        {
            "공고명": "A시청 청사 청소용역",
            "발주기관": "A시청",
            "지역": "서울",
            "기초금액": 50000000,
            "마감일": today + timedelta(days=2),
            "업종": "청소용역",
            "참여가능": True,
            "경쟁강도": "높음",
            "추천액션": "가격 검토 필요",
            "보류사유": None,
            "서류준비": False,
            "확인여부": True,
            "ai_요약": "서울 소재 청소용역 면허 보유 업체 대상. 계약기간 1년. 전자입찰 방식.",
            "참여가능성": 72,
            "서류체크": {"사업자등록증": True, "청소용역 면허": True, "실적증명서": False, "보험증권": False},
            "확인필요조건": ["서울 소재 요건 확인 필요", "최근 3년 실적 1건 이상"],
            "유사낙찰률": 87.8,
            "유사낙찰가범위": "43,500,000 ~ 44,200,000원",
        },
        {
            "공고명": "B공단 시설관리 위탁용역",
            "발주기관": "B공단",
            "지역": "경기",
            "기초금액": 72000000,
            "마감일": today + timedelta(days=4),
            "업종": "시설관리",
            "참여가능": True,
            "경쟁강도": "보통",
            "추천액션": "오늘 서류 확인",
            "보류사유": None,
            "서류준비": False,
            "확인여부": False,
            "ai_요약": "경기 소재 시설관리 업체 대상. 건물 전기·소방 설비 포함. 계약기간 2년.",
            "참여가능성": 85,
            "서류체크": {"사업자등록증": True, "시설관리 면허": True, "실적증명서": True, "보험증권": False},
            "확인필요조건": ["전기공사업 면허 포함 여부 확인"],
            "유사낙찰률": 91.2,
            "유사낙찰가범위": "65,000,000 ~ 67,500,000원",
        },
        {
            "공고명": "C구청 홍보물 제작 용역",
            "발주기관": "C구청",
            "지역": "서울",
            "기초금액": 18000000,
            "마감일": today + timedelta(days=7),
            "업종": "인쇄·홍보",
            "참여가능": True,
            "경쟁강도": "낮음",
            "추천액션": "참여 가능성 높음",
            "보류사유": None,
            "서류준비": True,
            "확인여부": False,
            "ai_요약": "서울 소재 인쇄·홍보물 제작 업체 대상. 리플렛 5,000부 포함.",
            "참여가능성": 91,
            "서류체크": {"사업자등록증": True, "인쇄업 신고증": True, "실적증명서": True, "보험증권": True},
            "확인필요조건": [],
            "유사낙찰률": 94.5,
            "유사낙찰가범위": "16,800,000 ~ 17,200,000원",
        },
        {
            "공고명": "D기관 IT 유지보수 용역",
            "발주기관": "D기관",
            "지역": "경기",
            "기초금액": 35000000,
            "마감일": today + timedelta(days=10),
            "업종": "IT유지보수",
            "참여가능": False,
            "경쟁강도": "높음",
            "추천액션": "참여 보류",
            "보류사유": "지역 조건 미충족",
            "서류준비": False,
            "확인여부": False,
            "ai_요약": "수도권 소재 IT 유지보수 업체 대상. 네트워크 장비 관리 포함.",
            "참여가능성": 20,
            "서류체크": {"사업자등록증": True, "SW사업자 확인서": False, "실적증명서": False, "보험증권": False},
            "확인필요조건": ["SW사업자 확인서 발급 필요", "수도권 소재 요건 확인"],
            "유사낙찰률": 82.3,
            "유사낙찰가범위": "28,000,000 ~ 30,000,000원",
        },
        {
            "공고명": "E시 물품 납품 계약",
            "발주기관": "E시청",
            "지역": "서울",
            "기초금액": 12000000,
            "마감일": today + timedelta(days=1),
            "업종": "물품납품",
            "참여가능": True,
            "경쟁강도": "보통",
            "추천액션": "가격 검토 필요",
            "보류사유": None,
            "서류준비": False,
            "확인여부": True,
            "ai_요약": "서울 소재 물품 납품 업체 대상. 사무용품 일괄 납품.",
            "참여가능성": 78,
            "서류체크": {"사업자등록증": True, "물품납품 실적": False, "보험증권": True, "세금완납증명": False},
            "확인필요조건": ["납품 실적 1건 이상 요건 확인"],
            "유사낙찰률": 89.1,
            "유사낙찰가범위": "10,800,000 ~ 11,300,000원",
        },
    ]
    return pd.DataFrame(data)

df = load_data()

# ── 헤더 ───────────────────────────────────────────────────────
st.title("📋 AI Bid Action Agent")
st.caption(f"오늘의 입찰 액션 대시보드 — {datetime.today().strftime('%Y-%m-%d')}")
st.divider()

# ── 상단 요약 카드 ──────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
today = datetime.today()

신규공고 = len(df)
마감임박 = len(df[df["마감일"] <= today + timedelta(days=3)])
참여가능 = len(df[df["참여가능"] == True])
서류미준비 = len(df[(df["참여가능"] == True) & (df["서류준비"] == False)])
미확인 = len(df[df["확인여부"] == False])
조건적합 = len(df[df["참여가능"] == True])
기회금액 = df[df["참여가능"] == True]["기초금액"].sum()

c1.metric("📌 신규 공고", f"{신규공고}건")
c2.metric("🔴 마감 임박", f"{마감임박}건")
c3.metric("✅ 참여 가능", f"{참여가능}건")
c4.metric("📄 서류 미준비", f"{서류미준비}건")
c5.metric("👁 미확인", f"{미확인}건")
c6.metric("💰 기회 금액", f"{기회금액/100000000:.1f}억")

st.divider()

# ── 공고 리스트 + 상세 ─────────────────────────────────────────
st.subheader("오늘 확인할 공고")

# 필터
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    filter_참여 = st.selectbox("참여 가능 여부", ["전체", "가능만", "불가만"])
with col_f2:
    filter_경쟁 = st.selectbox("경쟁 강도", ["전체", "낮음", "보통", "높음"])
with col_f3:
    filter_지역 = st.selectbox("지역", ["전체"] + list(df["지역"].unique()))

filtered = df.copy()
if filter_참여 == "가능만":
    filtered = filtered[filtered["참여가능"] == True]
elif filter_참여 == "불가만":
    filtered = filtered[filtered["참여가능"] == False]
if filter_경쟁 != "전체":
    filtered = filtered[filtered["경쟁강도"] == filter_경쟁]
if filter_지역 != "전체":
    filtered = filtered[filtered["지역"] == filter_지역]

# 공고 리스트
for _, row in filtered.iterrows():
    dday = (row["마감일"] - today).days
    dday_str = f"D-{dday}" if dday >= 0 else "마감"
    참여_icon = "✅" if row["참여가능"] else "❌"

    if dday <= 2:
        border_color = "#ff4b4b"
    elif dday <= 5:
        border_color = "#ffa500"
    else:
        border_color = "#cccccc"

    with st.expander(
        f"{참여_icon} {row['공고명']} | {row['발주기관']} | "
        f"{int(row['기초금액']/1000000)}M | "
        f"{'🔴' if dday <= 2 else '🟡' if dday <= 5 else '⚪'} {dday_str} | "
        f"👉 {row['추천액션']}"
    ):
        left, right = st.columns([1, 1])

        with left:
            st.markdown("**📝 AI 공고 요약**")
            st.info(row["ai_요약"])

            st.markdown("**🏢 참여 가능성**")
            st.progress(row["참여가능성"] / 100)
            st.caption(f"{row['참여가능성']}% — {'참여 권장' if row['참여가능성'] >= 70 else '신중 검토 필요'}")

            if row["확인필요조건"]:
                st.markdown("**⚠️ 확인 필요 조건**")
                for 조건 in row["확인필요조건"]:
                    st.warning(조건)
            else:
                st.success("확인 필요 조건 없음")

        with right:
            st.markdown("**📄 제출 서류 체크리스트**")
            for 서류, 준비 in row["서류체크"].items():
                if 준비:
                    st.markdown(f"✅ {서류}")
                else:
                    st.markdown(f"❌ {서류} — 준비 필요")

            st.markdown("**📊 유사 낙찰 사례**")
            st.markdown(f"- 평균 낙찰률: **{row['유사낙찰률']}%**")
            st.markdown(f"- 낙찰가 참고 범위: **{row['유사낙찰가범위']}**")
            st.caption("※ 실제 투찰가는 원가·자격·현장조건에 따라 달라지는 참고용 지표입니다.")

st.divider()

# ── 하단 차트 ──────────────────────────────────────────────────
st.subheader("입찰 현황 분석")
chart1, chart2, chart3 = st.columns(3)

# 경쟁 강도 분포
with chart1:
    st.markdown("**경쟁 강도 분포**")
    경쟁_counts = df["경쟁강도"].value_counts()
    fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))
    colors = ["#ff6b6b", "#ffa94d", "#69db7c"]
    ax1.pie(
        경쟁_counts.values,
        labels=경쟁_counts.index,
        autopct="%1.0f%%",
        colors=colors[:len(경쟁_counts)],
        startangle=90
    )
    fig1.patch.set_alpha(0)
    st.pyplot(fig1)

# 지역별 공고 수
with chart2:
    st.markdown("**지역별 공고 수**")
    지역_counts = df["지역"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
    ax2.barh(지역_counts.index, 지역_counts.values, color="#4dabf7")
    ax2.set_xlabel("건수")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    fig2.patch.set_alpha(0)
    st.pyplot(fig2)

# 마감 임박 현황
with chart3:
    st.markdown("**마감 임박 공고 현황**")
    df["D-day"] = (df["마감일"] - today).dt.days
    df_sorted = df.sort_values("D-day")
    fig3, ax3 = plt.subplots(figsize=(3.5, 3.5))
    bar_colors = ["#ff4b4b" if d <= 2 else "#ffa500" if d <= 5 else "#74c0fc" for d in df_sorted["D-day"]]
    ax3.barh(
        [n[:8] for n in df_sorted["공고명"]],
        df_sorted["D-day"],
        color=bar_colors
    )
    ax3.set_xlabel("남은 일수")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    fig3.patch.set_alpha(0)
    st.pyplot(fig3)

# 보류 사유
st.markdown("**보류 사유**")
보류df = df[df["보류사유"].notna()][["공고명", "발주기관", "보류사유"]]
if len(보류df) > 0:
    st.dataframe(보류df, use_container_width=True, hide_index=True)
else:
    st.success("보류 공고 없음")

st.caption("※ 이 대시보드는 참고용 정보를 제공하며, 최종 입찰 판단은 담당자가 직접 확인 후 결정하시기 바랍니다.")
