FROM debian:stable-slim

# Cài Poppler utils
RUN apt-get update && apt-get install -y poppler-utils && rm -rf /var/lib/apt/lists/*

# Thư mục làm việc mặc định
WORKDIR /data

# Mặc định chạy bash (hoặc bạn có thể thay CMD)
CMD ["/bin/bash"]

