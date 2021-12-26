import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
from predict import Predict

UPLOAD_FOLDER = './test_csv'
DOWNLOAD_FOLDER = './output'
ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        # flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        # flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('predict', filename=filename))
    return redirect(url_for('index'))

@app.route('/predict/<filename>')
def predict(filename):
    output = 'test_y.csv'
    predict = Predict(filename, output)
    predict.predict_x()
    return redirect(url_for('.complete', output=output))

@app.route('/complete', methods=['GET'])
def complete():
    output = request.args['output']
    return render_template('complete.html', filename=output)

@app.route('/download/<name>', methods=['POST'])
def download_file(name):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], name)

if __name__ == '__main__':
    app.run()