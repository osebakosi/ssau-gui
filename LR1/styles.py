from constants import (
    COLOR_DARK, COLOR_LIGHT, COLOR_LABEL_BG, COLOR_LABEL_TEXT,
    COLOR_LABEL_BORDER, COLOR_BUTTON, COLOR_BUTTON_HOVER,
    COLOR_BUTTON_PRESSED, BUTTON_MIN_WIDTH, BUTTON_MIN_HEIGHT,
    BUTTON_PADDING, LABEL_PADDING
)

MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 {COLOR_DARK}, stop: 1 {COLOR_LIGHT});
        border-radius: 10px;
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        font-size: 24px;
        font-weight: bold;
        color: {COLOR_LABEL_TEXT};
        background-color: {COLOR_LABEL_BG};
        padding: {LABEL_PADDING};
        border-radius: 10px;
        border: 2px solid {COLOR_LABEL_BORDER};
    }}
"""

BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {COLOR_BUTTON};
        color: white;
        border: none;
        padding: {BUTTON_PADDING};
        font-size: 14px;
        font-weight: bold;
        border-radius: 8px;
        min-width: {BUTTON_MIN_WIDTH}px;
        min-height: {BUTTON_MIN_HEIGHT}px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_BUTTON_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {COLOR_BUTTON_PRESSED};
    }}
"""

