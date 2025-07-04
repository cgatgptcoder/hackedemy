import subprocess

def run_script(script_name):
    print(f"🚀 Đang chạy {script_name}...")
    result = subprocess.run(['python', script_name])
    if result.returncode != 0:
        print(f"❌ Script {script_name} đã gặp lỗi!")
    else:
        print(f"✅ Hoàn thành {script_name}.\n")

if __name__ == "__main__":
    # Chạy pdf.py
    run_script("pdf.py")
    # Chạy pdf2img.py 
    run_script("pdf2img.py")
    # Chạy pdfreader.py
    run_script("pdfreader.py")

    # Chạy ai.py
    run_script("ai.py")
