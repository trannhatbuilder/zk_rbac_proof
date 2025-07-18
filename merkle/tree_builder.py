import hashlib
import json
import random

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def hash_leaf(name: str, secret: str) -> str:
    return sha256(name + secret)

def hash_node(left: str, right: str) -> str:
    return sha256(left + right)

def build_merkle_tree(leaves: list[str]) -> tuple[list[list[str]], str]:
    tree = [leaves]
    current_level = leaves

    while len(current_level) > 1:
        next_level = []

        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1]
            parent = hash_node(left, right)
            next_level.append(parent)

        tree.insert(0, next_level)
        current_level = next_level

    root = tree[0][0]
    return tree, root

if __name__ == "__main__":
    # 4 nhân viên thuộc IT
    users = [
        {"name": "Alice", "secret": "s3cr3t1"},
        {"name": "Bob",   "secret": "s3cr3t2"},
        {"name": "Carol", "secret": "s3cr3t3"},
        {"name": "Dave",  "secret": "s3cr3t4"}
    ]

    # Băm từng leaf
    hashed_leaves = [hash_leaf(u["name"], u["secret"]) for u in users]

    # Xây cây
    tree, root = build_merkle_tree(hashed_leaves)

    # Random chọn 1 người làm người cần chứng minh
    selected_index = random.randint(0, 3)
    selected_user = users[selected_index]
    selected_leaf = hashed_leaves[selected_index]

    # Lưu thông tin gốc (Merkle Root)
    with open("merkle_root.txt", "w") as f:
        f.write(root)

    # Lưu thông tin để dùng trong bước tiếp theo
    with open("leaves.json", "w") as f:
        json.dump(hashed_leaves, f, indent=2)

    with open("selected_user.json", "w") as f:
        json.dump({
            "index": selected_index,
            "name": selected_user["name"],
            "secret": selected_user["secret"],
            "leaf": selected_leaf
        }, f, indent=2)

    print("✅ Merkle Tree built. Root:", root)
    print("🔍 Selected Prover:", selected_user["name"])
