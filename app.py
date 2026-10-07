import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Road Accident Dashboard",
    page_icon="🚗",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #666666;
        font-size: 16px;
        margin-top: 0px;
        margin-bottom: 20px;
    }

    div[data-testid="metric-container"] {
        border: 1px solid #e6e6e6;
        padding: 18px;
        border-radius: 12px;
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SOURCE
# =========================================================
SOURCE_TEXT = (
    "ที่มา: กรมควบคุมโรค, "
    "ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนน "
    "จากระบบบูรณาการข้อมูลการตายจากอุบัติเหตุทางถนน (3 ฐาน) "
    "ปี 2567, data.go.th"
)

# =========================================================
# PATH
# =========================================================
BASE_DIR = Path(__file__).parent

DATA_PATH = (
    BASE_DIR
    / "road-accident-dashboard"
    / "outputs"
    / "dashboard_data.json"
)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    df = df.dropna(how="all")

    # แปลงเดือนเป็นตัวเลข
    if "month" in df.columns:
        df["month_numeric"] = pd.to_numeric(
            df["month"],
            errors="coerce"
        )

    return df


try:
    df = load_data()

except FileNotFoundError:

    st.error(
        "ไม่พบไฟล์ dashboard_data.json\n\n"
        "ตรวจสอบว่าไฟล์อยู่ที่ "
        "`road-accident-dashboard/outputs/dashboard_data.json`"
    )

    st.stop()

except Exception as e:

    st.error(
        f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}"
    )

    st.stop()

# =========================================================
# MONTH NAMES
# =========================================================
MONTH_NAMES = {
    1: "ม.ค.",
    2: "ก.พ.",
    3: "มี.ค.",
    4: "เม.ย.",
    5: "พ.ค.",
    6: "มิ.ย.",
    7: "ก.ค.",
    8: "ส.ค.",
    9: "ก.ย.",
    10: "ต.ค.",
    11: "พ.ย.",
    12: "ธ.ค."
}

MONTH_FULL_NAMES = {
    1: "มกราคม",
    2: "กุมภาพันธ์",
    3: "มีนาคม",
    4: "เมษายน",
    5: "พฤษภาคม",
    6: "มิถุนายน",
    7: "กรกฎาคม",
    8: "สิงหาคม",
    9: "กันยายน",
    10: "ตุลาคม",
    11: "พฤศจิกายน",
    12: "ธันวาคม"
}

