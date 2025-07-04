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
text_folder_path = "txt_output"

# Cấu hình API key của bạn
# LƯU Ý: Không nên cứng nhắc API key trong code. Nên dùng biến môi trường để bảo mật hơn.
genai.configure(api_key="AIzaSyDWpBekYHSjzqtiJPR6-1e9xYKkTpUuBDo")

# Kiểm tra xem thư mục đầu vào có tồn tại không
if not os.path.exists(text_folder_path):
    print(f"❌ Lỗi: Thư mục '{text_folder_path}' không tồn tại. Vui lòng kiểm tra đường dẫn.")
    exit()

# Lấy danh sách tất cả các file .txt trong thư mục và sắp xếp theo tên
# Việc sắp xếp giúp đảm bảo thứ tự xử lý nhất quán (ví dụ: output1.txt, output2.txt, ...)
all_txt_files = sorted([f for f in os.listdir(text_folder_path) if f.endswith('.txt')])

if not all_txt_files:
    print(f"⚠️ Cảnh báo: Không tìm thấy file .txt nào trong thư mục '{text_folder_path}'.")
    exit()

print(f"Tìm thấy {len(all_txt_files)} file .txt để xử lý trong '{text_folder_path}'.")

batch_number = 0

for txt_file in all_txt_files:
    batch_number += 1
    current_batch_files = [txt_file]  # Đóng vào list để logic sau không đổi

    
    combined_txt_for_batch = "" # Chuỗi để lưu nội dung kết hợp của lô hiện tại
    processed_filenames = [] # Danh sách tên file trong lô hiện tại

    print(f"\n--- Bắt đầu xử lý lô số {batch_number} ---")
    for filename in current_batch_files:
        file_path = os.path.join(text_folder_path, filename)
        processed_filenames.append(filename)
        print(f"Đang đọc file: {filename}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_txt_for_batch += f.read()
            # Thêm dấu phân cách rõ ràng giữa nội dung các file
            combined_txt_for_batch += f"\n\n--- Hết nội dung từ {filename} ---\n\n" 
        except Exception as e:
            print(f"❌ Đã xảy ra lỗi khi đọc file '{filename}': {e}")
            # Bạn có thể quyết định bỏ qua file này hoặc thoát chương trình nếu lỗi nghiêm trọng

    # Kiểm tra xem có nội dung để xử lý trong lô này không
    if not combined_txt_for_batch.strip():
        print(f"⚠️ Lô số {batch_number} không có nội dung để xử lý. Bỏ qua.")
        continue

    # Gửi yêu cầu tạo nội dung cho lô hiện tại đến Gemini API
    prompt = f"""
        Hãy đóng vai một giáo viên. Dựa vào nội dung văn bản dưới đây, mỗi chương hãy tạo 30-60 câu hỏi trắc nghiệm để kiểm tra kiến thức.

        Yêu cầu:
        - Mỗi câu hỏi có 4 lựa chọn (A, B, C, D).
        - Các phương án sai phải hợp lý và có liên quan.
        - Ghi rõ đáp án đúng sau mỗi câu hỏi (ví dụ: **Đáp án:** A).
        Hãy làm tối đa số câu hỏi có thể làm được 
        Văn bản:
        \"\"\"
        {combined_txt_for_batch}
        \"\"\"
        """
    try:
        print(f"✅ Đã đọc văn bản thành công cho lô {batch_number} (từ các file: {', '.join(processed_filenames)}). Đang gửi yêu cầu đến Gemini...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)

        generated_questions = response.text

        # In kết quả ra màn hình cho lô hiện tại
        print(f"\n🎉 CÁC CÂU HỎI TRẮC NGHIỆM ĐÃ TẠO CHO LÔ {batch_number}:\n")
        print(generated_questions)

        # --- Gọi hàm để lưu câu hỏi vào file ---
        # Đặt tên file output có số lô để dễ quản lý, ví dụ: my_quiz_output_batch_1.txt, my_quiz_output_batch_2.txt
        output_filename = f"result/my_quiz_output_batch_{batch_number}.txt"
        save_questions_to_txt(generated_questions, output_filename) 

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi gọi Gemini API cho lô {batch_number}: {e}")

print("\n--- Tất cả các lô đã được xử lý xong! ---")
