import sys, pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox


from assets.ui.app_ui import Ui_MainWindow
from connect import Form


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.appUI = Ui_MainWindow()
        self.appUI.setupUi(self)
        self.appUI.stackedWidget.setCurrentIndex(0)
        self.appUI.btn_home_2.setChecked(True)

        self.appUI.middle_sidebar_widget.hide()


    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.appUI.middle_sidebar_widget.findChildren(QPushButton) \
                    + self.appUI.full_sidebar_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [4, 4]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_btn_home_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(0)
    
    def on_btn_home_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(0)

    def on_btn_db_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(1)

    def on_btn_db_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(1)

    def on_btn_add_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(2)

    def on_btn_add_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(2)

    def on_btn_settings_1_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(3)

    def on_btn_settings_2_toggled(self):
        self.appUI.stackedWidget.setCurrentIndex(3)

    def on_btn_connect_click(self):
        # self.connect.clicked.connect(self.Form)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("assets/style/app_style.qss", "r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())