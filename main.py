# main
import sys
from PyQt6.QtWidgets import QApplication
from ui_module import CalculatorApp # UI 파일연결

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = CalculatorApp()
    dlg.show()
    sys.exit(app.exec())