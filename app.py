from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename
import ocr_1 as ocr
import time
import os
import io
from medical_test import medical_tests

app = Flask(__name__)

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
				image=file.read()
				print(type(image))
				temp=medical_tests
				temp=temp.lower()
				result= ocr.get_data(image, temp)
				return jsonify(result)

	if(request.method == 'GET'):
		return jsonify({"about":"hello__world!"})
	return "Reached end!!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)