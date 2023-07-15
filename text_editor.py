from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as msg 
import os

from termcolor import colored


class Dodopad(Tk):
    def __init__(self):
        super().__init__()
        self.title("DodoPad")
        self.geometry("873x556")

        self.show_line_number = BooleanVar()

        self.menubar = self.create_menubar()
        self.status_bar = self.create_status_bar()
        self.y_scrollbar, self.x_scrollbar = self.create_scroll_bar()
        self.line_number_panel = self.create_line_number_panel()
        self.textbox_font = ('Lucida console',12,'bold')
        self.textbox = self.create_textbox()

        self.file_path = ''
        self.text_change = False
        self.selected_text = False

        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.show_menubar()
        self.start_line_number()
        self.show_scrollbar()
        self.show_status()
        self.menu_operation_key_bindings()

    def create_menubar(self):
        menubar = Menu(self)
        return menubar
    
    def create_file_menu(self):
        file = Menu(self, tearoff = False)
        file.add_command(label = "New", accelerator = "Ctrl+N", command = lambda : self.new_file(False))
        file.add_command(label = "Open", accelerator = "Ctrl+O", command = lambda : self.open_file(False))
        file.add_separator()
        file.add_command(label = "Save", accelerator = "Ctrl+S", command = lambda : self.save_file(False))
        file.add_command(label = "Save As", accelerator = "Ctrl+Shift+S", command = self.save_file_as)
        file.add_separator()
        file.add_command(label = "New Window", accelerator = "Ctrl+Alt+W", command = "#")
        file.add_separator()
        file.add_command(label = "Exit", accelerator = "Ctrl+Q", command = self.exit_window)
        self.menubar.add_cascade(label = "File", menu = file)

    def create_edit_menu(self):
        edit = Menu(self, tearoff = False)
        edit.add_command(label = "Undo", accelerator = "Ctrl+Z", command = self.textbox.edit_undo)
        edit.add_command(label = "Redo", accelerator = "Ctrl+Y", command = self.textbox.edit_redo)
        edit.add_separator()
        edit.add_command(label = "Cut", accelerator = "Ctrl+X", command = lambda : self.cut_text(False))
        edit.add_command(label = "Copy", accelerator = "Ctrl+C", command = lambda : self.copy_text(False))
        edit.add_command(label = "Paste", accelerator = "Ctrl+V", command = lambda : self.paste_text(False))
        edit.add_separator()
        edit.add_command(label = "Select All", accelerator = "Ctrl+A", command = lambda : self.select_all(False))
        self.menubar.add_cascade(label = "Edit", menu = edit)

    def create_view_menu(self):
        view = Menu(self, tearoff = False)
        view.add_checkbutton(label = "Zoom In", accelerator = "Ctrl+", command = lambda : self.zoom("plus"))
        view.add_checkbutton(label = "Zoom Out", accelerator = "Ctrl-", command = lambda : self.zoom("minus"))
        view.add_checkbutton(label = "Line Number", variable = self.show_line_number, onvalue = True, offvalue = False)
        # view.add_command(label = "Side Pane", command = "")
        self.menubar.add_cascade(label = "View", menu = view)

    def show_menubar(self):
        self.config(menu = self.menubar)

    def create_textbox(self):
        textbox = Text(self, font = self.textbox_font, spacing1 = 2, spacing2 = 5, spacing3 = 2, wrap = NONE, selectbackground = "green", undo = True, yscrollcommand = self.y_scrollbar.set, xscrollcommand = self.x_scrollbar.set)
        textbox.pack(fill = BOTH, expand = True)
        # textbox.config()
        return textbox
    
    def create_line_number_panel(self):
        linenumber = Text(self, width = 3, padx = 0, state = DISABLED, takefocus = 0, background = 'grey', spacing1 = 2, spacing2 = 5, spacing3 = 2, wrap = NONE, font = ('Lucida console',12,'bold'), bg = "#f1fbeb", fg = "#ae31b4", yscrollcommand = self.y_scrollbar.set)
        linenumber.pack(side = LEFT, fill = Y)
        return linenumber

    def get_linenumber(self):
        output = ""
        row, _ = self.textbox.index(END).split('.')
        for i in range(1, int(row)):
            output = output + str(i) +"\n"
        return output
    
    def update_linenumber(self):
        line_number = self.get_linenumber()
        self.line_number_panel.config(state = "normal")
        self.line_number_panel.delete(0.1, END)
        self.line_number_panel.insert(0.1, line_number)
        self.line_number_panel.config(state = DISABLED)

    def start_line_number(self):
        self.textbox.bind('<Any-KeyPress>', lambda event: self.update_linenumber())

    def create_scroll_bar(self):
        vertical_scrollbar = Scrollbar(self, cursor = "circle")
        vertical_scrollbar.pack(fill = Y, side = RIGHT) 
        
        horizontal_scrollbar = Scrollbar(self, cursor = "circle", orient = HORIZONTAL)
        horizontal_scrollbar.pack(fill = X, side = BOTTOM)

        return vertical_scrollbar, horizontal_scrollbar

    def show_scrollbar(self):
        self.y_scrollbar.config(command = self.multiple_yview)
        self.x_scrollbar.config(command = self.textbox.xview)

    def multiple_yview(self, *args):
        self.textbox.yview(*args)
        self.line_number_panel.yview(*args)

    def create_status_bar(self):
        statusbar = Label(self, text = "Status:", font = ("Lucida Calligraphy", 10), anchor = W)
        statusbar.pack(fill = X, side = BOTTOM)
        return statusbar

    def status_bar_function(self):
        # print(f"is text area modified to show in status bar? = {self.textbox.edit_modified()}")
        if self.textbox.edit_modified():
            self.text_change = True
            content = self.textbox.get(0.0, END)
            words = len(content.split())
            characters = len(content)
            self.status_bar.config(text = f"Words: {words}  Characters: {characters}")
        
        self.textbox.edit_modified(False)

    def show_status(self):
        self.textbox.bind('<<Modified>>', lambda event: self.status_bar_function())


    # adding functionalities to the file menus
    def new_file(self, e):
        self.textbox.delete(0.0, END)
        self.file_path = ''

    def open_file(self, e):
        self.file_path = filedialog.askopenfilename(initialdir = os.getcwd, title = "Open File", filetypes = (('Text File', 'txt'), ('All Files', '*.*')))
        if self.file_path != '':
            file_name = os.path.basename(self.file_path)
            content = open(self.file_path, 'r')
            self.textbox.insert(0.0, content.read())
            self.title(f"{file_name} - DodoPad")
            self.start_line_number()

    def save_file(self, e):
        print(self.file_path)
        if self.file_path == '':
            save_path = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt', filetypes = (('Text File', 'txt'), ('All Files', '*.*')))
            try:
                content = self.textbox.get(0.0, END)
                save_path.write(content)
                save_path.close()
            except AttributeError:
                print(colored("User terminated the save file operation intentionally !!", "red"))
        else:
            content = self.textbox.get(0.0, END)
            file = open(self.file_path, 'w')
            file.write(content)

    def save_file_as(self):
        save_path = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt', filetypes = (('Text File', 'txt'), ('All Files', '*.*')))
        content = self.textbox.get(0.0, END)
        save_path.write(content)
        save_path.close()
        if self.file_path != '': 
            os.remove(self.file_path)

    def exit_window(self):
        if self.text_change == True:
            choice = msg.askyesnocancel(title = "Warning", message = "Do you want to save the file?")
            if choice is True:
                if self.file_path != '':
                    content = self.textbox.get(0.0, END)
                    file = open(self.file_path, 'w')
                    file.write(content)
                    self.destroy()
                else:
                    content = self.textbox.get(0.0, END)
                    save_path = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt', filetypes = (('Text File', 'txt'), ('All Files', '*.*')))
                    save_path.write(content)
                    save_path.close()
                    self.destroy()
            elif choice is False:
                self.destroy()
            else:
                pass
        else:
            self.destroy()

    def run(self):
        self.mainloop()

    # adding functionalities to the edit menu -> undo redo cut copy paste
    def select_all(self, e):
        self.textbox.tag_add('sel', '1.0', 'end')

    def cut_text(self, e):
        if e:
            self.selected_text = self.clipboard_get()
        else:
            if self.textbox.selection_get():
                # get the selected text
                self.selected_text = self.textbox.selection_get()
                # delete the selected text
                self.textbox.delete('sel.first', 'sel.last')
                # append to clipboard
                self.clipboard_append(self.selected_text)

    def copy_text(self, e):
        if e:
            self.selected_text = self.clipboard_get()
        else:
            if self.textbox.selection_get():
                # clear the clipboard
                self.clipboard_clear()
                # get the selected text
                self.selected_text = self.textbox.selection_get()
                # append to clipboard
                self.clipboard_append(self.selected_text)

    def paste_text(self, e):
        if e:
            self.selected_text = self.clipboard_get()
        else:    
            if self.selected_text:
                position = self.textbox.index(INSERT)
                self.textbox.insert(position, self.selected_text)

    # def undo_text(self, e):
    #     pass

    # def redo_text(self, e):
    #     pass

    # adding functionalities to the view menu -> zoom in, zoom out
    def zoom(self, e):
        op_str = e
        print(self.textbox_font)
        if op_str == "plus":
            self.textbox_font[1] += 2
        elif op_str == "minus":
            self.textbox_font[1] -= 2
        else: 
            pass
        self.textbox.config(font = self.textbox_font)

    def menu_operation_key_bindings(self):
        # file menu
        self.bind('<Control-Key-n>', self.new_file)
        self.bind('<Control-Key-o>', self.open_file)
        self.bind('<Control-Key-s>', self.save_file)
        # edit menu
        self.bind('<Control-Key-x>', self.cut_text)
        self.bind('<Control-Key-c>', self.copy_text)
        self.bind('<Control-Key-v>', self.paste_text)
        self.bind('<Control-Key-a>', self.select_all)
        # view menu
        self.bind('<Control-Key-+>', self.zoom)
        self.bind('<Control-Key-->', self.zoom)
        

class Main:
    if __name__ == '__main__':
        win = Dodopad()
        win.run()
