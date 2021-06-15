from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
# from pytoggle import PyToggle
from main5 import Ui_handler
from parse_function import add_to_db, request_to_db, accounts_have
# import datetime
import logging



log = logging.getLogger('user')
log.setLevel(logging.INFO)
fh = logging.FileHandler('logs/logs.log', 'a', 'utf-8')
formatter = logging.Formatter(f"%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
log.addHandler(fh)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_handler()
        self.ui.setupUi(self)

        self.rightMenuIsOpened = False
        self.leftMenuIsOpened = False
        self.ui.pls_wait_msg.hide()


        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.toggle_positions()
        self.btn_functions()
        self.set_info_about_sales()
        self.ui.csgo_check.setChecked(False)
        self.show()

    def btn_functions(self):
        self.ui.btnSell.clicked.connect(self.start_animate_right_menu)
        self.ui.btnClose.clicked.connect(self.close_app)
        self.ui.btnAdd.clicked.connect(self.start_animate_left_menu)
        self.ui.btnAddToDB.clicked.connect(self.prepare_to_add_to_db)
        self.ui.btn_req.clicked.connect(self.request_to_db)
        self.ui.btnRefresh.clicked.connect(self.set_info_about_sales)
        self.ui.btn_clear.clicked.connect(self.clear_area)

    def close_app(self):
        log.info('App was closed')
        self.close()

    def clear_area(self):
        self.ui.rtrn_link.setText('')
        self.ui.rtrn_login.setText('')
        self.ui.rtrn_pass.setText('')
        self.ui.gamesLine.setText('')
        self.ui.levelLine.setText('')
        self.ui.csgo_check.setChecked(False)
        self.ui.dayz_check.setChecked(False)
        self.ui.pubg_check.setChecked(False)
        self.ui.rust_check.setChecked(False)
        self.ui.vac_check.setChecked(False)
        self.ui.r6_check.setChecked(False)

    def set_info_about_sales(self):
        self.accounts_have, self.accounts_sold, self.last_sale = accounts_have()
        self.ui.labelLastSale.setText(f'Last sale was at: {self.last_sale[0]}')
        self.ui.labelLeft.setText(f'Accounts left: {self.accounts_have}')
        self.ui.labelSold.setText(f'Accounts sold: {self.accounts_sold}')


    def request_to_db(self):
        self.ui.error_msg.setText('ERROR')
        self.account_link = self.ui.rtrn_link.text().strip()
        self.account_login = self.ui.rtrn_login.text().strip()
        self.account_password = self.ui.rtrn_pass.text().strip()
        self.games_count = self.ui.gamesLine.text().strip()
        self.account_level = self.ui.levelLine.text().strip()
        self.dayz = self.ui.dayz_check.isChecked()
        self.rust = self.ui.rust_check.isChecked()
        self.pubg = self.ui.pubg_check.isChecked()
        self.r6 = self.ui.r6_check.isChecked()
        self.csgo = self.ui.csgo_check.isChecked()
        self.get_banned = self.ui.vac_check.isChecked()
        self.result = request_to_db(account_link=self.account_link,
                                    login=self.account_login,
                                    password=self.account_password,
                                    games_count=self.games_count,
                                    lvl=self.account_level,
                                    dayz=self.dayz,
                                    rust=self.rust,
                                    pubg=self.pubg,
                                    r6=self.r6,
                                    csgo=self.csgo,
                                    get_banned=self.get_banned)

        print(self.result)
        if self.result == 404:
            log.info("""
            ACCOUNT WAS NOT GOT!
            ERROR
                """)
            self.clear_area()
            self.start_animate_error_msg()
        elif self.result == 405:
            log.info("""
            ACCOUNT WAS NOT GOT!
            ALL ACCOUNTS WERE SOLD
            """)
            self.clear_area()
            self.ui.error_msg.setText('ALL ACCOUNTS WERE SOLD')
            self.start_animate_error_msg()
        else:
            if self.result[0] == 0:
                self.ui.rtrn_link.setText(self.result[1][0][5])
                self.ui.rtrn_login.setText(self.result[1][0][6])
                self.ui.rtrn_pass.setText(self.result[1][0][7])
                self.ui.gamesLine.setText(str(self.result[1][0][8]))
                self.ui.levelLine.setText(str(self.result[1][0][9]))
            elif self.result[0] == 1:
                self.ui.rtrn_login.setText(self.result[1][0][5])
                self.ui.rtrn_pass.setText(self.result[1][0][6])
                self.ui.gamesLine.setText(str(self.result[1][0][8]))
                self.ui.levelLine.setText(str(self.result[1][0][9]))
            elif self.result[0] == 2:
                self.ui.rtrn_pass.setText(self.result[1][0][5])
                self.ui.gamesLine.setText(str(self.result[1][0][7]))
                self.ui.levelLine.setText(str(self.result[1][0][8]))
            elif self.result[0] == 3:
                self.ui.rtrn_login.setText(self.result[1][0][5])
                self.ui.gamesLine.setText(str(self.result[1][0][6]))
                self.ui.levelLine.setText(str(self.result[1][0][7]))
            elif self.result[0] == 4:
                self.ui.rtrn_link.setText(self.result[1][0][5])
                self.ui.rtrn_pass.setText(self.result[1][0][6])
                self.ui.gamesLine.setText(str(self.result[1][0][8]))
                self.ui.levelLine.setText(str(self.result[1][0][9]))
            elif self.result[0] == 5:
                self.ui.rtrn_link.setText(self.result[1][0][5])
                self.ui.gamesLine.setText(str(self.result[1][0][7]))
                self.ui.levelLine.setText(str(self.result[1][0][8]))
            if self.result[1][0][0] == 1:
                self.ui.r6_check.setChecked(True)
            if self.result[1][0][1] == 1:
                self.ui.csgo_check.setChecked(True)
            if self.result[1][0][2] == 1:
                self.ui.pubg_check.setChecked(True)
            if self.result[1][0][3] == 1:
                self.ui.rust_check.setChecked(True)
            if self.result[1][0][4] == 1:
                self.ui.dayz_check.setChecked(True)
            self.set_info_about_sales()
            log.info(f"""
            ACCOUNT WAS GOT SUCCESSFULLY!
            login: {self.ui.rtrn_login.text()},
            password: {self.ui.rtrn_pass.text()},
            link: {self.ui.rtrn_link.text()}
            """)

    def prepare_to_add_to_db(self):
        self.ui.pls_wait_msg.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_to_db)
        self.timer.start(100)

    def add_to_db(self):
        self.timer.stop()
        self.account_link = self.ui.linkLine.text()
        self.account_login = self.ui.loginLine.text()
        self.account_password = self.ui.passLine.text()

        if self.account_login.strip() == '':
            self.start_animate_unsuccess_msg()
            log.info(f"""
                    Account WASNT ADDED
                    login: {self.account_login},
                    password: {self.account_password}
                    link: {self.account_link}
                """)
        elif self.account_password.strip() == '':
            self.start_animate_unsuccess_msg()
            log.info(f"""
                     Account WASNT ADDED
                    login: {self.account_login},
                    password: {self.account_password}
                    link: {self.account_link}
                """)
        else:
            try:
                add_to_db(login = self.account_login, password = self.account_password, account_link = self.account_link)
                self.start_animate_success_msg()
                self.set_info_about_sales()
                log.info(log.info(f"""
            Account SUCCESSFULLY ADDED!
            login: {self.account_login},
            password: {self.account_password}
            link: {self.account_link}
            """))
            except Exception as exc:
                print(exc)
                self.start_animate_unsuccess_msg()
                log.info(f"""
                        Account WASNT ADDED
                        login: {self.account_login},
                        password: {self.account_password}
                        link: {self.account_link}
                        """)

    def start_animate_right_menu(self):
        self.animation = QPropertyAnimation(self.ui.rightMenu, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.setDuration(700)

        if self.rightMenuIsOpened:
            self.animation.setStartValue(QRect(54, 65, 730, 520))
            self.animation.setEndValue(QRect(745, 65, 40, 520))
            self.rightMenuIsOpened = False
        else:
            self.animation.setStartValue(QRect(745, 65, 40, 520))
            self.animation.setEndValue(QRect(54, 65, 730, 520))
            self.rightMenuIsOpened = True

        self.animation.start()

    def start_animate_left_menu(self):
        self.animation = QPropertyAnimation(self.ui.leftMenu, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.setDuration(700)

        if self.leftMenuIsOpened:
            self.animation.setStartValue(QRect(15, 65, 730, 520))
            self.animation.setEndValue(QRect(15, 65, 40, 520))
            self.leftMenuIsOpened = False
        else:
            self.animation.setStartValue(QRect(15, 65, 40, 520))
            self.animation.setEndValue(QRect(15, 65, 730, 520))
            self.leftMenuIsOpened = True

        self.animation.start()

    def start_animate_error_msg(self):
        self.animation = QPropertyAnimation(self.ui.error_msg, b'geometry')
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(500)
        self.animation.setStartValue(QRect(160, -35, 400, 35))
        self.animation.setEndValue(QRect(160, 0, 400, 35))
        self.timer = QTimer()
        self.timer.timeout.connect(self.stop_animate_error_msg)
        self.timer.start(3500)
        self.animation.start()


    def stop_animate_error_msg(self):
        self.animation = QPropertyAnimation(self.ui.error_msg, b'geometry')
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(400)
        self.animation.setStartValue(QRect(160, 0, 400, 35))
        self.animation.setEndValue(QRect(160, -35, 400, 35))
        self.timer.stop()
        self.animation.start()

    def start_animate_success_msg(self):
        self.animation = QPropertyAnimation(self.ui.successMsg, b'geometry')
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(700)
        self.animation.setStartValue(QRect(120, 520, 510, 60))
        self.animation.setEndValue(QRect(120, 459, 510, 60))
        self.timer = QTimer()
        self.timer.timeout.connect(self.stop_animate_success_msg)
        self.timer.start(3500)
        self.ui.pls_wait_msg.hide()
        self.animation.start()

    def stop_animate_success_msg(self):
        self.animation = QPropertyAnimation(self.ui.successMsg, b'geometry')
        self.animation.setDuration(500)
        self.animation.setStartValue(QRect(120, 459, 510, 60))
        self.animation.setEndValue(QRect(120, 520, 510, 60))
        self.timer.stop()
        self.animation.start()

    def start_animate_unsuccess_msg(self):
        self.animation = QPropertyAnimation(self.ui.unsuccessMsg, b'geometry')
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(700)
        self.animation.setStartValue(QRect(170, 520, 421, 61))
        self.animation.setEndValue(QRect(170, 459, 421, 61))
        self.timer = QTimer()
        self.timer.timeout.connect(self.stop_animate_unsuccess_msg)
        self.timer.start(3500)
        self.ui.pls_wait_msg.hide()
        self.animation.start()

    def stop_animate_unsuccess_msg(self):
        self.animation = QPropertyAnimation(self.ui.unsuccessMsg, b'geometry')
        self.animation.setDuration(500)
        self.animation.setStartValue(QRect(170, 459, 421, 61))
        self.animation.setEndValue(QRect(170, 520, 421, 61))
        self.timer.stop()
        self.animation.start()


    def toggle_positions(self):
        self.ui.dayz_check.setGeometry(QRect(115, 345, 61, 20))
        self.ui.rust_check.setGeometry(QRect(205, 345, 51, 21))
        self.ui.pubg_check.setGeometry(QRect(290, 345, 51, 21))
        self.ui.r6_check.setGeometry(QRect(368, 345, 51, 21))
        self.ui.csgo_check.setGeometry(QRect(438, 345, 41, 21))
        self.ui.vac_check.setGeometry(QRect(512, 345, 41, 21))


if __name__ == '__main__':
    log.info('APP IS ACTIVE')
    app = QApplication(sys.argv)
    win = MainWindow()

    sys.exit(app.exec_())

