import os
txt_path="output/output.txt"
def split_txt_by_words(txt_path, words_per_part=500):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    words = text.split()
    total_parts = (len(words) + words_per_part - 1) // words_per_part

    # Tạo thư mục chứa kết quả
    output_folder = "txt_split_result"
    os.makedirs(output_folder, exist_ok=True)

    for i in range(total_parts):
        part_words = words[i * words_per_part : (i + 1) * words_per_part]
        part_text = ' '.join(part_words)
        output_path = os.path.join(output_folder, f"part_{i+1}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(part_text)
        print(f"✅ Đã lưu: {output_path}")

# Gọi hàm với file txt cần tách
split_txt_by_words("output.txt", words_per_part=500)
