from flask import Flask, request, render_template_string
import subprocess
import os
import sys

# Đảm bảo terminal hiển thị đúng UTF-8
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Load HTML template
html_path = os.path.join(os.path.dirname(__file__), "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_template = f.read()

@app.route("/", methods=["GET", "POST"])
def zk_process():
    if request.method == "GET":
        return render_template_string(html_template)

    email = request.form.get("email")
    secret = request.form.get("secret")
    result_message = ""

    if not email or '@' not in email:
        return render_template_string(html_template + '<p class="error">❌ Invalid email format.</p>')

    try:
        # Step 1: Run generate_input_json.py
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../merkle/generate_input_json.py"))
        script_dir = os.path.dirname(script_path)

        try:
            result = subprocess.run(
                ["python", script_path, "--email", email, "--secret", secret],
                cwd=script_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                check=True
            )
            print("✅ generate_input_json.py success")
            print("STDOUT:", result.stdout)
            
        except subprocess.CalledProcessError as e:
            print("❌ Error calling generate_input_json.py")
            print("Return code:", e.returncode)
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            return render_template_string(html_template + f"<p class='error'>❌ Error in generate_input_json.py:<br><pre>{e.stderr}</pre></p>")

        # Step 2: Generate witness
        wasm_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/merkle_proof_js/merkle_proof.wasm"))
        input_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../inputs/input.json"))
        witness_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/witness.wtns"))

        subprocess.run([
            "snarkjs.cmd", "wtns", "calculate",
            "--wasm", wasm_path,
            "--input", input_path,
            "--witness", witness_path
        ], check=True, text=True, encoding="utf-8", errors="ignore")

        # Step 3: Generate proof
        zkey_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/merkle_proof_final.zkey"))
        proof_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/proof.json"))
        public_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/public.json"))

        subprocess.run([
            "snarkjs.cmd", "groth16", "prove",
            zkey_path,
            witness_path,
            proof_path,
            public_path
        ], check=True, text=True, encoding="utf-8", errors="ignore")

        result_message = "<p class='message'>✅ Proof generated successfully!</p>"

    except subprocess.CalledProcessError as e:
        result_message = f"<p class='error'>❌ Error during ZK process:<br><pre>{e.stderr or str(e)}</pre></p>"

    return render_template_string(html_template + result_message)

if __name__ == "__main__":
    app.run(debug=True)
