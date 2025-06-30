import fitz  # PyMuPDF
import re

# === Đường dẫn file PDF gốc ===
input_pdf = "input/input.pdf"

# === Mẫu tiêu đề chương (bạn có thể chỉnh thêm) ===
chapter_pattern = re.compile(
    r"(Chương\s+\d+|CHAPTER\s+\d+|CHƯƠNG\s+[IVX]+)",
    re.IGNORECASE
)

# === Mở file PDF ===
doc = fitz.open(input_pdf)
num_pages = doc.page_count

chapter_starts = []

# === Tìm trang bắt đầu của các chương ===
for i in range(num_pages):
    text = doc[i].get_text()
    if chapter_pattern.search(text):
        chapter_starts.append(i)

if not chapter_starts:
    print("Không tìm thấy tiêu đề chương. Hãy kiểm tra regex.")
    exit()

print(f"Tìm thấy {len(chapter_starts)} chương.")

# === Tách mỗi chương thành 1 file PDF ===
for idx, start_page in enumerate(chapter_starts):
    if idx + 1 < len(chapter_starts):
        end_page = chapter_starts[idx + 1]
    else:
        end_page = num_pages

    new_doc = fitz.open()
    # Copy các trang từ start_page đến end_page -1
    new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)

    # Xuất file tên rõ ràng
    filename = f"output/Chapter_{idx + 1}.pdf"
    new_doc.save(filename)
    print(f"Đã xuất: {filename}")
