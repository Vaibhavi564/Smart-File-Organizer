import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QFrame, QProgressBar
)
from PyQt5.QtCore import Qt

class FileOrganizer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart File Organizer PRO")
        self.setGeometry(400, 200, 500, 350)

        self.folder_path = ""

        # Title
        self.title = QLabel("📂 Smart File Organizer", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Folder label
        self.label = QLabel("No folder selected", self)
        self.label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.select_btn = QPushButton("📁 Choose Folder", self)
        self.select_btn.clicked.connect(self.select_folder)

        self.organize_btn = QPushButton("⚡ Organize Files", self)
        self.organize_btn.clicked.connect(self.organize_files)

        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setValue(0)

        # Status
        self.status = QLabel("", self)
        self.status.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.label)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.organize_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        self.setLayout(layout)

        # Dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Segoe UI;
            }
            QPushButton {
                background-color: #4CAF50;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00c853;
            }
        """)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            self.label.setText(self.folder_path)

    def get_unique_name(self, dest):
        base, ext = os.path.splitext(dest)
        i = 1
        while os.path.exists(dest):
            dest = f"{base}_{i}{ext}"
            i += 1
        return dest

    def organize_files(self):
        if not self.folder_path:
            self.status.setText("⚠️ Select folder first!")
            return

        files = os.listdir(self.folder_path)
        total = len(files)
        moved = 0
        skipped = 0

        for i, file in enumerate(files):
            file_path = os.path.join(self.folder_path, file)

            if os.path.isfile(file_path):
                try:
                    if file.endswith((".jpg", ".png", ".jpeg")):
                        dest_folder = os.path.join(self.folder_path, "Images")
                    elif file.endswith(".pdf"):
                        dest_folder = os.path.join(self.folder_path, "PDFs")
                    elif file.endswith(".txt"):
                        dest_folder = os.path.join(self.folder_path, "Text")
                    else:
                        skipped += 1
                        continue

                    os.makedirs(dest_folder, exist_ok=True)

                    dest = os.path.join(dest_folder, file)
                    dest = self.get_unique_name(dest)

                    shutil.move(file_path, dest)
                    moved += 1

                except:
                    skipped += 1

            # Update progress bar
            progress_value = int((i + 1) / total * 100)
            self.progress.setValue(progress_value)

        self.status.setText(f"✅ Moved: {moved} | Skipped: {skipped}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec_())