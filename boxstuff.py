from boxsdk import OAuth2, Client

import random, string 
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def store_tokens(access_token, refresh_token):
	print 'yo storing tokens'

oauth = OAuth2(
	client_id='kggd57v55n11en7uachopnihimxi66lo',
	client_secret='c3Ug5MrxcI3fkAdo9zCKLZvZ4oMS65tl',
	store_tokens= store_tokens,
)


@app.route('/auth')
def box_auth():
	auth_url, csrf_token = oauth.get_authorization_url('http://localhost:3000/box_callback')
	return redirect(auth_url)

@app.route("/box_callback")
def box_callback():
	code = request.args.get('code')
	access_token, refresh_token = oauth.authenticate(code)
	client = Client(oauth)
	file_path = '/Users/davidbliu/desktop/wd/filtering/comp/IMG_0860_comp.png'
	file_name = id_generator()+'.png'
	folder_id = '7173575673'
	box_file = client.folder(folder_id).upload(file_path, file_name)
	print box_file
	return 'uploaded box file'

@app.route("/box_upload")
def box_upload():
	return client
