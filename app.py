import streamlit as st
import os
import pandas as pd
import docx
import base64

# পেজ সেটআপ
st.set_page_config(page_title="মাল্টি-ক্যাটাগরি রিপোর্ট পোর্টাল", page_icon="📁", layout="wide")

# ফাইল সংরক্ষণের মূল ফোল্ডার
UPLOAD_DIR = "reports_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ক্যাটাগরির তালিকা
CATEGORIES = [
    "Monthly Report", 
    "Annual Report", 
    "Project Report", 
    "Audit Report", 
    "Vouchers & Bills",
    "Other Documents"
]

st.title("📁 ফাইল ও রিপোর্ট ম্যানেজমেন্ট পোর্টাল")
st.markdown("---")

# সাইডবার মেনু
menu = ["রিপোর্ট দেখুন (View Reports)", "নতুন ফাইল আপলোড (Upload File)"]
choice = st.sidebar.selectbox("মেনু নির্বাচন করুন", menu)

# --- নতুন ফাইল আপলোড সেকশন ---
if choice == "নতুন ফাইল আপলোড (Upload File)":
    st.subheader("📤 নতুন ফাইল জমা দিন")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category = st.selectbox("ক্যাটাগরি/ফোল্ডারের ধরন সিলেক্ট করুন", CATEGORIES)
    with col2:
        year = st.selectbox("বছর নির্বাচন করুন", ["2024", "2025", "2026", "2027", "2028"])
    with col3:
        month = st.selectbox("মাস নির্বাচন করুন", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
    
    uploaded_file = st.file_uploader(
        "এক্সেল (.xlsx), ওয়ার্ড (.docx) বা পিডিএফ (.pdf) ফাইল সিলেক্ট করুন", 
        type=["xlsx", "xls", "docx", "pdf"]
    )
    
    if uploaded_file is not None:
        save_path = os.path.join(UPLOAD_DIR, category, year, month)
        os.makedirs(save_path, exist_ok=True)
        
        file_path = os.path.join(save_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ ফাইল জমা হয়েছে: `{uploaded_file.name}` ({category} ➔ {year} ➔ {month})")

# --- ফাইল দেখার ও প্রিভিউ সেকশন ---
elif choice == "রিপোর্ট দেখুন (View Reports)":
    st.subheader("📂 সংরক্ষিত ফাইলসমূহ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categories_available = sorted(os.listdir(UPLOAD_DIR)) if os.path.exists(UPLOAD_DIR) else []
        selected_cat = st.selectbox("ক্যাটাগরি সিলেক্ট করুন", categories_available if categories_available else ["কোনো ডেটা নেই"])
    
    with col2:
        cat_path = os.path.join(UPLOAD_DIR, selected_cat) if selected_cat != "কোনো ডেটা নেই" else ""
        years_available = sorted(os.listdir(cat_path)) if os.path.exists(cat_path) else []
        selected_year = st.selectbox("বছর সিলেক্ট করুন", years_available if years_available else ["কোনো ডেটা নেই"])
    
    with col3:
        year_path = os.path.join(cat_path, selected_year) if selected_year != "কোনো ডেটা নেই" else ""
        months_available = sorted(os.listdir(year_path)) if os.path.exists(year_path) else []
        selected_month = st.selectbox("মাস সিলেক্ট করুন", months_available if months_available else ["কোনো ডেটা নেই"])
        
    if selected_cat != "কোনো ডেটা নেই" and selected_year != "কোনো ডেটা নেই" and selected_month != "কোনো ডেটা নেই":
        target_dir = os.path.join(UPLOAD_DIR, selected_cat, selected_year, selected_month)
        files = os.listdir(target_dir) if os.path.exists(target_dir) else []
        
        if files:
            selected_file = st.selectbox("ফাইল সিলেক্ট করুন", files)
            file_full_path = os.path.join(target_dir, selected_file)
            
            # ডাউনলোড বাটন
            with open(file_full_path, "rb") as f:
                st.download_button(
                    label=f"⬇️ {selected_file} ডাউনলোড করুন",
                    data=f,
                    file_name=selected_file
                )
            
            st.markdown("---")
            st.write("### 👁️ লাইভ প্রিভিউ (Live Preview)")
            
            # Excel Preview
            if selected_file.endswith(('.xlsx', '.xls')):
                try:
                    df = pd.read_excel(file_full_path)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"এক্সেল ফাইল পড়তে সমস্যা হয়েছে: {e}")
                    
            # Word Preview
            elif selected_file.endswith('.docx'):
                try:
                    doc = docx.Document(file_full_path)
                    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
                    st.text_area("ডকুমেন্টের লেখা:", value="\n\n".join(full_text), height=400)
                except Exception as e:
                    st.error(f"ওয়ার্ড ফাইল পড়তে সমস্যা হয়েছে: {e}")

            # PDF Preview
            elif selected_file.endswith('.pdf'):
                try:
                    with open(file_full_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"পিডিএফ ফাইল দেখতে সমস্যা হয়েছে: {e}")
        else:
            st.info("এই ফোল্ডারে কোনো ফাইল পাওয়া যায়নি।")