# =========================================================
# TITLE
# =========================================================
st.markdown(
    '<p class="main-title">🚗 Road Accidents in Thailand 2024</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">'
    'Dashboard วิเคราะห์ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนนในประเทศไทย'
    '</p>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("🔎 ตัวกรองข้อมูล")

st.sidebar.caption(
    "สามารถเลือกได้หลายค่า • หากไม่เลือก หมายถึงแสดงข้อมูลทั้งหมด"
)

temp_df = df.copy()

# =========================================================
# FILTER : PROVINCE
# =========================================================
province_options = []

if "province" in temp_df.columns:

    province_options = sorted(
        temp_df["province"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_provinces = st.sidebar.multiselect(
    "จังหวัด",
    province_options,
    placeholder="ทุกจังหวัด",
    key="province_filter"
)

if selected_provinces:

    temp_df = temp_df[
        temp_df["province"]
        .astype(str)
        .isin(selected_provinces)
    ]

# =========================================================
# FILTER : SEX
# =========================================================
sex_options = []

if "sex" in temp_df.columns:

    sex_options = sorted(
        temp_df["sex"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_sexes = st.sidebar.multiselect(
    "เพศ",
    sex_options,
    placeholder="ทุกเพศ",
    key="sex_filter"
)

if selected_sexes:

    temp_df = temp_df[
        temp_df["sex"]
        .astype(str)
        .isin(selected_sexes)
    ]

# =========================================================
# FILTER : AGE
# =========================================================
age_options = []

if "age_group" in temp_df.columns:

    age_options = sorted(
        temp_df["age_group"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_ages = st.sidebar.multiselect(
    "ช่วงอายุ",
    age_options,
    placeholder="ทุกช่วงอายุ",
    key="age_filter"
)

if selected_ages:

    temp_df = temp_df[
        temp_df["age_group"]
        .astype(str)
        .isin(selected_ages)
    ]

# =========================================================
# FILTER : MONTH
# ตัด -1 และค่าที่ไม่ใช่ 1–12 ออก
# =========================================================
month_options = []

if "month_numeric" in temp_df.columns:

    month_options = (
        temp_df.loc[
            temp_df["month_numeric"].between(1, 12),
            "month_numeric"
        ]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    month_options = sorted(month_options)

selected_months = st.sidebar.multiselect(
    "เดือน",
    month_options,
    format_func=lambda x: MONTH_FULL_NAMES.get(x, str(x)),
    placeholder="ทุกเดือน",
    key="month_filter"
)

if selected_months:

    temp_df = temp_df[
        temp_df["month_numeric"]
        .isin(selected_months)
    ]

# =========================================================
# FILTER : VEHICLE
# =========================================================
vehicle_options = []

if "vehicle" in temp_df.columns:

    vehicle_options = sorted(
        temp_df["vehicle"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

selected_vehicles = st.sidebar.multiselect(
    "ประเภทยานพาหนะ",
    vehicle_options,
    placeholder="ทุกประเภท",
    key="vehicle_filter"
)

if selected_vehicles:

    temp_df = temp_df[
        temp_df["vehicle"]
        .astype(str)
        .isin(selected_vehicles)
    ]

# =========================================================
# FINAL FILTERED DATA
# =========================================================
filtered_df = temp_df.copy()

# =========================================================
# RESET FILTER
# =========================================================
if st.sidebar.button(
    "🔄 รีเซ็ตตัวกรอง",
    use_container_width=True
):

    for key in [
        "province_filter",
        "sex_filter",
        "age_filter",
        "month_filter",
        "vehicle_filter"
    ]:

        if key in st.session_state:
            del st.session_state[key]

    st.rerun()

st.sidebar.markdown("---")

st.sidebar.write(
    f"ข้อมูลหลังกรอง: **{len(filtered_df):,} รายการ**"
)

# แสดงจำนวน filter ที่กำลังเลือก
active_filters = (
    len(selected_provinces)
    + len(selected_sexes)
    + len(selected_ages)
    + len(selected_months)
    + len(selected_vehicles)
)

if active_filters > 0:

    st.sidebar.caption(
        f"กำลังเลือก {active_filters} เงื่อนไข"
    )

# =========================================================
# EMPTY CHECK
# =========================================================
if filtered_df.empty:

    st.warning(
        "ไม่พบข้อมูลที่ตรงกับตัวกรองที่เลือก "
        "ลองลดจำนวนเงื่อนไขหรือกดรีเซ็ตตัวกรอง"
    )

    st.stop()

# =========================================================
# KPI
# =========================================================
st.subheader("📊 ภาพรวม")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_records = len(filtered_df)

kpi1.metric(
    "ผู้เสียชีวิตทั้งหมด",
    f"{total_records:,} คน"
)

# =========================================================
# TOP PROVINCE
# =========================================================
if "province" in filtered_df.columns:

    province_counts = (
        filtered_df["province"]
        .dropna()
        .value_counts()
    )

    if not province_counts.empty:

        top_province = province_counts.index[0]
        top_province_count = province_counts.iloc[0]

        kpi2.metric(
            "จังหวัดสูงสุด",
            top_province,
            f"{top_province_count:,} คน"
        )

    else:
        kpi2.metric("จังหวัดสูงสุด", "-")

else:
    kpi2.metric("จังหวัดสูงสุด", "-")

# =========================================================
# TOP VEHICLE
# =========================================================
if "vehicle" in filtered_df.columns:

    vehicle_counts = (
        filtered_df["vehicle"]
        .dropna()
        .value_counts()
    )

    if not vehicle_counts.empty:

        top_vehicle = vehicle_counts.index[0]
        top_vehicle_count = vehicle_counts.iloc[0]

        kpi3.metric(
            "พาหนะที่พบมากที่สุด",
            top_vehicle,
            f"{top_vehicle_count:,} คน"
        )

    else:
        kpi3.metric("พาหนะที่พบมากที่สุด", "-")

else:
    kpi3.metric("พาหนะที่พบมากที่สุด", "-")

# =========================================================
# TOP AGE
# =========================================================
if "age_group" in filtered_df.columns:

    age_counts = (
        filtered_df["age_group"]
        .dropna()
        .value_counts()
    )

    if not age_counts.empty:

        top_age = age_counts.index[0]
        top_age_count = age_counts.iloc[0]

        kpi4.metric(
            "ช่วงอายุสูงสุด",
            top_age,
            f"{top_age_count:,} คน"
        )

    else:
        kpi4.metric("ช่วงอายุสูงสุด", "-")

else:
    kpi4.metric("ช่วงอายุสูงสุด", "-")

st.caption(SOURCE_TEXT)

st.divider()

# =========================================================
# TOP PROVINCES
# =========================================================
if "province" in filtered_df.columns:

    st.subheader(
        "📍 จังหวัดที่มีผู้เสียชีวิตสูงสุด"
    )

    province_chart = (
        filtered_df["province"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    province_chart.columns = [
        "จังหวัด",
        "จำนวนผู้เสียชีวิต"
    ]

    fig_province = px.bar(
        province_chart,
        x="จำนวนผู้เสียชีวิต",
        y="จังหวัด",
        orientation="h",
        text="จำนวนผู้เสียชีวิต"
    )

    fig_province.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        xaxis_title="จำนวนผู้เสียชีวิต",
        yaxis_title=""
    )

    fig_province.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_province,
        use_container_width=True
    )

    st.caption(SOURCE_TEXT)

# =========================================================
# MONTHLY TREND
# =========================================================
if "month_numeric" in filtered_df.columns:

    st.subheader(
        "📅 แนวโน้มผู้เสียชีวิตรายเดือน"
    )

    month_chart_df = filtered_df[
        filtered_df["month_numeric"]
        .between(1, 12)
    ].copy()

    if not month_chart_df.empty:

        month_chart = (
            month_chart_df
            .groupby("month_numeric")
            .size()
            .reset_index(
                name="จำนวนผู้เสียชีวิต"
            )
            .sort_values("month_numeric")
        )

        month_chart["เดือน"] = (
            month_chart["month_numeric"]
            .map(MONTH_NAMES)
        )

        fig_month = px.line(
            month_chart,
            x="เดือน",
            y="จำนวนผู้เสียชีวิต",
            markers=True
        )

        fig_month.update_layout(
            xaxis_title="เดือน",
            yaxis_title="จำนวนผู้เสียชีวิต"
        )

        fig_month.update_traces(
            mode="lines+markers+text",
            text=month_chart["จำนวนผู้เสียชีวิต"],
            textposition="top center"
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )

        st.caption(
            SOURCE_TEXT
            + " | กราฟแสดงเฉพาะข้อมูลเดือน 1–12"
        )

    else:

        st.info(
            "ไม่มีข้อมูลเดือน 1–12 "
            "ภายใต้ตัวกรองที่เลือก"
        )

# =========================================================
# SEX + AGE
# =========================================================
left_col, right_col = st.columns(2)

# =========================================================
# SEX
# =========================================================
with left_col:

    if "sex" in filtered_df.columns:

        st.subheader(
            "👤 ผู้เสียชีวิตจำแนกตามเพศ"
        )

        sex_chart = (
            filtered_df["sex"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        sex_chart.columns = [
            "เพศ",
            "จำนวน"
        ]

        fig_sex = px.pie(
            sex_chart,
            names="เพศ",
            values="จำนวน",
            hole=0.45
        )

        fig_sex.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_sex,
            use_container_width=True
        )

        st.caption(SOURCE_TEXT)

# =========================================================
# AGE
# =========================================================
with right_col:

    if "age_group" in filtered_df.columns:

        st.subheader(
            "🎂 ผู้เสียชีวิตจำแนกตามช่วงอายุ"
        )

        age_chart = (
            filtered_df["age_group"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        age_chart.columns = [
            "ช่วงอายุ",
            "จำนวน"
        ]

        fig_age = px.bar(
            age_chart,
            x="ช่วงอายุ",
            y="จำนวน",
            text="จำนวน"
        )

        fig_age.update_layout(
            xaxis_title="ช่วงอายุ",
            yaxis_title="จำนวนผู้เสียชีวิต"
        )

        fig_age.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )

        st.caption(SOURCE_TEXT)

# =========================================================
# VEHICLE
# =========================================================
if "vehicle" in filtered_df.columns:

    st.subheader(
        "🏍️ ผู้เสียชีวิตจำแนกตามประเภทยานพาหนะ"
    )

    vehicle_chart = (
        filtered_df["vehicle"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    vehicle_chart.columns = [
        "ประเภทยานพาหนะ",
        "จำนวน"
    ]

    fig_vehicle = px.bar(
        vehicle_chart,
        x="จำนวน",
        y="ประเภทยานพาหนะ",
        orientation="h",
        text="จำนวน"
    )

    fig_vehicle.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        xaxis_title="จำนวนผู้เสียชีวิต",
        yaxis_title=""
    )

    fig_vehicle.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )

    st.caption(SOURCE_TEXT)

# =========================================================
# DISTRICT
# =========================================================
if "district" in filtered_df.columns:

    st.subheader(
        "🗺️ อำเภอที่มีผู้เสียชีวิตสูงสุด"
    )

    district_chart = (
        filtered_df["district"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    district_chart.columns = [
        "อำเภอ",
        "จำนวน"
    ]

    fig_district = px.bar(
        district_chart,
        x="จำนวน",
        y="อำเภอ",
        orientation="h",
        text="จำนวน"
    )

    fig_district.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        xaxis_title="จำนวนผู้เสียชีวิต",
        yaxis_title=""
    )

    fig_district.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_district,
        use_container_width=True
    )

    st.caption(SOURCE_TEXT)

# =========================================================
# INSIGHTS
# =========================================================
st.divider()

st.subheader("💡 Insights")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    if "province" in filtered_df.columns:

        province_counts = (
            filtered_df["province"]
            .dropna()
            .value_counts()
        )

        if not province_counts.empty:

            province_name = province_counts.index[0]
            province_value = province_counts.iloc[0]

            province_percent = (
                province_value
                / len(filtered_df)
                * 100
            )

            st.info(
                f"จังหวัดที่พบผู้เสียชีวิตสูงสุดคือ "
                f"**{province_name}** "
                f"จำนวน **{province_value:,} คน** "
                f"คิดเป็นประมาณ "
                f"**{province_percent:.1f}%** "
                f"ของข้อมูลหลังการกรอง"
            )

with insight_col2:

    if "vehicle" in filtered_df.columns:

        vehicle_counts = (
            filtered_df["vehicle"]
            .dropna()
            .value_counts()
        )

        if not vehicle_counts.empty:

            vehicle_name = vehicle_counts.index[0]
            vehicle_value = vehicle_counts.iloc[0]

            vehicle_percent = (
                vehicle_value
                / len(filtered_df)
                * 100
            )

            st.info(
                f"ยานพาหนะที่พบมากที่สุดคือ "
                f"**{vehicle_name}** "
                f"จำนวน **{vehicle_value:,} คน** "
                f"คิดเป็นประมาณ "
                f"**{vehicle_percent:.1f}%** "
                f"ของข้อมูลหลังการกรอง"
            )

st.caption(SOURCE_TEXT)

# =========================================================
# DATA TABLE
# =========================================================
st.divider()

with st.expander(
    "📋 ดูข้อมูลที่ใช้ใน Dashboard"
):

    display_df = filtered_df.copy()

    if "month_numeric" in display_df.columns:

        display_df = display_df.drop(
            columns=["month_numeric"]
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(SOURCE_TEXT)

# =========================================================
# DATA SOURCE
# =========================================================
st.divider()

st.subheader("📚 แหล่งข้อมูล")

st.markdown(
    """
**ชุดข้อมูล:** ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนน  
จากระบบบูรณาการข้อมูลการตายจากอุบัติเหตุทางถนน (3 ฐาน) ปี 2567

**หน่วยงาน:** กรมควบคุมโรค  
**ปีข้อมูล:** 2567 (2024)  
**แหล่งเผยแพร่:** data.go.th

**หมายเหตุการใช้งาน Dashboard**
- ตัวกรองสามารถเลือกได้มากกว่า 1 ค่า
- หากไม่เลือกค่าในตัวกรอง หมายถึงใช้ข้อมูลทั้งหมด
- ตัวเลือกของ Filter จะเปลี่ยนตามเงื่อนไขที่เลือกก่อนหน้า
- ค่าเดือนที่ไม่อยู่ในช่วง 1–12 เช่น `-1` ไม่ถูกนำมาแสดงใน Filter เดือนและกราฟรายเดือน
- ข้อมูลที่ไม่มีเดือนยังคงถูกเก็บไว้สำหรับการวิเคราะห์ตัวแปรอื่น
"""
)

# =========================================================
# FOOTER
# =========================================================
st.caption(
    "Road Accident Dashboard | "
    "ข้อมูลอุบัติเหตุทางถนนในประเทศไทย"
)