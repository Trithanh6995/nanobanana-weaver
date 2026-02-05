import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình bảo mật (Lấy mã từ két sắt Secrets)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Bạn chưa thiết lập API Key trong phần Secrets của Streamlit!")

# 2. Giao diện ứng dụng
st.set_page_config(page_title="NanoBanana Weaver", page_icon="🍌")
st.title("🍌 NanoBanana Weaver")
st.write("Ứng dụng ghép nhân vật vào bối cảnh bằng AI")

# Chia làm 2 cột để tải ảnh
col1, col2 = st.columns(2)

with col1:
    char_file = st.file_uploader("👤 Chọn ảnh Nhân Vật", type=['jpg', 'png', 'jpeg'])
    if char_file:
        st.image(char_file, caption="Nhân vật của bạn", use_container_width=True)

with col2:
    bg_file = st.file_uploader("🏞️ Chọn ảnh Bối Cảnh", type=['jpg', 'png', 'jpeg'])
    if bg_file:
        st.image(bg_file, caption="Bối cảnh bạn muốn", use_container_width=True)

# Ô nhập mô tả hành động
prompt_text = st.text_input("📝 Nhân vật đang làm gì?", placeholder="Ví dụ: Đang ngồi đọc sách bên cửa sổ...")

# Nút bấm xử lý
if st.button("🚀 Bắt đầu tạo ảnh", use_container_width=True):
    if char_file and bg_file and prompt_text:
        with st.spinner("NanoBanana đang 'dệt' ảnh..."):
            try:
                # Gọi mô gia đình Gemini 1.5 Flash (Xử lý ảnh cực tốt)
                model = genai.GenerativeModel('gemini-1.5-flash')
                char_img = Image.open(char_file)
                bg_img = Image.open(bg_file)
                
                # Gửi yêu cầu cho AI
                response = model.generate_content([
                    f"Hãy đóng vai là NanoBanana. Dựa trên ảnh nhân vật và ảnh bối cảnh này, "
                    f"hãy mô tả chi tiết cách nhân vật thực hiện hành động: {prompt_text}. "
                    f"Hãy chú ý đến ánh sáng và sự hòa hợp giữa người và cảnh.",
                    char_img, bg_img
                ])
                
                st.success("Xong rồi! Đây là kết quả:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi: {e}")
    else:
        st.warning("Bạn cần tải đủ 2 ảnh và nhập mô tả nhé!")