# 🛡️ A Zero-Knowledge Role-Based Authentication System

🔐 A privacy-preserving authentication system that allows users to prove they belong to a specific role or department (e.g. IT, HR, Sales) **without revealing their identity or secret**. This enhances access control security while maintaining user confidentiality and data minimization.

---

## 👥 Team Information  
**Group:** [xyz]

**Members**  
- 👤 Name: {Full Name}  
  - 💬 Discord: {username}  
  - 🐙 GitHub: {username}  
  - 🛠️ Role: {Role}

---

## 📄 Technical Report

### 1️⃣ Real‑World Problem & Motivation  
In traditional systems, RBAC often requires users to provide credentials or personal data, which can be exposed or intercepted. Our system enables **privacy-friendly authentication** using **zero-knowledge proofs (ZKP)**.

### 2️⃣ Limitations of Existing Solutions  
⚠️ Issues with current approaches:  
- Password-based methods leak secrets  
- Centralized identity = privacy risks  
- Role checks can be forged or replayed

### 3️⃣ Proposed Approach  
✅ Use ZKP to prove role membership **without revealing identity**.  
✅ Merkle trees + circuits + proof generation + frontend redirect.  
✅ Access is only granted after successful zk‑proof verification.

### 4️⃣ Technical Components  
- 🧩 **Merkle Tree (Python):** Hash leaf of email+secret and generate proof  
- ⚙️ **Circom + snarkjs:** Generate WASM + zkey + proof using Groth16  
- 🌐 **Flask Backend:** Accepts form data, runs proof generation pipeline  
- 🖥️ **Frontend (HTML/CSS/JS):** Collects info, shows progress, redirects  

---

## 🎯 Project Outcomes and Reflections

### ✅ Benefits
- 🔒 Secure access without secret leakage  
- 👁️‍🗨️ Privacy‑compliant design  
- 🪪 No identity exposure

### 💡 Key Learnings  
- Understanding ZKP flow (witness → proof → verify)  
- Circuit design with Circom requires clear logic  
- Backend ↔ Frontend synchronization for real-time status

### ⚠️ Challenges  
- Subprocess error handling in Python  
- Path bugs in generating proof inputs  
- Managing Flask sessions for department‑specific redirects

### 🔭 ZKP Reflections  
We explored real-world **use cases** of ZKP:  
- 🧾 Authentication without revealing data  
- 🏛️ Role-based permissions  
- 🔐 Compliance in private systems  
ZKPs provide **completeness, soundness, zero-knowledge** – ideal for confidential access control.

---

## 🔗 References

- 📚 [Zero-Knowledge Proof – Wikipedia](https://en.wikipedia.org/wiki/Zero-knowledge_proof?utm_source=chatgpt.com)  
- 🔐 [ZK Authentication Explained – Paubox](https://www.paubox.com/blog/how-zero-knowledge-authentication-works?utm_source=chatgpt.com)  
- 🧠 [ZKP Use Cases – QuickNode](https://www.quicknode.com/builders-guide/top-10-zero-knowledge-proof-applications?utm_source=chatgpt.com)  
- 🛡️ [ZKP in 5G & Identity – Wilson Center](https://5g.wilsoncenter.org/article/dont-trust-when-you-can-verify-primer-zero-knowledge-proofs?utm_source=chatgpt.com)  
- 🧱 [Blockchain ZKP in IoT – MDPI](https://www.mdpi.com/1424-8220/23/7/3443?utm_source=chatgpt.com)  
- 👥 [RBAC Overview – Wikipedia](https://en.wikipedia.org/wiki/Role-based_access_control?utm_source=chatgpt.com)

---

📌 *This project was developed as part of a research exploration into privacy-first authentication models using Zero‑Knowledge technology.*

## Presentaion Slide
Please provide a link to a presentation slide of your project. Alternatively, you may upload your slide deck (max 25 slides) as a .pdf file directly into your project folder.

## Video Demo 

Please provide a link to a video demo of your project. The demo should be no longer than 5 minutes.

