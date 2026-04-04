import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Tech Layoffs Dashboard",
                   page_icon = "📊",
                   layout = "wide",
)   

st.title("Video Games Sales") 

df = pd.read_csv("assets/vgsales.csv")

# --- Small clean data ---
df_2 = df.sample(n = 100,random_state=4) #สุ่มแถวมา 5 แถว , ถ้าไม่มั random state จะสุ่มไปเรื่อยๆใช้อันนี้เพื่อเลือก state ที่แน่นอน 
df_2.reset_index(drop = True ,inplace = True) # reset index , inplace คือการเปลี่ยนแปลงข้อมูลเดิมโดยไม่ต้องเอาตัวแปรใหม่มารับ , drop คือ drop index เดิมทิ้ง 
df_2.drop('Rank', axis = 1 , inplace =True , errors = 'ignore')# ลบคอลัม Rank แทนที่ df_2 ที่เดิม และ ไม่สน error เพราะตอนรันที่หลังจะติด error rank ไม่มีอยู่จริงเพราะลบไปแล้ว

df_3 = df_2.copy() # .copy() เพื่อทำสำเนาแยกให้ใช้ memory แยกกัน แต่ถ้า df_3 = df_2 มันจะใช้ memory เดิม แค่เปลี่ยนชื่อจาก df_2 เป็น df_3
df_3[['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']] = df_3[['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']].astype(str) + ' M'


# --- SIDE BAR ---
st.sidebar.header("Filter here") #ตั้งหัวข้อ sidebar

Genre_v = st.sidebar.multiselect(
    "Select the Genre:", #Label
    options=df["Genre"].unique(),# options คือการตั้งค่าตัวเลือกให้เลือกได้จาก Column Genre ใน DataFrame df
    # .unique() คือคำสั่งของ pandas เพื่อกรองค่าซ้ำออก ให้เหลือที่ไม่ซ้ำ (Unique values)
    default=df["Genre"].unique() # default คือการตั้งค่าเริ่มต้นให้เลือกทุกอย่างใน Column
) 

Platform_v = st.sidebar.multiselect(
    "Select the Platform:",
    options=df["Platform"].unique(),
    default=df["Platform"].unique()
)

df_selection = df_3.query(
    "Genre == @Genre_v & Platform == @Platform_v" # @ คือการอ้างอิงถึงซักอย่าง ในที่นี้คือการอ้างอิงถึงตัวแปร Job และ Company_Size
)

st.dataframe(df_selection) #แสดงตารางข้อมูลที่ผ่านการกรองแล้ว

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

Total_Sales = (
    df_2.groupby(by=["Genre"])[["Global_Sales"]].sum().round(1).reset_index() #groupby คือการจัดกลุ่มข้อมูลตาม Genre แล้วคำนวณค่าเฉลี่ยของ Global_Sales จากนั้น reset_index() เพื่อให้ Genre กลายเป็น column ปกติ
)                                                       #round(1) ปัดขึ้นให้เหลือ 1 ตำแหน่ง
fig_bar = px.bar(
    Total_Sales, # ใข้ dataframe
    x="Global_Sales", #ใช้ column salary เป็นแกน x
    #y=Total_Sales.index, #ให้แสดงเลข index ของ job_title เป็นแกน y
    y = Total_Sales.index,
    title = "<b>Total Global Sales</b>",
    color_discrete_sequence = ["#0083B8"] * len(Total_Sales),
    template = "plotly_white"
)

st.plotly_chart(fig_bar) 

   

