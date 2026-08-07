import base64
import docx
import pandas as pd
import streamlit as st
from datetime import datetime

# --- পেজ সেটআপ (সরকারী জাতীয় বাতায়ন থিম) ---
st.set_page_config(
    page_title="সমাজসেবা অধিদপ্তর - ডিজিটাল নথি ও রিপোর্ট ড্যাশবোর্ড",
    page_icon="🟢",
    layout="wide"
)

# --- কাস্টম সিএসএস স্টাইলিং ---
st.markdown("""
    <style>
    .main-header {
        background-color: #006a4e;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        text-align: center;
        border-bottom: 4px solid #f42a41;
        margin-bottom: 15px;
    }
    .notice-board {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px 15px;
        border-radius: 3px;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .card-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- টপ হেডার ---
st.markdown("""
    <div class="main-header">
        <h3 style="margin:0; color:#fff;">গণপ্রজাতন্ত্রী বাংলাদেশ সরকার</h3>
        <h1 style="margin:5px 0; color:#fff; font-size:28px;">সমাজসেবা অধিদপ্তর (DSS)</h1>
        <p style="margin:0; font-size:14px;">ডিজিটাল তথ্য ফাইল ব্যবস্থাপনা ও রিপোর্ট ড্যাশবোর্ড</p>
    </div>
""", unsafe_allow_html=True)

# --- সাইডবার মেনু ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/8/84/Government_Seal_of_Bangladesh.svg", width=90)
st.sidebar.title("📌 প্রধান মেনু")
st.sidebar.markdown("---")

selected_menu = st.sidebar.radio(
    "মেনু নির্বাচন করুন:",
    [
        "🏠 হোম / এক নজরে",
        "📂 ফাইল ভিউয়ার ও আপলোডার",
        "📄 অডিট ও ফরওয়ার্ডিং নথি",
        "📢 নোটিশ ও অফিস আদেশ",
        "⚙️ হেল্পডেস্ক ও যোগাযোগ"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **জরুরি কল:** ৩৩৩ (সরকারি তথ্য ও সেবা) | ১০৯৮ (শিশু সহায়তা)")

# ==========================================
# ১. হোম / এক নজরে
# ==========================================
if selected_menu == "🏠 হোম / এক নজরে":
    st.markdown("""
        <div class="notice-board">
            <b>📢 সর্বশেষ সংবাদ / নোটিশ:</b> সমাজসেবা অধিদপ্তরের সব ধরণের অফিসিয়াল ফাইল, অডিট রিপোর্ট ও ফরওয়ার্ডিং লেটার সরাসরি আপলোড ও ভিউ সিস্টেম চালু করা হয়েছে।
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 অফিসিয়াল কার্যক্রম ও ই-সেবা সংক্ষেপ")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="card-box"><h4>অডিট রিপোর্ট</h4><h2 style="color:#006a4e;">১২ টি</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card-box"><h4>ফরওয়ার্ডিং চিঠি</h4><h2 style="color:#006a4e;">৪৫ টি</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card-box"><h4>মাসিক অগ্রগতি</h4><h2 style="color:#006a4e;">৮ টি</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="card-box"><h4>অন্যান্য নথি</h4><h2 style="color:#006a4e;">২৩ টি</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 প্রধান সেবাসমূহ (ই-সেবা বাতায়ন)")
    
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        st.success("👴 **সামাজিক নিরাপত্তা কর্মসূচী**\n* বয়স্ক ভাতা\n* বিধবা ও স্বামী নিগৃহীতা ভাতা")
    with s_col2:
        st.info("♿ **প্রতিবন্ধিতা বিষয়াবলী**\n* প্রতিবন্ধী ভাতা ও শিক্ষা উপবৃত্তি\n* প্রতিবন্ধিতা সনাক্তকরণ জরিপ")
    with s_col3:
        st.warning("🧒 **শিশু সুরক্ষা সেবা**\n* সরকারি শিশু পরিবার\n* চাইল্ড হেল্পলাইন ১০৯৮")

# ==========================================
# ২. ফাইল ভিউয়ার ও আপলোডার (প্রধান কাজের জায়গা)
# ==========================================
elif selected_menu == "📂 ফাইল ভিউয়ার ও আপলোডার":
    st.subheader("📂 অফিস নথি আপলোড ও সরাসরি ভিউয়ার")
    st.caption("Excel, Word, অথবা PDF ফাইল আপলোড করুন। ফাইল ডাউনলোড না করেই সরাসরি ব্রাউজারে দেখা যাবে।")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox(
            "📁 নথির ধরন/ক্যাটাগরি", 
            ["অডিট রিপোর্ট", "ফরওয়ার্ডিং চিঠি", "মাসিক সমন্বয় সভা", "অফিস আদেশ / নোটিশ", "প্রকল্প ও বাজেট", "অন্যান্য"]
        )
    with col2:
        month = st.selectbox("📅 মাস", ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"])
    with col3:
        year = st.selectbox("🗓️ বছর", [2026, 2025, 2024])

    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        f"'{category}' ক্যাটাগরির জন্য ফাইলটি নির্বাচন করুন (Excel, PDF, Word)", 
        type=["xlsx", "xls", "pdf", "docx"]
    )

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        
        st.success(f"✅ সফলভাবে ফাইলের তথ্য পড়া হয়েছে: **{uploaded_file.name}** ({category} - {month} {year})")
        st.markdown("---")
        st.subheader("👁️ নথির ভেতরের তথ্য (Live View)")

        if file_type in ["xlsx", "xls"]:
            try:
                df = pd.read_excel(uploaded_file)
                st.dataframe(df, use_container_width=True)
            except Exception:
                st.error("এক্সেল ফাইলটি রেন্ডার করতে সমস্যা হচ্ছে।")

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

        elif file_type == "pdf":
            try:
                base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception:
                st.error("PDF ফাইলটি প্রদর্শন করা যাচ্ছে না।")

# ==========================================
# ৩. অডিট ও ফরওয়ার্ডিং নথি (আর্কাইভ)
# ==========================================
elif selected_menu == "📄 অডিট ও ফরওয়ার্ডিং নথি":
    st.subheader("📄 সংরক্ষিত অডিট ও ফরওয়ার্ডিং ফাইল আর্কাইভ")
    st.markdown("এখানে পূর্বে সংরক্ষিত সব ধরণের অফিসিয়ালী প্রসেস করা নথিপত্র ফিল্টার করে দেখার সুবিধা রয়েছে।")
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.selectbox("ক্যাটাগরি ফিল্টার", ["সকল ক্যাটাগরি", "অডিট রিপোর্ট", "ফরওয়ার্ডিং চিঠি", "মাসিক সভা"])
    with f_col2:
        st.text_input("🔍 ফাইল নাম দিয়ে খুঁজুন")
        
    st.info("📌 বর্তমানে নতুন ফাইলগুলো 'ফাইল ভিউয়ার ও আপলোডার' মেনু থেকে লাইভ প্রিভিউ করা যাবে।")

# ==========================================
# ৪. নোটিশ ও অফিস আদেশ
# ==========================================
elif selected_menu == "📢 নোটিশ ও অফিস আদেশ":
    st.subheader("📢 হালনাগাদ নোটিশ ও অফিস আদেশ")
    
    st.write("• **০৩-০৮-২০২৬:** মাসিক সমন্বয় সভা সংক্রান্ত বিজ্ঞপ্তি প্রকাশ।")
    st.write("• **২৭-০৭-২০২৬:** ফ্যামিলি কার্ড স্বেচ্ছাসেবক নিয়োজিতকরণ সংশোধন সংক্রান্ত নোটিশ।")
    st.write("• **১৫-ও৬-২০২৬:** অডিট আপত্তি নিষ্পত্তি বিষয়ক জরুরি নির্দেশনা।")

# ==========================================
# ৫. হেল্পডেস্ক ও যোগাযোগ
# ==========================================
elif selected_menu == "⚙️ হেল্পডেস্ক ও যোগাযোগ":
    st.subheader("📞 অফিস যোগাযোগ ও হটলাইন")
    st.write("**সমাজসেবা অধিদপ্তর**")
    st.write("সমাজসেবা ভবন, ই-৮/বি-১, আগারগাঁও, শেরেবাংলা নগর, ঢাকা-১২০৭।")
    st.write("📧 ইমেইল: info@dss.gov.bd")
    st.write("🌐 ওয়েবসাইট: https://dss.gov.bd")
