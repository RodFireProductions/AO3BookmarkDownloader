## Main ##
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6.QtCore import QLine, Qt
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from tkinter import filedialog
import database
# import utils

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AO3 Bookmark Downloader")
        self.setWindowIcon(QIcon("icon.ico"))
        uic.loadUi("gui.ui", self)

        ## Initial Set Up ##
        # Auth
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)

        # Settings
        folder_path = ""
        self.folderButton.clicked.connect(self.setDownloadFolder)

        # Buttons
        self.fetchButton.clicked.connect(self.fetchBookmarks)

    def setDownloadFolder(self):
        self.folder_path = filedialog.askdirectory()

    def updateStatus(self, message):
        self.statusText.setText(message)

    def getInputs(self):
        input = { missing: "", error: False }
        input["file_type"] = self.fileType.currentText()
        # TODO: finish

    def fetchBookmarks(self):
        inputs = self.getInputs()
        if input.error:
            self.updateStatus("Missing : {0}".format(input.missing))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = App()
    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing app...")
