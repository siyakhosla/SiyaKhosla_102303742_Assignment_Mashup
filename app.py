from flask import Flask, request, render_template_string
import os, zipfile, smtplib
from email.message import EmailMessage
from pydub import AudioSegment

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
Upload Audio Files: <input type="file" name="files" multiple><br><br>
Duration (seconds): <input name="duration"><br><br>
Email ID: <input name="email"><br><br>
<input type="submit" value="Generate">
</form>
</div>
</body>
</html>
"""



def send_email(receiver):
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    with zipfile.ZipFile("mashup.zip","w") as z:
        z.write("output.mp3")

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Your mashup is attached.")

    with open("mashup.zip","rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename="mashup.zip")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(sender,password)
        smtp.send_message(msg)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        files = request.files.getlist("files")
        duration = int(request.form["duration"])
        email = request.form["email"]

        os.makedirs("uploads", exist_ok=True)

        final = AudioSegment.empty()

        for f in files:
            path = os.path.join("uploads", f.filename)
            f.save(path)

            audio = AudioSegment.from_file(path)
            final += audio[:duration * 1000]

        final.export("output.mp3", format="mp3")

        send_email(email)   # your existing email function

        return "Mashup created & emailed successfully!"

    return render_template_string(HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
