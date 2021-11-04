import tkinter as tk

"""
Practice example from Official Python docs (https://docs.python.org/3/library/tkinter.html)

- Create an app with a single entry field
- Print out the contents in the terminal
"""


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.entry = tk.Entry()
        self.entry.pack()

        self.contents = tk.StringVar()
        self.entry["textvariable"] = self.contents

        self.entry.bind(
            '<Key-Return>',
            self.print_contents
        )

    def print_contents(self, event):
        print(
            "Hi. The content is:\n",
            self.contents.get()
        )


app = App(tk.Tk())
app.mainloop()

