#!/usr/bin/python3 -B

import gi, data, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

dir = {'DataBase':'Cur', 'Math':['Dir', '4096'], 'Book.pdf':['File', '19986']}

class Main_Client(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Ftps\'s Drive')
        self.set_size_request(1280, 800)
        self.s = None
        self.timeout_id = None
        self.running_cycle()


    def get_soc(self, s):
        self.s = s

    def on_exit(self, button):
        self.s.send(b'0')
        self.destroy()

    def running_cycle(self):
        grid = Gtk.Grid()

        exit_but = Gtk.Button.new_with_label('Exit')
        exit_but.connect('clicked', self.on_exit)
        grid.attach(exit_but, 3, 4, 1, 1)

        self.add(grid)

class Login_Screen(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Login Window')

        self.timeout_id = None

        box1 = Gtk.Box(spacing=6)
        box2 = Gtk.Box(spacing=6)

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        grid.attach(box1, 0, 0, 1, 1)

        label_u = Gtk.Label()
        label_u.set_text('Username:')
        grid.attach(label_u, 1, 1, 1, 1)
        self.entry_u = Gtk.Entry()
        grid.attach(self.entry_u, 2, 1, 2, 1)

        label_p = Gtk.Label()
        label_p.set_text('Password:')
        grid.attach(label_p, 1, 2, 1, 1)
        self.entry_p = Gtk.Entry()
        self.entry_p.set_visibility(False)
        grid.attach(self.entry_p, 2, 2, 2, 1)

        login_but = Gtk.Button.new_with_label('Login')
        login_but.connect('clicked', self.on_login)
        grid.attach(login_but, 1, 4, 1, 1)
        exit_but = Gtk.Button.new_with_label('Exit')
        exit_but.connect('clicked', self.on_exit)
        grid.attach(exit_but, 3, 4, 1, 1)

        grid.attach(box2, 4, 5, 1, 1)

        self.add(grid)
        self.s = None


    def on_exit(self, button):
        self.destroy()

    def on_login(self, button):
        self.s = data.login(self.entry_u.get_text(), self.entry_p.get_text())
        if self.s == None:
            print('Login failed.')
        else:
            pass
            #self.s.send(b'0')

        self.on_exit(button)
        #Main_Client(self, s)

    def ret_sock(self):
        return self.s


if __name__ == '__main__':
    win = Login_Screen()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
    s = win.ret_sock()

    if s != None:
        win = Main_Client()
        win.connect('destroy', Gtk.main_quit)
        win.get_soc(s)
        win.show_all()
        Gtk.main()
