from flask import Flask, request, render_template_string, send_file
from pydub import AudioSegment
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Mashup Generator</title>
<style>
body {
    font-family: Arial;
    background: #f5dede;
}
.container {
    width: 420px;
    margin: 60px auto;
    background: white;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.2);
}
input, button {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    border-radius: 8px;
}
button {
    background: #2d6cdf;
    color: white;
    border: none;
}
</style>
</head>
<body>
<div class="container">
<h2>Mashup Generator</h2>
<form method="post" enctype="multipart/form-data">
Upload Audio Files:
<input type="file" name="files" multiple required><br><br>

Duration (seconds):
<input name="duration" required><br><br>

<button type="submit">Generate Mashup</button>
</form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        files = request.files.getlist("files")
        duration = int(request.form["duration"])

        os.makedirs("uploads", exist_ok=True)

        final = AudioSegment.empty()

        for f in files:
            path = os.path.join("uploads", f.filename)
            f.save(path)

            audio = AudioSegment.from_file(path)
            final += audio[:duration * 1000]

        final.export("output.mp3", format="mp3")

        return send_file("output.mp3", as_attachment=True)

    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

