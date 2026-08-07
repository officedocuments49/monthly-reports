import base64
import docx
import pandas as pd
import streamlit as st
from datetime import datetime

# --- পেজ সেটআপ ---
st.set_page_config(page_title="অফিস ম্যানেজমেন্ট সিস্টেম", page_icon="🏢", layout="wide")

# --- সাইডবার মেনু তৈরি ---
st.sidebar.title("🏢 অফিস ড্যাশবোর্ড")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "📌 নেভিগেশন মেনু",
    ["🏠 ড্যাশবোর্ড হোম", "📤 ফাইল আপলোড ও ভিউয়ার", "🗂️ ফাইল আর্কাইভ (ক্যাটাগরি)"]
)

# বর্তমান মাস ও বছর
current_year = datetime.now().year
months = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"]
categories = ["অডিট রিপোর্ট", "ফরওয়ার্ডিং চিঠি", "মাসিক রিপোর্ট", "অফিস নোটিশ", "অন্যান্য"]

# ==========================================
# ১. ড্যাশবোর্ড হোম পেজ
# ==========================================
if menu == "🏠 ড্যাশবোর্ড হোম":
    st.title("📊 অফিস ড্যাশবোর্ড - ওভারভিউ")
    st.markdown("এখানে অফিসের সব ডকুমেন্টের একটি সারসংক্ষেপ দেখতে পাবেন।")
    st.markdown("---")
    
    # সুন্দর কিছু ডামি স্ট্যাটিস্টিকস বক্স
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="মোট অডিট রিপোর্ট", value="১২ টি", delta="এই মাসে ২ টি")
    col2.metric(label="ফরওয়ার্ডিং চিঠি", value="৪৫ টি", delta="এই মাসে ৫ টি")
    col3.metric(label="মাসিক রিপোর্ট", value="৮ টি")
    col4.metric(label="অন্যান্য ফাইল", value="২৩ টি")
    
    st.info("👈 বাম দিকের মেনু থেকে 'ফাইল আপলোড ও ভিউয়ার' অপশনে গিয়ে আপনার প্রয়োজনীয় ডকুমেন্ট আপলোড করুন এবং সরাসরি দেখুন।")

# ==========================================
# ২. ফাইল আপলোড ও ভিউয়ার পেজ
# ==========================================
elif menu == "📤 ফাইল আপলোড ও ভিউয়ার":
    st.title("📤 নতুন ডকুমেন্ট আপলোড এবং ভিউয়ার")
    st.markdown("ডাউনলোড ছাড়াই অফিসের ফাইল এখানে সরাসরি দেখতে পাবেন।")
    st.markdown("---")

    # ক্যাটাগরি ও সময় নির্বাচনের অপশন
    st.subheader("১. ফাইলের ধরন ও সময় নির্বাচন করুন")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_category = st.selectbox("📁 ফাইলের ক্যাটাগরি", categories)
    with col2:
        selected_month = st.selectbox("📅 মাস", months)
    with col3:
        selected_year = st.selectbox("🗓️ বছর", [current_year, current_year-1, current_year-2])

    st.markdown("---")
    
    # ফাইল আপলোড বক্স
    st.subheader(f"২. {selected_month}, {selected_year} এর '{selected_category}' আপলোড করুন")
    uploaded_file = st.file_uploader("Excel, Word বা PDF ফাইল নির্বাচন করুন", type=["xlsx", "xls", "pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        st.success(f"✅ ফাইল সফলভাবে লোড হয়েছে: **{uploaded_file.name}**")
        
        st.subheader("👁️ ডকুমেন্টের ভেতরের তথ্য:")
        
        # এক্সেল ভিউয়ার
        if file_type in ["xlsx", "xls"]:
            try:
                df = pd.read_excel(uploaded_file)
                st.dataframe(df, use_container_width=True)
            except Exception:
                st.error("এক্সেল ফাইলটি পড়তে সমস্যা হচ্ছে।")

        # ওয়ার্ড ভিউয়ার
        elif file_type == "docx":
            try:
                doc = docx.Document(uploaded_file)
                full_text = [p.text for p in doc.paragraphs if p.text.strip() != ""]
                if full_text:
                    for para in full_text:
                        st.write(f"• {para}")
                else:
                    st.warning("ফাইলের ভেতরে কোনো টেক্সট পাওয়া যায়নি।")
            except Exception:
                st.error("ওয়ার্ড ফাইলটি পড়তে সমস্যা হচ্ছে।")

        # পিডিএফ ভিউয়ার
        elif file_type == "pdf":
            try:
                base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception:
                st.error("PDF ফাইলটি প্রদর্শন করা যাচ্ছে না।")

# ==========================================
# ৩. ফাইল আর্কাইভ পেজ
# ==========================================
elif menu == "🗂️ ফাইল আর্কাইভ (ক্যাটাগরি)":
    st.title("🗂️ অফিস ফাইল আর্কাইভ")
    st.markdown("এখানে আপলোড করা ফাইলগুলো মাস ও ক্যাটাগরি অনুযায়ী সাজানো থাকবে।")
    st.markdown("---")
    
    # ফিল্টার অপশন
    col1, col2 = st.columns(2)
    with col1:
        search_category = st.selectbox("ক্যাটাগরি অনুযায়ী খুঁজুন", ["সব ক্যাটাগরি"] + categories)
    with col2:
        search_month = st.selectbox("মাস অনুযায়ী খুঁজুন", ["সব মাস"] + months)
        
    st.markdown("---")
    
    st.info(f"🔍 আপনি খুঁজছেন: **{search_category}** - **{search_month}** মাসের ডেটা।")
    st.write("*(যেহেতু এটি একটি প্রাথমিক সেটআপ, পরবর্তীতে ডেটাবেস যুক্ত করলে এখানে আপনার সেভ করা সব পুরোনো ফাইল লিস্ট আকারে দেখা যাবে। আপাতত আপলোডার পেজ থেকে ফাইল দেখতে পারবেন।)*")
