import time as tm

import gui
import data
import connector

class just_text():
	def __init__(self):
		self.gui = gui.just_ui(self)
		self.db = data.just_db()
		self.connect = connector.just_server(self)
		self.update_from_db()
	# Update and get function
	def update_from_db(self):
		server_id = self.db.was_server()
		if server_id:
			server_info = self.db.get_connection(server_id)
			self.gui.username.set(server_info[1])
			self.gui.ip.set(server_info[2])
			self.gui.port.set(server_info[3])
		else:
			self.gui.username.set(connector.sk.gethostname())
			self.gui.ip.set(connector.sk.gethostbyname(connector.sk.gethostname()))
			self.gui.port.set('4567')
		self.update_connections()
	def update_connections(self):
		self.gui.use_ui['connected'].delete(0, self.gui.use_ui['connected'].size())
		for connection in self.db.get_connection():
			if 'server' in connection:
				continue
			self.gui.add_connected(connection)
	def get_host_name(self):
		host_name = self.gui.username.get()
		if host_name != '':
			return host_name
		else:
			return connector.sk.gethostname()
	##############################
	# gui Functions
	def start_server(self, details):
		username, ip, port = details
		state, error = self.connect.start_server(ip, port)
		if not state:
			gui.messagebox.showerror('Could not start Server',
				'Server could not start due to:\n'+error)
			return
		self.connect.start_server_listener()
		_id = self.db.was_server()
		_data = data.connection(
			self.db.sum_connections()+1, username, ip, port, 'server', tm.time())
		if not _id:
			self.db.add_connection(_data)
		else:
			_data.id = _id
			self.db.update_connection(_data)
		self.gui.server_info.set(username+' '+ip+':'+str(port))
		self.gui.server_button.set('Stop server')
	def close_server(self):
		self.connect.close_server()
		self.gui.server_info.set('Server Offline')
		self.gui.server_button.set('Start server')
	def connect_to_server_(self):
		if len(self.gui.use_ui['connected'].curselection()) > 0:
			self.selected_connection()
		else:
			gui.dialog(self.gui, 'Connect to server')
	def connect_to_server(self, details):
		username, ip, port = details
		conn, error = self.connect.start_client(ip, port)
		if not conn:
			gui.messagebox.showerror('Could not connect to Server',
				'Client could not connect to server due to:\n'+error)
			return
		conn.settimeout(5)
		try:
			username = conn.recv(100).decode()
			conn.settimeout(None)
		except:
			conn.close()
			gui.messagebox.showerror('Could not connect to Server',
				'Client could not connect to server due to:\n'+'Not a valid just_server server. Took too long to respond')
			return
		_id_ = self.db.is_connection((username, ip, port, 'out_server'))
		if not _id_:
			_id = self.db.new_index()
			send_time = tm.time()
			_data = data.connection(_id, username, ip, port, 'out_server', send_time)
			self.db.add_connection(_data)
			self.connect.online_clients[_id] = [conn, False]
			self.connect.start_client_listener(_id)
			self.gui.add_connected([_id, username, ip, port, 'out_server', send_time])
			self.gui.load_messager(_id, (username, ip, port), [])
			return
		self.connect.online_clients[_id_] = [conn, False]
		self.connect.start_client_listener(_id_)
		self.gui.load_messager(_id_, (username, ip, port), self.db.get_messages(_id_))
		self.gui.connection_button.set('Close Connection')
	def remove_client(self):
		_id = self.gui.at_ui['id']
		self.db.del_connection(_id)
		self.db.del_messages(_id)
		try:self.connect.close_client(_id)
		except:pass
		self.gui.back()
	def reconnect(self, _id):
		info = self.db.get_connection(_id)
		if 'in_server' in info:
			return
		conn, error = self.connect.start_client(info[2], info[3])
		if not conn:
			gui.messagebox.showerror('Could not connect to Server',
				'Client could not connect to server due to:\n'+error)
			return
		conn.send(self.get_host_name().encode())
		self.connect.online_clients[_id] = [conn, False]
		self.connect.start_client_listener(_id)
		return True
	def connection_mode(self):
		_id = self.gui.at_ui['id']
		if self.gui.connection_button.get().lower() == 'close connection':
			self.connect.close_client(_id)
			self.gui.connection_button.set('Re-Connect')
			if self.db.get_connection(_id)[-2] == 'in_server':
				self.gui.use_ui['connect']['state'] = 'disabled'
		else:
			if self.reconnect(_id):
				self.gui.connection_button.set('Close connection')
				self.gui.use_ui['connect']['state'] = 'normal'
	def send_message(self):
		_id = self.gui.at_ui['id']
		message = self.gui.message.get()
		if message == '':
			return
		state, error = self.connect.send_message(_id, message)
		if not state:
			gui.messagebox.showerror('Message not sent',
			'Message could not be sent due to:\n'+error)
			return
		sent_at = tm.time()
		_data = data.messages(_id, message, 'send', sent_at)
		self.db.add_message(_data)
		self.gui.message.set('')
		self.gui.show_message([_id, message, 'send', sent_at])
	def selected_connection(self):
		selected = self.gui.use_ui['connected'].curselection()
		if len(selected) == 0:
			return
		selected = self.gui.use_ui['connected'].get(selected[0])
		_id = int(selected[selected.index('ID:')+3:selected.index('Mode:')].strip())
		details = self.db.get_connection(_id)
		messages = self.db.get_messages(_id)
		self.gui.load_messager(_id, (details[1], details[2], details[3]), messages)
		if self.gui.at_ui['id'] == _id:
			if _id not in self.connect.online_clients.keys():
				self.gui.connection_button.set('Re-Connect')
				if self.db.get_connection(_id)[-2] == 'in_server':
					self.gui.use_ui['connect']['state'] = 'disabled'
			else:
				self.gui.connection_button.set('Close Connection')
	######################
	# db Functions
	######################
	# Connect Functions
	def got_new_client(self, conn, addr):
		conn.settimeout(5)
		try:
			username = conn.recv(100).decode()
			conn.settimeout(None)
		except:
			conn.close()
			return
		_id_ = self.db.is_connection((username, addr[0], addr[1], 'in_server'))
		conn_time = tm.time()
		if not _id_:
			_id = self.db.new_index()
			_data = data.connection(_id, username, addr[0], addr[1], 'in_server', conn_time)
			self.db.add_connection(_data)
			self.connect.online_clients[_id] = [conn, False]
			self.connect.start_client_listener(_id)
			self.gui.add_connected([_id, username, addr[0], addr[1], 'in_server', conn_time])
		else:
			_data = data.connection(_id_, username, addr[0], addr[1], 'in_server', conn_time)
			self.db.update_connection(_data)
			self.connect.online_clients[_id_] = [conn, False]
			self.connect.start_client_listener(_id_)
		if self.gui.at_ui['id'] == _id_:
			self.gui.connection_button.set('Close connection')
			self.gui.use_ui['connect']['state'] = 'normal'
	def got_server_error(self, error):
		got = gui.messagebox.askokcancel('Server error', 'Server has got error:\n'+str(error)+'\nDo you wish to restart server?')
		if got:
			info = self.db.get_connection(self.db.was_server())
			self.start_server((info[1], info[2], info[3]))
		else:
			self.gui.server_info.set('Server Offline')
			self.gui.server_button.set('Start server')
	def got_client_data(self, _id, data_):
		recv_time = tm.time()
		_data = data.messages(_id, data_, 'recv', recv_time)
		self.db.add_message(_data)
		self.gui.show_message([_id, data_, 'recv', recv_time])
	def client_closed(self, _id, reason):
		def last_():
			self.connect.close_client(_id)
			if self.gui.at_ui['id'] == _id:
				self.gui.connection_button.set('Re-Connect')
				if self.db.get_connection(_id)[-2] == 'in_server':
					self.gui.use_ui['connect']['state'] = 'disabled'
		if 'forcibly closed' in reason:
			last_()
			return
		_, username, ip, port, _, _ = self.db.get_connection(_id)
		info = 'Connection to '+username+' '+ip+':'+str(port)+' has faced error:\n'+reason+'\n'
		got = gui.messagebox.askokcancel('Connection error',info+'Try reconnecting?')
		if got:
			if self.reconnect(_id):
				return
		last_()
	######################

def main():
	Just_Text = just_text()
	Just_Text.gui.mainloop()

if __name__ == '__main__':
	main()