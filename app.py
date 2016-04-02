import os
import sys
import json
from os import listdir
from os.path import isfile, join

from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from flask import render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['mp4', 'png'])
VIDEO_EXTENSIONS = set(['.mp4'])
IMAGE_EXTENSIONS = set(['.png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def to_json(obj):
	return jsonify(obj)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def mkdir(email):
	os.system('mkdir -p '+app.config['UPLOAD_FOLDER']+'/'+email)
def get_email_dir(email):
	return app.config['UPLOAD_FOLDER']+'/'+email
def get_files_in_root(root):
	fnames = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			fnames.append(name)
	return fnames

def is_photo(fname):
	return '.png' in fname
def is_video(fname):
	return '.mp4' in fname
def get_users():
	root = app.config['UPLOAD_FOLDER']
	return [name for name in os.listdir(root)]

def get_compressed_videos(email):
	root = 'uploads/'+email+'/compressed'
	return ['/'+root+'/'+f for f in get_files_in_root(root) if is_video(f)]
def get_compressed_photos(email):
	root = 'uploads/'+email+'/compressed'
	return ['/'+root+'/'+f for f in get_files_in_root(root) if is_photo(f)]

@app.route('/pick')
def pick():
	email = request.args.get('email')
	compressed_videos = get_compressed_videos(email)
	compressed_photos = get_compressed_photos(email)
	return render_template('pick.html', 
		email = email,
		users = get_users(),
		compressed_photos = json.dumps(compressed_photos),
		compressed_videos = json.dumps(compressed_videos))	

@app.route('/users')
def show_users():
	return to_json({'users':get_users()})
	
@app.route('/uploads')
def show_uploads():
	email = request.args.get('email')
	mkdir(email)
	photos = get_compressed_photos(email)
	videos = get_compressed_videos(email)
	return to_json({'compressed_photos': photos, 'compressed_videos': videos})

@app.route('/uploads/<email>/<subdir>/<filename>')
def uploaded_file(email, subdir, filename):
	return send_from_directory(app.config['UPLOAD_FOLDER']+'/'+email+'/'+subdir, filename)

@app.route('/upload_file', methods = ['POST'])
def upload_file():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		email = request.args.get('email')
		subdir = request.args.get('type')
		if subdir != 'full':
			subdir = 'compressed'
		dir = email +'/'+ subdir
		mkdir(dir)
		filename = dir+'/'+filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return 'ok'


if __name__ == "__main__":
	app.run(debug=True, port = 3000)