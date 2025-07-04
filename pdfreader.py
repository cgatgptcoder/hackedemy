import easyocr
import os
import re

# Tạo đối tượng EasyOCR
reader = easyocr.Reader(['vi'])

# --- Đường dẫn thư mục ---
input_root_folder = 'img_output'
output_folder = 'txt_output'

# Tạo thư mục output nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

print(f"Bắt đầu xử lý ảnh từ thư mục gốc: {input_root_folder}")

# Hàm sắp xếp tự nhiên tên file
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# --- Duyệt qua tất cả thư mục con ---
subfolders = sorted(
    [d for d in os.listdir(input_root_folder)
     if os.path.isdir(os.path.join(input_root_folder, d)) and d.startswith("Chapter_")],
    key=natural_sort_key
)

if not subfolders:
    print("⚠️ Không tìm thấy thư mục con nào bắt đầu bằng 'Chapter_'.")
else:
    for subfolder in subfolders:
        chapter_path = os.path.join(input_root_folder, subfolder)
        print(f"\n📂 Đang xử lý thư mục: {subfolder}")

        # Lấy danh sách ảnh trong thư mục
        image_files = [f for f in os.listdir(chapter_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

        # Sắp xếp ảnh tự nhiên
        image_files.sort(key=natural_sort_key)

        if not image_files:
            print(f"⚠️ Thư mục '{subfolder}' không có ảnh nào.")
            continue

        # Tên file output riêng cho chương này
        chapter_output_txt = os.path.join(output_folder, f"{subfolder}.txt")

        # Mở file ở chế độ 'w' để tạo mới
        with open(chapter_output_txt, 'w', encoding='utf-8') as f_out:
            f_out.write(f"====================\nChương: {subfolder}\n====================\n")

        for filename in image_files:
            image_path = os.path.join(chapter_path, filename)

            print(f"   🔹 Đang xử lý ảnh: {filename}")
            try:
                results = reader.readtext(image_path)

                lines = [text for (_, text, _) in results]
                extracted_text = "\n".join(lines)

                # Chuẩn bị nội dung để ghi
                text_to_write = f"\n--- Văn bản từ ảnh: {filename} ---\n{extracted_text}\n"

                # Ghi nối tiếp vào file chương
                with open(chapter_output_txt, 'a', encoding='utf-8') as f_out:
                    f_out.write(text_to_write)

                print(f"      ✅ Đã trích xuất '{filename}'")

            except Exception as e:
                print(f"      ❌ Lỗi khi xử lý '{filename}': {e}")

print("\n🎉 Quá trình xử lý đã hoàn tất!")
print(f"Các file văn bản đã được lưu trong thư mục: {output_folder}")
