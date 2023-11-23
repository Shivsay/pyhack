from tkinter import *
from tkinter import ttk
import sys
import os


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from pyhack.api.api_helper import getShowStories


class MainGui(ttk.Frame):
    def __init__(self, root, frm):

        self.root = root
        self.frm = frm
        self.i=0

        self.storiesColumns = ('title', 'score')
        self.stories = ttk.Treeview(root, columns=self.storiesColumns,
                                    show='headings')
        self.stories.column('title', width=450)
        self.stories.column('score', width=90, anchor='center',stretch=False)
        self.stories.heading('title', text='Title')
        self.stories.heading('score', text='Score')
        self.stories.grid(row=0, column=0, rowspan=5, padx=10,
                          pady=10, sticky="nsew")




        def changeFrame():
            if self.i % 2 == 0:
                self.frm.tkraise()
            else:
                self.frm.delete(1.0, 'end')
                self.stories.tkraise()
            self.i += 1

        self.btn = ttk.Button(root, text="Change", command=changeFrame).grid(row=1, column=1)
        contents = getShowStories()
        for content in contents:
            self.stories.insert('', 'end', values=(content.title, content.score))


class comments(Text):
    def __init__(self, root):
        super().__init__(root, borderwidth=5)
        self.grid(column=0, row=0, rowspan=5, padx=10, pady=10, sticky="nsew") 
        '''
        self.text = Text(root,wrap="word", font=("Arial", 12))
        self.text.grid(row=0, column=2, rowspan=5, padx=10,
                       pady=10, sticky="nsew")
        '''


class listTree(ttk.Treeview):
    def __init__(self, root):
        self.storiesColumns = ('title', 'score')

        super().__init__(root, columns=self.storiesColumns, show='headings')
        self.column('title', width=450)
        self.column('score', width=90, anchor='center', stretch=False)
        self.heading('title', text='Title')
        self.heading('score', text='Score')
        self.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew") 

        scrollbar = ttk.Scrollbar(root, orient='vertical', command=self.yview)
        self.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')




root = Tk()
root.title("PyHack")

for i in range(1):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)


ffr = ttk.Frame(root, borderwidth=5, relief="sunken").grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
app = MainGui(listTree(root), comments(root))
root.mainloop()
