from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Make sure to set the UPLOAD_FOLDER and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html", title="FotoHive")

@app.route("/aboutme")
def about_me():
    return render_template("about.html", title="About Me")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'picture' not in request.files:
            return redirect(request.url)
        file = request.files['picture']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template("upload.html", title="Upload Picture")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login here
        username = request.form['username']
        password = request.form['password']
        # Add login logic here
        return redirect(url_for('index'))
    return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run(debug=True)
