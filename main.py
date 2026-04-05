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
df_2 = df.sample(n = 100,random_state=4) #สุ่มแถวมา 100 แถว , ถ้าไม่มั random state จะสุ่มไปเรื่อยๆใช้อันนี้เพื่อเลือก state ที่แน่นอน 
df_2.reset_index(drop = True ,inplace = True) # reset index , inplace คือการเปลี่ยนแปลงข้อมูลเดิมโดยไม่ต้องเอาตัวแปรใหม่มารับไม่ต้องเอา data frame ใหม่มารับ , drop คือ drop index เดิมทิ้ง 
df_2.drop('Rank', axis = 1 , inplace =True , errors = 'ignore')# ลบคอลัม Rank แทนที่ df_2 ที่เดิม และ ไม่สน error เพราะตอนรันที่หลังจะติด error rank ไม่มีอยู่จริงเพราะลบไปแล้ว

#df_3 = df_2.copy() # .copy() เพื่อทำสำเนาแยกให้ใช้ memory แยกกัน แต่ถ้า df_3 = df_2 มันจะใช้ memory เดิม แค่เปลี่ยนชื่อจาก df_2 เป็น df_3
#df_3[['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']] = df_3[['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']].astype(str) + ' M'


# --- SIDE BAR ---
st.sidebar.header("Filter here") #ตั้งหัวข้อ sidebar

Genre_v = st.sidebar.multiselect(
    "Select the Genre:", #Label
    options=df_2["Genre"].unique(),# options คือการตั้งค่าตัวเลือกให้เลือกได้จาก Column Genre ใน DataFrame df
    # .unique() คือคำสั่งของ pandas เพื่อกรองค่าซ้ำออก ให้เหลือที่ไม่ซ้ำ (Unique values)
    default=df_2["Genre"].unique() # default คือการตั้งค่าเริ่มต้นให้เลือกทุกอย่างใน Column
) 

Platform_v = st.sidebar.multiselect(
    "Select the Platform:",
    options=df_2["Platform"].unique(),
    default=df_2["Platform"].unique()
)

df_selection = df_2.query(
    "Genre == @Genre_v & Platform == @Platform_v" # @ คือการอ้างอิงถึงซักอย่าง ในที่นี้คือการอ้างอิงถึงตัวแปร Genre_v และ Platform_v
)

st.dataframe(df_selection) #แสดงตารางข้อมูลที่ผ่านการกรองแล้ว


# --- MAIN PAGE ---
st.title("Bar Chart : Total Sales Dash Borad")

# Calculate
total_na_sales = df_selection['NA_Sales'].sum().round(2)
total_jp_sales = df_selection['JP_Sales'].sum().round(2) #ทั้งสอง total_na_sales และ total_jp_sales เมื่อ sum ออกมาจะมีตัวเลข 0.000..2 ออกมา
                                                         #เพราะเลขบางตังเมื่อแปลงเลขฐาน 10 เป็นเลขฐาน 2 มันจะแปลงได้ไม่ลงตัวทำให้เกิดทศนิยมไม่รู้จบ 
                                                         #ปรากฏการณ์นี้เรียกว่า floating point precision error มันคือข้อจำกัดทางคอมพิวเตอร์ ไม่ใช่ความผิดพลาดของข้อมูล  
                                                         # from decimal import Decimal ใช้ library นี้ถ้าอนากให้เป๊ะ จริงๆ ถ้าต้องการจัดการสิ่งที่จำเป็นจริงเช่น ในการการบัญชี/การเงิน
total_eu_sales = df_selection['EU_Sales'].sum().round(2)
total_other_sales = df_selection['Other_Sales'].sum().round(2)

total_global_sales = df_selection['Global_Sales'].sum().round(2)

# --- DASH BOARD TEXT ---
left_column , right_column = st.columns(2)
left_column_1 , right_column_1 = st.columns([1,1])
center_col, = st.columns(1 , vertical_alignment="center")

#center_col = st.columns(1 , vertical_alignment="center") #returnเป็น list ใช้ไม่ได้

with left_column : 
    st.subheader("North America Sales :")  #หัวข้อย่อย
    st.markdown(f'Total : {total_na_sales} Million Dollors')   #การเรียกใช้ 
    
with right_column :
    st.subheader("Japan Sales :") 
    st.markdown(f'Total : {total_jp_sales} Milliion Dollors')
    
with left_column_1 :
    st.subheader("Europe Sales")
    st.markdown(f"Total : {total_eu_sales} Million Dollors")
    
with right_column_1 :
    st.subheader('Others')
    st.markdown(f"Total : {total_other_sales} Million Dollors")
    

with center_col :
    st.subheader("Global Sales")
    st.markdown(f"Total : {total_global_sales} Million Dollors")
    
#center_col = (center_col.subheader('Global Sales').markdown(f"Total : {total_global_sales}")) #ใช้ไมได้เพราะsunheader จะ return none

 


st.write("---") #ขีดเส้นแบ่ง 
 

# --- SET-UP BEFORE BAR CHART ---

#ใส่วงเล็บเพื่อให้เว้นบรรทัดได้ code จะได้ไม่รก
Total_Sales = (
    df_selection.groupby(by=["Genre"])[["Global_Sales"]]
    .sum()
    .round(1)
    .reset_index()
    .sort_values(by = "Global_Sales") #groupby คือการจัดกลุ่มข้อมูลตาม Genre แล้วคำนวณค่าเฉลี่ยของ Global_Sales จากนั้น reset_index() เพื่อให้ Genre กลายเป็น column ปกติ
)                                                       #round(1) ปัดขึ้นให้เหลือ 1 ตำแหน่ง
# --- BAR CHART ---

if Total_Sales.empty:
    st.warning("The Graph is Empty !")
else :    
    fig_bar = px.bar(
        Total_Sales, # ใข้ dataframe
        x="Global_Sales", #ใช้ column Global_Sales เป็นแกน x
        y = "Genre", #ให้แสดงเลข index ของ Genre เป็นแกน y
        orientation= 'h', #horizontal bar chart
        title = "<b>Total Global Sales</b>",
        color_discrete_sequence = ["#F78708"] * len(Total_Sales),
        template = "plotly_white" ,
        text = 'Genre'    
    )
    # --- PLOT BAR CHART ---
    fig_bar.update_traces(
    texttemplate = "%{x:.1f} M", #ใช้ค่าจากแกน x มาเปลี่ยนให้เป็น str แล้วเขียน M เพื่ม
    textposition = "outside" #กำหนดข้อความให้อยู่นอกแท่งกราฟ
)
    
    st.plotly_chart(fig_bar)

# --- Error Chart ---
 
#fig_bar_2 = fig_bar[['Global_Sales']].astype(str) + " M"
#st.plotly_chart(fig_bar_2) 
#ใช้คำสั่ง pandas ไม่ได้นะอย่าสับสน





