# ZK-RBAC-PROOF 🌟

A Zero-Knowledge Proof (ZKP) system for Role-Based Access Control (RBAC) using Merkle Trees and Circom. This project allows users to prove their membership in a specific role (e.g., developer, manager) without revealing their identity, leveraging cryptographic techniques for privacy and security.

View detail: [https://github.com/trannhatbuilder/zk_rbac_proof](https://github.com/trannhatbuilder/zk_rbac_proof)

## 📚 Overview

The `zk_rbac_proof` project implements a ZKP-based RBAC system where:
- **Users** are represented by leaves in a Merkle Tree, computed as Poseidon hashes of their email and secret.
- **Roles** are stored in JSON files, with each role forming a separate Merkle Tree.
- **Proofs** are generated using a Circom circuit to verify that a user's leaf belongs to the Merkle Tree of a role, without disclosing the leaf or path details.
- **Privacy** is ensured through ZKP, making it ideal for secure access control in decentralized systems.

### How It Works 🛠️
1. **Merkle Tree Construction**:
   - Each role has a Merkle Tree with up to 8 leaves (depth 3), padded with zeros if fewer users exist.
   - Leaves are computed as `Poseidon(email, secret)`.
   - The tree is built using Poseidon hash, with the root publicly verifiable.
2. **ZKP Circuit**:
   - A Circom circuit verifies that a private leaf belongs to the Merkle Tree with a given public root.
   - The circuit uses private inputs (`leaf`, `path_elements`, `path_index`) and a public input (`root`).
3. **Proof Generation**:
   - A Python script generates `input.json` containing the leaf, path elements, path indices, and root.
   - The circuit is compiled to generate a witness, which can be used to create a ZKP.

## 📋 Prerequisites

To run this project, you need:
- **Node.js** (v16 or higher) 📦
- **Python** (v3.8 or higher) 🐍
- **Circom** (v2.1.4 or higher) 🔧
- **circomlibjs** for Poseidon hash implementation 📚
- **Git** for cloning the repository 🗂️

## 🛠️ Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/trannhatbuilder/zk_rbac_proof.git
   cd zk_rbac_proof
   ```

2. **Install Node.js Dependencies**:
   ```bash
   npm install circomlibjs
   ```

3. **Install Circom**:
   Follow the [Circom installation guide](https://docs.circom.io/getting-started/installation/) to install Circom globally:
   ```bash
   cargo install circom
   ```

## 🚀 Usage

### Step 1: Generate Input JSON
Run the Python script to create `input.json` for a user:
```bash
python merkle/generate_input_json.py --email Rubies@it.company.com --secret alpha
```
This generates `inputs/input.json` with:
- `leaf`: Poseidon hash of email and secret (as string).
- `path_elements`: Sibling nodes in the Merkle path (as strings).
- `path_index`: Binary path from leaf to root.
- `root`: Merkle Tree root (as string).

Example `input.json`:
```json
{
    "leaf": "5903683782933244403104578331549097114770768190915928837963158142113708397305",
    "path_elements": [
        "1120536590839353993575965644345642079324237516011443018778214032167403535744",
        "14744269619966411208579211824598458697587494354926760081771325075741142829156",
        "7423237065226347324353380772367382631490014989348495481811164164159255474657"
    ],
    "path_index": [1, 0, 0],
    "root": "13555663317189784585752133547932541150983958257564988288602046835017124861460"
}
```

### Step 2: Compile the Circom Circuit
Compile the circuit to generate R1CS and WASM files:
```bash
circom circuits/merkle_proof.circom --r1cs --wasm --sym -o outputs/
```
This creates:
- `main.r1cs`: Rank-1 Constraint System.
- `main.wasm`: WebAssembly file for witness generation.
- `main.sym`: Symbol file for debugging.

### Step 3: Generate Witness
Generate a witness for the proof using `input.json`:
```bash
node node outputs/merkle_proof_js/generate_witness.js outputs/merkle_proof_js/merkle_proof.wasm inputs/input.json outputs/witness.wtns
```

### Step 4: Generate and Verify Proof
*(To be implemented)*: Use a ZKP prover (e.g., snarkjs) to generate and verify the proof. Example steps:
```bash
snarkjs groth16 setup main.r1cs powersOfTau28_hez_final_16.ptau main_zkp.zkey( I recommend build ptau by hand)
snarkjs groth16 prove outputs/merkle_proof_final.zkey outputs/witness.wtns outputs/proof.json outputs/public.json
snarkjs groth16 verify outputs/verification_key.json outputs/public.json outputs/proof.json
```

## 🧠 Theory Behind the Project

### Zero-Knowledge Proofs
ZKP allows a prover to convince a verifier of a statement's truth without revealing underlying data. In this project, ZKP ensures that a user belongs to a role without disclosing their email or secret.

### Merkle Trees
A Merkle Tree is a binary tree where:
- **Leaves** store hashes of data (here, `Poseidon(email, secret)`).
- **Non-leaf nodes** are hashes of their children.
- **Root** is a single hash representing the entire dataset.
The circuit verifies that a leaf belongs to the tree by recomputing the root using a Merkle path.

### Poseidon Hash
Poseidon is a ZKP-friendly hash function used for efficient arithmetic circuit computations. It is implemented via `circomlib` in the circuit and `circomlibjs` in the scripts.

### RBAC with ZKP
- Each role (e.g., developer) has a Merkle Tree of authorized users.
- Users prove membership in a role's tree using ZKP, ensuring privacy.
- The public root is verified on-chain or by an access control system.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## 📬 Contact

For questions or feedback, reach out to [trannhatbuilder](https://github.com/trannhatbuilder).

---
Built with ❤️ by [trannhatbuilder](https://github.com/trannhatbuilder)
