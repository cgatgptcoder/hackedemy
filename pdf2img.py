from pdf2image import convert_from_path
import os

# Tên file PDF
pdf_file = "input/input.pdf"
output_folder = "img_output/images"
# Tách tên file không đuôi
pdf_filename_no_ext = os.path.splitext(os.path.basename(pdf_file))[0]

# Tạo thư mục output riêng
output_folder = os.path.join("output", "images")
os.makedirs(output_folder, exist_ok=True)

# Chuyển PDF thành ảnh
images = convert_from_path(pdf_file)

# Lưu từng trang dưới dạng JPG
for i, image in enumerate(images):
    output_path = os.path.join(output_folder, f"page_{i+1}.jpg")
    image.save(output_path, "JPEG")

print(f"✅ Đã xuất PDF thành ảnh JPG trong thư mục: {output_folder}")
