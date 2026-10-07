import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Road Safety Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COLORS
# =========================================================
NAVY = "#082F5F"
BLUE = "#1479FF"
TEAL = "#00A896"
PINK = "#F25577"
ORANGE = "#F49A25"
PURPLE = "#7137C8"

BG = "#EDF4FA"
CARD = "#FFFFFF"
TEXT = "#082F5F"
SUBTEXT = "#657D98"
BORDER = "#C8D8E7"


# =========================================================
# CSS
# =========================================================
st.markdown(
    f"""
<style>

.stApp {{
    background:
        radial-gradient(circle at 75% 0%, #D9EDFF 0%, transparent 27%),
        {BG};
}}

.block-container {{
    max-width: 1520px;
    padding-top: 4rem !important;
    padding-left: 1.7rem;
    padding-right: 1.7rem;
    padding-bottom: 3rem;
}}

header[data-testid="stHeader"] {{
    background: {BG} !important;
}}

h1, h2, h3, h4, h5, h6 {{
    color: {TEXT} !important;
    font-weight: 850 !important;
}}

p {{
    color: {TEXT};
}}


/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {{
    background:
        radial-gradient(
            circle at 85% 8%,
            rgba(86,154,255,.22),
            transparent 25%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(122,55,244,.18),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #081C38 0%,
            #0A2346 45%,
            #091B36 100%
        );

    border-right: 1px solid rgba(255,255,255,.08);
    box-shadow: 4px 0 20px rgba(0,0,0,.18);
}}

section[data-testid="stSidebar"] > div {{
    padding-top: 1.4rem;
}}

section[data-testid="stSidebar"] h2 {{
    color: #FFFFFF !important;
    font-size: 27px !important;
    font-weight: 900 !important;
}}

section[data-testid="stSidebar"] p {{
    color: #BFD0E6 !important;
}}

section[data-testid="stSidebar"] hr {{
    border-top: 1px solid rgba(255,255,255,.10);
}}


/* =====================================================
   FILTER CARDS
===================================================== */

section[data-testid="stSidebar"]
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background:
        linear-gradient(
            180deg,
            rgba(255,255,255,.07),
            rgba(255,255,255,.04)
        );

    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 18px;
    padding: 8px 9px 12px;
    margin-bottom: 10px;

    box-shadow: 0 7px 16px rgba(0,0,0,.16);
}}

section[data-testid="stSidebar"] label {{
    color: #EDF5FF !important;
    font-size: 16px !important;
    font-weight: 850 !important;
}}


/* =====================================================
   SELECT BOX
===================================================== */

section[data-testid="stSidebar"]
div[data-baseweb="select"] > div {{
    background: #102A4E !important;

    border: 1px solid rgba(255,255,255,.14) !important;

    border-radius: 12px !important;

    min-height: 49px;
}}

section[data-testid="stSidebar"]
div[data-baseweb="select"] span {{
    color: #F4F8FF !important;
}}

section[data-testid="stSidebar"]
div[data-baseweb="select"] svg {{
    fill: #E1EBF8 !important;
}}


/* =====================================================
   MULTISELECT TAGS
===================================================== */

section[data-testid="stSidebar"]
div[data-baseweb="tag"] {{
    background:
        linear-gradient(
            135deg,
            #1687FF,
            #6948FF
        ) !important;

    border-radius: 9px;

    color: #FFFFFF !important;
}}

section[data-testid="stSidebar"]
div[data-baseweb="tag"] span {{
    color: #FFFFFF !important;
}}


/* =====================================================
   RESET
===================================================== */

section[data-testid="stSidebar"]
.stButton > button {{
    min-height: 55px;
    width: 100%;

    border: none;
    border-radius: 15px;

    background:
        linear-gradient(
            100deg,
            #0A7FFF 0%,
            #1557E0 48%,
            #7A37F4 100%
        );

    color: #FFFFFF !important;
    font-size: 16px;
    font-weight: 900;

    box-shadow:
        0 8px 18px rgba(45,84,205,.30);
}}


/* =====================================================
   HERO
===================================================== */

.hero {{
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(
            circle at 88% 20%,
            rgba(122,198,255,.95),
            transparent 19%
        ),
        radial-gradient(
            circle at 70% 110%,
            rgba(24,114,193,.65),
            transparent 38%
        ),
        linear-gradient(
            115deg,
            #072C58 0%,
            #0B4A86 58%,
            #46A3F1 100%
        );

    border-radius: 22px;

    padding: 28px 32px;

    margin-bottom: 24px;

    min-height: 200px;

    box-shadow:
        0 13px 30px rgba(18,63,103,.18);
}}

.hero::after {{
    content: "🏙️   🛣️   🚙";

    position: absolute;
    right: 42px;
    bottom: 25px;

    font-size: 43px;
    opacity: .82;
    letter-spacing: 12px;
}}

.hero-title {{
    color: white !important;

    font-size: 43px;

    font-weight: 900;

    position: relative;
    z-index: 3;
}}

.hero-subtitle {{
    color: #E7F3FF !important;

    font-size: 18px;

    font-weight: 650;

    margin-top: 9px;

    position: relative;
    z-index: 3;
}}

.hero-meta {{
    display: flex;

    gap: 34px;

    margin-top: 28px;

    position: relative;

    z-index: 3;
}}

.hero-meta-item {{
    display: flex;

    align-items: center;

    gap: 10px;

    color: #FFFFFF;

    font-size: 14px;

    font-weight: 650;
}}

.hero-icon {{
    width: 43px;
    height: 43px;

    display: flex;

    align-items: center;
    justify-content: center;

    background: rgba(255,255,255,.16);

    border-radius: 12px;

    font-size: 21px;
}}


/* =====================================================
   SECTION
===================================================== */

.section-title {{
    color: {NAVY};

    font-size: 27px;

    font-weight: 900;

    margin-top: 6px;

    margin-bottom: 15px;
}}


/* =====================================================
   KPI
===================================================== */

.kpi-card {{
    border-radius: 18px;

    padding: 20px;

    min-height: 170px;

    border: 1px solid rgba(140,170,200,.20);

    box-shadow:
        0 8px 20px rgba(30,70,110,.08);
}}

.kpi-pink {{
    background: linear-gradient(135deg,#FFE8ED,#FFF7F9);
}}

.kpi-blue {{
    background: linear-gradient(135deg,#E2F3FF,#F8FCFF);
}}

.kpi-orange {{
    background: linear-gradient(135deg,#FFF0D7,#FFF9EF);
}}

.kpi-purple {{
    background: linear-gradient(135deg,#EEE4FF,#FAF7FF);
}}

.kpi-icon {{
    width: 48px;
    height: 48px;

    display: flex;

    justify-content: center;
    align-items: center;

    border-radius: 50%;

    font-size: 22px;

    margin-bottom: 10px;
}}

.icon-pink {{ background: #FFC9D5; }}
.icon-blue {{ background: #CDE9FF; }}
.icon-orange {{ background: #FFE0AC; }}
.icon-purple {{ background: #DFCEFF; }}

.kpi-label {{
    color: {TEXT};

    font-size: 15px;

    font-weight: 800;
}}

.kpi-value {{
    color: {TEXT};

    font-size: 30px;

    font-weight: 900;

    margin-top: 8px;
}}

.kpi-detail {{
    display: inline-block;

    margin-top: 11px;

    padding: 5px 11px;

    border-radius: 20px;

    background: #E7F8EF;

    color: #12845A;

    font-size: 13px;

    font-weight: 850;
}}


/* =====================================================
   SOURCE
===================================================== */

.source-box {{
    background: rgba(255,255,255,.72);

    border: 1px solid {BORDER};

    border-radius: 12px;

    padding: 10px 14px;

    margin-top: 12px;
    margin-bottom: 14px;

    color: #697F98;

    font-size: 12px;
}}


/* =====================================================
   CROSS FILTER
===================================================== */

.crossfilter-box {{
    background: #DFF1FF;

    border: 1px solid #ADD6F5;

    border-left: 5px solid {BLUE};

    border-radius: 12px;

    padding: 12px 15px;

    margin-bottom: 17px;

    color: {NAVY};
}}


/* =====================================================
   INSIGHT
===================================================== */

.insight-box {{
    background: #FFFFFF;

    border: 1px solid {BORDER};

    border-radius: 15px;

    padding: 18px;

    min-height: 120px;

    box-shadow:
        0 5px 14px rgba(35,75,110,.06);
}}

.insight-label {{
    color: {SUBTEXT};

    font-size: 14px;

    font-weight: 750;
}}

.insight-value {{
    color: {TEXT};

    font-size: 24px;

    font-weight: 900;

    margin-top: 8px;
}}

.insight-sub {{
    color: {SUBTEXT};

    font-size: 14px;

    margin-top: 5px;
}}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SOURCE
# =========================================================
SOURCE_TEXT = (
    "กรมควบคุมโรค — "
    "ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนน "
    "จากระบบบูรณาการข้อมูลการตายจากอุบัติเหตุทางถนน "
    "(3 ฐาน) ปี 2567, data.go.th"
)

SOURCE_URL = "https://data.go.th/dataset/rtddi"


# =========================================================
# MONTH
# =========================================================
MONTH_SHORT = {
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
    12: "ธ.ค.",
}

MONTH_FULL = {
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
    12: "ธันวาคม",
}


# =========================================================
# PROVINCE NAME MAPPING
# =========================================================
THAI_TO_EN = {
    # แก้ตรงนี้สำคัญมาก
    "กรุงเทพมหานคร": "Bangkok Metropolis",

    "กระบี่": "Krabi",
    "กาญจนบุรี": "Kanchanaburi",
    "กาฬสินธุ์": "Kalasin",
    "กำแพงเพชร": "Kamphaeng Phet",
    "ขอนแก่น": "Khon Kaen",
    "จันทบุรี": "Chanthaburi",
    "ฉะเชิงเทรา": "Chachoengsao",
    "ชลบุรี": "Chon Buri",
    "ชัยนาท": "Chai Nat",
    "ชัยภูมิ": "Chaiyaphum",
    "ชุมพร": "Chumphon",
    "เชียงราย": "Chiang Rai",
    "เชียงใหม่": "Chiang Mai",
    "ตรัง": "Trang",
    "ตราด": "Trat",
    "ตาก": "Tak",
    "นครนายก": "Nakhon Nayok",
    "นครปฐม": "Nakhon Pathom",
    "นครพนม": "Nakhon Phanom",
    "นครราชสีมา": "Nakhon Ratchasima",
    "นครศรีธรรมราช": "Nakhon Si Thammarat",
    "นครสวรรค์": "Nakhon Sawan",
    "นนทบุรี": "Nonthaburi",
    "นราธิวาส": "Narathiwat",
    "น่าน": "Nan",
    "บึงกาฬ": "Bueng Kan",
    "บุรีรัมย์": "Buri Ram",
    "ปทุมธานี": "Pathum Thani",
    "ประจวบคีรีขันธ์": "Prachuap Khiri Khan",
    "ปราจีนบุรี": "Prachin Buri",
    "ปัตตานี": "Pattani",
    "พระนครศรีอยุธยา": "Phra Nakhon Si Ayutthaya",
    "พะเยา": "Phayao",
    "พังงา": "Phangnga",
    "พัทลุง": "Phatthalung",
    "พิจิตร": "Phichit",
    "พิษณุโลก": "Phitsanulok",
    "เพชรบุรี": "Phetchaburi",
    "เพชรบูรณ์": "Phetchabun",
    "แพร่": "Phrae",
    "ภูเก็ต": "Phuket",
    "มหาสารคาม": "Maha Sarakham",
    "มุกดาหาร": "Mukdahan",
    "แม่ฮ่องสอน": "Mae Hong Son",
    "ยโสธร": "Yasothon",
    "ยะลา": "Yala",
    "ร้อยเอ็ด": "Roi Et",
    "ระนอง": "Ranong",
    "ระยอง": "Rayong",
    "ราชบุรี": "Ratchaburi",
    "ลพบุรี": "Lop Buri",
    "ลำปาง": "Lampang",
    "ลำพูน": "Lamphun",
    "เลย": "Loei",
    "ศรีสะเกษ": "Si Sa Ket",
    "สกลนคร": "Sakon Nakhon",
    "สงขลา": "Songkhla",
    "สตูล": "Satun",
    "สมุทรปราการ": "Samut Prakan",
    "สมุทรสงคราม": "Samut Songkhram",
    "สมุทรสาคร": "Samut Sakhon",
    "สระแก้ว": "Sa Kaeo",
    "สระบุรี": "Saraburi",
    "สิงห์บุรี": "Sing Buri",
    "สุโขทัย": "Sukhothai",
    "สุพรรณบุรี": "Suphan Buri",
    "สุราษฎร์ธานี": "Surat Thani",
    "สุรินทร์": "Surin",
    "หนองคาย": "Nong Khai",
    "หนองบัวลำภู": "Nong Bua Lam Phu",
    "อ่างทอง": "Ang Thong",
    "อำนาจเจริญ": "Amnat Charoen",
    "อุดรธานี": "Udon Thani",
    "อุตรดิตถ์": "Uttaradit",
    "อุทัยธานี": "Uthai Thani",
    "อุบลราชธานี": "Ubon Ratchathani",
}


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
# HELPERS
# =========================================================
def source_box(extra=""):

    text = SOURCE_TEXT

    if extra:
        text += f" | {extra}"

    st.markdown(
        f'<div class="source-box">📌 ที่มา: {text}</div>',
        unsafe_allow_html=True,
    )


def section_title(text):

    st.markdown(
        f'<div class="section-title">{text}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(
    css_class,
    icon_class,
    icon,
    title,
    value,
    detail,
):

    st.markdown(
        f"""<div class="kpi-card {css_class}">
<div class="kpi-icon {icon_class}">{icon}</div>
<div class="kpi-label">{title}</div>
<div class="kpi-value">{value}</div>
<div class="kpi-detail">{detail}</div>
</div>""",
        unsafe_allow_html=True,
    )


def insight_card(
    title,
    value,
    subtitle,
    border_color,
):

    st.markdown(
        f"""<div class="insight-box"
style="border-top:5px solid {border_color};">
<div class="insight-label">{title}</div>
<div class="insight-value">{value}</div>
<div class="insight-sub">{subtitle}</div>
</div>""",
        unsafe_allow_html=True,
    )


def style_chart(
    fig,
    height=440,
):

    fig.update_layout(
        height=height,

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Arial",
            color=TEXT,
            size=14,
        ),

        xaxis=dict(
            gridcolor="#E5EDF5",
            zeroline=False,
            linecolor="#CCD9E5",
        ),

        yaxis=dict(
            gridcolor="#E5EDF5",
            zeroline=False,
            linecolor="#CCD9E5",
        ),

        margin=dict(
            l=20,
            r=25,
            t=20,
            b=25,
        ),
    )

    return fig


def get_selected_point(event):

    try:

        points = event.selection.points

        if points:
            return points[0]

    except Exception:
        pass

    return None


def set_cross_filter(
    key,
    value,
):

    current = (
        st.session_state
        .cross_filters
        .get(key)
    )

    if current != value:

        st.session_state.cross_filters[key] = value

        st.rerun()


def apply_cross_filters(data):

    result = data.copy()

    cross = st.session_state.cross_filters

    if cross.get("province"):

        result = result[
            result["province"].astype(str)
            == str(cross["province"])
        ]


    if cross.get("district"):

        result = result[
            result["district"].astype(str)
            == str(cross["district"])
        ]


    if cross.get("month"):

        result = result[
            result["month_numeric"]
            == cross["month"]
        ]


    if cross.get("sex"):

        result = result[
            result["sex"].astype(str)
            == str(cross["sex"])
        ]


    if cross.get("age"):

        result = result[
            result["age_group"].astype(str)
            == str(cross["age"])
        ]


    if cross.get("vehicle"):

        result = result[
            result["vehicle"].astype(str)
            == str(cross["vehicle"])
        ]


    return result


def keep_valid_multiselect(
    key,
    options,
):

    if key not in st.session_state:
        return

    values = st.session_state[key]

    if not isinstance(
        values,
        list,
    ):

        st.session_state[key] = []

        return

    st.session_state[key] = [
        value
        for value in values
        if value in options
    ]


# =========================================================
# SESSION
# =========================================================
if "cross_filters" not in st.session_state:

    st.session_state.cross_filters = {
        "province": None,
        "district": None,
        "month": None,
        "sex": None,
        "age": None,
        "vehicle": None,
    }


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    with open(
        DATA_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)


    df = pd.DataFrame(data)

    df = df.dropna(
        how="all"
    )


    df["month_numeric"] = pd.to_numeric(
        df["month"],
        errors="coerce",
    )


    return df


# =========================================================
# LOAD THAILAND MAP
# =========================================================
@st.cache_data
def load_thailand_geojson():

    url = (
        "https://raw.githubusercontent.com/"
        "apisit/thailand.json/master/thailand.json"
    )

    response = requests.get(
        url,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# LOAD DATA
# =========================================================
try:

    df = load_data()

except Exception as e:

    st.error(
        f"ไม่สามารถโหลดข้อมูลได้: {e}"
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown(
        "## 📊 ตัวกรองข้อมูล"
    )

    st.caption(
        "เลือกได้หลายค่า • หากไม่เลือก หมายถึงใช้ข้อมูลทั้งหมด"
    )

    st.divider()


manual_df = df.copy()


# =========================================================
# PROVINCE
# =========================================================
province_options = sorted(
    manual_df["province"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

keep_valid_multiselect(
    "manual_province",
    province_options,
)


with st.sidebar.container(
    border=True
):

    selected_provinces = st.multiselect(
        "📍 จังหวัด",
        province_options,
        placeholder="ทุกจังหวัด",
        key="manual_province",
    )


if selected_provinces:

    manual_df = manual_df[
        manual_df["province"]
        .astype(str)
        .isin(selected_provinces)
    ]


# =========================================================
# SEX
# =========================================================
sex_options = sorted(
    manual_df["sex"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

keep_valid_multiselect(
    "manual_sex",
    sex_options,
)


with st.sidebar.container(
    border=True
):

    selected_sexes = st.multiselect(
        "👤 เพศ",
        sex_options,
        placeholder="ทุกเพศ",
        key="manual_sex",
    )


if selected_sexes:

    manual_df = manual_df[
        manual_df["sex"]
        .astype(str)
        .isin(selected_sexes)
    ]


# =========================================================
# AGE
# =========================================================
age_options = sorted(
    manual_df["age_group"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

keep_valid_multiselect(
    "manual_age",
    age_options,
)


with st.sidebar.container(
    border=True
):

    selected_ages = st.multiselect(
        "🎂 ช่วงอายุ",
        age_options,
        placeholder="ทุกช่วงอายุ",
        key="manual_age",
    )


if selected_ages:

    manual_df = manual_df[
        manual_df["age_group"]
        .astype(str)
        .isin(selected_ages)
    ]


# =========================================================
# MONTH
# =========================================================
month_options = (
    manual_df.loc[
        manual_df["month_numeric"]
        .between(
            1,
            12,
        ),
        "month_numeric",
    ]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

month_options = sorted(
    month_options
)

keep_valid_multiselect(
    "manual_month",
    month_options,
)


with st.sidebar.container(
    border=True
):

    selected_months = st.multiselect(
        "📅 เดือน",
        month_options,
        format_func=lambda x: MONTH_FULL[x],
        placeholder="ทุกเดือน",
        key="manual_month",
    )


if selected_months:

    manual_df = manual_df[
        manual_df["month_numeric"]
        .isin(selected_months)
    ]


# =========================================================
# VEHICLE
# =========================================================
vehicle_options = sorted(
    manual_df["vehicle"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

keep_valid_multiselect(
    "manual_vehicle",
    vehicle_options,
)


with st.sidebar.container(
    border=True
):

    selected_vehicles = st.multiselect(
        "🚗 ประเภทยานพาหนะ",
        vehicle_options,
        placeholder="ทุกประเภท",
        key="manual_vehicle",
    )


if selected_vehicles:

    manual_df = manual_df[
        manual_df["vehicle"]
        .astype(str)
        .isin(selected_vehicles)
    ]


# =========================================================
# RESET
# =========================================================
with st.sidebar:

    if st.button(
        "↻ รีเซ็ตตัวกรองทั้งหมด",
        use_container_width=True,
    ):

        st.session_state.cross_filters = {
            "province": None,
            "district": None,
            "month": None,
            "sex": None,
            "age": None,
            "vehicle": None,
        }


        for key in [
            "manual_province",
            "manual_sex",
            "manual_age",
            "manual_month",
            "manual_vehicle",
        ]:

            if key in st.session_state:

                del st.session_state[key]


        st.rerun()


# =========================================================
# FILTER DATA
# =========================================================
filtered_df = apply_cross_filters(
    manual_df
)


with st.sidebar:

    st.divider()

    st.markdown(
        f"""
**ข้อมูลที่กำลังแสดง**

### {len(filtered_df):,} รายการ
"""
    )


# =========================================================
# HERO
# =========================================================
st.markdown(
    """<div class="hero">
<div class="hero-title">🚗 Road Safety Dashboard</div>
<div class="hero-subtitle">การวิเคราะห์ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนนในประเทศไทย • ปี 2567 (2024)</div>
<div class="hero-meta">
<div class="hero-meta-item"><div class="hero-icon">📊</div><div>ข้อมูลจาก<br><b>กรมควบคุมโรค</b></div></div>
<div class="hero-meta-item"><div class="hero-icon">📅</div><div>ข้อมูลปี<br><b>2567 (2024)</b></div></div>
<div class="hero-meta-item"><div class="hero-icon">📍</div><div>ครอบคลุม<br><b>77 จังหวัด</b></div></div>
</div>
</div>""",
    unsafe_allow_html=True,
)


# =========================================================
# CROSS FILTER STATUS
# =========================================================
cross = st.session_state.cross_filters

active = []


if cross["province"]:

    active.append(
        f"จังหวัด: {cross['province']}"
    )


if cross["district"]:

    active.append(
        f"อำเภอ: {cross['district']}"
    )


if cross["month"]:

    active.append(
        f"เดือน: {MONTH_FULL[cross['month']]}"
    )


if cross["sex"]:

    active.append(
        f"เพศ: {cross['sex']}"
    )


if cross["age"]:

    active.append(
        f"ช่วงอายุ: {cross['age']}"
    )


if cross["vehicle"]:

    active.append(
        f"พาหนะ: {cross['vehicle']}"
    )


if active:

    st.markdown(
        f"""<div class="crossfilter-box">
🎯 <b>กำลังกรองจากการคลิกกราฟ:</b>
{" • ".join(active)}
</div>""",
        unsafe_allow_html=True,
    )


if filtered_df.empty:

    st.warning(
        "ไม่พบข้อมูลตรงกับเงื่อนไขที่เลือก"
    )

    st.stop()


# =========================================================
# KPI DATA
# =========================================================
province_count = (
    filtered_df["province"]
    .dropna()
    .value_counts()
)

vehicle_count = (
    filtered_df["vehicle"]
    .dropna()
    .value_counts()
)

age_count = (
    filtered_df["age_group"]
    .dropna()
    .value_counts()
)


# =========================================================
# KPI
# =========================================================
section_title(
    "📊 ภาพรวมข้อมูล"
)

k1, k2, k3, k4 = st.columns(
    4
)


with k1:

    kpi_card(
        "kpi-pink",
        "icon-pink",
        "👥",
        "ผู้เสียชีวิตทั้งหมด",
        f"{len(filtered_df):,} คน",
        "ข้อมูลปี 2567",
    )


with k2:

    kpi_card(
        "kpi-blue",
        "icon-blue",
        "📍",
        "จังหวัดสูงสุด",

        (
            province_count.index[0]
            if not province_count.empty
            else "-"
        ),

        (
            f"{province_count.iloc[0]:,} คน"
            if not province_count.empty
            else "-"
        ),
    )


with k3:

    kpi_card(
        "kpi-orange",
        "icon-orange",
        "🏍️",
        "พาหนะที่พบมากที่สุด",

        (
            vehicle_count.index[0]
            if not vehicle_count.empty
            else "-"
        ),

        (
            f"{vehicle_count.iloc[0]:,} คน"
            if not vehicle_count.empty
            else "-"
        ),
    )


with k4:

    kpi_card(
        "kpi-purple",
        "icon-purple",
        "👥",
        "ช่วงอายุสูงสุด",

        (
            age_count.index[0]
            if not age_count.empty
            else "-"
        ),

        (
            f"{age_count.iloc[0]:,} คน"
            if not age_count.empty
            else "-"
        ),
    )


source_box()


# =========================================================
# MAP + MONTH
# =========================================================
st.divider()

section_title(
    "🗺️ พื้นที่และช่วงเวลา"
)


c1, c2 = st.columns(
    2,
    gap="large",
)


# =========================================================
# MAP
# =========================================================
with c1:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🗺️ จำนวนผู้เสียชีวิต แยกตามจังหวัด"
        )

        st.caption(
            "สีเข้มหมายถึงจำนวนผู้เสียชีวิตสูงกว่า • คลิกจังหวัดเพื่อกรอง Dashboard"
        )


        map_df = (
            filtered_df["province"]
            .dropna()
            .value_counts()
            .reset_index()
        )


        map_df.columns = [
            "จังหวัด",
            "จำนวนผู้เสียชีวิต",
        ]


        map_df["province_en"] = (
            map_df["จังหวัด"]
            .map(
                THAI_TO_EN
            )
        )


        map_df = map_df.dropna(
            subset=[
                "province_en"
            ]
        )


        try:

            geojson = (
                load_thailand_geojson()
            )


            fig_map = px.choropleth(
                map_df,

                geojson=geojson,

                locations="province_en",

                # GeoJSON นี้ใช้ properties.name
                featureidkey="properties.name",

                color="จำนวนผู้เสียชีวิต",

                hover_name="จังหวัด",

                custom_data=[
                    "จังหวัด"
                ],

                hover_data={
                    "province_en": False,
                    "จำนวนผู้เสียชีวิต": True,
                },

                color_continuous_scale=[
                    "#FFE1E8",
                    "#FFB1C0",
                    "#FF7890",
                    "#F04467",
                    "#B60D36",
                ],
            )


            # =================================================
            # LOCK MAP
            # =================================================
            fig_map.update_geos(
                visible=False,

                projection_type="mercator",

                lataxis_range=[
                    5.8,
                    20.5,
                ],

                lonaxis_range=[
                    97.5,
                    105.7,
                ],

                showcoastlines=False,

                showframe=False,

                bgcolor="rgba(0,0,0,0)",
            )


            fig_map.update_traces(
                marker_line_color="#444444",

                marker_line_width=1,
            )


            fig_map.update_layout(
                clickmode="event+select",

                height=620,

                paper_bgcolor="#FFFFFF",

                margin=dict(
                    l=0,
                    r=0,
                    t=0,
                    b=0,
                ),

                coloraxis_colorbar=dict(
                    title="จำนวน",

                    thickness=13,

                    len=0.62,

                    x=1.01,

                    y=0.52,

                    tickfont=dict(
                        size=12,
                        color=SUBTEXT,
                    ),
                ),
            )


            map_event = st.plotly_chart(
                fig_map,

                use_container_width=True,

                key="province_map",

                on_select="rerun",

                selection_mode="points",

                config={
                    "displayModeBar": False,
                    "scrollZoom": False,
                },
            )


            point = get_selected_point(
                map_event
            )


            if point:

                customdata = point.get(
                    "customdata"
                )


                if customdata:

                    selected_province = (
                        customdata[0]
                    )


                    set_cross_filter(
                        "province",
                        selected_province,
                    )


        except Exception as e:

            st.warning(
                "ไม่สามารถโหลดแผนที่ประเทศไทยได้"
            )

            st.caption(
                str(e)
            )


        source_box()


# =========================================================
# MONTH
# =========================================================
with c2:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📈 แนวโน้มผู้เสียชีวิตรายเดือน"
        )

        st.caption(
            "แนวโน้มจำนวนผู้เสียชีวิตในแต่ละเดือน ปี 2567"
        )


        month_df = filtered_df[
            filtered_df[
                "month_numeric"
            ]
            .between(
                1,
                12,
            )
        ].copy()


        month_chart = (
            month_df
            .groupby(
                "month_numeric"
            )
            .size()
            .reset_index(
                name="จำนวนผู้เสียชีวิต"
            )
            .sort_values(
                "month_numeric"
            )
        )


        month_chart[
            "เดือน"
        ] = (
            month_chart[
                "month_numeric"
            ]
            .map(
                MONTH_SHORT
            )
        )


        fig_month = px.line(
            month_chart,

            x="เดือน",

            y="จำนวนผู้เสียชีวิต",

            markers=True,

            text="จำนวนผู้เสียชีวิต",
        )


        fig_month.update_traces(
            line=dict(
                color=PINK,
                width=4,
            ),

            marker=dict(
                color=PINK,
                size=10,
            ),

            textposition="top center",
        )


        style_chart(
            fig_month,
            620,
        )


        event = st.plotly_chart(
            fig_month,

            use_container_width=True,

            key="month_chart",

            on_select="rerun",

            selection_mode="points",
        )


        point = get_selected_point(
            event
        )


        if point:

            reverse_month = {
                value: key
                for key, value
                in MONTH_SHORT.items()
            }


            month_num = (
                reverse_month.get(
                    point.get("x")
                )
            )


            if month_num:

                set_cross_filter(
                    "month",
                    month_num,
                )


        source_box(
            "แสดงเฉพาะเดือน 1–12"
        )


# =========================================================
# PEOPLE
# =========================================================
st.divider()

section_title(
    "👥 ลักษณะของผู้เสียชีวิต"
)


c3, c4 = st.columns(
    2,
    gap="large",
)


# =========================================================
# SEX
# =========================================================
with c3:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 👤 ผู้เสียชีวิตจำแนกตามเพศ"
        )


        sex_chart = (
            filtered_df["sex"]
            .dropna()
            .value_counts()
            .reset_index()
        )


        sex_chart.columns = [
            "เพศ",
            "จำนวน",
        ]


        fig_sex = px.pie(
            sex_chart,

            names="เพศ",

            values="จำนวน",

            hole=0.55,

            color_discrete_sequence=[
                BLUE,
                PINK,
                PURPLE,
                TEAL,
            ],
        )


        fig_sex.update_traces(
            textposition="inside",

            textinfo="percent+label",
        )


        fig_sex.update_layout(
            height=420,

            paper_bgcolor="#FFFFFF",
        )


        event = st.plotly_chart(
            fig_sex,

            use_container_width=True,

            key="sex_chart",

            on_select="rerun",

            selection_mode="points",
        )


        point = get_selected_point(
            event
        )


        if point:

            value = point.get(
                "label"
            )


            if value:

                set_cross_filter(
                    "sex",
                    value,
                )


        source_box()


# =========================================================
# AGE
# =========================================================
with c4:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🎂 ผู้เสียชีวิตจำแนกตามช่วงอายุ"
        )


        age_chart = (
            filtered_df["age_group"]
            .dropna()
            .value_counts()
            .reset_index()
        )


        age_chart.columns = [
            "ช่วงอายุ",
            "จำนวนผู้เสียชีวิต",
        ]


        fig_age = px.bar(
            age_chart,

            x="ช่วงอายุ",

            y="จำนวนผู้เสียชีวิต",

            text="จำนวนผู้เสียชีวิต",

            color_discrete_sequence=[
                PURPLE
            ],
        )


        fig_age.update_traces(
            textposition="outside"
        )


        style_chart(
            fig_age,
            420,
        )


        event = st.plotly_chart(
            fig_age,

            use_container_width=True,

            key="age_chart",

            on_select="rerun",

            selection_mode="points",
        )


        point = get_selected_point(
            event
        )


        if point:

            value = point.get(
                "x"
            )


            if value:

                set_cross_filter(
                    "age",
                    value,
                )


        source_box()


# =========================================================
# VEHICLE + DISTRICT
# =========================================================
st.divider()

section_title(
    "🚦 พาหนะและพื้นที่ระดับอำเภอ"
)


c5, c6 = st.columns(
    2,
    gap="large",
)


# =========================================================
# VEHICLE
# =========================================================
with c5:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🏍️ ประเภทยานพาหนะ"
        )


        vehicle_chart = (
            filtered_df["vehicle"]
            .dropna()
            .value_counts()
            .head(12)
            .reset_index()
        )


        vehicle_chart.columns = [
            "ประเภทยานพาหนะ",
            "จำนวนผู้เสียชีวิต",
        ]


        fig_vehicle = px.bar(
            vehicle_chart,

            x="จำนวนผู้เสียชีวิต",

            y="ประเภทยานพาหนะ",

            orientation="h",

            text="จำนวนผู้เสียชีวิต",

            color_discrete_sequence=[
                ORANGE
            ],
        )


        fig_vehicle.update_layout(
            yaxis=dict(
                categoryorder="total ascending",
                title="",
            )
        )


        fig_vehicle.update_traces(
            textposition="outside"
        )


        style_chart(
            fig_vehicle,
            480,
        )


        event = st.plotly_chart(
            fig_vehicle,

            use_container_width=True,

            key="vehicle_chart",

            on_select="rerun",

            selection_mode="points",
        )


        point = get_selected_point(
            event
        )


        if point:

            value = point.get(
                "y"
            )


            if value:

                set_cross_filter(
                    "vehicle",
                    value,
                )


        source_box()


# =========================================================
# DISTRICT
# =========================================================
with c6:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🗺️ อำเภอที่มีผู้เสียชีวิตสูงสุด"
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
            "จำนวนผู้เสียชีวิต",
        ]


        fig_district = px.bar(
            district_chart,

            x="จำนวนผู้เสียชีวิต",

            y="อำเภอ",

            orientation="h",

            text="จำนวนผู้เสียชีวิต",

            color_discrete_sequence=[
                TEAL
            ],
        )


        fig_district.update_layout(
            yaxis=dict(
                categoryorder="total ascending",
                title="",
            )
        )


        fig_district.update_traces(
            textposition="outside"
        )


        style_chart(
            fig_district,
            480,
        )


        event = st.plotly_chart(
            fig_district,

            use_container_width=True,

            key="district_chart",

            on_select="rerun",

            selection_mode="points",
        )


        point = get_selected_point(
            event
        )


        if point:

            value = point.get(
                "y"
            )


            if value:

                set_cross_filter(
                    "district",
                    value,
                )


        source_box()


# =========================================================
# INSIGHTS
# =========================================================
st.divider()

section_title(
    "💡 สรุปข้อมูลสำคัญ"
)


i1, i2, i3 = st.columns(
    3
)


with i1:

    if not province_count.empty:

        insight_card(
            "📍 จังหวัดที่มีจำนวนสูงสุด",

            province_count.index[0],

            f"{province_count.iloc[0]:,} คน",

            BLUE,
        )


with i2:

    if not age_count.empty:

        insight_card(
            "👥 ช่วงอายุที่พบมากที่สุด",

            age_count.index[0],

            f"{age_count.iloc[0]:,} คน",

            PURPLE,
        )


with i3:

    if not vehicle_count.empty:

        insight_card(
            "🏍️ พาหนะที่พบมากที่สุด",

            vehicle_count.index[0],

            f"{vehicle_count.iloc[0]:,} คน",

            ORANGE,
        )


# =========================================================
# TABLE
# =========================================================
st.divider()


with st.expander(
    "📋 ดูข้อมูลที่ใช้ใน Dashboard"
):

    display_df = (
        filtered_df.copy()
    )


    if (
        "month_numeric"
        in display_df.columns
    ):

        display_df = display_df.drop(
            columns=[
                "month_numeric"
            ]
        )


    st.dataframe(
        display_df,

        use_container_width=True,

        hide_index=True,

        height=350,
    )


# =========================================================
# DATA QUALITY
# =========================================================
with st.expander(
    "✅ Data Quality"
):

    q1, q2, q3 = st.columns(
        3
    )


    q1.metric(
        "จำนวน Records",

        f"{len(filtered_df):,}",
    )


    missing_cells = (
        filtered_df
        .isna()
        .sum()
        .sum()
    )


    total_cells = (
        filtered_df.shape[0]
        * filtered_df.shape[1]
    )


    missing_pct = (
        missing_cells
        / total_cells
        * 100

        if total_cells
        else 0
    )


    q2.metric(
        "Missing Values",

        f"{missing_pct:.2f}%",
    )


    unknown_month = (
        ~filtered_df[
            "month_numeric"
        ]
        .between(
            1,
            12,
        )
    ).sum()


    q3.metric(
        "ไม่ระบุเดือน",

        f"{unknown_month:,}",
    )


# =========================================================
# SOURCE
# =========================================================
with st.expander(
    "📚 แหล่งข้อมูลและข้อจำกัด"
):

    st.markdown(
        f"""
**ชุดข้อมูล**  
ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนน จากระบบบูรณาการข้อมูลการตายจากอุบัติเหตุทางถนน (3 ฐาน) ปี 2567

**หน่วยงาน:** กรมควบคุมโรค  
**ปีข้อมูล:** 2567 (2024)  
**แหล่งเผยแพร่:** data.go.th  
**Dataset:** {SOURCE_URL}

**หมายเหตุ**
- ค่าเดือนที่ไม่อยู่ในช่วง 1–12 ไม่ถูกใช้ในกราฟรายเดือน
- Filter สามารถเลือกได้หลายค่า
- คลิกจังหวัดบนแผนที่เพื่อกรอง Dashboard
- คลิกเดือน เพศ อายุ พาหนะ หรืออำเภอเพื่อกรองต่อได้
- จำนวนผู้เสียชีวิตที่แสดงเป็นจำนวนในชุดข้อมูล ไม่ใช่อัตราความเสี่ยงโดยตรง
"""
    )


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.markdown(
    f"""
<div style="
text-align:center;
color:{SUBTEXT};
font-size:13px;
padding:12px;
">
Thailand Road Safety Dashboard • Statistics & Data Visualization
</div>
""",
    unsafe_allow_html=True,
)