import base64
import docx
import pandas as pd
import streamlit as st
from datetime import datetime

# --- পেজ সেটআপ (সরকারী জাতীয় বাতায়ন থিম) ---
st.set_page_config(
    page_title="সমাজসেবা অধিদপ্তর (DSS) - ডিজিটাল পোর্টাল",
    page_icon="🟢",
    layout="wide"
)

# --- কাস্টম সিএসএস স্টাইলিং (জাতীয় বাতায়ন হেডার ডিজাইন) ---
st.markdown("""
    <style>
    .top-gov-bar {
        background-color: #006a4e;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        border-bottom: 4px solid #f42a41;
        margin-bottom: 15px;
    }
    .top-gov-title {
        font-size: 26px;
        font-weight: bold;
        margin: 0;
        color: #ffffff;
    }
    .top-gov-sub {
        font-size: 13px;
        margin: 0;
        color: #f1f1f1;
    }
    .section-header {
        background-color: #e9ecef;
        padding: 8px 12px;
        border-left: 5px solid #006a4e;
        border-radius: 3px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .info-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- শীর্ষ ব্যানার ---
st.markdown("""
    <div class="top-gov-bar">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p class="top-gov-sub">গণপ্রজাতন্ত্রী বাংলাদেশ সরকার</p>
                <h1 class="top-gov-title">সমাজসেবা অধিদপ্তর (DSS)</h1>
                <p class="top-gov-sub">সমাজকল্যাণ মন্ত্রণালয় | ডিজিটাল ফাইল ব্যবস্থাপনা ও তথ্য পোর্টাল</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- মূল ড্রপডাউন নেভিগেশন মেনুবার (ড্যাশবোর্ডের উপরে) ---
col_m1, col_m2 = st.columns([1, 2])

with col_m1:
    main_menu = st.selectbox(
        "📌 প্রধান মেনু নির্বাচন করুন:",
        [
            "🏠 হোম / এক নজরে",
            "📂 নথি ও ফাইল ভিউয়ার (আপলোড)",
            "📊 পরিস্থিতি ও সামাজিক সুরক্ষা",
            "💰 আর্থিক ও বাজেট তথ্য",
            "💼 নিয়োগ ও সেবা",
            "📞 যোগাযোগ ও স্থান"
        ]
    )

with col_m2:
    # ড্রপডাউন মেনু সিলেক্ট করার পর সাব-ক্যাটাগরি
    if main_menu == "📊 পরিস্থিতি ও সামাজিক সুরক্ষা":
        sub_menu = st.selectbox("🔹 সাব-মেনু (পরিস্থিতি):", ["বয়স্ক ভাতা পরিস্থিতি", "প্রতিবন্ধী ভাতা তথ্য", "শিশু সুরক্ষা সেবা"])
    elif main_menu == "💰 আর্থিক ও বাজেট তথ্য":
        sub_menu = st.selectbox("🔹 সাব-মেনু (আর্থিক):", ["অনুদানের আর্থিক বিবরণী", "বার্ষিক বাজেট ও অডিট", "প্রকল্প ব্যয়"])
    elif main_menu == "💼 নিয়োগ ও সেবা":
        sub_menu = st.selectbox("🔹 সাব-মেনু (নিয়োগ):", ["চলতি নিয়োগ বিজ্ঞপ্তি", "ফলাফল ও রোল নম্বর", "সেবা প্রদান প্রতিশ্রুতি (UCAS)"])
    elif main_menu == "📞 যোগাযোগ ও স্থান":
        sub_menu = st.selectbox("🔹 সাব-মেনু (যোগাযোগ):", ["অধিদপ্তর কার্যালয়", "জেলা সমাজসেবা কার্যালয়সমূহ", "জরুরি হটলাইন"])
    else:
        sub_menu = "সাধারণ তথ্য"

st.markdown("---")

# ==========================================
# ১. হোম / এক নজরে
# ==========================================
if main_menu == "🏠 হোম / এক নজরে":
    st.markdown('<div class="section-header">📢 সাধারণ নোটিশ ও হালনাগাদ বার্তা</div>', unsafe_allow_html=True)
    st.info("অফিসের সব অডিট রিপোর্ট, ফরওয়ার্ডিং চিঠি, ও সরকারি নথি ক্যাটাগরি অনুসারে সরাসরি ফাইল ভিউয়ারে দেখতে 'নথি ও ফাইল ভিউয়ার' সিলেক্ট করুন।")

    st.subheader("📊 সমাজসেবা অধিদপ্তরের কার্যক্রম এক নজরে")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("মোট উপকারভোগী", "১.২ কোটি+", "+৫ লাখ এই বছর")
    k2.metric("আর্থিক বরাদ্দ", "১০,৫০০ কোটি ৳", "২০২৫-২০২৬")
    k3.metric("জেলা কার্যালয়", "৬৪ টি", "সারাদেশে")
    k4.metric("উপজেলা অফিস", "৪৯২ টি", "সক্রিয় সেবা")

# ==========================================
# ২. নথি ও ফাইল ভিউয়ার (প্রধান আপলোড অপশন)
# ==========================================
elif main_menu == "📂 নথি ও ফাইল ভিউয়ার (আপলোড)":
    st.markdown('<div class="section-header">📂 ফাইল আপলোড ও সরাসরি ভিউয়ার (ডাউনলোড ছাড়া)</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("📁 নথির ক্যাটাগরি", ["অডিট রিপোর্ট", "ফরওয়ার্ডিং চিঠি", "মাসিক সভা", "অফিস আদেশ", "অন্যান্য"])
    with col2:
        month = st.selectbox("📅 মাস", ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"])
    with col3:
        year = st.selectbox("🗓️ বছর", [2026, 2025, 2024])

    uploaded_file = st.file_uploader("আপনার ফাইল সিলেক্ট করুন (Excel, PDF, Word)", type=["xlsx", "xls", "pdf", "docx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        st.success(f"✅ নির্বাচিত ফাইল: **{uploaded_file.name}** ({category} - {month} {year})")
        st.markdown("---")
        st.subheader("👁️ লাইভ ফাইল ভিউ (Live Content):")

        # এক্সেল ভিউ
        if file_type in ["xlsx", "xls"]:
            try:
                df = pd.read_excel(uploaded_file)
                st.dataframe(df, use_container_width=True)
            except Exception:
                st.error("এক্সেল ফাইলটি রেন্ডার করা যাচ্ছে না।")

        # ওয়ার্ড ভিউ
        elif file_type == "docx":
            try:
                doc = docx.Document(uploaded_file)
                full_text = [p.text for p in doc.paragraphs if p.text.strip() != ""]
                if full_text:
                    for para in full_text:
                        st.write(f"• {para}")
                else:
                    st.warning("ফাইলের ভেতরে কোনো লিখা পাওয়া যায়নি।")
            except Exception:
                st.error("ওয়ার্ড ফাইলটি পড়তে সমস্যা হচ্ছে।")

        # পিডিএফ ভিউ
        elif file_type == "pdf":
            try:
                base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception:
                st.error("PDF প্রদর্শন করা যাচ্ছে না।")

# ==========================================
# ৩. পরিস্থিতি ও সামাজিক সুরক্ষা
# ==========================================
elif main_menu == "📊 পরিস্থিতি ও সামাজিক সুরক্ষা":
    st.markdown(f'<div class="section-header">📊 পরিস্থিতি বিবরণী: {sub_menu}</div>', unsafe_allow_html=True)
    if sub_menu == "বয়স্ক ভাতা পরিস্থিতি":
        st.write("• **উপকারভোগীর সংখ্যা:** ৫৮ লাখ১ হাজার জন।")
        st.write("• **ভাতার হার:** মাসিক ৬০০ টাকা হারে সরাসরি জিটুপি (G2P) পদ্ধতিতে প্রদান।")
    elif sub_menu == "প্রতিবন্ধী ভাতা তথ্য":
        st.write("• **উপকারভোগীর সংখ্যা:** ২৯ লাখ জন।")
        st.write("• **ভাতার হার:** মাসিক ৮৫০ টাকা।")
    else:
        st.write("• চাইল্ড হেল্পলাইন ১০৯৮ এবং সরকারি শিশু পরিবারের হালনাগাদ তথ্য।")

# ==========================================
# ৪. আর্থিক ও বাজেট তথ্য
# ==========================================
elif main_menu == "💰 আর্থিক ও বাজেট তথ্য":
    st.markdown(f'<div class="section-header">💰 আর্থিক হিসাব ও বিবরণী: {sub_menu}</div>', unsafe_allow_html=True)
    st.write("• অর্থ বছরের বাজেট বরাদ্দ ও ছাড়কৃত অর্থের হিসাব।")
    st.write("• বার্ষিক অভ্যন্তরীণ ও বহিঃঅডিট রিপোর্ট সংক্রান্ত সারসংক্ষেপ।")

# ==========================================
# ৫. নিয়োগ ও সেবা
# ==========================================
elif main_menu == "💼 নিয়োগ ও সেবা":
    st.markdown(f'<div class="section-header">💼 সমাজসেবা অধিদপ্তর নিয়োগ সংক্রান্ত: {sub_menu}</div>', unsafe_allow_html=True)
    st.write("• সমাজসেবা অধিদপ্তরের বিভিন্ন ক্যাডারে নিয়োগ বিজ্ঞপ্তি ও আবেদনের লিংক।")
    st.write("• লিখিত ও মৌখিক পরীক্ষার সময়সূচী ও আসন বিন্যাস।")

# ==========================================
# ৬. যোগাযোগ ও স্থান
# ==========================================
elif main_menu == "📞 যোগাযোগ ও স্থান":
    st.markdown(f'<div class="section-header">📞 যোগাযোগ ও দপ্তর অবস্থান: {sub_menu}</div>', unsafe_allow_html=True)
    st.write("**সমাজসেবা ভবন**")
    st.write("ই-৮/বি-১, আগারগাঁও, শেরেবাংলা নগর, ঢাকা-১২০৭।")
    st.write("☎️ ফোন: +৮৮-০২-৫৫০০৭৩০৩ | 📧 ইমেইল: info@dss.gov.bd")
