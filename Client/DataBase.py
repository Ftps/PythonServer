#!/usr/bin/python3 -B

import gi, data, time, warnings, os, pickle, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

dir =  [('Books', 'Cur', '4096'),
        ('Math', 'Dir', '4096'),
        ('Book.pdf', 'File', '19986'),
        ('File.docx', 'File', '1287')]

class Confirm(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Create New Folder')
        self.timeout_id = None
        self.num = 0

    def window(self):
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        box_top = Gtk.Box(spacing=6)
        grid.attach(box_top, 0, 0, 1, 1)

        label_u = Gtk.Label()
        label_u.set_text(self.label)
        label_u.set_justify(Gtk.Justification.CENTER)
        grid.attach(label_u, 1, 1, 3, 1)

        box = Gtk.Box(spacing=6)
        grid.attach_next_to(box, label_u, Gtk.PositionType.BOTTOM, 3, 1)

        okay_but = Gtk.Button.new_with_label('Yes')
        okay_but.connect('clicked', self.okay_but)
        grid.attach_next_to(okay_but, box, Gtk.PositionType.BOTTOM, 1, 1)

        mid_box = Gtk.Box(spacing=6)
        grid.attach_next_to(mid_box, okay_but, Gtk.PositionType.RIGHT, 1, 1)

        exit_but = Gtk.Button.new_with_label('No')
        exit_but.connect('clicked', self.exit_but)
        grid.attach_next_to(exit_but, mid_box, Gtk.PositionType.RIGHT, 1, 1)

        end_box = Gtk.Box(spacing=6)
        grid.attach_next_to(end_box, exit_but, Gtk.PositionType.BOTTOM, 2, 1)

        self.add(grid)
        self.show_all()

    def okay_but(self, button):
        self.num = 1
        self.destroy()

    def exit_but(self, button):
        self.num = 0
        self.destroy()

    def get_num(self):
        return self.num

    def label(self, text):
        self.label = text

class Folder_Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Create New Folder')
        self.s = None
        self.timeout_id = None
        self.num = 0
        self.folder = ""

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        box_top = Gtk.Box(spacing=6)
        grid.attach(box_top, 0, 0, 1, 1)

        label_u = Gtk.Label()
        label_u.set_text('Folder Name:')
        grid.attach(label_u, 1, 1, 1, 1)
        self.entry_u = Gtk.Entry()
        grid.attach_next_to(self.entry_u, label_u, Gtk.PositionType.RIGHT, 2, 1)

        new_but = Gtk.Button.new_with_label('Create')
        new_but.connect('clicked', self.create_f)

        v_box = Gtk.Box(spacing=6)

        exit_but = Gtk.Button.new_with_label('Cancel')
        exit_but.connect('clicked', self.exit_but)

        end_box = Gtk.Box(spacing=6)

        grid.attach_next_to(new_but, label_u, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(v_box, new_but, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(exit_but, v_box, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(end_box, exit_but, Gtk.PositionType.BOTTOM, 2, 1)

        self.add(grid)
        self.show_all()

    def create_f(self, button):
        self.num = 1
        self.folder = self.entry_u.get_text()
        self.destroy()

    def exit_but(self, button):
        self.num = 0
        self.destroy()

    def get_num(self):
        return self.num

    def get_fold(self):
        return self.folder


class Main_Client(Gtk.Window):

    def __init__(self):

        self.s = None
        self.timeout_id = None
        self.download_folder = data.DEFAULT_FOLDER
        self.transfer = 1
        self.action = 1
        self.treeview = None


    def get_soc(self, s):
        self.s = s

    def get_act(self):
        return self.action

    def window(self):

        Gtk.Window.__init__(self, title='Ftps\'s Drive')
        #self.set_size_request(1280, 800)
        color = Gdk.color_parse('grey')
        rgba = Gdk.RGBA.from_color(color)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=DeprecationWarning)
            self.override_background_color(0, rgba)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.oof = None

        box_top = Gtk.Box(spacing=6)
        self.grid.attach(box_top, 0, 0, 1, 1)

        stack = pickle.loads(self.s.recv(data.BUFFSIZE))
        self.add_tree(stack)

        add_but = Gtk.Button.new_with_label('Add File')
        add_but.connect('clicked', self.add_but)

        rem_but = Gtk.Button.new_with_label('Remove File/Dir')
        rem_but.connect('clicked', self.remove_but)

        mkdir_but = Gtk.Button.new_with_label('Create Directory')
        mkdir_but.connect('clicked', self.makedir_but)


        self.change_but = Gtk.Button.new_with_label('-')
        self.change_but.connect('clicked', self.action_but)

        path_but = Gtk.Button.new_with_label('Change Path')
        path_but.connect('clicked', self.path_change)

        home_but = Gtk.Button.new_with_label('Home')
        home_but.connect('clicked', self.home_but)


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

        self.grid.attach(box_1, 1, 18, 1, 1)
        self.grid.attach_next_to(add_but, box_1, Gtk.PositionType.BOTTOM, 2, 1)
        self.grid.attach_next_to(box_2, add_but, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(rem_but, box_2, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(box_3, rem_but, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(mkdir_but, box_3, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(box_4, add_but, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.change_but, box_4, Gtk.PositionType.BOTTOM, 2, 1)
        self.grid.attach_next_to(box_5, self.change_but, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(path_but, box_5, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(box_6, path_but, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(home_but, box_6, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(box_7, home_but, Gtk.PositionType.RIGHT, 4, 1)
        self.grid.attach_next_to(exit_but, box_7, Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(box_8, exit_but, Gtk.PositionType.BOTTOM, 3, 1)

        self.add(self.grid)
        self.show_all()

    def add_but(self, button):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=DeprecationWarning)
            dialog = Gtk.FileChooserDialog(title="Please select a file",
                     action=Gtk.FileChooserAction.OPEN,
                     buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        t = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()
        if t == Gtk.ResponseType.OK:
            print('File selected')
            self.s.send(b'6')
            data.send_file(self.s, filename)

            stack = pickle.loads(self.s.recv(data.BUFFSIZE))
            self.add_tree(stack)


    def remove_but(self, button):
        model, mode = self.select.get_selected()
        try:
            print(model[mode][0])
        except:
            print('Nothing selected.')
            return

        self.folder = model[mode][0]
        self.action = 4
        Gtk.main_quit()


    def makedir_but(self, button):
        self.action = 3
        self.s.send(b'2')
        Gtk.main_quit()

    def home_but(self, button):
        self.s.send(b'3')
        stack = pickle.loads(self.s.recv(data.BUFFSIZE))
        self.add_tree(stack)

    def path_change(self, button):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=DeprecationWarning)
            dialog = Gtk.FileChooserDialog(title="Please choose a folder",
                     action=Gtk.FileChooserAction.SELECT_FOLDER,
                     buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        if dialog.run() == Gtk.ResponseType.OK:
            self.download_folder = dialog.get_filename()
            print(self.download_folder)

        dialog.destroy()

    def action_but(self, button):
        if button.get_label() == '<':
            self.s.send(b'1')
            t = self.s.recv(data.BUFFSIZE)
            if  t == b'name':
                self.s.send(str.encode('..'))

                self.oof = None

                stack = pickle.loads(self.s.recv(data.BUFFSIZE))
                print(stack)
                self.add_tree(stack)
                return
            else:
                print('Error changing directory.')
                sys.exit(-1)

        elif button.get_label() == 'X':
            return

        model, mode = self.select.get_selected()

        try:
            print(model[mode][0])
        except:
            print('Nothing selected.')
            return

        if button.get_label() == 'Change Directory':
            self.s.send(b'1')
            t = self.s.recv(data.BUFFSIZE)
            if  t == b'name':
                self.s.send(str.encode(model[mode][0]))
                self.oof = None
                stack = pickle.loads(self.s.recv(data.BUFFSIZE))
                self.add_tree(stack)
            else:
                print('Error changing directory.')
                sys.exit(-1)
        elif button.get_label() == 'Download File':
            self.action = 5
            self.folder = model[mode][0]
            Gtk.main_quit()


    def add_tree(self, stack):
        if self.treeview != None:
            self.scroll.destroy()
            self.treeview.destroy()
            self.change_but.set_label('-')
        else:
            self.back = Gtk.Button()
            self.back.connect('clicked', self.action_but)
            self.label = Gtk.Button()
            self.grid.attach(self.back, 1, 1, 1, 1)
            self.grid.attach_next_to(self.label, self.back, Gtk.PositionType.RIGHT, 2, 1)
            box_init = Gtk.Box(spacing=6)
            self.grid.attach_next_to(box_init, self.back, Gtk.PositionType.BOTTOM, 1, 1)


        self.list_store = Gtk.ListStore(str, str, str)
        for ref in stack:
            if ref[1] != 'Cur':
                self.list_store.append(list(ref))
            else:
                self.oof = ref
        self.lang = self.list_store.filter_new()

        self.treeview = Gtk.TreeView.new_with_model(self.lang)
        for i, column_title in enumerate(['Name', 'Type', 'Size(Kb)']):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        if self.oof[0] == 'DataBase':
            self.back.set_label('X')
        else:
            self.back.set_label('<')

        self.label.set_label(self.oof[0])


        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True)
        self.grid.attach(self.scroll, 1, 3, 14, 15)
        self.scroll.add(self.treeview)
        self.show_all()
        self.select = self.treeview.get_selection()
        self.select.connect("changed", self.chnd)

    def on_exit(self, button):
        self.s.send(b'0')
        self.action = 0
        Gtk.main_quit()

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
        self.show_all()
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
    win.action = 0
    win.s.send(b'0')
    Gtk.main_quit()

def make_dir(win):
    p = Folder_Window()
    p.connect('destroy', Gtk.main_quit)
    Gtk.main()

    if p.get_num() == 1:
        t = win.s.recv(data.BUFFSIZE)
        if t == b'name':
            win.s.send(str.encode(p.get_fold()))
            t = win.s.recv(data.BUFFSIZE)
            if t == b'1':
                print('Folder created.')
            else:
                print('Folder already exists.')

            win.s.send(b'1')
            stack = pickle.loads(win.s.recv(data.BUFFSIZE))
            win.add_tree(stack)
        else:
            print('Error creating folder.')
            sys.exit(-2)

def delete_obj(win):
    p = Confirm()
    p.connect('destroy', Gtk.main_quit)
    p.label('Are you sure you wish to delete the following object?\nAll data inside will be lost.')
    p.window()
    Gtk.main()

    if p.get_num() == 1:
        win.s.send(b'4')
        t = win.s.recv(data.BUFFSIZE)
        if t == b'name':
            win.s.send(str.encode(win.folder))

            stack = pickle.loads(win.s.recv(data.BUFFSIZE))
            win.add_tree(stack)
        else:
            print('Error deleting object.')
            sys.exit(-3)

def download_file(win):
    p = Confirm()
    p.connect('destroy', Gtk.main_quit)
    p.label('Are you sure you wish to download the file to the current directory?\n' + win.download_folder)
    p.window()
    Gtk.main()

    if p.get_num() == 1:
        win.s.send(b'5')
        data.receive_file(win.s, win.folder, win.download_folder)



if __name__ == '__main__':
    win = Login_Screen()
    win.connect('destroy', Gtk.main_quit)
    Gtk.main()
    s = win.ret_sock()

    if s != None:
        win = Main_Client()
        win.get_soc(s)
        win.window()
        win.connect('destroy', kill_drive)
        while win.action != 0:
            Gtk.main()
            if win.action == 3:
                make_dir(win)
            elif win.action == 4:
                delete_obj(win)
            elif win.action == 5:
                download_file(win)
