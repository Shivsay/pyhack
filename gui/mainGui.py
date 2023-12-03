from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import sys
import os
from threading import Thread


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from pyhack.api.api_helper import getTop, getTopStories, getShowStories, getNewStories, getJobStories, getComments, parseComment


class Comments(ScrolledText):
    def __init__(self, root, id):
        super().__init__(root, borderwidth=5)

        self.grid(column=0, row=0, rowspan=5,columnspan=2, padx=10, pady=10, sticky="nsew") 
        self.id = id
        self.content = getTop(id)
        self.insert('end',self.content[0])
        self.insert('end',"\n=======COMMENTS=======")
        self.insert('end',"\n\n\n")
        #self.comments = Text(wrap="word", font=("Arial", 12))
        #self.comments.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")

    def asyncComment(self, commentFunc):
        Thread(target=commentFunc).start()
    
    def fillComments(self, level, id):
        comments = getComments(id)
        level += ('\t')
        if comments is not None:
            for comment in comments:
                c = parseComment(comment)
                self.insert('end', level) 
                self.insert('end', c) 
                self.insert('end',"\n\n")
                root.update()
                self.asyncComment(self.fillComments(level, comment))
        # self.insert('end',"-------C------")  
        self.insert('end',"\n") 


class ListTree(ttk.Frame):
    def __init__(self, root, updateWindow_callback, contentFunction_callback):
        super().__init__(root) 

        self.updateWindow_callback = updateWindow_callback
        self.storiesColumns = ('title', 'score')
        self.listTree = ttk.Treeview(columns=self.storiesColumns, show='headings')
        self.listTree.column('title', width=450)
        self.listTree.column('score', width=90, anchor='center', stretch=False)
        self.listTree.heading('title', text='Title')
        self.listTree.heading('score', text='Score')
        self.listTree.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew") 
        self.contentFunction = contentFunction_callback

        scrollbar = ttk.Scrollbar(orient='vertical', command=self.listTree.yview)
        self.listTree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, rowspan=4, padx=10, pady=10,sticky='ns')

        contents = contentFunction_callback
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
        print("Created Main")

        self.listTypeFunction = getShowStories()

        self.frames = {} 
        self.frames[1] = ListTree(root, self.changeFrame, self.listTypeFunction)
        self.frames[1].grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")
        
        self.topStoriesBtn = ttk.Button(root, text="Top", command=lambda: self.changeType(getTopStories()))
        self.topStoriesBtn.grid(row=0,column=2,pady=10)

        self.showStoriesBtn = ttk.Button(root, text="ShowHN", command=lambda: self.changeType(getShowStories()))
        self.showStoriesBtn.grid(row=1,column=2,pady=10) 

        self.newStoriesBtn = ttk.Button(root, text="New",command=lambda: self.changeType(getNewStories()))
        self.newStoriesBtn.grid(row=2,column=2,pady=10)

        self.jobStoriesBtn = ttk.Button(root, text="Job", command=lambda: self.changeType(getJobStories()))
        self.jobStoriesBtn.grid(row=3,column=2,pady=10)

        self.backBtn = ttk.Button(root, text="Back", command=self.raiseList, state=DISABLED)
        self.backBtn.grid(row=5, column=2, pady=10)

    def changeType(self, item):
        print("Changed type");
        self.frames[1].destroy() 
        self.frames[1] = ListTree(root, self.changeFrame, item)
        self.frames[1].selfRaise()

    def raiseList(self):
        print("Destroy Content")
        self.frames[0].destroy() 
        self.backBtn['state'] = DISABLED

        self.topStoriesBtn['state'] = NORMAL 
        self.showStoriesBtn['state'] = NORMAL
        self.newStoriesBtn['state'] = NORMAL
        self.jobStoriesBtn['state'] = NORMAL
        self.frames[1].selfRaise()
        

    def changeFrame(self, id):
        print(id)
        print("ENTER")
        self.topStoriesBtn['state'] = DISABLED
        self.showStoriesBtn['state'] = DISABLED
        self.newStoriesBtn['state'] = DISABLED
        self.jobStoriesBtn['state'] = DISABLED
        
        self.frames[0]=Comments(root,id)
        self.frames[0].tkraise()
        self.backBtn['state'] = NORMAL
        print("Expand Content")
        self.frames[0].asyncComment(self.frames[0].fillComments("", id))



root = Tk()
root.title("PyHack")

# Grid setup
for i in range(5):
    root.grid_rowconfigure(i, weight=0)
root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)


app = MainGui(root)
print("Running")
root.mainloop()
