import json
import os
import argparse
import sys
import re
import subprocess
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# ======== CONFIGURATION ========
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEE_FOLDER = os.path.join(CURRENT_DIR, "../employees")
INPUT_FILE = os.path.join(CURRENT_DIR, "../inputs/input.json")  # Ensure correct path when called from Flask
REQUIRED_DEPTH = 3
TOTAL_LEAVES = 2 ** REQUIRED_DEPTH

# ======== HELPER: Convert string to integer ========
def str_to_bigint(s):
    return int.from_bytes(s.encode(), 'big')

# ======== POSEIDON HASH ========
def poseidon_hash(inputs):
    """Call Node.js script to perform Poseidon hash."""
    if len(inputs) != 2:
        raise ValueError("Poseidon hash requires exactly 2 inputs.")

    js_path = os.path.join(CURRENT_DIR, "poseidon_hash.js")

    result = subprocess.run(
        ["node", js_path, str(inputs[0]), str(inputs[1])],
        capture_output=True,
        text=True,
        check=True
    )
    return int(result.stdout.strip())

def poseidon_hash_leaf(email, secret):
    return poseidon_hash([str_to_bigint(email), str_to_bigint(secret)])

def poseidon_hash_node(left, right):
    return poseidon_hash([left, right])

# ======== EXTRACT ROLE FROM EMAIL ========
def extract_role_from_email(email):
    match = re.search(r'@(\w+)\.company\.com$', email)
    if match:
        return match.group(1)
    else:
        print("[ERROR] Email must follow the format @<role>.company.com")
        sys.exit(1)

# ======== BUILD MERKLE TREE ========
def build_merkle_tree(hashed_leaves):
    current_level = hashed_leaves
    tree = [current_level]
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            next_level.append(poseidon_hash_node(left, right))
        tree.append(next_level)
        current_level = next_level
    return tree, tree[-1][0]

# ======== GENERATE MERKLE PROOF ========
def generate_merkle_proof(tree, leaf_index):
    proof = []
    index = leaf_index
    for level in tree[:-1]:
        sibling_index = index ^ 1
        if sibling_index < len(level):
            proof.append(level[sibling_index])
        else:
            proof.append(level[index])  # If no sibling, use itself
        index //= 2
    return proof

# ======== MAIN ========
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True, help="User email")
    parser.add_argument("--secret", required=True, help="User secret/password")
    args = parser.parse_args()

    role = extract_role_from_email(args.email)
    employee_file = os.path.join(EMPLOYEE_FOLDER, f"employees_{role}.json")

    if not os.path.exists(employee_file):
        print(f"[ERROR] File not found: {employee_file}")
        sys.exit(1)

    with open(employee_file, "r") as f:
        employees = json.load(f)

    # Find user index
    index = None
    for i, emp in enumerate(employees):
        if emp["email"] == args.email and emp["secret"] == args.secret:
            index = i
            break

    if index is None:
        print("❌ No matching account found with provided email and password.")
        sys.exit(1)

    # Hash all leaves
    hashed_leaves = [poseidon_hash_leaf(emp["email"], emp["secret"]) for emp in employees]
    while len(hashed_leaves) < TOTAL_LEAVES:
        hashed_leaves.append(0)  # Padding with 0 (bigint)

    # Build Merkle Tree
    tree, root = build_merkle_tree(hashed_leaves)

    leaf = hashed_leaves[index]
    proof = generate_merkle_proof(tree, index)
    path_index = [(index >> i) & 1 for i in range(REQUIRED_DEPTH)]

    # Write input.json
    input_data = {
        "leaf": leaf,
        "path_elements": proof,
        "path_index": path_index,
        "root": root
    }

    os.makedirs(os.path.dirname(INPUT_FILE), exist_ok=True)
    with open(INPUT_FILE, "w") as f:
        json.dump(input_data, f, indent=4)

    # Announcements
    # print(f"✅ input.json has been successfully created.")
    # print(f"🔍 User: {args.email} (index = {index}) in role `{role}`")
    # print(f"🌳 Merkle Root: {root}")

if __name__ == "__main__":
    main()


