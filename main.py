import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Tech Layoffs Dashboard",
                   page_icon = "📊",
                   layout = "wide",
)   

st.title("AI Job Market Trend 2026 (Raw Data)") 


df = pd.read_csv("assets/AI_Job_Market_Trends_2026.csv")
#first_clean-data
df = df.drop(columns = ['job_id', 'job_posting_month','job_openings']) #ลบ column ที่ไม่จำเป็นออก

# --- SIDE BAR ---

st.sidebar.header("Filter here") #ตั้งหัวข้อ sidebar

Job = st.sidebar.multiselect(
    "Select the Job:", #Label
    options=df["job_title"].unique(),# options คือการตั้งค่าตัวเลือกให้เลือกได้จาก Column    job_title ใน DataFrame df
    # .unique() คือคำสั่งของ pandas เพื่อกรองค่าซ้ำออก ให้เหลือที่ไม่ซ้ำ (Unique values)
    default=df["job_title"].unique() # default คือการตั้งค่าเริ่มต้นให้เลือกทุกอย่างใน Column
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
''' # รอ clean data ใหม่ก่อนทำ Dashboard

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
    
st.write("---") #ขีดเส้นแบ่ง''' 
 

# --- BAR CHART ---
job_salary = (
    df_selection.groupby(by=["job_title"])[["salary"]].mean().reset_index() #groupby คือการจัดกลุ่มข้อมูลตาม job_title แล้วคำนวณค่าเฉลี่ยของ salary จากนั้น reset_index() เพื่อให้ job_title กลายเป็น column ปกติ
)
