import sys
import time as tm
import tkinter as tk
from tkinter import messagebox

class just_ui(tk.Tk):
	def __init__(self, king, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.king = king
		self.geometry("470x500")
		self.title("Just text v0.1")

		if 'win' in sys.platform:
			self.fonty = ('segoe print', 15)
			self.btfont = ('segoe print', 10)
			self.lbFont = ('segoe print', 9)
		else:
			self.fonty = ('ubuntu mono', 15)
			self.btfont = ('ubuntu mono', 10)
			self.lbFont = ('ubuntu mono', 9)
		self.setVariables()

		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (main_page, messager):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky='nsew')

		self.show_frame(main_page)
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
	def setVariables(self):
		self.at_ui = {
			'page': 'main_page',
			'id': None
		}
		self.use_ui = {}
		self.messages_at_ui = []

		self.server_info = tk.StringVar()
		self.server_info.set("Server Offline")

		self.server_button = tk.StringVar()
		self.server_button.set("Start server")

		self.connection_button = tk.StringVar()
		self.connection_button.set('Close connection')

		self.messager_name = tk.StringVar()
		self.messager_name.set('Username')
		self.messager_ip = tk.StringVar()
		self.messager_ip.set('127.0.0.1')
		self.messager_port = tk.StringVar()
		self.messager_port.set('4567')

		self.message = tk.StringVar()

		self.username = tk.StringVar()
		self.ip = tk.StringVar()
		self.port = tk.StringVar()
	def show_message(self, _message):
		_id, message_text, mode, time = _message
		if _id != self.at_ui['id']:
			return
		if mode == 'recv':
			message = 'Recv Time: '+tm.ctime(time)+'\n'+message_text
			lb = tk.Label(self.use_ui['messages'], text=message, bg='cyan', fg='black',
			wraplength=350, justify='left', anchor='w', font=self.lbFont)
			lb.pack(fill='x', expand=True)
			self.messages_at_ui.append(lb)
		else:
			message = 'Send Time: '+tm.ctime(time)+'\n'+message_text
			lb = tk.Label(self.use_ui['messages'], text=message, bg='magenta', fg='black',
			wraplength=350, justify='right', anchor='e', font=self.lbFont)
			lb.pack(fill='x', expand=True)
			self.messages_at_ui.append(lb)
		last = self.use_ui['scroll_messages'].get()[1]
		self.use_ui['scroll_messages'].set(last, last)
	def load_messager(self, _id, info, messages):
		self.at_ui['id'] = _id
		self.messager_name.set(info[0])
		self.messager_ip.set(info[1])
		self.messager_port.set(info[2])
		for message in messages:
			self.show_message(message)
		self.show_frame(messager)
		self.at_ui['page'] = 'messager'
	def add_connected(self, details):
		_id, username, ip, port, mode, time = details
		info = 'Name: '+username+' Address: '+ip+':'+str(port)+' ID: '+str(_id)+' Mode: '+mode#+' Time: '+tm.ctime(time)
		self.use_ui['connected'].insert(0, info)
	# Button commands handler
	def server_call(self):
		if self.server_button.get().lower() == 'start server':
			dialog(self)
		else:
			self.king.close_server()
	def back(self):
		self.king.update_connections()
		self.show_frame(main_page)
		self.at_ui['id'] = None
		self.at_ui['page'] = 'main_page'
		for message in self.messages_at_ui:
			message.destroy()
		self.message.set('')
		self.use_ui['messages'].pack_forget()
		self.use_ui['connect']['state'] = 'normal'
