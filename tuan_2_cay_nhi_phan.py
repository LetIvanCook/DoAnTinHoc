import csv
import json
import pickle
import os


# --- 1. CODE CẤU TRÚC DỮ LIỆU (CTDL) ---

class Node:
    """Một nút trong Cây Nhị phân Tìm kiếm."""

    def __init__(self, key, data):
        # Đảm bảo key luôn là số
        self.key = float(key)
        self.data = data
        self.left = None
        self.right = None

    def to_dict(self):
        """Hàm đệ quy để chuyển Cây thành một Dictionary (để lưu JSON)."""
        node_dict = {
            'key': self.key,
            'data': self.data,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
        return node_dict


class BinarySearchTree:
    """Lớp Cây Nhị phân Tìm kiếm (BST) chính."""

    def __init__(self):
        self.root = None
        self.node_count = 0

    def insert(self, key, data):
        """Phương thức công khai để chèn một nút mới."""

        # *** HÀNG RÀO BẢO VỆ (SỬA LỖI) ***
        # Chỉ chấp nhận key là số (int hoặc float)
        if not isinstance(key, (int, float)):
            print(f"LỖI (Hàm Insert): Khóa '{key}' không phải là số. Bỏ qua.")
            return

        if self.root is None:
            self.root = Node(key, data)
        else:
            self._insert_recursive(self.root, key, data)
        self.node_count += 1

    def _insert_recursive(self, current_node, key, data):
        """Hàm đệ quy (private) để tìm đúng vị trí và chèn nút."""

        # Dòng code này giờ đã an toàn vì chúng ta đảm bảo
        # cả 'key' và 'current_node.key' đều là SỐ (float)
        if key < current_node.key:
            # Đi sang trái
            if current_node.left is None:
                current_node.left = Node(key, data)
            else:
                self._insert_recursive(current_node.left, key, data)
        else:
            # Đi sang phải
            if current_node.right is None:
                current_node.right = Node(key, data)
            else:
                self._insert_recursive(current_node.right, key, data)

    def in_order_traversal(self):
        """Duyệt cây theo thứ tự (Trái -> Gốc -> Phải)."""
        print("\n--- Duyệt Cây theo thứ tự (In-Order Traversal) ---")
        self._in_order_recursive(self.root)
        print("--- Kết thúc duyệt ---")

    def _in_order_recursive(self, current_node):
        if current_node:
            self._in_order_recursive(current_node.left)
            print(f"Key: {current_node.key}")
            self._in_order_recursive(current_node.right)

    # --- 2. CÁC HÀM LƯU FILE ---

    def save_to_pickle(self, file_path):
        """Lưu toàn bộ Cây ra file Nhị phân (Binary)."""
        print(f"\n--- Đang lưu file Nhị phân (Pickle) ---")
        try:
            with open(file_path, 'wb') as f_bin:
                pickle.dump(self.root, f_bin)
            print(f"Đã lưu Cây ra file: {file_path}")
        except Exception as e:
            print(f"LỖI khi lưu Pickle: {e}")

    def save_to_json(self, file_path):
        """Lưu toàn bộ Cây ra file Text (JSON)."""
        print(f"\n--- Đang lưu file Text (JSON) ---")
        if self.root is None:
            print("Cây rỗng, không có gì để lưu.")
            return

        try:
            tree_dict = self.root.to_dict()
            with open(file_path, 'w', encoding='utf-8') as f_json:
                json.dump(tree_dict, f_json, ensure_ascii=False, indent=4)
            print(f"Đã lưu Cây ra file: {file_path}")
        except Exception as e:
            print(f"LỖI khi lưu JSON: {e}")


# --- 3. HÀM CHÍNH ĐỂ CHẠY CHƯƠNG TRÌNH (ĐÃ SỬA LỖI) ---

def main():
    """Hàm chính điều phối: Đọc CSV -> Xây Cây -> Lưu Cây."""

    # --- A. ĐỊNH NGHĨA TÊN FILE VÀ TIÊU CHÍ SẮP XẾP ---

    # Sửa lỗi: Chỉ đường dẫn chính xác vào thư mục 'data'
    INPUT_DIR = 'data'
    INPUT_FILE = os.path.join(INPUT_DIR, 'filtered_australia_pisa_2018.csv')

    # Bạn có thể đổi KEY_COLUMN sang cột khác nếu muốn
    # ...
    KEY_COLUMN = 'W_FSTUWT_SCH_SUM'

    OUTPUT_DIR = 'output'
    OUTPUT_JSON = os.path.join(OUTPUT_DIR, 'pisa_tree.json')
    OUTPUT_PICKLE = os.path.join(OUTPUT_DIR, 'pisa_tree.bin')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    bst = BinarySearchTree()

    print(f"--- Đọc {INPUT_FILE} và xây dựng Cây BST (Khóa: {KEY_COLUMN}) ---")
    rows_processed = 0
    rows_skipped = 0

    try:
        with open(INPUT_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Lấy giá trị khóa từ hàng
                key_value_str = row[KEY_COLUMN]

                # *** PHẦN LỌC LỖI QUAN TRỌNG NHẤT ***

                # 1. Kiểm tra xem giá trị có phải là chuỗi rỗng không
                if key_value_str == "" or key_value_str is None:
                    rows_skipped += 1
                    continue  # Bỏ qua hàng này và đi đến hàng tiếp theo

                # 2. Thử chuyển đổi sang float
                try:
                    key = float(key_value_str)

                    # 3. Chỉ khi chuyển đổi thành công, mới chèn vào cây
                    bst.insert(key, row)
                    rows_processed += 1

                except (ValueError, TypeError):
                    # Xử lý các trường hợp 'abc' hoặc lỗi khác
                    rows_skipped += 1

    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file: {INPUT_FILE}")
        return
    except KeyError:
        print(f"LỖI: Không tìm thấy cột '{KEY_COLUMN}' trong file CSV.")
        return
    except Exception as e:
        print(f"LỖI không xác định khi đọc file: {e}")
        return

    print(f"\nĐã xây dựng Cây thành công.")
    print(f"Tổng số học sinh đã xử lý (nút): {rows_processed}")
    print(f"Tổng số hàng bị bỏ qua (dữ liệu trống/lỗi): {rows_skipped}")

    # --- C. LƯU CẤU TRÚC DỮ LIỆU ---
    bst.save_to_json(OUTPUT_JSON)
    bst.save_to_pickle(OUTPUT_PICKLE)

    print("\n--- HOÀN THÀNH TOÀN BỘ QUY TRÌNH ---")


# --- CHẠY HÀM MAIN KHI SCRIPT ĐƯỢC GỌI ---
if __name__ == "__main__":
    main()