from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

html_path = os.path.join(os.path.dirname(__file__), "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_template = f.read()

@app.route("/", methods=["GET", "POST"])
def verify():
    result_html = ""
    if request.method == "POST":
        try:
            proof_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/proof.json"))
            public_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/public.json"))
            vkey_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../outputs/verification_key.json"))

            # Run snarkjs verify
            subprocess.check_call([
                "snarkjs.cmd", "groth16", "verify",
                vkey_path, public_path, proof_path
            ])
            result_html = "<p class='success'>✅ Proof is valid!</p>"

        except subprocess.CalledProcessError:
            result_html = "<p class='error'>❌ Invalid proof.</p>"

    return render_template_string(html_template, result=result_html)

if __name__ == "__main__":
    app.run(debug=True)
