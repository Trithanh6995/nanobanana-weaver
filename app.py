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
st.set_page_config(page_title="NanoBanana Weaver v2", page_icon="🎨")
st.title("🎨 NanoBanana Weaver v2")
st.markdown("#### App ghép nhân vật và tạo ảnh thực tế")

col1, col2 = st.columns(2)
with col1:
    char_file = st.file_uploader("👤 Ảnh Nhân Vật", type=['jpg', 'png', 'jpeg'])
    if char_file:
        st.image(char_file, caption="Nhân vật mẫu", use_container_width=True)

with col2:
    bg_file = st.file_uploader("🏞️ Ảnh Bối Cảnh", type=['jpg', 'png', 'jpeg'])
    if bg_file:
        st.image(bg_file, caption="Bối cảnh mẫu", use_container_width=True)

prompt_user = st.text_input("📝 Mô tả hành động:", placeholder="Ví dụ: Nhân vật đang ngồi uống trà trong bối cảnh này...")

# --- 3. XỬ LÝ VÀ TẠO ẢNH ---
if st.button("🚀 Vẽ Ảnh Ngay", use_container_width=True):
    if char_file and bg_file and prompt_user:
        with st.spinner("Đang phân tích và vẽ ảnh... Vui lòng đợi trong giây lát!"):
            try:
                # Bước A: Dùng Gemini Flash để tạo một "siêu mô tả" (Master Prompt)
                vision_model = genai.GenerativeModel('gemini-1.5-flash')
                char_img = Image.open(char_file)
                bg_img = Image.open(bg_file)
                
                analysis_prompt = (
                    f"Dựa trên 2 ảnh này, hãy tạo 1 câu lệnh tiếng Anh cực kỳ chi tiết để vẽ ảnh: "
                    f"Đặt nhân vật trong ảnh 1 vào bối cảnh ảnh 2. Hành động: {prompt_user}. "
                    f"Mô tả chi tiết ngoại hình, quần áo, ánh sáng và sự hòa hợp. "
                    f"Chỉ trả về câu lệnh tiếng Anh, không nói gì thêm."
                )
                
                master_prompt = vision_model.generate_content([analysis_prompt, char_img, bg_img]).text
                
                # Bước B: Dùng model Imagen để vẽ ảnh (Sử dụng model tạo ảnh của Google)
                # Lưu ý: Một số tài khoản cần quyền truy cập Imagen 3
                image_model = genai.GenerativeModel('imagen-3.0-generate-001')
                
                # Tạo ảnh từ Master Prompt
                response = image_model.generate_content(master_prompt)
                
                # Bước C: Hiển thị kết quả
                st.success("Tác phẩm của bạn đã hoàn thành!")
                
                # Lấy dữ liệu ảnh và hiển thị
                for generated_image in response.generated_images:
                    st.image(generated_image.image, caption="Kết quả từ NanoBanana", use_container_width=True)
                    
                    # Nút tải ảnh về
                    img_byte_arr = io.BytesIO()
                    generated_image.image.save(img_byte_arr, format='PNG')
                    st.download_button(label="📥 Tải ảnh về máy", 
                                       data=img_byte_arr.getvalue(), 
                                       file_name="nano_banana_result.png", 
                                       mime="image/png")

            except Exception as e:
                st.error(f"Có lỗi nhỏ: {e}")
                st.info("Mẹo: Nếu lỗi về 'model not found', có thể tài khoản của bạn đang dùng bản miễn phí chưa mở quyền vẽ ảnh trực tiếp. Nhưng đừng lo, mình có thể giúp bạn cách khác!")
    else:
        st.warning("Bạn hãy chọn đủ 2 ảnh và nhập mô tả nhé!")
