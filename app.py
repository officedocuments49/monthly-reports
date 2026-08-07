import base64
import docx
import pandas as pd
import streamlit as st

# পেজের লেআউট ও সুন্দর ডিজাইন সেটআপ
st.set_page_config(
    page_title="অফিস ফাইল ড্যাশবোর্ড", page_icon="📁", layout="wide"
)

# সাইডবার মেনু
st.sidebar.title("📌 নেভিগেশন")
st.sidebar.info("আপনার প্রয়োজনীয় ফাইল আপলোড করুন এবং ডাউনলোড ছাড়াই সরাসরি দেখুন।")

# মূল টাইটেল ও হেডার
st.title("📂 অফিস ফাইল ভিউয়ার ও ড্যাশবোর্ড")
st.markdown("---")

# আপলোড সেকশন (কার্ড স্টাইলে)
st.subheader("📤 নতুন ফাইল আপলোড করুন")
uploaded_file = st.file_uploader("আপনার ফাইলটি নির্বাচন করুন", type=["xlsx", "xls", "pdf", "docx"])

st.markdown("---")

# ফাইল আপলোড করা হলে তা প্রদর্শন করার সেকশন
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    # ফাইল ইনফরমেশন কার্ড
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success(f"✅ নির্বাচিত ফাইল: **{uploaded_file.name}**")
    with col2:
        st.info(f"📁 ফাইল টাইপ: **{file_type.upper()}**")

    st.subheader("👁️ ফাইলের ভেতরের তথ্য (Live View)")

    # ১. এক্সেল ফাইল ভিউ
    if file_type in ["xlsx", "xls"]:
        try:
            df = pd.read_excel(uploaded_file)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error("এক্সেল ফাইলটি পড়তে সমস্যা হচ্ছে। ফাইলটির ফরম্যাট সঠিক আছে কিনা দেখুন।")

    # ২. ওয়ার্ড ফাইল ভিউ
    elif file_type == "docx":
        try:
            doc = docx.Document(uploaded_file)
            full_text = [p.text for p in doc.paragraphs if p.text.strip() != ""]
            
            if full_text:
                for para in full_text:
                    st.write(f"• {para}")
            else:
                st.warning("ফাইলের ভেতরে কোনো টেক্সট পাওয়া যায়নি।")
        except Exception as e:
            st.error("ওয়ার্ড ফাইলটি পড়তে সমস্যা হচ্ছে।")

    # ৩. পিডিএফ ফাইল ভিউ
    elif file_type == "pdf":
        try:
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error("PDF ফাইলটি প্রদর্শন করা যাচ্ছে না।")

else:
    # কোনো ফাইল আপলোড না থাকলে সুন্দর ওয়েলকাম মেসেজ
    st.info("👆 ফাইলের বিস্তারিত দেখতে ও রিড করতে ওপরের বক্সে একটি Excel, Word বা PDF ফাইল আপলোড করুন।")
