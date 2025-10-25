"""Модуль сигналов для валюты EUR."""

from PyQt5.QtCore import QObject, pyqtSignal


class EurSignals(QObject):
    """Класс сигналов для изменений EUR."""
    
    eur_changed = pyqtSignal(float)
