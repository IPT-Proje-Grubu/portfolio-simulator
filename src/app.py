import sys

from PyQt6.QtWidgets import QApplication

from src.portfolio import PortfolioState
from src.ui import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Portfolio Simulator")

    state = PortfolioState()
    window = MainWindow(state)
    window.show()

    return app.exec()
