import json
import hashlib
import os

# ======== CẤU HÌNH ========
EMPLOYEE_FILE = "employees/employees_finance.json"   # Thay đổi theo bộ phận
INPUT_FILE = "inputs/input.json"
REQUIRED_DEPTH = 3  # Tổng số node lá là 2^depth
INDEX_TO_PROVE = 1  # Thứ tự employee cần chứng minh
# ==========================

def hash_leaf(email, secret):
    data = (email + secret).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def hash_node(left, right):
    return hashlib.sha256((left + right).encode("utf-8")).hexdigest()

def build_merkle_tree(hashed_leaves):
    current_level = hashed_leaves
    tree = [current_level]
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i + 1 < len(current_level) else left
            next_level.append(hash_node(left, right))
        tree.append(next_level)
        current_level = next_level
    return tree, tree[-1][0]

def generate_merkle_proof(tree, leaf_index):
    proof = []
    index = leaf_index
    for level in tree[:-1]:
        sibling_index = index ^ 1  # 0 <-> 1, 2 <-> 3 ...
        if sibling_index < len(level):
            proof.append(level[sibling_index])
        else:
            proof.append(level[index])  # padding node
        index //= 2
    return proof

# ====== Load danh sách nhân sự ======
with open(EMPLOYEE_FILE, "r") as f:
    employees = json.load(f)

# ====== Tính toán tổng số leaf cần (2^depth) ======
TOTAL_LEAVES = 2 ** REQUIRED_DEPTH

# ====== Hash leaf gốc ======
hashed_leaves = [hash_leaf(emp["email"], emp["secret"]) for emp in employees]

# ====== Padding bằng leaf rỗng (hash("")) nếu thiếu ======
EMPTY_HASH = hashlib.sha256("".encode("utf-8")).hexdigest()
while len(hashed_leaves) < TOTAL_LEAVES:
    hashed_leaves.append(EMPTY_HASH)

# ====== Build Merkle Tree ======
tree, root = build_merkle_tree(hashed_leaves)

# ====== Lấy leaf cần chứng minh ======
employee = employees[INDEX_TO_PROVE]
leaf = hashed_leaves[INDEX_TO_PROVE]
proof = generate_merkle_proof(tree, INDEX_TO_PROVE)

# ====== Tính path_index (bit phải trái) ======
path_index = [(INDEX_TO_PROVE >> i) & 1 for i in range(REQUIRED_DEPTH)]

# ====== Ghi input.json ======
input_data = {
    "leaf": int(leaf, 16),
    "path_elements": [int(p, 16) for p in proof],
    "path_index": path_index,
    "root": int(root, 16)
}

os.makedirs(os.path.dirname(INPUT_FILE), exist_ok=True)
with open(INPUT_FILE, "w") as f:
    json.dump(input_data, f, indent=4)

# ====== In thông báo ======
print(f"✅ Generated Merkle Tree with root: {root}")
print(f"🔒 Proving for: {employee['email']} (index {INDEX_TO_PROVE})")
print(f"📥 input.json generated with depth = {REQUIRED_DEPTH}, total leaves = {TOTAL_LEAVES}")
