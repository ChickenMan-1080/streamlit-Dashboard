import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Tech Layoffs Dashboard",
                   page_icon = "📊",
                   layout = "wide",
)   

st.title("AI Job Market Trend 2026 (Raw Data)") 


df = pd.read_csv("assets/AI_Job_Market_Trends_2026.csv")

# --- SIDE BAR ---

st.sidebar.header("Filter here") #ตั้งหัวข้อ sidebar

Job = st.sidebar.multiselect(
    "Select the Job:", #Label
    options=df["job_title"].unique(), #.unique() คือสั่งของ pandas เพื่อกรองค่าซ้ำออก เหลือที่ไม่ซ้ำก (Unique values)
    default=df["job_title"].unique() #default คือการตั้งค่าเริ่มต้นให้เลือกทุกอย่างใน Column
) 

Company_Size = st.sidebar.multiselect(
    "Select the Company Size:",
    options=df["company_size"].unique(),
    default=df["company_size"].unique()
)

df_selection = df.query(
    "job_title == @Job & company_size == @Company_Size" # @ คือการอ้างอิงถึงซักอย่าง ในที่นี้คือการอ้างอิงถึงตัวแปร Job และ Company_Size
)

st.dataframe(df_selection) #แสดงตารางข้อมูลที่ผ่านการกรองแล้ว

## --- AI Market Trend 2026 Dashboard ---
'''
.
.
.
.
'''

'''
# --- MAIN PAGE ---
st.title("Bar Chart : AI Dashboard")

# Calculate
total_layoffs_2024 = int(df_selection['layoffs_2024'].sum())
total_layoffs_2025 = int(df_selection['layoffs_2025'].sum())

left_column , right_column = st.columns(2)
with left_column : 
    st.subheader("Layoffs in 2024 :")  #หัวข้อย่อย
    st.markdown(f'Total : {total_layoffs_2024}')
    
with right_column :
    st.subheader("Layoffs in 2025 :") 
    st.markdown(f'Total : {total_layoffs_2025}')
    
st.write("---") #ขีดเส้นแบ่ง''' #เปลี่ยน Datasets รอ clean data ใหม่ ก่อนทำ Dashboard
 
## ยังไม่ได้ clean data 