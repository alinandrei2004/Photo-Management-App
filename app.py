from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

UPLOAD_FOLDER = 'static/uploads'
THUMBNAIL_FOLDER = 'static/thumbnails'  # New folder for thumbnails
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

# Ensure the upload and thumbnail folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

# Mocked pictures list to hold uploaded picture details
pictures = [
    {'filename': 'default.jpg', 'name': 'Default Picture'}  # Predefined picture
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_thumbnail(source_path, target_path, size=(100, 100)):
    try:
        with Image.open(source_path) as img:
            img.thumbnail(size)
            img.save(target_path)
    except Exception as e:
        print(f"Error creating thumbnail: {e}")

@app.route("/", methods=['GET'])
def index():
    thumbnails = [{'filename': pic['filename'], 'name': pic['name']} for pic in pictures]
    return render_template("index.html", title="FotoHive", pictures=thumbnails)

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
            filename = request.form['filename'] if request.form['filename'] else file.filename
            category = request.form.get('category', 'uncategorized')

            # Save original image
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Create and save thumbnail
            thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
            create_thumbnail(file_path, thumbnail_path)

            pictures.append({'filename': filename, 'name': filename, 'category': category})
            return redirect(url_for('index'))
        
        flash('Invalid file type')
        return redirect(request.url)

    # If method is not POST, render the upload form
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
