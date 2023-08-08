import tkinter as tk
from tkinter import filedialog


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.text_area = tk.Text(self.root)
        self.file_path = None

        self.build_ui()

    def build_ui(self):
        self.text_area.pack(fill=tk.BOTH, expand=1)

        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"),
                                                               ("Text Files", "*.txt"),
                                                               ("Python Files", "*.py")])
        if self.file_path:
            print(self.file_path)
            self.text_area.delete(1.0, tk.END)
            with open(self.file_path, "r") as file:
                data = file.read()
                print(data)
                self.text_area.insert(tk.INSERT, data)

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        new_file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("All Files", "*.*"),
                                                                ("Text Files", "*.txt"),
                                                                ("Python Files", "*.py")])
        if new_file_path:
            self.file_path = new_file_path
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()
