## Main ##
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QListWidgetItem
from PyQt6.QtCore import QLine, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from tkinter import filedialog
from typing import Any
import webbrowser
import utils

github_link = "https://github.com/RodFireProductions/AO3BookmarkDownloader"

class Thread(QThread):
    result = pyqtSignal(bool)
    def __init__(self, app, method, *args):
        super().__init__()
        self.app = app
        self.method = method
        self.args = args
        self.start()

    def run(self):
        res = self.method(self.app, self.args)
        self.result.emit(res)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AO3 Bookmark Downloader")
        self.setWindowIcon(QIcon("icon.ico"))
        uic.loadUi("gui.ui", self)

        ## Initial Set Up ##
        # Auth
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.sessionThread = None

        # Misc
        self.ficScrollBar.setMaximum(self.ficList.count())
        self.ficScrollBar.sliderMoved.connect(self.ficList.setCurrentRow)

        # Settings
        self.folder_path = ""
        self.folderButton.clicked.connect(self.setDownloadFolder)
        self.usernameInput.setPlaceholderText("Username")
        self.passwordInput.setPlaceholderText("Password")

        # Buttons
        self.fetchButton.clicked.connect(self.fetchBookmarks)
        self.githubLink.clicked.connect(self.openGitHub)

    def openGitHub(self):
        webbrowser.open(github_link)

    def addToFicList(self):
        print("todo")

    def setDownloadFolder(self):
        self.folder_path = filedialog.askdirectory()

    def updateStatus(self, message, color):
        self.statusText.setText(message)
        if color == None:
            color = utils.colors["status"]
        self.statusText.setStyleSheet(f"color: {color}")

    def getInputs(self):
        input = { "missing": [], "error": False }
        input["file_type"] = self.fileType.currentText()

        if self.folder_path != "":
            input["folder"] = self.folder_path
        else:
            input["error"] = True
            input["missing"].append("Download Location")

        if self.allRadio.isChecked():
            input["all"] = True
        elif self.leftOffRadio.isChecked():
            input["all"] = False
        else:
            input["error"] = True
            input["missing"].append("Where to Start")

        if self.usernameInput.text() == "":
            input["error"] = True
            input["missing"].append("Username")
        else:
            input["username"] = self.usernameInput.text()

        if self.passwordInput.text() == "":
            input["error"] = True
            input["missing"].append("Password")
        else:
            input["password"] = self.passwordInput.text()
        return input

    def fetchBookmarks(self):
        settings = self.getInputs()
        # if settings["error"]:
        #     self.updateStatus(f"Missing: {settings['missing']}", utils.colors["error"])
        #     return
        self.updateStatus("Authenticating...", None)
        self.sessionThread = Thread(self, utils.startSession, settings)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = App()
    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing app...")
