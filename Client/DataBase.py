#!/usr/bin/python3 -B

import gi, data, time, warnings
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

dir =  [('Books', 'Cur', '4096'),
        ('Math', 'Dir', '4096'),
        ('Book.pdf', 'File', '19986'),
        ('File.docx', 'File', '1287')]

class Path_Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Change Path')
        self.s = None
        self.timeout_id = None
        self.num = 0

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        box_top = Gtk.Box(spacing=6)
        grid.attach(box_top, 0, 0, 1, 1)

        label_u = Gtk.Label()
        label_u.set_text('Path:')
        grid.attach(label_u, 1, 1, 1, 1)
        self.entry_u = Gtk.Entry()
        grid.attach_next_to(self.entry_u, label_u, Gtk.PositionType.RIGHT, 3, 1)

        path_but = Gtk.Button.new_with_label('New Path')
        path_but.connect('clicked', self.new_p)

        def_but = Gtk.Button.new_with_label('Default Path')
        def_but.connect('clicked', self.def_fol)

        exit_but = Gtk.Button.new_with_label('Exit')
        exit_but.connect('clicked', self.exit_but)


    def new_p(self, button):
        self.num = 1
        self.destroy()

    def def_fol(self, button):
        self.num = 2
        self.destroy()

    def exit_but(self, button):
        self.num = 0
        self.destroy()

    def get_num(self):
        return self.num

    def get_path(self):
        return self.entry_u.get_text()

class Main_Client(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Ftps\'s Drive')
        #self.set_size_request(1280, 800)
        color = Gdk.color_parse('grey')
        rgba = Gdk.RGBA.from_color(color)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=DeprecationWarning)
            self.override_background_color(0, rgba)

        self.s = None
        self.timeout_id = None
        self.download_folder = data.DEFAULT_FOLDER
        self.transfer = 1
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

        self.oof = None

        self.list_store = Gtk.ListStore(str, str, str)
        for ref in dir:
            if ref[1] != 'Cur':
                self.list_store.append(list(ref))
            else:
                self.oof = ref
        lang = self.list_store.filter_new()

        self.treeview = Gtk.TreeView.new_with_model(lang)
        for i, column_title in enumerate(['Name', 'Type', 'Size(Kb)']):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        box_top = Gtk.Box(spacing=6)
        grid.attach(box_top, 0, 0, 1, 1)

        if self.oof[0] == 'DataBase':
            self.back = Gtk.Button(label='X')
        else:
            self.back = Gtk.Button(label='<')
        self.back.connect('clicked', self.back_dir)
        grid.attach(self.back, 1, 1, 1, 1)


        label = Gtk.Button(label=self.oof[0])
        grid.attach_next_to(label, self.back, Gtk.PositionType.RIGHT, 2, 1)

        box_init = Gtk.Box(spacing=6)
        grid.attach_next_to(box_init, self.back, Gtk.PositionType.BOTTOM, 1, 1)


        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        grid.attach_next_to(scroll, box_init, Gtk.PositionType.BOTTOM, 14, 15)
        scroll.add(self.treeview)


        add_but = Gtk.Button.new_with_label('Add File')
        add_but.connect('clicked', self.add_but)

        rem_but = Gtk.Button.new_with_label('Remove File/Dir')
        rem_but.connect('clicked', self.remove_but)

        mkdir_but = Gtk.Button.new_with_label('Create Directory')
        mkdir_but.connect('clicked', self.makedir_but)


        self.change_but = Gtk.Button.new_with_label('Change Directory')
        self.change_but.connect('clicked', self.action_but)

        path_but = Gtk.Button.new_with_label('Change Path')
        path_but.connect('clicked', self.path_change)

        home_but = Gtk.Button.new_with_label('Home')
        home_but.connect('clicked', self.action_but)


        exit_but = Gtk.Button.new_with_label('Exit')
        exit_but.connect('clicked', self.on_exit)


        box_1 = Gtk.Box(spacing=6)
        box_2 = Gtk.Box(spacing=6)
        box_3 = Gtk.Box(spacing=6)
        box_4 = Gtk.Box(spacing=6)
        box_5 = Gtk.Box(spacing=6)
        box_6 = Gtk.Box(spacing=6)
        box_7 = Gtk.Box(spacing=6)
        box_8 = Gtk.Box(spacing=6)

        grid.attach_next_to(box_1, scroll, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(add_but, box_1, Gtk.PositionType.BOTTOM, 2, 1)
        grid.attach_next_to(box_2, add_but, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(rem_but, box_2, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(box_3, rem_but, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(mkdir_but, box_3, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(box_4, add_but, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.change_but, box_4, Gtk.PositionType.BOTTOM, 2, 1)
        grid.attach_next_to(box_5, self.change_but, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(path_but, box_5, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(box_6, path_but, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(home_but, box_6, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(box_7, home_but, Gtk.PositionType.RIGHT, 4, 1)
        grid.attach_next_to(exit_but, box_7, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(box_8, exit_but, Gtk.PositionType.BOTTOM, 3, 1)

        self.add(grid)
        self.show_all()

        self.select = self.treeview.get_selection()
        self.select.connect("changed", self.chnd)

    def add_but(self, button):
        print('ADD FILE')

    def remove_but(self, button):
        print('REMOVE KEBAB')

    def makedir_but(self, button):
        print('MAKE DIRECT')


    def path_change(self, button):
        p = Path_Window()
        p.connect('destroy', Gtk.main_quit)
        n = p.get_num()
        if n == 0:
            return
        if n == 1:
            test = p.get_path()
            if os.path.exists(test):
                self.download_folder = test
            else:
                print('You bafoon')
        if n == 2:
            self.download_folder = data.DEFAULT_FOLDER

        print(self.download_folder)

    def action_but(self, button):
        print('DOWN SYNDROME')
        print('Button Label: ' + button.get_label())
        model, mode = self.select.get_selected()
        try:
            print(model[mode][0])
        except:
            print('Nothing selected')

    def back_dir(self, button):
        if button.get_label() == '<':
            print('BACK THE HELL UP')
        else:
            print('YOU CAN\'T GO BACK')

    def chnd(self, selection):
        model, mode = selection.get_selected()
        if mode is not None:
            if model[mode][1] != 'Dir':
                self.change_but.set_label('Download File')
            else:
                self.change_but.set_label('Change Directory')



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

def kill_drive(win):
    if win.transfer == 1:
        return

    win.s.send(b'0')
    Gtk.main_quit()

if __name__ == '__main__':
    win = Login_Screen()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
    s = win.ret_sock()

    if s != None:
        win = Main_Client()
        win.connect('destroy', kill_drive)
        win.get_soc(s)
        win.show_all()
        Gtk.main()
