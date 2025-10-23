import pandas as pd
import os

# Định nghĩa các đường dẫn file
INPUT_DIR = 'data'
OUTPUT_DIR = 'output'
INPUT_FILE = os.path.join(INPUT_DIR, 'filtered_australia_pisa_2018.csv')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'processed_pisa_data.csv')


def read_data(file_path):
    """Đọc file CSV từ đường dẫn được cung cấp."""
    print(f"--- 1. Đang đọc dữ liệu từ: {file_path} ---")
    if not os.path.exists(file_path):
        print(f"LỖI: Không tìm thấy file đầu vào tại: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
        print("Đọc dữ liệu thành công.")
        print(f"Tổng số hàng ban đầu: {len(df)}")
        return df
    except Exception as e:
        print(f"LỖI khi đọc file: {e}")
        return None


def process_data(df):
    """Xử lý dữ liệu (ví dụ: loại bỏ các hàng thiếu dữ liệu)."""
    if df is None:
        return None

    print("\n--- 2. Đang xử lý dữ liệu ---")

    # Ví dụ xử lý: Chỉ giữ lại các hàng có đủ dữ liệu ở các cột 'STUBEHA' và 'SCMCEG'
    cols_to_check = ['STUBEHA', 'SCMCEG', 'TEACHBEHA']
    df_processed = df.dropna(subset=cols_to_check)

    print(f"Đã loại bỏ {len(df) - len(df_processed)} hàng bị thiếu dữ liệu.")
    print(f"Tổng số hàng sau khi xử lý: {len(df_processed)}")
    return df_processed


def write_data(df, file_path):
    """Ghi DataFrame đã xử lý ra file CSV mới."""
    if df is None:
        return

    print(f"\n--- 3. Đang ghi dữ liệu ra: {file_path} ---")

    # Đảm bảo thư mục 'output' tồn tại
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        # index=False để không ghi cột index (số thứ tự) của pandas
        df.to_csv(file_path, index=False, encoding='utf-8')
        print("Ghi file thành công!")
        print(f"Bạn có thể tìm file kết quả tại: {file_path}")
    except Exception as e:
        print(f"LỖI khi ghi file: {e}")


def main():
    """Hàm chính điều phối toàn bộ quy trình."""
    print("Bắt đầu quy trình xử lý dữ liệu PISA...")

    # Bước 1: Đọc
    data = read_data(INPUT_FILE)

    # Bước 2: Xử lý
    processed_data = process_data(data)

    # Bước 3: Ghi
    write_data(processed_data, OUTPUT_FILE)

    print("\nQuy trình hoàn tất.")


if __name__ == "__main__":
    main()