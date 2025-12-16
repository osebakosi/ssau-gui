import sys
from pathlib import Path
from PyQt5.QtCore import QUrl, QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from datetime import *


class Interface(QObject):
    SAVE_DIRECTORY = "saved_canvas"
    TIMER_INTERVAL_MS = 5000
    
    hashPrint = hex(abs(hash(f'{datetime.now()}')))[2:]
    saveRequested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(self.TIMER_INTERVAL_MS)
        
        save_path = Path(self.SAVE_DIRECTORY)
        save_path.mkdir(parents=True, exist_ok=True)
        self.save_dir = str(save_path)
    
    def on_timer_timeout(self):
        self.saveRequested.emit(self.hashPrint) 


if __name__ == '__main__':
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)
    engine.load("mainWindow.qml")

    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    sys.exit(app.exec())
