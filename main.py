import pandas as pd
import os
import tkinter as tk
from tkinter import ttk

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
        print("Vui lòng tạo thư mục 'data' và để file CSV của bạn vào đó.")
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

    # .dropna() sẽ loại bỏ bất kỳ hàng nào có giá trị NaN (rỗng)
    # trong các cột được chỉ định trong 'subset'
    df_processed = df.dropna(subset=cols_to_check)

    print(f"Đã loại bỏ {len(df) - len(df_processed)} hàng bị thiếu dữ liệu.")
    print(f"Tổng số hàng sau khi xử lý: {len(df_processed)}")
    return df_processed


def write_data(df, file_path):
    """Ghi DataFrame đã xử lý ra file CSV mới."""
    if df is None or df.empty:
        print("\nKhông có dữ liệu để ghi (DataFrame rỗng).")
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


# --- HÀM MỚI ĐƯỢC THÊM VÀO ---
def show_data_in_gui(df, title="Hiển thị DataFrame"):
    """
    Hiển thị một DataFrame của pandas trong cửa sổ Tkinter
    sử dụng widget Treeview (bảng).
    Hàm này nhận đầu vào là một DataFrame, không phải đường dẫn file.
    """
    if df is None or df.empty:
        print("LỖI (GUI): Không có dữ liệu để hiển thị (DataFrame rỗng).")
        return

    print("Mở cửa sổ GUI... (Đóng cửa sổ để kết thúc script)")

    # --- 1. Tạo cửa sổ giao diện (GUI) ---
    root = tk.Tk()
    root.title(title)
    root.geometry("800x600")  # Kích thước cửa sổ ban đầu

    # Frame (khung) chứa Treeview và thanh cuộn
    frame = ttk.Frame(root)
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    # --- 2. Tạo Treeview (Bảng) ---
    tree = ttk.Treeview(frame, show='headings')

    # Lấy danh sách tên cột
    tree["columns"] = list(df.columns)

    # Cấu hình các cột
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='w')

    # --- 3. Thêm dữ liệu vào Bảng ---
    for index, row in df.iterrows():
        # Xử lý giá trị NaN (rỗng) để hiển thị ""
        values = ["" if pd.isna(val) else val for val in row]
        tree.insert("", "end", values=tuple(values))

    # --- 4. Thêm thanh cuộn (Scrollbars) ---
    yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side="right", fill="y")

    xscroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=xscroll.set)
    xscroll.pack(side="bottom", fill="x")

    # Đặt Treeview vào frame
    tree.pack(side="left", fill="both", expand=True)

    # --- 5. Chạy vòng lặp chính của GUI ---
    root.mainloop()


def main():
    """Hàm chính điều phối toàn bộ quy trình."""
    print("Bắt đầu quy trình xử lý dữ liệu PISA...")

    # Bước 1: Đọc
    data = read_data(INPUT_FILE)

    # Bước 2: Xử lý
    processed_data = process_data(data)

    # Bước 3: Ghi
    write_data(processed_data, OUTPUT_FILE)

    # --- BƯỚC 4 (MỚI): HIỂN THỊ GUI ---
    print("\n--- 4. Đang hiển thị dữ liệu đã xử lý ---")
    # Chúng ta sẽ hiển thị 'processed_data' (dữ liệu đã xử lý)
    show_data_in_gui(processed_data, title="Dữ liệu PISA đã xử lý")

    print("\nQuy trình hoàn tất. Cửa sổ GUI đã đóng.")


if __name__ == "__main__":
    main()
