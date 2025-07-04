import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter

# Đường dẫn PDF gốc
input_pdf_path = "input/input.pdf"

# Từ khóa xác định tiêu đề bài
keyword = "Bài"

# Mở PDF để đọc text
doc = fitz.open(input_pdf_path)

# Danh sách trang bắt đầu mỗi bài
start_pages = []

for page_num in range(doc.page_count):
    text = doc[page_num].get_text().lower()
    if keyword.lower() in text:
        start_pages.append(page_num)
        print(f"Phát hiện '{keyword}' ở trang {page_num + 1}")

# Nếu không tìm thấy trang nào thì dừng
if not start_pages:
    print("Không tìm thấy từ khóa!")
    exit()

# Đảm bảo thêm trang cuối cùng
start_pages.append(doc.page_count)

# Mở lại bằng PyPDF2 để tách
reader = PdfReader(input_pdf_path)

# Tạo các file nhỏ
for i in range(len(start_pages) - 1):
    writer = PdfWriter()
    start = start_pages[i]
    end = start_pages[i + 1]
    for j in range(start, end):
        writer.add_page(reader.pages[j])

    output_filename = f"Bai_{i+1}.pdf"
    with open(output_filename, "wb") as out_file:
        writer.write(out_file)
    print(f"Đã tạo file: {output_filename}")
