import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. CẤU HÌNH API ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Lỗi: Chưa tìm thấy API Key trong phần Secrets!")

# --- 2. GIAO DIỆN ---
st.set_page_config(page_title="NanoBanana Weaver v2.1", page_icon="🍌")
st.title("🍌 NanoBanana Weaver v2.1")
st.markdown("#### App tạo ảnh nhân vật trong bối cảnh mới")

col1, col2 = st.columns(2)
with col1:
    char_file = st.file_uploader("👤 Ảnh Nhân Vật", type=['jpg', 'png', 'jpeg'])
    if char_file:
        st.image(char_file, caption="Nhân vật mẫu", use_container_width=True)

with col2:
    bg_file = st.file_uploader("🏞️ Ảnh Bối Cảnh", type=['jpg', 'png', 'jpeg'])
    if bg_file:
        st.image(bg_file, caption="Bối cảnh mẫu", use_container_width=True)

prompt_user = st.text_input("📝 Hành động:", placeholder="Ví dụ: Hai nhân vật đang hôn nhau...")

# --- 3. XỬ LÝ VÀ TẠO ẢNH ---
if st.button("🚀 Vẽ Ảnh Ngay", use_container_width=True):
    if char_file and bg_file and prompt_user:
        with st.spinner("Đang xử lý dữ liệu..."):
            try:
                # Sửa tên model thành phiên bản ổn định nhất
                # Sử dụng gemini-1.5-flash hoặc gemini-pro-vision tùy khu vực
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                char_img = Image.open(char_file)
                bg_img = Image.open(bg_file)
                
                # Yêu cầu Gemini tạo mô tả ảnh cực chi tiết (Master Prompt)
                analysis_query = (
                    f"Combine these two images. Place the character from image 1 into the setting of image 2. "
                    f"Action: {prompt_user}. Make it realistic with matching lighting and shadows. "
                    f"Give me a detailed image generation prompt in English."
                )
                
                response = model.generate_content([analysis_query, char_img, bg_img])
                master_prompt = response.text
                
                st.info("💡 AI đã lập kế hoạch vẽ ảnh. Đang tiến hành tạo hình...")
                
                # Thử nghiệm tạo ảnh với Imagen
                try:
                    # Tên model chuẩn cho Imagen trên AI Studio
                    imagen = genai.GenerativeModel('imagen-3.0-generate-001')
                    img_response = imagen.generate_content(master_prompt)
                    
                    # Hiển thị ảnh kết quả
                    generated_img = img_response.generated_images[0].image
                    st.image(generated_img, caption="Kết quả từ NanoBanana", use_container_width=True)
                    
                    # Nút tải về
                    buf = io.BytesIO()
generated_img.save(buf, format="PNG")
                    st.download_button("📥 Tải ảnh về", buf.getvalue(), "result.png", "image/png")
                    
                except Exception as img_err:
                    st.warning("⚠️ Tài khoản của bạn hiện chưa được mở quyền vẽ ảnh Imagen 3 trực tiếp.")
                    st.write("Nhưng đây là mô tả chi tiết để bạn có thể dán vào các công cụ vẽ ảnh khác (như Midjourney/DALL-E):")
                    st.code(master_prompt)
                    
            except Exception as e:
                st.error(f"Lỗi hệ thống: {e}")
    else:
        st.warning("Vui lòng tải ảnh và nhập mô tả!")
