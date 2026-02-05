import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình API
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Chưa thấy API Key trong Secrets!")
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")

st.set_page_config(page_title="NanoBanana Weaver", page_icon="🍌")
st.title("🍌 NanoBanana Weaver")

# 2. Giao diện tải ảnh
col1, col2 = st.columns(2)
with col1:
    char_file = st.file_uploader("👤 Chọn ảnh Nhân Vật", type=['jpg', 'png', 'jpeg'])
with col2:
    bg_file = st.file_uploader("🏞️ Chọn ảnh Bối Cảnh", type=['jpg', 'png', 'jpeg'])

prompt_user = st.text_input("📝 Nhân vật đang làm gì?", placeholder="Ví dụ: Đang cầm cây quốc xới đất...")

# 3. Nút xử lý
if st.button("🚀 Thực hiện ngay", use_container_width=True):
    if char_file and bg_file and prompt_user:
        with st.spinner("NanoBanana đang dệt dữ liệu..."):
            try:
                # Dùng model cơ bản nhất để tránh lỗi 404
                model = genai.GenerativeModel('gemini-pro-vision')
                
                char_img = Image.open(char_file)
                bg_img = Image.open(bg_file)
                
                # Gửi yêu cầu
                response = model.generate_content([
                    f"Combine these images. Place the person from Image 1 into the setting of Image 2. Action: {prompt_user}. Describe the combined scene in detail.",
                    char_img, bg_img
                ])
                
                st.success("Đã hoàn thành!")
                st.markdown("### 🖼️ Kết quả phân tích từ AI:")
                st.write(response.text)
                
            except Exception as e:
                # Nếu vẫn lỗi 404, thử sang model dự phòng cuối cùng
                try:
                    model_alt = genai.GenerativeModel('gemini-1.5-flash')
                    response = model_alt.generate_content([
                        f"Combine these images. Person from Image 1 in setting of Image 2. Action: {prompt_user}.",
                        char_img, bg_img
                    ])
                    st.write(response.text)
                except:
                    st.error(f"Lỗi hệ thống: {e}. Vui lòng kiểm tra lại API Key.")
    else:
        st.warning("Vui lòng tải đủ 2 ảnh và nhập mô tả.")
