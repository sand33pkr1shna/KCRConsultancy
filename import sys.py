import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QDateEdit, QCalendarWidget, QHBoxLayout
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt

class PoultryManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poultry Management App")
        self.connection = sqlite3.connect('poultry.db')
        self.create_tables()

        self.create_widgets()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS egg_production (
                            id INTEGER PRIMARY KEY,
                            date DATE UNIQUE,
                            type TEXT,
                            production INTEGER
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS egg_prices (
                            id INTEGER PRIMARY KEY,
                            date DATE UNIQUE,
                            price FLOAT
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                            id INTEGER PRIMARY KEY,
                            date DATE UNIQUE,
                            quantity INTEGER
                          )''')
        self.connection.commit()
        cursor.close()

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.notebook = QTabWidget()
        layout.addWidget(self.notebook)

        self.production_tab = QWidget()
        self.notebook.addTab(self.production_tab, "Production")
        self.create_production_widgets()

        self.price_tab = QWidget()
        self.notebook.addTab(self.price_tab, "Price")
        self.create_price_widgets()

        self.sales_tab = QWidget()
        self.notebook.addTab(self.sales_tab, "Sales")
        self.create_sales_widgets()

        self.export_tab = QWidget()
        self.notebook.addTab(self.export_tab, "Export Data")
        self.create_export_widgets()

    def create_production_widgets(self):
        layout = QVBoxLayout(self.production_tab)

        date_label = QLabel("Date:")
        layout.addWidget(date_label)
        self.production_date_edit = QLineEdit()
        layout.addWidget(self.production_date_edit)
        
        self.production_date_calendar = QCalendarWidget()
        self.production_date_calendar.setGridVisible(True)
        self.production_date_calendar.clicked.connect(self.update_production_date)
        layout.addWidget(self.production_date_calendar)

        type_label = QLabel("Type:")
        layout.addWidget(type_label)
        self.production_type_entry = QLineEdit()
        layout.addWidget(self.production_type_entry)

        quantity_label = QLabel("Quantity:")
        layout.addWidget(quantity_label)
        self.production_quantity_entry = QLineEdit()
        layout.addWidget(self.production_quantity_entry)

        add_production_button = QPushButton("Add Production")
        add_production_button.clicked.connect(self.add_production)
        layout.addWidget(add_production_button)

        self.production_canvas = QWidget()
        layout.addWidget(self.production_canvas)

        self.show_production_graph()

    def update_production_date(self, date):
        selected_date = self.production_date_calendar.selectedDate()
        self.production_date_edit.setText(selected_date.toString())

    def create_price_widgets(self):
        layout = QVBoxLayout(self.price_tab)

        date_label = QLabel("Date:")
        layout.addWidget(date_label)
        self.price_date_edit = QLineEdit()
        layout.addWidget(self.price_date_edit)
        
        self.price_date_calendar = QCalendarWidget()
        self.price_date_calendar.setGridVisible(True)
        self.price_date_calendar.clicked.connect(self.update_price_date)
        layout.addWidget(self.price_date_calendar)

        value_label = QLabel("Value:")
        layout.addWidget(value_label)
        self.price_value_entry = QLineEdit()
        layout.addWidget(self.price_value_entry)

        set_price_button = QPushButton("Set Price")
        set_price_button.clicked.connect(self.set_price)
        layout.addWidget(set_price_button)

        self.revenue_canvas = QWidget()
        layout.addWidget(self.revenue_canvas)

        self.show_revenue_graph()

    def update_price_date(self, date):
        selected_date = self.price_date_calendar.selectedDate()
        self.price_date_edit.setText(selected_date.toString())

    def create_sales_widgets(self):
        layout = QVBoxLayout(self.sales_tab)

        date_label = QLabel("Date:")
        layout.addWidget(date_label)
        self.sales_date_edit = QLineEdit()
        layout.addWidget(self.sales_date_edit)
        
        self.sales_date_calendar = QCalendarWidget()
        self.sales_date_calendar.setGridVisible(True)
        self.sales_date_calendar.clicked.connect(self.update_sales_date)
        layout.addWidget(self.sales_date_calendar)

        quantity_label = QLabel("Quantity:")
        layout.addWidget(quantity_label)
        self.sales_quantity_entry = QLineEdit()
        layout.addWidget(self.sales_quantity_entry)

        add_sales_button = QPushButton("Add Sales")
        add_sales_button.clicked.connect(self.add_sales)
        layout.addWidget(add_sales_button)

        self.sales_canvas = QWidget()
        layout.addWidget(self.sales_canvas)

        self.show_sales_graph()

    def update_sales_date(self, date):
        selected_date = self.sales_date_calendar.selectedDate()
        self.sales_date_edit.setText(selected_date.toString())

    def create_export_widgets(self):
        layout = QVBoxLayout(self.export_tab)

        export_data_button = QPushButton("Export Data")
        export_data_button.clicked.connect(self.export_database)
        layout.addWidget(export_data_button)

    def add_production(self):
        date = self.production_date_edit.text()
        egg_type = self.production_type_entry.text()
        quantity = self.production_quantity_entry.text()

        if date and egg_type and quantity:
            cursor = self.connection.cursor()
            try:
                cursor.execute('REPLACE INTO egg_production (date, type, production) VALUES (?, ?, ?)', (date, egg_type, quantity))
                self.connection.commit()
                QMessageBox.information(self, "Success", "Production entry added successfully.")
                self.production_date_edit.clear()
                self.production_type_entry.clear()
                self.production_quantity_entry.clear()
                self.show_production_graph()  
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error adding production entry: {e}")
            finally:
                cursor.close()
        else:
            QMessageBox.critical(self, "Error", "Please fill in all fields for production entry.")

    def set_price(self):
        date = self.price_date_edit.text()
        value = self.price_value_entry.text()

        if date and value:
            cursor = self.connection.cursor()
            try:
                cursor.execute('REPLACE INTO egg_prices (date, price) VALUES (?, ?)', (date, value))
                self.connection.commit()
                QMessageBox.information(self, "Success", "Price entry added successfully.")
                self.price_date_edit.clear()
                self.price_value_entry.clear()
                self.show_revenue_graph()  
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error adding price entry: {e}")
            finally:
                cursor.close()
        else:
            QMessageBox.critical(self, "Error", "Please fill in all fields for price entry.")

    def add_sales(self):
        date = self.sales_date_edit.text()
        quantity = self.sales_quantity_entry.text()

        if date and quantity:
            cursor = self.connection.cursor()
            try:
                cursor.execute('REPLACE INTO sales (date, quantity) VALUES (?, ?)', (date, quantity))
                self.connection.commit()
                QMessageBox.information(self, "Success", "Sales entry added successfully.")
                self.sales_date_edit.clear()
                self.sales_quantity_entry.clear()
                self.show_sales_graph()  
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error adding sales entry: {e}")
            finally:
                cursor.close()
        else:
            QMessageBox.critical(self, "Error", "Please fill in all fields for sales entry.")

    def show_production_graph(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT date, type, production FROM egg_production')
        data = cursor.fetchall()
        cursor.close()

        dates = []
        productions = {'A': [], 'B': [], 'C': []}  
        colors = {'A': 'blue', 'B': 'green', 'C': 'red'}  

        for row in data:
            date = row[0]
            type = row[1]
            production = row[2]
            if date not in dates:
                dates.append(date)
            for t in productions.keys():
                if t == type:
                    productions[t].append(production)
                else:
                    productions[t].append(0)

        fig, ax = plt.subplots()
        for type, color in colors.items():
            ax.plot(dates, productions[type], color=color, label=f'Production Type {type}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Production')
        ax.set_title('Production Over Time')
        plt.xticks(rotation=45)
        ax.legend()

        self.plot_to_canvas(fig, self.production_canvas)

    def show_sales_graph(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT date, quantity FROM sales')
        data = cursor.fetchall()
        cursor.close()

        dates = [row[0] for row in data]
        sales = [row[1] for row in data]

        fig, ax = plt.subplots()
        ax.plot(dates, sales, color='green', label='Sales')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales')
        ax.set_title('Sales Over Time')
        plt.xticks(rotation=45)

        self.plot_to_canvas(fig, self.sales_canvas)

    def show_revenue_graph(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT ep.date, ep.production, s.quantity, ep.production * p.price AS revenue
            FROM egg_production ep
            LEFT JOIN sales s ON ep.date = s.date
            LEFT JOIN egg_prices p ON ep.date = p.date
        ''')
        data = cursor.fetchall()
        cursor.close()

        dates = [row[0] for row in data]
        revenue = [row[3] if row[3] else 0 for row in data]

        fig, ax = plt.subplots()
        ax.plot(dates, revenue, color='orange', label='Revenue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Revenue')
        ax.set_title('Revenue Over Time')
        plt.xticks(rotation=45)

        self.plot_to_canvas(fig, self.revenue_canvas)

    def plot_to_canvas(self, fig, canvas):
        layout = QVBoxLayout()
        layout.addWidget(FigureCanvas(fig))
        canvas.setLayout(layout)

    def export_database(self):
        egg_production_df = pd.read_sql_query('SELECT * FROM egg_production', self.connection)
        egg_prices_df = pd.read_sql_query('SELECT * FROM egg_prices', self.connection)
        sales_df = pd.read_sql_query('SELECT * FROM sales', self.connection)

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "Excel files (*.xlsx)")
        if file_path:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                egg_production_df.to_excel(writer, sheet_name='Egg Production', index=False)
                egg_prices_df.to_excel(writer, sheet_name='Egg Prices', index=False)
                sales_df.to_excel(writer, sheet_name='Sales', index=False)
            QMessageBox.information(self, "Success", "Database exported to Excel successfully.")

    def closeEvent(self, event):
        self.connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PoultryManagementApp()
    window.show()
    sys.exit(app.exec_())
