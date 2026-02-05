import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- Cấu hình API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chưa cấu hình API Key trong Secrets!")

st.set_page_config(page_title="NanoBanana Weaver v2.2", page_icon="🍌")
st.title("🍌 NanoBanana Weaver v2.2")

col1, col2 = st.columns(2)
with col1:
    char_file = st.file_uploader("👤 Nhân Vật", type=['jpg', 'png', 'jpeg'])
with col2:
    bg_file = st.file_uploader("🏞️ Bối Cảnh", type=['jpg', 'png', 'jpeg'])

prompt_user = st.text_input("📝 Hành động:", placeholder="Ví dụ: Đang ngồi uống cà phê...")

if st.button("🚀 Thực hiện ngay", use_container_width=True):
    if char_file and bg_file and prompt_user:
        with st.spinner("NanoBanana đang dệt dữ liệu..."):
            try:
                # Sử dụng model có độ tương thích cao nhất hiện nay
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                char_img = Image.open(char_file)
                bg_img = Image.open(bg_file)
                
                # Lệnh yêu cầu AI xử lý
                query = [
                    f"Combine these images: Put the person from Image 1 into the location of Image 2. "
                    f"Action: {prompt_user}. Describe the final merged scene in vivid detail as if it was a real photo.",
                    char_img, bg_img
                ]
                
                response = model.generate_content(query)
                
                st.success("Đã dệt xong kịch bản hình ảnh!")
                st.markdown("### 🖼️ Kết quả phân tích:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.warning("Vui lòng cung cấp đủ 2 ảnh và hành động!")
            except Exception as e:
                st.error(f"Lỗi hệ thống: {e}")
    else:
        st.warning("Vui lòng tải ảnh và nhập mô tả!")

