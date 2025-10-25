"""
Приложение на PyQt5 для конвертации между валютами USD, EUR и RUB
с использованием актуальных курсов валют из внешнего API.
"""

import sys
from PyQt5.QtWidgets import QApplication

from signals import UsdSignals, EurSignals, RubSignals, CommonSignals
from widgets import CurrencyConverterWidget


def main():
    """Точка входа в приложение конвертера валют."""
    app = QApplication(sys.argv)

    # Создание экземпляров сигналов
    usd_signals = UsdSignals()
    eur_signals = EurSignals()
    rub_signals = RubSignals()
    common_signals = CommonSignals()

    # Создание и отображение главного виджета
    converter = CurrencyConverterWidget(
        usd_signals, 
        eur_signals, 
        rub_signals, 
        common_signals
    )
    converter.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
