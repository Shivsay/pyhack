import tkinter as tk
import requests
import json
import webbrowser

class HackerNewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HackerNews App")
        self.root.geometry("800x600")

        # Global variables
        self.api_url_top = "https://hacker-news.firebaseio.com/v0/topstories.json"
        self.api_url_new = "https://hacker-news.firebaseio.com/v0/newstories.json"
        self.api_url_item = "https://hacker-news.firebaseio.com/v0/item/{}.json"
        self.story_ids = []
        self.current_page = 1
        self.stories_per_page = 10

        # Widgets
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=("Arial", 12), width=100)
        self.listbox.grid(row=0, column=0, rowspan=5, padx=10, pady=10, sticky="nsew")
        self.listbox.bind("<Double-Button-1>", self.display_comments)

        self.text_widget = tk.Text(root, wrap="word", font=("Arial", 12), width=100)
        self.text_widget.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(root, command=self.text_widget.yview)
        self.scrollbar.grid(row=0, column=2, rowspan=5, sticky="nsew")
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.radio_var = tk.StringVar()
        self.radio_var.set("top")
        self.radio_top = tk.Radiobutton(root, text="Top Stories", variable=self.radio_var, value="top", command=self.update_stories)
        self.radio_top.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.radio_new = tk.Radiobutton(root, text="New Stories", variable=self.radio_var, value="new", command=self.update_stories)
        self.radio_new.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.prev_button = tk.Button(root, text="Previous Page", command=self.prev_page)
        self.prev_button.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.next_button = tk.Button(root, text="Next Page", command=self.next_page)
        self.next_button.grid(row=7, column=1, padx=10, pady=5, sticky="w")


        # Configure grid weights
        for i in range(9):
            root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Initialize the app
        self.update_stories()

    def fetch_stories(self, url):
        response = requests.get(url)
        return json.loads(response.text)

    def fetch_story_details(self, story_id):
        url = self.api_url_item.format(story_id)
        response = requests.get(url)
        return json.loads(response.text)

    def display_stories(self):
        self.listbox.delete(0, tk.END)  # Clear the listbox
        start_index = (self.current_page - 1) * self.stories_per_page
        end_index = start_index + self.stories_per_page
        for story_id in self.story_ids[start_index:end_index]:
            story = self.fetch_story_details(story_id)
            title = story.get("title", "N/A")
            score = story.get("score", "N/A")
            self.listbox.insert(tk.END, f"{title} - Score: {score}")

    def display_comments(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            story_id = self.story_ids[selected_index[0]]
            story = self.fetch_story_details(story_id)
            title = story.get("title", "N/A")
            url = story.get("url", "N/A")

            self.text_widget.delete(1.0, tk.END)  # Clear the text widget
            self.text_widget.insert(tk.END, f"{title}\nURL: {url}\n\n", "bold")


    def _display_comments_recursive(self, story, bar, level=0):
        for comment_id in story.get("kids", []):
            comment = self.fetch_story_details(comment_id)
            author = comment.get("by", "N/A")
            text = comment.get("text", "N/A")
            score = comment.get("score", "N/A")
            indent = " " * (level * 4)
            self.text_widget.insert(tk.END, f"{indent}{author} - Score: {score}\n{text}\n\n", f"level{level}")
            bar.next()
            # Recursively display replies
            self._display_comments_recursive(comment, bar, level + 1)

    def update_stories(self):
        if self.radio_var.get() == "top":
            url = self.api_url_top
        else:
            url = self.api_url_new

        self.story_ids = self.fetch_stories(url)
        self.current_page = 1
        self.display_stories()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_stories()

    def next_page(self):
        total_pages = (len(self.story_ids) + self.stories_per_page - 1) // self.stories_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_stories()


root = tk.Tk()
app = HackerNewsApp(root)
root.mainloop()