class main_page(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_rowconfigure((0, 1), weight=0)
		self.grid_columnconfigure((0, 1), weight=1)

		self.grid_rowconfigure(2, weight=1)

		server_info = tk.Label(self, textvariable=controller.server_info,
			font=controller.fonty, fg='green')
		server_info.grid(row=0, column=0, columnspan=2, sticky='ew')

		server_mode = tk.Button(self, textvariable=controller.server_button, font=controller.btfont,
			bd=0, fg='yellow', bg='black', command=controller.server_call)
		server_mode.grid(row=1, column=0, sticky='ew', padx=3)
		connect = tk.Button(self, text='Connect to server', font=controller.btfont,
			command=controller.king.connect_to_server_,
			bd=0, fg='magenta', bg='black')
		connect.grid(row=1, column=1, sticky='ew', padx=3)

		lb_f = tk.LabelFrame(self, text='Connected')
		lb_f.grid_rowconfigure(0, weight=1)
		lb_f.grid_columnconfigure(0, weight=1)

		scroll = tk.Scrollbar(lb_f)
		connected = tk.Listbox(lb_f, yscrollcommand=scroll.set, bd=0, font=controller.lbFont)
		controller.use_ui['connected'] = connected
		scroll.config(command=connected.yview)

		connected.grid(row=0, column=0, sticky='nsew')
		scroll.grid(row=0, column=1, sticky='ns')
		lb_f.grid(row=2, column=0, columnspan=2, sticky='nsew')

class messager(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.grid_rowconfigure((0, 1, 2, 4), weight=0)
		self.grid_columnconfigure((0, 1, 2, 3), weight=1)
		self.grid_rowconfigure(3, weight=1)

		# Messager info area
		username = tk.Label(self, textvariable=controller.messager_name,
			font=controller.fonty, fg='magenta')
		username.grid(row=0, column=0, columnspan=4, sticky='ew')
		ip = tk.Label(self, text="IP: ",
			font=controller.lbFont)
		ip.grid(row=1, column=0, sticky='w')
		server_ip = tk.Label(self, textvariable=controller.messager_ip,
			font=controller.lbFont)
		server_ip.grid(row=1, column=1, sticky='w')
		port = tk.Label(self, text="Port: ",
			font=controller.lbFont)
		port.grid(row=1, column=2, sticky='w')
		server_port = tk.Label(self, textvariable=controller.messager_port,
			font=controller.lbFont)
		server_port.grid(row=1, column=3, sticky='w')

		frm_bts = tk.Frame(self)
		frm_bts.grid_columnconfigure((0, 1, 2), weight=1)
		frm_bts.grid(row=2, column=0, columnspan=4, sticky='ew')
		#################################

		# Messeger buttons
		server_mode = tk.Button(frm_bts, text="Back", font=controller.btfont,
			command=controller.back,
			bd=0, fg='cyan', bg='black')
		server_mode.grid(row=0, column=0, sticky='ew', padx=3)
		Remove = tk.Button(frm_bts, text='Remove', font=controller.btfont,
			command=controller.king.remove_client,
			bd=0, fg='cyan', bg='black')
		Remove.grid(row=0, column=1, sticky='ew', padx=3)
		connect = tk.Button(frm_bts, textvariable=controller.connection_button, font=controller.btfont,
			command=controller.king.connection_mode,
			bd=0, fg='cyan', bg='black')
		controller.use_ui['connect'] = connect
		connect.grid(row=0, column=2, sticky='ew', padx=3)

		##################################
		frm_msg = tk.Frame(self)
		frm_msg.grid_rowconfigure(0, weight=1)
		frm_msg.grid_columnconfigure(0, weight=1)
		##################################

		# Messages area
		scroll = tk.Scrollbar(frm_msg)
		messages_container = tk.Canvas(frm_msg, yscrollcommand=scroll.set)
		messages = tk.Frame(messages_container)
		msg_id = messages_container.create_window((0, 0), window=messages, anchor='nw')

		def resize(e):
			messages_container.config(height=e.height-100, width=e.width-100)
			messages_container.itemconfig(msg_id, width=e.width)
		messages_container.bind('<Configure>', resize)
		messages.bind("<Configure>",
			lambda e: messages_container.configure(scrollregion=messages_container.bbox('all')))

		scroll.config(command=messages_container.yview)

		messages_container.grid(row=0, column=0, sticky='nsew')
		scroll.grid(row=0, column=1, sticky='ns')
		frm_msg.grid(row=3, column=0, columnspan=4, sticky='nsew')

		controller.use_ui['messages'] = messages
		controller.use_ui['scroll_messages'] = scroll
		##################################

		# Send message
		message = tk.Entry(self, font=controller.lbFont, textvariable=controller.message)
		message.grid(row=4, column=0, columnspan=3, sticky='nsew', pady=2)
		connect = tk.Button(self, text='Send', font=controller.btfont,
			command=controller.king.send_message,
			bd=0, fg='orange', bg='black')
		connect.grid(row=4, column=3, sticky='ew', padx=3, pady=2)
		##################################

class dialog(tk.Toplevel):
	def __init__(self, controller, heading='Start Server', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.heading = heading
		if heading.lower() == 'start server':
			self.username = controller.username
			self.ip = controller.ip
			self.port = controller.port
		else:
			self.username = tk.StringVar()
			self.ip = tk.StringVar()
			self.port = tk.StringVar()

		self.controller = controller
		self.title(heading)
		self.geometry('250x107')
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(3, weight=1)

		lb_name = tk.Label(self, text='Username : ')
		lb_name.grid(row=0, column=0, sticky='w')
		name = tk.Entry(self, textvariable=self.username)
		name.grid(row=0, column=1, sticky='ew')

		lb_ip = tk.Label(self, text='Ip : ')
		lb_ip.grid(row=1, column=0, sticky='w')
		ip = tk.Entry(self, textvariable=self.ip, width=21)
		ip.grid(row=1, column=1, sticky='w')

		lb_port = tk.Label(self, text='Port : ')
		lb_port.grid(row=2, column=0, sticky='w')
		port = tk.Entry(self, textvariable=self.port, width=9)
		port.grid(row=2, column=1, sticky='w')

		frm = tk.Frame(self)
		frm.grid_columnconfigure((0, 1), weight=1)
		frm.grid(row=3, column=0, columnspan=2, sticky='ew')

		cancle = tk.Button(frm, text='Cancle', command=self.destroy,
			bd=0, fg='white', bg='black', height=2)
		cancle.grid(row=0, column=0, sticky='ew', padx=3, pady=1)
		connect = tk.Button(frm, text='Connect', command=self.connect,
			bd=0, fg='white', bg='black', height=2)
		connect.grid(row=0, column=1, sticky='ew', padx=3, pady=1)
		self.resizable(0, 0)
	def connect(self):
		self.destroy()
		username, ip, port = self.username.get(), self.ip.get(), self.port.get()
		if username != '':
			if ip.count('.') == 3:
				nums = ip.split('.')
				for num in nums:
					try:
						int(num)
					except:
						messagebox.showerror('IP error','Invalid ip address\n'+ip)
						return
				try:
					port = int(port)
				except:
					messagebox.showerror('Port error', 'Invalid port number\n'+port)
					return
			else:
				messagebox.showerror('IP error','Invalid ip address\n'+ip)
				return
		else:
			messagebox.showinfo('Username required', 'Please imput a username')
			return
		if self.heading.lower() == 'start server':
			self.controller.king.start_server((username, ip, port))
		else:
			self.controller.king.connect_to_server((username, ip, port))
