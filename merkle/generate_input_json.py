import json
import os

# Đọc proof.json và merkle_root.txt ở cấp gốc
with open("proof.json") as f:
    proof = json.load(f)

with open("merkle_root.txt") as f:
    root = f.read().strip()

# Đảm bảo thư mục inputs/ tồn tại
inputs_dir = "inputs"
if not os.path.exists(inputs_dir):
    os.makedirs(inputs_dir)

# Ghi file input.json vào thư mục inputs/
input_data = {
    "leaf": int(proof["leaf"], 16),
    "path_elements": [int(e, 16) for e in proof["path_elements"]],
    "path_index": proof["path_index"],
    "root": int(root, 16)
}

with open(os.path.join(inputs_dir, "input.json"), "w") as f:
    json.dump(input_data, f, indent=2)

print("✅ input.json đã được tạo ở inputs/")
