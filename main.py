import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from api_request import CurrencyAPI
from PyQt5 import uic


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi('MainWindow.ui', self)
        self.show()

        self.stackedWidget.setCurrentIndex(0)

        self.username = "admin"
        self.password = "admin"

        self.currency_api = CurrencyAPI('cur_live_6v84QN0JOxhNdbLNq6IPkJhKyDBMejV7R7H7PN9O')
        self.currency_rates = self.currency_api.fetch_currency_rates()
        if self.currency_rates:
            currencies = list(self.currency_rates.keys())
            self.from_currency_box.currentIndexChanged.connect(self.filter_to_currency_box)
            self.from_currency_box.addItems(currencies)

        self.login_button.clicked.connect(self.login)
        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_converter_page)
        self.logout_button.clicked.connect(self.logout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == self.username and password == self.password:
            self.stackedWidget.setCurrentIndex(1)
            self.error_label.setText("")
        else:
            self.error_label.setText("Invalid Username or Password! try(admin : admin)")

    def filter_to_currency_box(self):
        from_currency = self.from_currency_box.currentText()

        self.to_currency_box.clear()

        currencies = [currency for currency in self.currency_rates.keys() if currency != from_currency]
        self.to_currency_box.addItems(currencies)

    def convert_currency(self):
        from_currency = self.from_currency_box.currentText()
        to_currency = self.to_currency_box.currentText()

        try:
            amount = float(self.currency_input.text())
            conversion_rate = self.currency_api.get_conversion_rate(from_currency, to_currency)
            result = round(amount * conversion_rate, 2)
            self.result_label.setText(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        except ValueError:
            self.result_label.setText("Please enter a valid amount!")

    def clear_converter_page(self):
        self.from_currency_box.setCurrentIndex(0)
        self.filter_to_currency_box()
        self.result_label.setText("")
        self.currency_input.clear()

    def logout(self):
        self.stackedWidget.setCurrentIndex(0)
        self.error_label.setText("")
        self.username_input.clear()
        self.password_input.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()