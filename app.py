from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mocked pictures list to hold uploaded picture details
pictures = [
    {'filename': 'default.jpg', 'name': 'Default Picture'}  # Predefined picture
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", title="FotoHive", pictures=pictures)

@app.route("/aboutme")
def about_me():
    return render_template("about.html", title="About Me")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['picture']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = request.form['filename']
            if not filename:
                filename = file.filename
            category = request.form.get('category', 'uncategorized')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pictures.append({'filename': filename, 'name': filename, 'category': category})
            return redirect(url_for('index'))
    return render_template("upload.html", title="Upload Picture")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':  # Simple check for example purposes
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template("login.html", title="Login")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/delete_picture/<filename>", methods=['POST'])
def delete_picture(filename):
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    # Find the picture in the list by filename and remove it
    for picture in pictures:
        if picture['filename'] == filename:
            pictures.remove(picture)
            # Delete the file from the filesystem
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'status': 'success', 'message': 'Picture deleted'}), 200
    
    return jsonify({'status': 'error', 'message': 'Picture not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
