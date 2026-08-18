print("ระบบตรวจสอบงานก่อสร้างกำลังเริ่มต้น...")
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

st.title("ระบบตรวจสอบงานคงค้างงานก่อสร้าง (Real-time)")

# 1. กำหนดรายการวัสดุหลักที่มี (Master List)
master_list = {
    "เหล็กเส้น 12 มม.": 100,
    "ปูนซีเมนต์ (ถุง)": 50,
    "อิฐมอญ": 1000
}

st.subheader("1. รายการวัสดุตั้งต้นในระบบ")
st.write(master_list)

# 2. ส่วนสำหรับอัปโหลดไฟล์งาน (รองรับ Excel หรือ CSV)
st.subheader("2. อัปโหลดไฟล์รายงานหน้างาน (ภาษาอังกฤษ)")
uploaded_file = st.file_uploader("เลือกไฟล์ Excel หรือ CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    # อ่านไฟล์
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("ข้อมูลดิบจากไฟล์ที่อัปโหลด:")
    st.dataframe(df)
    
    # สมมติว่าไฟล์มีคอลัมน์ 'Item' (ชื่อวัสดุอังกฤษ) และ 'Quantity' (จำนวน)
    if 'Item' in df.columns and 'Quantity' in df.columns:
        translator = GoogleTranslator(source='en', target='th')
        
        remaining_items = {}
        st.subheader("3. ผลการแปลและตรวจสอบรายการคงค้าง")
        
        for index, row in df.iterrows():
            eng_name = str(row['Item'])
            qty = row['Quantity']
            
            # แปลภาษาอังกฤษเป็นไทย
            thai_name = translator.translate(eng_name)
            
            st.write(f"- ไฟล์ระบุ: **{eng_name}** (แปลเป็นไทย: **{thai_name}**) | จำนวน: {qty}")
            
            # คำนวณยอดคงค้างเทียบกับ Master List
            if thai_name in master_list:
                remaining = master_list[thai_name] - qty
                remaining_items[thai_name] = remaining
            else:
                remaining_items[thai_name + " (ไม่พบในระบบหลัก)"] = -qty
                
        st.subheader("สรุปรายการที่ยังคงค้าง:")
        st.write(remaining_items)
    else:
        st.error("กรุณาตรวจสอบชื่อคอลัมน์ในไฟล์ ให้มีชื่อว่า 'Item' และ 'Quantity'")
