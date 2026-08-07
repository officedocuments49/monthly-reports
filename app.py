import base64
import docx
import pandas as pd
import streamlit as st
from datetime import datetime

# --- পেজ সেটআপ ---
st.set_page_config(
    page_title="সমাজসেবা অধিদপ্তর - ডিজিটাল ক্যাটাগরি ড্যাশবোর্ড",
    page_icon="🟢",
    layout="wide"
)

# --- সেশন স্টেট (যাতে ক্লিক করা ক্যাটাগরি মনে রাখে) ---
# এটি খুবই জরুরি, এটিই ক্লিক করার পর পেজ আপডেট করার কাজ করবে
if 'selected_category_key' not in st.session_state:
    st.session_state.selected_category_key = "job"

# --- কাস্টম সিএসএস (সুন্দর বাটন ও হেডার ডিজাইন) ---
st.markdown("""
    <style>
    .main-header {
        background-color: #006a4e;
        color: white;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        border-bottom: 4px solid #f42a41;
        margin-bottom: 20px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        color: white;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 14px;
        color: #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 17px;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #006a4e;
        transition: all 0.3s ease;
        line-height: 1.2;
    }
    .stButton>button:hover {
        background-color: #006a4e !important;
        color: white !important;
        border-color: #006a4e !important;
    }
    /* নির্বাচিত বাটনের কালার */
    .stButton>button:focus {
        background-color: #f42a41 !important;
        color: white !important;
        border-color: #f42a41 !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- টপ হেডার ---
st.markdown("""
    <div class="main-header">
        <h1>গণপ্রজাতন্ত্রী বাংলাদেশ সরকার - সমাজসেবা অধিদপ্তর</h1>
        <p>ডিজিটাল তথ্য ড্যাশবোর্ড ও ক্যাটাগরিভিত্তিক ফাইল ব্যবস্থাপনা</p>
    </div>
""", unsafe_allow_html=True)

st.subheader("📑 আপনার কাঙ্ক্ষিত ফাইল দেখতে নিচে ক্লিক করুন:")

# ==========================================
# ড্যাশবোর্ড গ্রিড (৮টি ক্লিকযোগ্য বাটন)
# ==========================================
# ১ম সারি (৪টি বাটন)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💼\nচাকরির ডকুমেন্টস", key="btn_job"):
        st.session_state.selected_category_key = "job"

with col2:
    if st.button("📊\nআরএসএস রিপোর্ট", key="btn_rss"):
        st.session_state.selected_category_key = "rss"

with col3:
    if st.button("🤱\nমাতৃকেন্দ্র রিপোর্ট", key="btn_maternity"):
        st.session_state.selected_category_key = "maternity"

with col4:
    if st.button("♿\nপ্রতিবন্ধী রিপোর্ট", key="btn_disability_rep"):
        st.session_state.selected_category_key = "disability_rep"

# ২য় সারি (৪টি বাটন)
col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("👴\nবয়স্ক ভাতার তথ্য", key="btn_oldage"):
        st.session_state.selected_category_key = "oldage"

with col6:
    if st.button("🦽\nপ্রতিবন্ধী ভাতার তথ্য", key="btn_disability_all"):
        st.session_state.selected_category_key = "disability_all"

with col7:
    if st.button("👩\nবিধবা ভাতার তথ্য", key="btn_widow"):
        st.session_state.selected_category_key = "widow"

with col8:
    if st.button("💳\nফ্যামিলি কার্ডের তথ্য", key="btn_family"):
        st.session_state.selected_category_key = "family"

st.markdown("---")

# ==========================================
# নির্বাচিত ক্যাটাগরির বিস্তারিত তথ্য ও ফাইল ভিউ
# ==========================================
# নির্বাচিত ক্যাটাগরির নাম ও আইকন সেট করা
cat_names = {
    "job": ("💼 চাকরির ডকুমেন্টস"),
    "rss": ("📊 আরএসএস রিপোর্ট"),
    "maternity": ("🤱 মাতৃকেন্দ্র রিপোর্ট"),
    "disability_rep": ("♿ প্রতিবন্ধী রিপোর্ট"),
    "oldage": ("👴 বয়স্ক ভাতার তথ্য"),
    "disability_all": ("🦽 প্রতিবন্ধী ভাতার তথ্য"),
    "widow": ("👩 বিধবা ভাতার তথ্য"),
    "family": ("💳 ফ্যামিলি কার্ডের তথ্য")
}

current_cat_key = st.session_state.selected_category_key
current_cat_name = cat_names.get(current_cat_key)

# নির্বাচিত ক্যাটাগরি সফলতার সাথে দেখানো
st.success(f"📌 আপনি বর্তমানে নির্বাচিত করেছেন: **{current_cat_name}**")

# সময় নির্বাচন (মাস ও বছর)
m_col1, m_col2 = st.columns(2)
with m_col1:
    month = st.selectbox("📅 মাস নির্বাচন করুন", ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"])
with m_col2:
    year = st.selectbox("🗓️ বছর নির্বাচন করুন", [2026, 2025, 2024, 2023])

# ফাইল আপলোডার বক্স (এটিই আপনার ফাইল দেখার জায়গা)
uploaded_file = st.file_uploader(
    f"'{current_cat_name}' এর জন্য নথি আপলোড করুন (Excel, PDF, Word)", 
    type=["xlsx", "xls", "pdf", "docx"]
)

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    st.info(f"📂 ফাইলের নাম: **{uploaded_file.name}** | সময়কাল: **{month} {year}**")
    st.markdown("---")
    st.subheader(f"👁️ '{current_cat_name}' - লাইভ ফাইল ভিউ:")

    # ১. এক্সেল ফাইল ভিউ
    if file_type in ["xlsx", "xls"]:
        try:
            df = pd.read_excel(uploaded_file)
            st.dataframe(df, use_container_width=True)
        except Exception:
            st.error("এক্সেল ফাইলটি প্রদর্শন করতে সমস্যা হচ্ছে।")

    # ২. ওয়ার্ড ফাইল ভিউ
    elif file_type == "docx":
        try:
            doc = docx.Document(uploaded_file)
            full_text = [p.text for p in doc.paragraphs if p.text.strip() != ""]
            if full_text:
                for para in full_text:
                    st.write(f"• {para}")
            else:
                st.warning("ওয়ার্ড ফাইলের ভেতরে কোনো টেক্সট পাওয়া যায়নি।")
        except Exception:
            st.error("ওয়ার্ড ফাইলটি পড়তে সমস্যা হচ্ছে।")

    # ৩. পিডিএফ ফাইল ভিউ
    elif file_type == "pdf":
        try:
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception:
            st.error("PDF ফাইলটি প্রদর্শন করা যাচ্ছে না।")

else:
    st.warning(f"👆 '{current_cat_name}' সংক্রান্ত কোনো ফাইল দেখতে ওপরের বক্সে একটি ফাইল আপলোড করুন।")
