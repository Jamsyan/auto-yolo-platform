import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine,QQmlComponent

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
file = Path('ui.qml').resolve()
engine.load(file)
sys.exit(app.exec())