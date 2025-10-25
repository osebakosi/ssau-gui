"""Модуль виджета конвертера валют."""

import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl


API_URL = "http://open.er-api.com/v6/latest/USD"


class CurrencyConverterWidget(QWidget):
    """
    Главный виджет для конвертации валют между USD, EUR и RUB.
    
    Предоставляет интерфейс для конвертации между тремя валютами
    и автоматически загружает актуальные курсы с внешнего API.
    """
    
    def __init__(self, usd_signals, eur_signals, rub_signals, common_signals):
        """Инициализация виджета конвертера валют."""
        super().__init__()
        self.usd_signals = usd_signals
        self.eur_signals = eur_signals
        self.rub_signals = rub_signals
        self.common_signals = common_signals
        self.rates = {}
        self.updating = False
        self.network_manager = QNetworkAccessManager()
        
        self.initUI()
        self.setupSignals()
        self.updateRatesFromAPI()

    def initUI(self):
        """Инициализация компонентов интерфейса."""
        self.setWindowTitle('Конвертер валют')

        layout = QVBoxLayout()

        self.usd_label = QLabel('Доллары (USD):')
        self.usd_input = QLineEdit()

        self.eur_label = QLabel('Евро (EUR):')
        self.eur_input = QLineEdit()

        self.rub_label = QLabel('Рубли (RUB):')
        self.rub_input = QLineEdit()

        self.clear_button = QPushButton('Очистить все поля')

        layout.addWidget(self.usd_label)
        layout.addWidget(self.usd_input)
        layout.addWidget(self.eur_label)
        layout.addWidget(self.eur_input)
        layout.addWidget(self.rub_label)
        layout.addWidget(self.rub_input)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    def setupSignals(self):
        """Подключение всех сигналов и слотов."""
        self.usd_signals.usd_changed.connect(self.updateEurRub)
        self.eur_signals.eur_changed.connect(self.updateUsdRub)
        self.rub_signals.rub_changed.connect(self.updateUsdEur)
        
        self.common_signals.clear_all.connect(self.onClearAll)
        self.common_signals.rates_updated.connect(self.onRatesUpdated)

        self.usd_input.textChanged.connect(self.onUsdChanged)
        self.eur_input.textChanged.connect(self.onEurChanged)
        self.rub_input.textChanged.connect(self.onRubChanged)

        self.clear_button.clicked.connect(self.onClearClicked)

    def updateRatesFromAPI(self):
        """Загрузка актуальных курсов валют с API."""
        request = QNetworkRequest(QUrl(API_URL))
        self.network_manager.get(request)
        self.network_manager.finished.connect(self.onAPIResponse)

    def onAPIResponse(self, reply):
        """Обработка ответа API с курсами валют."""
        error = reply.error()
        if error == reply.NoError:
            data = json.loads(reply.readAll().data())
            rates = data.get('rates', {})

            usd_to_eur = rates.get('EUR', 0)
            usd_to_rub = rates.get('RUB', 0)

            eur_to_usd = 1 / usd_to_eur if usd_to_eur else 0
            rub_to_usd = 1 / usd_to_rub if usd_to_rub else 0

            eur_to_rub = usd_to_rub / usd_to_eur if usd_to_eur else 0
            rub_to_eur = 1 / eur_to_rub if eur_to_rub else 0

            self.rates = {
                'usd_to_eur': usd_to_eur,
                'usd_to_rub': usd_to_rub,
                'eur_to_usd': eur_to_usd,
                'eur_to_rub': eur_to_rub,
                'rub_to_usd': rub_to_usd,
                'rub_to_eur': rub_to_eur
            }
            self.common_signals.rates_updated.emit(self.rates)
        else:
            print(f"Ошибка при загрузке курсов: {reply.errorString()}")

    def onRatesUpdated(self, new_rates):
        """Обновление внутренних курсов при получении новых данных."""
        self.rates = new_rates

    def onUsdChanged(self, text):
        """Обработка изменений в поле USD."""
        if self.updating or not self.rates:
            return
        try:
            value = float(text)
        except ValueError:
            return
        self.usd_signals.usd_changed.emit(value)

    def onEurChanged(self, text):
        """Обработка изменений в поле EUR."""
        if self.updating or not self.rates:
            return
        try:
            value = float(text)
        except ValueError:
            return
        self.eur_signals.eur_changed.emit(value)

    def onRubChanged(self, text):
        """Обработка изменений в поле RUB."""
        if self.updating or not self.rates:
            return
        try:
            value = float(text)
        except ValueError:
            return
        self.rub_signals.rub_changed.emit(value)

    def updateEurRub(self, usd_value):
        """Обновление полей EUR и RUB на основе значения USD."""
        if self.updating or not self.rates:
            return
        self.updating = True
        eur = usd_value * self.rates['usd_to_eur']
        rub = usd_value * self.rates['usd_to_rub']
        self.eur_input.setText(f"{eur:.2f}")
        self.rub_input.setText(f"{rub:.2f}")
        self.updating = False

    def updateUsdRub(self, eur_value):
        """Обновление полей USD и RUB на основе значения EUR."""
        if self.updating or not self.rates:
            return
        self.updating = True
        usd = eur_value * self.rates['eur_to_usd']
        rub = eur_value * self.rates['eur_to_rub']
        self.usd_input.setText(f"{usd:.2f}")
        self.rub_input.setText(f"{rub:.2f}")
        self.updating = False

    def updateUsdEur(self, rub_value):
        """Обновление полей USD и EUR на основе значения RUB."""
        if self.updating or not self.rates:
            return
        self.updating = True
        usd = rub_value * self.rates['rub_to_usd']
        eur = rub_value * self.rates['rub_to_eur']
        self.usd_input.setText(f"{usd:.2f}")
        self.eur_input.setText(f"{eur:.2f}")
        self.updating = False

    def onClearAll(self):
        """Очистка всех полей ввода."""
        self.updating = True
        self.usd_input.clear()
        self.eur_input.clear()
        self.rub_input.clear()
        self.updating = False

    def onClearClicked(self):
        """Обработка нажатия кнопки очистки."""
        self.common_signals.clear_all.emit()
