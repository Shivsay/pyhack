from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import sys
import os
from threading import Thread


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from pyhack.api.api_helper import getShowStories, getC, parseC


class Comments(ScrolledText):
    def __init__(self, root, id):
        super().__init__(root, borderwidth=5)

        self.grid(column=0, row=0, rowspan=5,columnspan=2, padx=10, pady=10, sticky="nsew") 
        self.id = id
        self.insert('end', "This is the heading\n\n\n")
        #self.asyncComment(self.fillComments("", self.id))
        #self.fillComments("", self.id)
        #self.comments = Text(wrap="word", font=("Arial", 12))
        #self.comments.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")

    def asyncComment(self, commentFunc):
        Thread(target=commentFunc).start()
    
    def fillComments(self, level, id):
        comments = getC(id)
        print("\n")
        level += ('\t')
        if comments is not None:
            for comment in comments:
                c = parseC(comment)
                print(level,c)
                self.insert('end', level) 
                self.insert('end', c) 
                self.insert('end',"\n\n")
                root.update()
                self.asyncComment(self.fillComments(level, comment))
        self.insert('end',"-------C------")  
        self.insert('end',"\n") 


class ListTree(ttk.Frame):
    def __init__(self, root, updateWindow_callback):
        super().__init__(root) 

        self.updateWindow_callback = updateWindow_callback
        self.storiesColumns = ('title', 'score')
        self.listTree = ttk.Treeview(columns=self.storiesColumns, show='headings')
        self.listTree.column('title', width=450)
        self.listTree.column('score', width=90, anchor='center', stretch=False)
        self.listTree.heading('title', text='Title')
        self.listTree.heading('score', text='Score')
        self.listTree.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew") 

        scrollbar = ttk.Scrollbar(orient='vertical', command=self.listTree.yview)
        self.listTree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, padx=10, pady=10,sticky='ns')

        contents = getShowStories()
        for content in contents:
            self.listTree.insert('', 'end', iid=content.item_id, values=(content.title, content.score))

        self.listTree.bind('<Double-1>', self.get_selected)
        self.selected = False

    def get_selected(self, event):
        selected = self.listTree.selection()
        self.updateWindow_callback(selected[0])
        return selected[0]

    def selfRaise(self):
        self.tkraise()
        self.listTree.tkraise()


class MainGui(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        print("Created")

        self.frames = {} 
        self.frames[1] = ListTree(root, self.changeFrame)
        self.frames[1].grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")
        self.btn = ttk.Button(root, text="Change", command=self.raiseList).grid(row=1, column=2)

    def raiseList(self):
        print("Raise")
        self.frames[0].destroy() 
        self.frames[1].selfRaise()
        

    def changeFrame(self, id):
        print(id)
        print("ENTER")
        
        self.frames[0]=Comments(root,id)
        self.frames[0].tkraise()
        print("FRAME RAISED??")
        self.frames[0].asyncComment(self.frames[0].fillComments("", id))



root = Tk()
root.title("PyHack")

for i in range(1):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)


app = MainGui(root)
print("Running")
root.mainloop()