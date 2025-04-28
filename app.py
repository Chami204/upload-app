from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

@app.route('/', methods=['GET', 'POST'])
def index():
    folders = []
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for dir in dirs:
            folders.append(os.path.relpath(os.path.join(root, dir), UPLOAD_FOLDER))

    if request.method == 'POST':
        parent_folder = request.form.get('parent_folder')
        sub_folder = request.form.get('sub_folder')
        nested_folder = request.form.get('nested_folder')
        files = request.files.getlist('file')  # 🔥 Get multiple files

        path = UPLOAD_FOLDER
        if parent_folder:
            path = os.path.join(path, secure_filename(parent_folder))
        if sub_folder:
            path = os.path.join(path, secure_filename(sub_folder))
        if nested_folder:
            path = os.path.join(path, secure_filename(nested_folder))

        create_folder(path)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(path, filename))

        return redirect(url_for('index'))

    return render_template('index.html', folders=folders)

if __name__ == '__main__':
    create_folder(UPLOAD_FOLDER)
    app.run(debug=True)
