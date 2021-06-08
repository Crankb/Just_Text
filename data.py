import sqlite3

def create_tables(conn):
	c = conn.cursor()
	with conn:
		c.execute("""
			CREATE TABLE IF NOT EXISTS connections(
				id PRIMARY KEY, username, ip, port, mode, time
			)""")
		c.execute("""
			CREATE TABLE IF NOT EXISTS messages(
				conn_id, message, mode, time
			)""")

def create_db():
	conn = sqlite3.connect('just_text.db', check_same_thread=False)
	create_tables(conn)
	return conn

class connection:
	def __init__(self, id, username, ip, port, mode, time):
		self.id = id
		self.username = username
		self.ip = ip
		self.port = port
		self.mode = mode
		self.time = time

class messages:
	def __init__(self, conn_id, message, mode, time):
		self.conn_id = conn_id
		self.message = message
		self.mode = mode
		self.time = time

class just_db():
	def __init__(self):
		self.conn = create_db()
	# Helper Functions
	def was_server(self):
		try:
			return self.conn.execute('SELECT id FROM connections WHERE mode = ?', ('server',)
				).fetchone()[0]
		except:
			return
	def sum_connections(self):
		return int(self.conn.execute('SELECT COUNT(*) FROM connections').fetchone()[0])
	def sum_messages(self):
		return int(self.conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0])
	def is_connection(self, details):
		username, ip, port, mode = details
		try:
			if mode == 'out_server':
				got = self.conn.execute('SELECT id FROM connections WHERE username = ? AND ip = ? AND port = ? AND mode = ?',
					(username, ip, port, mode)).fetchone()
			else:
				got = self.conn.execute('SELECT id FROM connections WHERE username = ? AND ip = ? AND mode = ?',
					(username, ip, mode)).fetchone()
			if got:
				return got[0]
		except:
			pass
	def new_index(self):
		got = self.conn.execute('SELECT id FROM connections ORDER BY id DESC LIMIT 1').fetchone()
		if got:
			return got[0] + 1
		else:
			return 1
	#############################
	# Add to db
	def add_connection(self, data):
		with self.conn:
			self.conn.execute('INSERT INTO connections VALUES (?, ?, ?, ?, ?, ?)', (
				data.id, data.username, data.ip, data.port, data.mode, data.time))
	def add_message(self, data):
		with self.conn:
			self.conn.execute('INSERT INTO messages VALUES (?, ?, ?, ?)', (
				data.conn_id, data.message, data.mode, data.time))
	#############################
	# Update db
	def update_connection(self, data):
		dt = [data.__dict__[key] for key in data.__dict__]
		with self.conn:
			self.conn.execute('UPDATE connections SET username = ?, ip = ?, port = ?, mode = ?, time = ? WHERE id = ?',
				(dt[1], dt[2], dt[3], dt[4], dt[5], dt[0]))
				#(data.username, data.ip. data.port, data.mode, data.time, data.id))
	#############################
	#Get from db
	def get_connection(self, which='all'):
		if which == 'all':
			return self.conn.execute('SELECT * FROM connections').fetchall()
		else:
			return self.conn.execute('SELECT * FROM connections WHERE id = ?', (which,)).fetchone()
	def get_messages(self, which='all'):
		if which == 'all':
			return self.conn.execute('SELECT * FROM messages').fetchall()
		else:
			return self.conn.execute('SELECT * FROM messages WHERE conn_id = ?', (which,)).fetchall()
	#############################
	# Delete from db
	def del_connection(self, _id):
		with self.conn:
			self.conn.execute('DELETE FROM connections WHERE id = ?', (_id,))
	def del_messages(self, _id):
		with self.conn:
			self.conn.execute('DELETE FROM messages WHERE conn_id = ?', (_id,))
	#############################

