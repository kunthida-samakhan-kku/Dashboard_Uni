import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="KKU Admission Dashboard", layout="wide")

# Load data safely
@st.cache_data
def load_data():
    file_path = 'data/processed/khonkaen_high_school_cleaned.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

df_hs = load_data()

st.title("KKU Admission Dashboard")

# Navigation
page = st.sidebar.radio("Navigation", [
    "PAGE 1 - OVERVIEW",
    "PAGE 2 - FACULTY & MAJOR",
    "PAGE 3 - STUDY BACKGROUND",
    "PAGE 4 - TREND",
    "PAGE 5 - GEOGRAPHIC ANALYSIS"
])

if page == "PAGE 1 - OVERVIEW":
    st.header("Overview")
    st.warning("⚠️ ไม่พบข้อมูล Open Data ที่เพียงพอ สำหรับวิเคราะห์การสมัครและการรับเข้าศึกษาของมหาวิทยาลัยขอนแก่น")
    
    if not df_hs.empty:
        st.subheader("ข้อมูลพื้นฐาน: จำนวนนักเรียนระดับมัธยมศึกษาตอนปลาย จังหวัดขอนแก่น")
        
        col1, col2 = st.columns(2)
        latest_year = df_hs['year'].max()
        latest_val = df_hs[df_hs['year'] == latest_year]['student_count'].values[0]
        
        with col1:
            st.metric(f"จำนวน ม.ปลาย จ.ขอนแก่น (ปี {latest_year})", f"{latest_val:,.0f} คน")
            
        fig = px.line(df_hs, x='year', y='student_count', title='แนวโน้มจำนวนนักเรียน ม.ปลาย จังหวัดขอนแก่น', markers=True)
        st.plotly_chart(fig, use_container_width=True)

elif page == "PAGE 2 - FACULTY & MAJOR":
    st.header("Faculty & Major Analysis")
    st.error("❌ ไม่พบข้อมูล Open Data ที่เพียงพอสำหรับวิเคราะห์ข้อมูลระดับคณะและสาขา")
    st.markdown("ตามเงื่อนไขของการพัฒนา Dashboard นี้ ห้ามใช้การประมาณค่าหรือสร้างข้อมูลขึ้นมาเองโดยไม่มีแหล่งอ้างอิง")

elif page == "PAGE 3 - STUDY BACKGROUND":
    st.header("Study Background")
    st.error("❌ ไม่พบข้อมูล Open Data ที่เพียงพอสำหรับระบุว่านักศึกษาที่เข้าเรียนจริงในแต่ละคณะมาจากสายการเรียนใด")
    st.warning("ข้อมูลนี้แสดงคุณสมบัติ/แผนการเรียนที่สาขาเปิดรับ ไม่ใช่สายการเรียนจริงของนักศึกษา")

elif page == "PAGE 4 - TREND":
    st.header("Trend Analysis")
    if not df_hs.empty:
        fig = px.bar(df_hs, x='year', y='student_count', title='แนวโน้มจำนวนนักเรียน ม.ปลาย จังหวัดขอนแก่น')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลเพียงพอ")

elif page == "PAGE 5 - GEOGRAPHIC ANALYSIS":
    st.header("Geographic Analysis")
    st.error("❌ ไม่พบข้อมูล Open Data ที่เพียงพอสำหรับวิเคราะห์จังหวัดของนักศึกษา KKU")
