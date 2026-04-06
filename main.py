from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os
import mysql.connector
import os

db=mysql.connector.connect(
	host=os.environ.get('DB_HOST'),
	user=os.environ.get('DB_USER'),
	password=os.environ.get('DB_PASS'),
	database=os.environ.get('DB_NAME'),
	port=int(os.environ.get('DB_PORT'))
)

cursor=db.cursor()

TOKEN = os.environ.get('TOKEN')
DATA_FOLDER = 'data'

if not os.path.exists(DATA_FOLDER):
	os.makedirs(DATA_FOLDER)

class Handler(BaseHTTPRequestHandler):

	def do_POST(self):
		if self.headers.get('Authorization') != TOKEN:
			self.send_response(403)
			self.end_headers()
			return

		length = int(self.headers['Content-Length'])
		body = self.rfile.read(length)
		data = json.loads(body)

		if self.path == '/save':
			with open(f"{DATA_FOLDER}/{data['UserId']}.json", 'w') as f:
				json.dump(data['Data'], f)

			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'{"status":"saved"}')

		elif self.path == '/load':
			path = f"{DATA_FOLDER}/{data['UserId']}.json"

			if os.path.exists(path):
				with open(path) as f:
					response = f.read()
			else:
				response = json.dumps({"Coins":0,"Blocks":[]})

			self.send_response(200)
			self.end_headers()
			self.wfile.write(response.encode())

		elif self.path == '/debug':
			print('received:', data)

			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'{"status":"ok"}')

		else:
			self.send_response(404)
			self.end_headers()

port = int(os.environ.get('PORT', 3000))
server = HTTPServer(('0.0.0.0', port), Handler)

print('running...')
server.serve_forever()
