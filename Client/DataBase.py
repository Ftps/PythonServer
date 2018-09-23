#!/usr/bin/python3 -B

import gi, data, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

dir =  [('DataBase', 'Cur', '4096'),
        ('Math', 'Dir', '4096'),
        ('Book.pdf', 'File', '19986')]

class Main_Client(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Ftps\'s Drive')
        #self.set_size_request(1280, 800)
        color = Gdk.color_parse('grey')
        rgba = Gdk.RGBA.from_color(color)
        self.override_background_color(0, rgba)
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
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        list_store = Gtk.ListStore(str, str, str)
        for ref in dir:
            list_store.append(list(ref))
        lang = list_store.filter_new()

        self.treeview = Gtk.TreeView.new_with_model(lang)
        for i, column_title in enumerate(['Name', 'Type', 'Size']):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        box_top = Gtk.Box(spacing=6)
        grid.attach(box_top, 0, 0, 1, 1)

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        grid.attach(scroll, 1, 1, 14, 15)
        scroll.add(self.treeview)

        box_sep = Gtk.Box(spacing=6)
        grid.attach_next_to(box_sep, scroll, Gtk.PositionType.BOTTOM, 1, 1)

        dow_but = Gtk.Button.new_with_label('Add File')
        dow_but.connect('clicked', self.download_but)
        grid.attach_next_to(dow_but, box_sep, Gtk.PositionType.BOTTOM, 2, 1)

        box_but = Gtk.Box(spacing=6)
        grid.attach_next_to(box_but, dow_but, Gtk.PositionType.RIGHT, 1, 1)

        add_but = Gtk.Button.new_with_label('Add File')
        add_but.connect('clicked', self.add_but)
        grid.attach_next_to(add_but, box_but, Gtk.PositionType.RIGHT, 2, 1)

        box_but1 = Gtk.Box(spacing=6)
        grid.attach_next_to(box_but1, add_but, Gtk.PositionType.RIGHT, 1, 1)

        rem_but = Gtk.Button.new_with_label('Remove File')
        rem_but.connect('clicked', self.remove_but)
        grid.attach_next_to(rem_but, box_but1, Gtk.PositionType.RIGHT, 2, 1)

        box_but2 = Gtk.Box(spacing=6)
        grid.attach_next_to(box_but2, rem_but, Gtk.PositionType.RIGHT, 4, 1)

        exit_but = Gtk.Button.new_with_label('Exit')
        exit_but.connect('clicked', self.on_exit)
        grid.attach_next_to(exit_but, box_but2, Gtk.PositionType.RIGHT, 2, 1)

        box_bot = Gtk.Box(spacing=6)
        grid.attach_next_to(box_bot, exit_but, Gtk.PositionType.BOTTOM, 3, 1)

        self.add(grid)
        self.show_all()

        select = self.treeview.get_selection()
        select.connect("changed", self.chnd)

    def add_but(self, button):
        print('ADD FILE')

    def remove_but(self, button):
        print('REMOVE KEBAB')

    def download_but(self, button):
        print('DOWN SYNDROME')

    def chnd(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            print(model[treeiter][0])

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
