import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from sightengine.client import SightengineClient
app = Flask(__name__)
app.secret_key = 'can\'t keep a secret'

client = SightengineClient('user_key', 'secret_key')  #credentials

os.chdir(r'maindirpath')  #change to maindirectory

UPLOAD_FOLDER = os.path.abspath('static/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mkv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method=='POST':
		# check if the post request has the image part
		if 'image' not in request.files:
			flash('No file part.')
			return redirect(request.url)
		f = request.files['image']
		if f and allowed_file(f.filename):
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			probability = client.check('nudity','wad','properties','celebrities','offensive','faces','scam','face-attributes','text').set_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			return render_template('analyse.html', filepath='uploads/{}'.format(filename), uploaded=True, probability=probability, lf = len(probability.get('faces', [])))
			#return str(output['text'])
	else:
		return redirect(url_for('homepage'))


if __name__ == '__main__':
	app.run(debug = True)
