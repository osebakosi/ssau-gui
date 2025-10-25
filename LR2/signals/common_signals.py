"""Модуль общих сигналов для конвертера валют."""

from PyQt5.QtCore import QObject, pyqtSignal


class CommonSignals(QObject):
    """Класс общих сигналов приложения."""
    
    clear_all = pyqtSignal()
    rates_updated = pyqtSignal(dict)
