import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. Cấu hình API bí mật ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chưa tìm thấy mã API trong phần Secrets của Streamlit!")

# --- 2. Giao diện người dùng ---
st.set_page_config(page_title="NanoBanana Weaver", page_icon="🍌")
st.title("🍌 NanoBanana Weaver")
st.write("Ghép nhân vật vào bối cảnh mới bằng AI")

col1, col2 = st.columns(2)
with col1:
    char_file = st.file_uploader("👤 Chọn ảnh Nhân Vật", type=['jpg', 'png', 'jpeg'])
with col2:
    bg_file = st.file_uploader("🏞️ Chọn ảnh Bối Cảnh", type=['jpg', 'png', 'jpeg'])

prompt_user = st.text_input("📝 Nhân vật đang làm gì?", placeholder="Ví dụ: Đang khiêu vũ...")

# --- 3. Xử lý logic ---
if st.button("🚀 Thực hiện ngay", use_container_width=True):
    if char_file and bg_file and prompt_user:
        with st.spinner("NanoBanana đang dệt dữ liệu..."):
            try:
                # Sử dụng model ổn định nhất
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                char_img = Image.open(char_file)
                bg_img = Image.open(bg_file)
                
                # Tạo lệnh yêu cầu AI mô tả bức ảnh kết hợp
                query = [
                    f"Combine these images. Put the person from Image 1 into the setting of Image 2. "
                    f"Action: {prompt_user}. Describe the resulting image in vivid detail.",
                    char_img, bg_img
                ]
                
                response = model.generate_content(query)
                
                st.success("Đã hoàn thành phân tích cảnh quay!")
                st.markdown("### 🖼️ Mô tả bức ảnh được tạo ra:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
    else:
        st.warning("Vui lòng tải đủ 2 ảnh và nhập mô tả hành động!")
