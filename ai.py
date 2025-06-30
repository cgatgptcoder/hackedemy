import google.generativeai as genai
import os

# --- Hàm để lưu câu hỏi vào file TXT ---
def save_questions_to_txt(questions_content, filename="quiz_questions.txt"):
    """
    Lưu nội dung câu hỏi trắc nghiệm vào một file văn bản.

    Args:
        questions_content (str): Nội dung các câu hỏi trắc nghiệm.
        filename (str): Tên file output (mặc định là 'quiz_questions.txt').
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(questions_content)
        print(f"\n✅ Đã lưu các câu hỏi vào file '{filename}' thành công!")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi lưu file '{filename}': {e}")

# --- Bắt đầu code chính của chương trình ---

# Đường dẫn đến thư mục chứa các file văn bản của bạn
text_folder_path = "txt_split_result"

# Danh sách các file bạn muốn đọc
files_to_read = ["output3.txt", "output4.txt"]

combined_txt = ""

try:
    for filename in files_to_read:
        file_path = os.path.join(text_folder_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_txt += f.read()
            combined_txt += "\n\n--- Hết nội dung từ " + filename + " ---\n\n"
        else:
            print(f"⚠️ Cảnh báo: Không tìm thấy file '{filename}' tại đường dẫn '{file_path}'. Bỏ qua file này.")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi khi đọc file: {e}")
    exit()

# Cấu hình API key của bạn
genai.configure(api_key="AIzaSyDWpBekYHSjzqtiJPR6-1e9xYKkTpUuBDo")

# Gửi yêu cầu tạo nội dung
prompt = f"""
    Hãy đóng vai một giáo viên. Dựa vào nội dung văn bản dưới đây, mỗi chương hãy tạo 20-30 câu hỏi trắc nghiệm để kiểm tra kiến thức.

    Yêu cầu:
    - Mỗi câu hỏi có 4 lựa chọn (A, B, C, D).
    - Các phương án sai phải hợp lý và có liên quan.
    - Ghi rõ đáp án đúng sau mỗi câu hỏi (ví dụ: **Đáp án:** A).

    Văn bản:
    \"\"\"
    {combined_txt}
    \"\"\"
    """
try:
    print("✅ Đã đọc văn bản thành công. Đang gửi yêu cầu đến Gemini...")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)

    generated_questions = response.text

    # In kết quả ra màn hình
    print("\n🎉 CÁC CÂU HỎI TRẮC NGHIỆM ĐÃ TẠO:\n")
    print(generated_questions)

    # --- Gọi hàm để lưu câu hỏi vào file ---
    save_questions_to_txt(generated_questions, "my_quiz_output.txt") # Bạn có thể thay đổi tên file ở đây

except Exception as e:
    print(f"❌ Đã xảy ra lỗi khi gọi Gemini API: {e}")