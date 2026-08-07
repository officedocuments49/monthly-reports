import base64
import json
import os
import streamlit as st

# --- পেজ সেটআপ ---
st.set_page_config(
    page_title="সমাজসেবা অধিদপ্তর - ডিজিটাল আর্কাইভ",
    page_icon="🟢",
    layout="wide"
)

# ডাটাবেস ফাইল
DB_FILE = "office_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

office_db = load_data()

if 'selected_cat_key' not in st.session_state:
    st.session_state.selected_cat_key = "job"

# --- সিএসএস স্টাইল ---
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
    .stButton>button {
        width: 100%;
        height: 75px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid #006a4e;
    }
    .stButton>button:hover {
        background-color: #006a4e !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# হেডার
st.markdown("""
    <div class="main-header">
        <h1 style="color:white; margin:0;">গণপ্রজাতন্ত্রী বাংলাদেশ সরকার - সমাজসেবা অধিদপ্তর</h1>
        <p style="margin:5px 0 0 0;">ডিজিটাল তথ্য ড্যাশবোর্ড ও ক্লাউড সেভ ফাইল ব্যবস্থাপনা</p>
    </div>
""", unsafe_allow_html=True)

st.subheader("📑 আপনার কাঙ্ক্ষিত ফাইল ও তথ্য দেখতে ক্যাটাগরিতে ক্লিক করুন:")

# ==========================================
# ৮টি বোতাম (ক্লিকযোগ্য ক্যাটাগরি)
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("💼\nচাকরির ডকুমেন্টস", key="b1"): st.session_state.selected_cat_key = "job"
with col2:
    if st.button("📊\nআরএসএস রিপোর্ট", key="b2"): st.session_state.selected_cat_key = "rss"
with col3:
    if st.button("🤱\nমাতৃকেন্দ্র রিপোর্ট", key="b3"): st.session_state.selected_cat_key = "maternity"
with col4:
    if st.button("♿\nপ্রতিবন্ধী রিপোর্ট", key="b4"): st.session_state.selected_cat_key = "disability_rep"

col5, col6, col7, col8 = st.columns(4)
with col5:
    if st.button("👴\nবয়স্ক ভাতার তথ্য", key="b5"): st.session_state.selected_cat_key = "oldage"
with col6:
    if st.button("🦽\nপ্রতিবন্ধী ভাতার তথ্য", key="b6"): st.session_state.selected_cat_key = "disability_all"
with col7:
    if st.button("👩\nবিধবা ভাতার তথ্য", key="b7"): st.session_state.selected_cat_key = "widow"
with col8:
    if st.button("💳\nফ্যামিলি কার্ডের তথ্য", key="b8"): st.session_state.selected_cat_key = "family"

st.markdown("---")

# ==========================================
# কন্টেন্ট ও আপলোড সেকশন
# ==========================================
cat_names = {
    "job": "💼 চাকরির ডকুমেন্টস",
    "rss": "📊 আরএসএস রিপোর্ট",
    "maternity": "🤱 মাতৃকেন্দ্র রিপোর্ট",
    "disability_rep": "♿ প্রতিবন্ধী রিপোর্ট",
    "oldage": "👴 বয়স্ক ভাতার তথ্য",
    "disability_all": "🦽 প্রতিবন্ধী ভাতার তথ্য",
    "widow": "👩 বিধবা ভাতার তথ্য",
    "family": "💳 ফ্যামিলি কার্ডের তথ্য"
}

current_key = st.session_state.selected_cat_key
current_name = cat_names[current_key]

st.success(f"📌 আপনি বর্তমানে নির্বাচিত করেছেন: **{current_name}**")

tab1, tab2 = st.tabs(["📂 এই ক্যাটাগরির সংরক্ষিত ফাইলসমূহ", "📤 নতুন ফাইল সেভ / আপলোড করুন"])

# --- ট্যাব ১: সেভ করা ফাইল দেখার ও মোছার জায়গা ---
with tab1:
    st.subheader(f"📑 '{current_name}' - এর সংরক্ষিত নথিপত্র")
    
    if current_key in office_db and len(office_db[current_key]) > 0:
        saved_items = office_db[current_key]
        
        # রিভার্স লুপ যাতে নতুন আপলোড করা ফাইল সবার ওপরে থাকে
        for idx, item in enumerate(saved_items):
            with st.expander(f"📄 {item['title']} ({item['month']} {item['year']})"):
                st.write(f"**নথির নাম:** {item.get('file_name', 'অজ্ঞাত ফাইল')}")
                st.write(f"**বিবরণ/নোট:** {item.get('note', 'কোনো নোট নেই')}")
                
                # ফাইল ডাউনলোড ও ডিলিট বাটন
                if "file_data" in item:
                    try:
                        file_bytes = base64.b64encode(item["file_data"].encode('utf-8')) if isinstance(item["file_data"], str) else base64.b64decode(item["file_data"])
                    except Exception:
                        file_bytes = b""

                    f_type = item.get("file_type", "pdf")
                    
                    btn_col1, btn_col2 = st.columns([2, 1])
                    
                    with btn_col1:
                        st.download_button(
                            label=f"📥 {item['title']} ডাউনলোড করুন",
                            data=base64.b64decode(item["file_data"]),
                            file_name=item.get('file_name', 'document.pdf'),
                            mime=f"application/{f_type}",
                            key=f"dl_{current_key}_{idx}"
                        )
                    
                    with btn_col2:
                        # ফাইল ডিলিট বাটন
                        if st.button(f"🗑️ ফাইলটি মুছে ফেলুন", key=f"del_{current_key}_{idx}"):
                            # লিস্ট থেকে ফাইল রিমুভ করা
                            office_db[current_key].pop(idx)
                            save_data(office_db)
                            st.success("✅ নথিটি সফলভাবে মুছে ফেলা হয়েছে!")
                            st.rerun()
                        
                st.markdown("---")
                
                # PDF প্রিভিউ
                if item.get("file_type") == "pdf":
                    pdf_display = f'<embed src="data:application/pdf;base64,{item["file_data"]}" width="100%" height="450" type="application/pdf">'
                    st.markdown(pdf_display, unsafe_allow_html=True)

    else:
        st.warning("এই ক্যাটাগরিতে এখনো কোনো ফাইল বা তথ্য জমা রাখা হয়নি। 'নতুন ফাইল সেভ / আপলোড করুন' ট্যাবে গিয়ে ফাইল যোগ করুন।")

# --- ট্যাব ২: ফাইল আপলোড ও ডাটাবেসে সেভ ---
with tab2:
    st.subheader(f"📤 '{current_name}' ক্যাটাগরিতে নতুন নথি জমা দিন")
    
    doc_title = st.text_input("নথির শিরোনাম/নাম লিখুন (যেমন: ২০২৬ সালের বার্ষিক অডিট বিবরণী)")
    c1, c2 = st.columns(2)
    with c1:
        month = st.selectbox("মাস", ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"])
    with c2:
        year = st.selectbox("বছর", [2026, 2025, 2024])
        
    doc_note = st.text_area("অতিরিক্ত কোনো বিবরণ বা সারসংক্ষেপ (ঐচ্ছিক)")
    uploaded_file = st.file_uploader("ফাইলটি নির্বাচন করুন (PDF, Word বা Excel)", type=["pdf", "xlsx", "xls", "docx"])
    
    if st.button("💾 ফাইল ও তথ্য স্থায়ীভাবে সেভ করুন"):
        if doc_title and uploaded_file is not None:
            file_bytes = uploaded_file.read()
            b64_file = base64.b64encode(file_bytes).decode('utf-8')
            f_type = uploaded_file.name.split(".")[-1].lower()
            
            new_entry = {
                "title": doc_title,
                "month": month,
                "year": year,
                "note": doc_note,
                "file_name": uploaded_file.name,
                "file_type": f_type,
                "file_data": b64_file
            }
            
            if current_key not in office_db:
                office_db[current_key] = []
                
            office_db[current_key].append(new_entry)
            save_data(office_db)
            
            st.success(f"✅ '{doc_title}' সফলভাবে সেভ করা হয়েছে!")
            st.rerun()
        else:
            st.error("অনুগ্রহ করে নথির শিরোনাম লিখুন এবং একটি ফাইল নির্বাচন করুন।")
