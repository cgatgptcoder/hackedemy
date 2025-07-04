import easyocr
import os

# Tạo đối tượng EasyOCR
reader = easyocr.Reader(['vi'])

# --- Đường dẫn thư mục ---
input_folder = 'input'
output_folder = 'output'

# File TXT duy nhất để chứa toàn bộ nội dung
output_txt_filename = 'tong_hop_noi_dung.txt'
output_txt_path = os.path.join(output_folder, output_txt_filename)

# Tạo thư mục output nếu chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Đã tạo thư mục: {output_folder}")

print(f"Bắt đầu xử lý ảnh từ thư mục: {input_folder}")

# Biến lưu toàn bộ văn bản từ tất cả ảnh
all_text = []

# --- Duyệt qua từng file trong thư mục input ---
for filename in sorted(os.listdir(input_folder)):
    # Chỉ xử lý các file ảnh (kiểm tra phần mở rộng)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
        image_path = os.path.join(input_folder, filename)

        print(f"\nĐang xử lý ảnh: {filename}...")
        try:
            # Thực hiện OCR trên ảnh
            results = reader.readtext(image_path)

            # Trích xuất văn bản từ kết quả OCR
            lines = [text for (_, text, _) in results]
            extracted_text = "\n".join(lines)

            # Thêm tiêu đề file và nội dung để dễ phân biệt
            all_text.append(f"========== Nội dung từ file: {filename} ==========\n")
            all_text.append(extracted_text)
            all_text.append("\n")  # Thêm khoảng cách sau mỗi ảnh

            print(f"✅ Đã xử lý '{filename}'")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý ảnh '{filename}': {e}")
    else:
        print(f"Bỏ qua file '{filename}' (không phải định dạng ảnh được hỗ trợ).")

# Ghi tất cả văn bản ra một file duy nhất
with open(output_txt_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(all_text))

print(f"\n🎉 Đã hoàn tất! Toàn bộ nội dung đã lưu vào file: {output_txt_filename}")
