"""Модуль сигналов для валюты RUB."""

from PyQt5.QtCore import QObject, pyqtSignal


class RubSignals(QObject):
    """Класс сигналов для изменений RUB."""
    
    rub_changed = pyqtSignal(float)
