import sys
import os
import pickle
import pandas as pd

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget, QMessageBox


from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox,
    QComboBox, QSpinBox
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon


DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")


class InventoryApp(QWidget):

    
    def save_internal_data(self):
     data = {
        "inventory": self.inventory_data,
        "withdraw": self.withdraw_data,
        "orders": self.orders_data,
        "camps_departments": self.camps_departments
    }
     with open("inventory_data.pkl", "wb") as f:
      pickle.dump(data, f)

    def load_internal_data(self):
       if os.path.exists("inventory_data.pkl"):
        with open("inventory_data.pkl", "rb") as f:
            data = pickle.load(f)
       self.inventory_data = data.get("inventory", [])
       self.withdraw_data = data.get("withdraw", [])
       self.orders_data = data.get("orders", [])
       self.camps_departments = data.get("camps_departments", [])
       self.refresh_inventory_table()
       self.refresh_withdraw_table()
       self.refresh_camp_dept_table()
       self.refresh_order_table()



    def closeEvent(self, event):
       self.save_internal_data()
       event.accept()



       # Load saved data if file exists
       if os.path.exists("inventory_data.pkl"):
        with open("inventory_data.pkl", "rb") as f:
         data = pickle.load(f)
        self.inventory_data = data.get("inventory", [])
        self.withdraw_data = data.get("withdraw", [])
        self.orders_data = data.get("orders", [])
        self.camps_departments = data.get("camps_departments", {})
                     
       else:
        self.inventory_data = []
        self.withdraw_data = []
        self.orders_data = []
        self.camps_departments = {}













    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Stationery Inventory Manager - IMS")
        self.setGeometry(100, 100, 1000, 600)

        self.inventory_data = []
        self.withdraw_data = []
        self.camps_departments = []
        self.orders_data = []

        self.tabs = QTabWidget()
        self.init_add_tab()
        self.init_withdraw_tab()
        self.init_camp_dept_tab()
        self.init_order_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        #self.save_all_btn = QPushButton("save all data")
       # self.save_all_btn.clicked.connect(self.save_all_data)
        #layout.addWidget(self.save_all_btn)

        self.setLayout(layout)
        self.load_data()

    def delete_camp_dept_entry(self):
        row = self.camp_dept_table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(
                self,
                "confirm deletion",
                "are you sure you want to delete?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.camps_departments.pop(row)
                self.refresh_camp_dept_table()
                self.refresh_order_table()



    def init_add_tab(self):
        self.add_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.item_input = QLineEdit()
        self.qty_input = QSpinBox()
        self.min_qty_input = QSpinBox()
        self.camp_input = QLineEdit()
        self.qty_input.setMaximum(999999999)
        self.min_qty_input.setMaximum(999999999)

        form_layout.addWidget(QLabel("Item"))
        form_layout.addWidget(self.item_input)
        form_layout.addWidget(QLabel("Quantity"))
        form_layout.addWidget(self.qty_input)
        form_layout.addWidget(QLabel("Min Qty"))
        form_layout.addWidget(self.min_qty_input)
        form_layout.addWidget(QLabel("Camp"))
        form_layout.addWidget(self.camp_input)

        self.add_button = QPushButton("Add to Inventory")
        self.add_button.clicked.connect(self.add_item)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(4)
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity", "Min Qty", "Camp"])
        self.inventory_table.itemChanged.connect(self.update_inventory_data)
        layout.addWidget(self.inventory_table)

        export_btn = QPushButton("Export to Excel")
        export_btn.clicked.connect(self.export_inventory)
        layout.addWidget(export_btn)

        self.delete_inventory_btn = QPushButton("Delete Selected Item")
        self.delete_inventory_btn.clicked.connect(self.delete_inventory_item)
        layout.addWidget(self.delete_inventory_btn)

        self.add_tab.setLayout(layout)
        self.tabs.addTab(self.add_tab, "Add to Inventory")

    def init_withdraw_tab(self):
        self.withdraw_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.badge_input = QLineEdit()
        self.item_select = QComboBox()
        self.withdraw_qty_input = QSpinBox()
        self.department_select = QComboBox()
        self.withdraw_camp_select = QComboBox()
        self.withdraw_date = QDate.currentDate().toString("yyyy-MM-dd")

        self.withdraw_qty_input.setMaximum(999999999)

        form_layout.addWidget(QLabel("Badge Number"))
        form_layout.addWidget(self.badge_input)
        form_layout.addWidget(QLabel("Item"))
        form_layout.addWidget(self.item_select)
        form_layout.addWidget(QLabel("Quantity"))
        form_layout.addWidget(self.withdraw_qty_input)
        form_layout.addWidget(QLabel("Department"))
        form_layout.addWidget(self.department_select)
        form_layout.addWidget(QLabel("Camp"))
        form_layout.addWidget(self.withdraw_camp_select)

        self.withdraw_button = QPushButton("Withdraw")
        self.withdraw_button.clicked.connect(self.withdraw_item)
        form_layout.addWidget(self.withdraw_button)

        layout.addLayout(form_layout)

        self.withdraw_table = QTableWidget()
        self.withdraw_table.setColumnCount(6)
        self.withdraw_table.setHorizontalHeaderLabels(["Badge", "Item", "Quantity", "Department", "Camp", "Date"])
        self.withdraw_table.itemChanged.connect(self.update_withdraw_data)
        layout.addWidget(self.withdraw_table)

        self.delete_withdraw_btn = QPushButton("Delete Selected Withdrawal")
        self.delete_withdraw_btn.clicked.connect(self.delete_withdrawal)
        layout.addWidget(self.delete_withdraw_btn)

        export_btn = QPushButton("Export Withdrawals to Excel")
        export_btn.clicked.connect(self.export_withdrawals)
        layout.addWidget(export_btn)

        self.withdraw_tab.setLayout(layout)
        self.tabs.addTab(self.withdraw_tab, "Withdraw Item")

    

    def init_camp_dept_tab(self):
        self.camp_dept_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.new_camp_input = QLineEdit()
        self.new_dept_input = QLineEdit()
        form_layout.addWidget(QLabel("New Camp"))
        form_layout.addWidget(self.new_camp_input)
        form_layout.addWidget(QLabel("New Department"))
        form_layout.addWidget(self.new_dept_input)

        self.save_camp_dept_btn = QPushButton("Save Camp & Department")
        self.save_camp_dept_btn.clicked.connect(self.save_camp_department)
        form_layout.addWidget(self.save_camp_dept_btn)

        layout.addLayout(form_layout)

        self.camp_dept_table = QTableWidget()
        self.camp_dept_table.setColumnCount(2)
        self.camp_dept_table.setHorizontalHeaderLabels(["Camp", "Department"])
        self.camp_dept_table.itemChanged.connect(self.update_camp_dept_data)
        layout.addWidget(self.camp_dept_table)


        self.delete_camp_dept_btn = QPushButton("Delete Selected Camp/Department")
        self.delete_camp_dept_btn.clicked.connect(self.delete_camp_dept_entry)
        layout.addWidget(self.delete_camp_dept_btn)





        export_btn = QPushButton("Export Camp/Dept Info")
        export_btn.clicked.connect(self.export_camp_department)
        layout.addWidget(export_btn)

        self.camp_dept_tab.setLayout(layout)
        self.tabs.addTab(self.camp_dept_tab, "Camp & Department")


    def init_order_tab(self):
        self.order_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.order_item_input = QLineEdit()
        self.order_qty_input = QSpinBox()
        self.order_camp_input = QLineEdit()
        self.order_qty_input.setMaximum(999999999)

        form_layout.addWidget(QLabel("Item"))
        form_layout.addWidget(self.order_item_input)
        form_layout.addWidget(QLabel("Quantity"))
        form_layout.addWidget(self.order_qty_input)
        form_layout.addWidget(QLabel("Camp"))
        form_layout.addWidget(self.order_camp_input)

        self.add_order_btn = QPushButton("Add Order")
        self.add_order_btn.clicked.connect(self.add_order)
        form_layout.addWidget(self.add_order_btn)

        layout.addLayout(form_layout)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(["Item", "Quantity", "Camp"])
        self.order_table.itemChanged.connect(self.update_order_data)
        layout.addWidget(self.order_table)

        self.delete_order_btn = QPushButton("Delete Selected Order")
        self.delete_order_btn.clicked.connect(self.delete_order)
        layout.addWidget(self.delete_order_btn)

        export_btn = QPushButton("Export Orders to Excel")
        export_btn.clicked.connect(self.export_orders)
        layout.addWidget(export_btn)

        self.order_tab.setLayout(layout)
        self.tabs.addTab(self.order_tab, "Orders")

    def add_item(self):
        item = self.item_input.text().strip()
        qty = self.qty_input.value()
        min_qty = self.min_qty_input.value()
        camp = self.camp_input.text().strip()

        if item:
            for row in self.inventory_data:
                if row[0] == item and row[3] == camp:
                    row[1] = int(row[1]) + qty
                    self.refresh_inventory_table()
                    break
            else:
                self.inventory_data.append([item, qty, min_qty, camp])
                self.refresh_inventory_table()

            self.item_input.clear()
            self.qty_input.setValue(0)
            self.min_qty_input.setValue(0)
            self.camp_input.clear()

    def withdraw_item(self):
        badge = self.badge_input.text()
        item = self.item_select.currentText()
        qty = self.withdraw_qty_input.value()
        department = self.department_select.currentText()
        camp = self.withdraw_camp_select.currentText()

        if item and qty > 0:
         if [camp, department] not in self.camps_departments:
            QMessageBox.warning(self, "error", f"in this camp '{camp}' no departmint '{department}'.")
            return

        for row in self.inventory_data:
            if row[0] == item and row[3] == camp:
                current_qty = int(row[1])
                if current_qty >= qty:
                    row[1] = current_qty - qty
                    self.withdraw_data.append([badge, item, qty, department, camp, self.withdraw_date])
                    self.refresh_inventory_table()
                    self.refresh_withdraw_table()
                    self.badge_input.clear()
                    self.withdraw_qty_input.setValue(0)
                else:
                    QMessageBox.warning(self, "Insufficient Quantity", f"Only {current_qty} of '{item}' in inventory.")
                break
        else:
            QMessageBox.warning(self, "Item Not Found", f"'{item}' not found in inventory for camp '{camp}'.")


    def save_camp_department(self):
        camp = self.new_camp_input.text().strip()
        dept = self.new_dept_input.text().strip()

        if camp and dept and [camp, dept] not in self.camps_departments:
            self.camps_departments.append([camp, dept])
            if camp not in [self.withdraw_camp_select.itemText(i) for i in range(self.withdraw_camp_select.count())]:
                self.withdraw_camp_select.addItem(camp)
            if dept not in [self.department_select.itemText(i) for i in range(self.department_select.count())]:
                self.department_select.addItem(dept)
            self.refresh_camp_dept_table()

        self.new_camp_input.clear()
        self.new_dept_input.clear()

    def add_order(self):
        item = self.order_item_input.text()
        qty = self.order_qty_input.value()
        camp = self.order_camp_input.text()
        if item:
            self.orders_data.append([item, qty, camp])
            self.refresh_order_table()
            self.order_item_input.clear()
            self.order_qty_input.setValue(0)
            self.order_camp_input.clear()

    def delete_withdrawal(self):
        row = self.withdraw_table.currentRow()
        if row >= 0:

         reply = QMessageBox.question(
              self,
                "confirm deletion",
                "are you sure you want to delete this?",
                QMessageBox.Yes | QMessageBox.No
            )

         if reply == QMessageBox.Yes:
                self.withdraw_data.pop(row)
                self.refresh_withdraw_table()
                self.refresh_order_table()

        else:
                QMessageBox.warning(self, "Error", "Please select a valid row to delete.")

    

    def delete_inventory_item(self):
     row = self.inventory_table.currentRow()
     if 0 <= row < len(self.inventory_data):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this inventory item?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.inventory_data.pop(row)
            self.refresh_inventory_table()
            self.refresh_order_table()
     else:
        QMessageBox.warning(self, "Error", "Please select a valid row to delete.")


    def delete_order(self):
     row = self.order_table.currentRow()
     if 0 <= row:
        reply = QMessageBox.question(
             self,
            "Confirm Deletion",
            "Are you sure you want to delete this order?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
               self.orders_data.pop(row)
               self.refresh_order_table()
               self.refresh_order_table()
     else:
        QMessageBox.warning(self, "Error", "Please select a valid row to delete.")


    def refresh_inventory_table(self):
        self.inventory_table.setRowCount(0)
        for row_data in self.inventory_data:
            row = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row)
            for col, item in enumerate(row_data):
                self.inventory_table.setItem(row, col, QTableWidgetItem(str(item)))
        self.item_select.clear()
        self.item_select.addItems(list({item[0] for item in self.inventory_data}))

    def refresh_withdraw_table(self):
        self.withdraw_table.setRowCount(0)
        for row_data in self.withdraw_data:
            row = self.withdraw_table.rowCount()
            self.withdraw_table.insertRow(row)
            for col, item in enumerate(row_data):
                self.withdraw_table.setItem(row, col, QTableWidgetItem(str(item)))

    def refresh_camp_dept_table(self):
        self.camp_dept_table.setRowCount(0)
        for row_data in self.camps_departments:
            row = self.camp_dept_table.rowCount()
            self.camp_dept_table.insertRow(row)
            for col, item in enumerate(row_data):
                self.camp_dept_table.setItem(row, col, QTableWidgetItem(str(item)))

    def refresh_order_table(self):
        self.order_table.setRowCount(0)
        for row_data in self.orders_data:
            row = self.order_table.rowCount()
            self.order_table.insertRow(row)
            for col, item in enumerate(row_data):
                self.order_table.setItem(row, col, QTableWidgetItem(str(item)))

    def update_inventory_data(self, item):
        self.inventory_data[item.row()][item.column()] = item.text()

    def update_withdraw_data(self, item):
        self.withdraw_data[item.row()][item.column()] = item.text()

    def update_camp_dept_data(self, item):
        self.camps_departments[item.row()][item.column()] = item.text()

    def update_order_data(self, item):
        self.orders_data[item.row()][item.column()] = item.text()

    def export_inventory(self):
        pd.DataFrame(self.inventory_data, columns=["Item", "Quantity", "Min Qty", "Camp"]).to_excel(os.path.join(DESKTOP, "inventory.xlsx"), index=False)

    def export_withdrawals(self):
        pd.DataFrame(self.withdraw_data, columns=["Badge", "Item", "Quantity", "Department", "Camp", "Date"]).to_excel(os.path.join(DESKTOP, "withdrawals.xlsx"), index=False)

    def export_camp_department(self):
        pd.DataFrame(self.camps_departments, columns=["Camp", "Department"]).to_excel(os.path.join(DESKTOP, "camp_departments.xlsx"), index=False)

    def export_orders(self):
        pd.DataFrame(self.orders_data, columns=["Item", "Quantity", "Camp"]).to_excel(os.path.join(DESKTOP, "orders.xlsx"), index=False)

   # def save_all_data(self):
     #   self.export_inventory()
     #   self.export_withdrawals()
      #  self.export_camp_department()
      #  self.export_orders()
      #  QMessageBox.information(self, "Saved", "All data saved successfully.")



    def load_data(self):
        try:
            inventory_file = os.path.join(DESKTOP, "inventory.xlsx")
            if os.path.exists(inventory_file):
                self.inventory_data = pd.read_excel(inventory_file).values.tolist()
            withdraw_file = os.path.join(DESKTOP, "withdrawals.xlsx")
            if os.path.exists(withdraw_file):
                self.withdraw_data = pd.read_excel(withdraw_file).values.tolist()
            orders_file = os.path.join(DESKTOP, "orders.xlsx")
            if os.path.exists(orders_file):
                self.orders_data = pd.read_excel(orders_file).values.tolist()
            camps_file = os.path.join(DESKTOP, "camp_departments.xlsx")
            if os.path.exists(camps_file):
                df = pd.read_excel(camps_file)
                self.camps_departments = df.values.tolist()
                for camp, dept in self.camps_departments:
                    if camp not in [self.withdraw_camp_select.itemText(i) for i in range(self.withdraw_camp_select.count())]:
                        self.withdraw_camp_select.addItem(camp)
                    if dept not in [self.department_select.itemText(i) for i in range(self.department_select.count())]:
                        self.department_select.addItem(dept)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading data:\n{e}")

        self.refresh_inventory_table()
        self.refresh_withdraw_table()
        self.refresh_camp_dept_table()
        self.refresh_order_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())

