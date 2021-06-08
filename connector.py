import time as tm
import socket as sk
import threading as thr

username = sk.gethostname()
ip = sk.gethostbyname(sk.gethostname())
port = 4567

class just_server:
	def __init__(self, controller):
		self.controller = controller
		self.run_server = True
		self.main_server = None
		self.online_clients = {}# id: [conn, listener_state]
	# Connections starters and stoppers
	def start_server(self, ip, port, listen=10):
		if not self.run_server:
			return False, 'run_server = False'
		sock = sk.socket()
		try:
			sock.bind((ip, port))
			sock.listen(listen)
		except Exception as e:
			return False, str(e)
		self.main_server = sock
		return True, ''
	def close_server(self):
		self.run_server = False
		self.main_server.close()
		self.main_server = None
	def start_client(self, ip, port):
		conn = sk.socket()
		try:
			conn.connect((ip, port))
		except Exception as e:
			return False, str(e)
		return conn, ''
	def close_client(self, _id):
		self.online_clients[_id][1] = False
		self.online_clients[_id][0].close()
		del self.online_clients[_id]
	###################################
	# Listeners starters
	def start_server_listener(self):
		thread = thr.Thread(target=self.server_listener)
		thread.setDaemon(True)
		thread.start()
	def start_client_listener(self, _id, buffer=1024):
		thread = thr.Thread(target=lambda: self.client_listener(_id, buffer))
		thread.setDaemon(True)
		thread.start()
	def server_listener(self):
		while self.run_server and self.main_server:
			try:
				conn, addr = self.main_server.accept()
			except Exception as e:
				if self.run_server:
					self.main_server.close()
					self.main_server = None
					self.controller.got_server_error(e)
				break
			self.controller.got_new_client(conn, addr)
		self.run_server = True
	def client_listener(self, _id, buffer):
		passed = 0
		self.online_clients[_id][1] = True
		while self.online_clients[_id][1]:
			try:
				data = self.online_clients[_id][0].recv(buffer)
			except Exception as e:
				try:
					if self.online_clients[_id][1]:
						self.controller.client_closed(_id, str(e))
				except:
					pass
				break
			if data:
				self.controller.got_client_data(_id, data.decode())
			else:
				passed += 1
			if passed > 20 and self.online_clients[_id][1]:
				self.controller.client_closed(_id, 'Connection undergone unknown error')
				break
		try:
			self.online_clients[_id][1] = False
		except:
			pass
	####################################
	def send_message(self, _id, message):
		if _id not in self.online_clients.keys():
			return False, 'Connection not established try reconnecting'
		if self.online_clients[_id][1]:
			try:
				self.online_clients[_id][0].send(message.encode())
				return True, ''
			except Exception as e:
				return False,  str(e)
		else:
			return False, 'Connection problem try reconnecting or wait for connection'