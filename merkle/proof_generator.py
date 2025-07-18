import json
from tree_builder import hash_node

def generate_merkle_proof(tree: list[list[str]], index: int):
    depth = len(tree) - 1
    path_elements = []
    path_index = []

    current_index = index

    for level in range(depth, 0, -1):
        sibling_index = current_index ^ 1  # XOR để tìm node bên cạnh (trái ↔ phải)
        sibling = tree[level][sibling_index]

        path_elements.append(sibling)
        path_index.append(current_index % 2)  # 0: trái, 1: phải

        current_index = current_index // 2  # lên tầng trên

    return path_elements, path_index

if __name__ == "__main__":
    with open("leaves.json") as f:
        leaves = json.load(f)

    with open("selected_user.json") as f:
        selected = json.load(f)
        index = selected["index"]

    # Khôi phục lại cây Merkle để sinh proof
    def rebuild_tree(leaves):
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
        return tree

    tree = rebuild_tree(leaves)
    path_elements, path_index = generate_merkle_proof(tree, index)

    # Lưu proof để dùng cho Circom
    with open("proof.json", "w") as f:
        json.dump({
            "leaf": selected["leaf"],
            "path_elements": path_elements,
            "path_index": path_index
        }, f, indent=2)

    print("✅ Merkle Proof generated for:", selected["name"])
