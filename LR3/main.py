import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QComboBox, QTabWidget,
                             QTableView, QMessageBox, QMenuBar, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction


class DatabaseManager:
    """Класс для управления подключением и запросами к SQLite БД"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self, db_name='database.db'):
        """Установить соединение с БД"""
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_test_data()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка подключения к БД: {e}")
            return False
    
    def create_test_data(self):
        """Создать тестовые таблицы и данные"""
        try:
            # Создание таблицы users
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER
                )
            ''')
            
            # Создание таблицы products
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    price REAL,
                    category TEXT
                )
            ''')
            
            # Проверка, есть ли данные
            self.cursor.execute('SELECT COUNT(*) FROM users')
            if self.cursor.fetchone()[0] == 0:
                # Вставка тестовых данных в users
                users_data = [
                    ('Иван Иванов', 'ivan@example.com', 25),
                    ('Мария Петрова', 'maria@example.com', 30),
                    ('Алексей Сидоров', 'alexey@example.com', 28),
                    ('Елена Смирнова', 'elena@example.com', 22),
                    ('Дмитрий Козлов', 'dmitry@example.com', 35)
                ]
                self.cursor.executemany(
                    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                    users_data
                )
            
            # Проверка, есть ли данные в products
            self.cursor.execute('SELECT COUNT(*) FROM products')
            if self.cursor.fetchone()[0] == 0:
                # Вставка тестовых данных в products
                products_data = [
                    ('Ноутбук', 45000.00, 'Электроника'),
                    ('Мышь', 500.00, 'Электроника'),
                    ('Клавиатура', 1500.00, 'Электроника'),
                    ('Монитор', 15000.00, 'Электроника'),
                    ('Книга Python', 800.00, 'Книги')
                ]
                self.cursor.executemany(
                    'INSERT INTO products (product_name, price, category) VALUES (?, ?, ?)',
                    products_data
                )
            
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка создания тестовых данных: {e}")
    
    def execute_query(self, query):
        """Выполнить SQL запрос и вернуть результаты"""
        try:
            self.cursor.execute(query)
            columns = [description[0] for description in self.cursor.description]
            rows = self.cursor.fetchall()
            return columns, rows
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None, None
    
    def get_column_names(self, table_name):
        """Получить имена колонок из таблицы"""
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in self.cursor.fetchall()]
            return columns
        except sqlite3.Error as e:
            print(f"Ошибка получения колонок: {e}")
            return []
    
    def close(self):
        """Закрыть соединение с БД"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.is_connected = False
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle('PyQt + SQL Application')
        self.setGeometry(100, 100, 900, 600)
        
        # Создание меню
        self.create_menu()
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Панель с кнопками и ComboBox
        controls_layout = QHBoxLayout()
        
        # Кнопка bt1
        self.bt1 = QPushButton('bt1 "SELECT Column"')
        self.bt1.clicked.connect(self.on_bt1_clicked)
        self.bt1.setEnabled(False)
        controls_layout.addWidget(self.bt1)
        
        # QComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItem('QComboBox "Colums"')
        self.combo_box.currentTextChanged.connect(self.on_combo_changed)
        self.combo_box.setEnabled(False)
        controls_layout.addWidget(self.combo_box)
        
        main_layout.addLayout(controls_layout)
        
        # Вторая строка с кнопками
        buttons_layout = QHBoxLayout()
        
        # Кнопка bt2
        self.bt2 = QPushButton('bt2 "Query2"')
        self.bt2.clicked.connect(self.on_bt2_clicked)
        self.bt2.setEnabled(False)
        buttons_layout.addWidget(self.bt2)
        
        # Кнопка bt3
        self.bt3 = QPushButton('bt3 "Query3"')
        self.bt3.clicked.connect(self.on_bt3_clicked)
        self.bt3.setEnabled(False)
        buttons_layout.addWidget(self.bt3)
        
        main_layout.addLayout(buttons_layout)
        
        # QTabWidget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Словарь для хранения вкладок
        self.tabs = {}
    
    def create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()
        
        # Меню
        menu = menubar.addMenu('Menu')
        
        # Set connection
        set_connection_action = QAction('Set connection', self)
        set_connection_action.triggered.connect(self.set_connection)
        menu.addAction(set_connection_action)
        
        # Close connection
        close_connection_action = QAction('Close connection', self)
        close_connection_action.triggered.connect(self.close_connection)
        menu.addAction(close_connection_action)
    
    def set_connection(self):
        """Установить соединение с БД"""
        if self.is_connected:
            QMessageBox.information(self, 'Информация', 'Соединение уже установлено')
            return
        
        if self.db_manager.connect():
            self.is_connected = True
            
            # Активировать кнопки
            self.bt1.setEnabled(True)
            self.bt2.setEnabled(True)
            self.bt3.setEnabled(True)
            self.combo_box.setEnabled(True)
            
            # Заполнить ComboBox колонками из таблицы users
            columns = self.db_manager.get_column_names('users')
            self.combo_box.clear()
            self.combo_box.addItem('QComboBox "Colums"')
            for column in columns:
                self.combo_box.addItem(column)
            
            # Выполнить запрос для Tab1
            self.create_tab('Tab1', 'SELECT * FROM sqlite_master')
            
            QMessageBox.information(self, 'Успех', 'Соединение с БД установлено')
        else:
            QMessageBox.critical(self, 'Ошибка', 'Не удалось подключиться к БД')
    
    def close_connection(self):
        """Закрыть соединение с БД"""
        if not self.is_connected:
            QMessageBox.information(self, 'Информация', 'Соединение не установлено')
            return
        
        # Закрыть соединение
        self.db_manager.close()
        self.is_connected = False
        
        # Деактивировать кнопки
        self.bt1.setEnabled(False)
        self.bt2.setEnabled(False)
        self.bt3.setEnabled(False)
        self.combo_box.setEnabled(False)
        
        # Очистить все вкладки
        self.tab_widget.clear()
        self.tabs.clear()
        
        # Очистить ComboBox
        self.combo_box.clear()
        self.combo_box.addItem('QComboBox "Colums"')
        
        QMessageBox.information(self, 'Успех', 'Соединение с БД закрыто')
    
    def create_tab(self, tab_name, query):
        """Создать или обновить вкладку с результатами запроса"""
        columns, rows = self.db_manager.execute_query(query)
        
        if columns is None or rows is None:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка выполнения запроса для {tab_name}')
            return
        
        # Создать модель для таблицы
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(columns)
        
        # Заполнить модель данными
        for row in rows:
            items = [QStandardItem(str(cell)) for cell in row]
            model.appendRow(items)
        
        # Создать или обновить вкладку
        if tab_name in self.tabs:
            # Обновить существующую вкладку
            table_view = self.tabs[tab_name]
            table_view.setModel(model)
        else:
            # Создать новую вкладку
            table_view = QTableView()
            table_view.setModel(model)
            table_view.resizeColumnsToContents()
            
            self.tab_widget.addTab(table_view, tab_name)
            self.tabs[tab_name] = table_view
    
    def on_bt1_clicked(self):
        """Обработчик нажатия кнопки bt1"""
        self.create_tab('Tab2', 'SELECT name FROM sqlite_master')
    
    def on_bt2_clicked(self):
        """Обработчик нажатия кнопки bt2"""
        self.create_tab('Tab4', 'SELECT * FROM users')
    
    def on_bt3_clicked(self):
        """Обработчик нажатия кнопки bt3"""
        self.create_tab('Tab5', 'SELECT * FROM products')
    
    def on_combo_changed(self, text):
        """Обработчик изменения выбора в ComboBox"""
        if text and text != 'QComboBox "Colums"':
            query = f'SELECT {text} FROM users'
            self.create_tab('Tab3', query)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
