import pandas as pd
import streamlit as st

# অ্যাপের টাইটেল
st.title("অফিস ফাইল ভিউয়ার ও আপলোডার")
st.write("যে কোনো ফাইল আপলোড করে ডাউনলোড ছাড়াই সরাসরি ব্রাউজারে দেখুন।")

# ফাইল আপলোডার
uploaded_file = st.file_uploader(
    "ফাইল নির্বাচন করুন (Excel, PDF, Word)", type=["xlsx", "xls", "pdf", "docx"]
)

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    st.success(f"আপলোড করা ফাইল: {uploaded_file.name}")
    st.write("---")

    # ১. এক্সেল ফাইল দেখানো
    if file_type in ["xlsx", "xls"]:
        try:
            df = pd.read_excel(uploaded_file)
            st.subheader("📊 এক্সেল ফাইলের তথ্য:")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error("এক্সেল ফাইলটি পড়তে সমস্যা হচ্ছে।")

    # ২. ওয়ার্ড (Word) ফাইল দেখানো
    elif file_type == "docx":
        try:
            import docx

            doc = docx.Document(uploaded_file)
            full_text = [p.text for p in doc.paragraphs if p.text.strip() != ""]

            st.subheader("📄 ওয়ার্ড ফাইলের লেখা:")
            if full_text:
                for para in full_text:
                    st.write(para)
            else:
                st.info("ফাইলের ভেতরে কোনো টেক্সট পাওয়া যায়নি।")
        except ModuleNotFoundError:
            st.error(
                "ওয়ার্ড ফাইল দেখতে 'python-docx' প্যাকেজ ইনস্টল থাকা প্রয়োজন।"
            )
        except Exception as e:
            st.error("ওয়ার্ড ফাইলটি পড়তে সমস্যা হচ্ছে।")

    # ৩. পিডিএফ (PDF) ফাইল দেখানো
    elif file_type == "pdf":
        try:
            import base64

            base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
            st.subheader("📕 PDF ভিউয়ার:")
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error("PDF ফাইলটি প্রদর্শন করা যাচ্ছে না।")
