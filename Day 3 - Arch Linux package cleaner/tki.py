import os
import tkinter as tk

from cleaner import Package, start_list, start_clean, clean_packages


"""
Checkbutton example

- Create an app with a single checkbox
- Change window on button press
- Print out the contents in the next window and console

Resources:
- https://tkdocs.com/tutorial/widgets.html#checkbutton
- https://stackoverflow.com/questions/34764598/tkinter-window-navigation-inside-a-gui
- https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
- https://stackoverflow.com/questions/8536518/how-do-i-create-multiple-checkboxes-from-a-list-in-a-for-loop-in-python-tkinter
- https://stackoverflow.com/questions/54101561/tkinter-gui-overlapping-or-refreshing-labels-from-a-list
"""


class CleanerApp(tk.Tk):
    packages: list[Package] = None
    to_process: list[str] = None

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.current_frame = None

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        cls = globals()[page_name]
        self.current_frame = cls(self.container, self)
        self.current_frame.pack(fill="both", expand=True)


class StartPage(tk.Frame):
    """Class representing the start page."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Find packages!")
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(
            self,
            text="List all packages",
            command=lambda: self.show_package_page("list")
        )
        button.pack()

    def show_package_page(self, command):
        # scope = cleaner.create_scope("all")

        if command == "list":
            self.controller.packages = start_list(["/usr/bin"])

        elif command == "clean":
            self.controller.packages = start_clean("")

        self.controller.show_frame("PackagePage")


class PackagePage(tk.Frame):
    """Page consisting of all found packages"""
    checkboxes = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Here are all the packages")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(
            self,
            text="Go back",
            command=lambda: controller.show_frame("StartPage")
        )
        button.pack()
        self.list_gathered_packaged()
        button = tk.Button(
            self,
            text="Submit",
            command=lambda: self.navigate_to_confirmation()
        )
        button.pack()

    def create_scrollable_frame(self):
        wrapper = tk.LabelFrame(self)

        canvas = tk.Canvas(
            wrapper,
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        scrollbar = tk.Scrollbar(
            wrapper,
            orient=tk.VERTICAL,
            command=canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        wrapper.pack(
            fill=tk.BOTH,
            expand=tk.YES
        )
        return frame

    def create_scrollable_text_frame(self):
        frame = self.create_scrollable_frame()
        text = tk.Text(frame, cursor="arrow")
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        return text

    def list_gathered_packaged(self):
        """LIst packages gathered"""
        if self.controller.packages is None:
            return 0

        text = self.create_scrollable_text_frame()

        for package in self.controller.packages:
            state = tk.IntVar()
            location = package.location
            cb = tk.Checkbutton(
                text,
                text=package.name,
                justify=tk.LEFT,
                bg="white",
                variable=state
            )
            self.checkboxes.append([cb, state, location])
            text.window_create(tk.END, window=cb)
            text.insert(tk.END, "\n")

    def print_checkbox_state(self):
        full_paths = []

        for checkbox in self.checkboxes:
            checkbox, state, location = checkbox
            if state.get():
                full_paths.append(
                    os.path.join(
                        location, checkbox.cget("text")
                    )
                )

        return full_paths

    def navigate_to_confirmation(self):
        self.controller.to_process = self.print_checkbox_state()
        self.checkboxes = None
        self.controller.show_frame("ConfirmationPage")


class ConfirmationPage(tk.Frame):
    """Class representing the start page."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Clean all selected packages?")
        label.pack(side="top", fill="x", pady=10)

        confirm_button = tk.Button(
            self,
            text="Clean",
            command=lambda: self.process_packages()
        )
        confirm_button.pack()

        quit_button = tk.Button(
            self,
            text="Quit",
            command=lambda: app.destroy()
        )
        quit_button.pack()

    def process_packages(self):
        to_process = self.controller.to_process

        self.controller.checkboxes = None
        self.controller.to_process = None

        clean_packages(to_process)


if __name__ == "__main__":
    app = CleanerApp()
    app.mainloop()

