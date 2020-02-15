from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename
import ocr_1 as ocr
import time
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = r'C:\Users\rrite\Downloads\ARK\image_sih'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ocr', methods = ['GET', 'POST'])
def index():
	if(request.method == 'POST'):
		if(request.files):
			file=request.files['file']
			if (file.filename == ''):
				return "No file selected"
			if (file and allowed_file(file.filename)):
				filename = secure_filename(file.filename)
				print(filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				temp = ocr.get_diagonsitics(r'C:\Users\rrite\Downloads\ARK\medical_tests.txt')
				result= ocr.get_data(UPLOAD_FOLDER+"\\"+filename, temp)
				return jsonify(result)

	if(request.method == 'GET'):
		return jsonify({"about":"hello__world!"})
	return "Reached end!!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)