from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os
import shutil


class FileOrganizer(Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart File Organizer")
        self.geometry("700x550")
        self.resizable(False, False)

        self.folder_path = ""

        Label(
            self,
            text="Smart File Organizer",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        frame = Frame(self)
        frame.pack(pady=10)

        self.path_entry = Entry(frame, width=60)
        self.path_entry.grid(row=0, column=0, padx=5)

        Button(
            frame,
            text="Browse",
            command=self.select_folder
        ).grid(row=0, column=1)

        Button(
            self,
            text="Start Organizing",
            bg="green",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.organize_files
        ).pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=550,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.progress_label = Label(
            self,
            text="0%",
            font=("Arial", 10)
        )
        self.progress_label.pack()

        self.status = Label(
            self,
            text="Waiting...",
            font=("Arial", 10, "italic")
        )
        self.status.pack(pady=5)

        # Log Box
        self.log = Text(self, width=80, height=18)
        self.log.pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.folder_path = folder
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, folder)

    def organize_files(self):

        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder.")
            return

        file_types = {
            ".png": "Images",
            ".jpg": "Images",
            ".jpeg": "Images",
            ".gif": "Images",

            ".txt": "Text Files",
            ".pdf": "PDF Files",
            ".docx": "Documents",
            ".doc": "Documents",

            ".mp3": "Music",
            ".wav": "Music",

            ".mp4": "Videos",
            ".avi": "Videos",
            ".mkv": "Videos",

            ".py": "Python Files",
            ".cpp": "C++ Files",
            ".c": "C Files",
            ".java": "Java Files",

            ".zip": "Archives",
            ".rar": "Archives"
        }

        files = [
            f for f in os.listdir(self.folder_path)
            if os.path.isfile(os.path.join(self.folder_path, f))
        ]

        if len(files) == 0:
            messagebox.showinfo("Info", "Folder is empty!")
            return

        self.progress["maximum"] = len(files)
        self.progress["value"] = 0

        self.log.delete(1.0, END)

        moved = 0

        try:
            for index, file in enumerate(files, start=1):

                full_path = os.path.join(self.folder_path, file)

                extension = os.path.splitext(file)[1].lower()

                folder = file_types.get(extension, "Others")

                destination = os.path.join(self.folder_path, folder)

                os.makedirs(destination, exist_ok=True)

                shutil.move(full_path, os.path.join(destination, file))

                moved += 1

                self.log.insert(
                    END,
                    f"✔ {file}  →  {folder}\n"
                )

                self.progress["value"] = index

                percent = int((index / len(files)) * 100)

                self.progress_label.config(text=f"{percent}% Completed")

                self.status.config(text=f"Organizing : {file}")

                self.update_idletasks()

            self.status.config(text="✔ File organization completed successfully!")

            self.log.insert(
                END,
                f"\n\nTotal Files Organized : {moved}"
            )

            messagebox.showinfo(
                "Success",
                f"Successfully organized {moved} files."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = FileOrganizer()
    app.mainloop()