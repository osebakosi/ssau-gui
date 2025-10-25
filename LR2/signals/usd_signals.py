"""Модуль сигналов для валюты USD."""

from PyQt5.QtCore import QObject, pyqtSignal


class UsdSignals(QObject):
    """Класс сигналов для изменений USD."""
    
    usd_changed = pyqtSignal(float)
