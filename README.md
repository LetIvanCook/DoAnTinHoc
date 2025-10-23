# Báo cáo Tiến độ Tuần: Dự án Xử lý Dữ liệu PISA

Dự án này là một phần của báo cáo tiến độ hàng tuần, thực hiện quy trình ETL (Extract - Transform - Load) cơ bản với bộ dữ liệu PISA 2018 của Úc.

## Mục tiêu

Mục tiêu của tuần này là xây dựng một kịch bản (script) Python có khả năng:
1.  **Extract (Trích xuất)**: Đọc file CSV dữ liệu thô (`filtered_australia_pisa_2018.csv`).
2.  **Transform (Biến đổi)**: Thực hiện một bước làm sạch dữ liệu cơ bản.
3.  **Load (Tải)**: Ghi dữ liệu đã làm sạch ra một file CSV mới.

## Các bước đã thực hiện

Kịch bản `process_data.py` thực hiện các công việc sau:

1.  **Đọc dữ liệu**: Tải dữ liệu từ `data/filtered_australia_pisa_2018.csv` vào một DataFrame của pandas.
2.  **Xử lý dữ liệu**: Áp dụng phương thức `dropna()` để loại bỏ bất kỳ hàng nào có giá trị bị thiếu (NaN) trong các cột `STUBEHA`, `SCMCEG`, và `TEACHBEHA`.
3.  **Ghi dữ liệu**: Lưu DataFrame đã được làm sạch vào thư mục `output/` với tên `processed_pisa_data.csv`.

## Cách chạy dự án

1.  Tạo môi trường ảo và kích hoạt:
    ```bash
    python -m venv venv
    source venv/bin/activate  # (Trên macOS/Linux)
    .\venv\Scripts\activate   # (Trên Windows)
    ```
2.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
3.  Đặt file `filtered_australia_pisa_2018.csv` vào thư mục `data/`.
4.  Chạy kịch bản:
    ```bash
    python process_data.py
    ```