# Inventory Management App

Welcome to the **Inventory Management App**, a lightweight desktop application built with Python and PyQt5. This project provides a clean and intuitive GUI to manage product inventories — ideal for small businesses, personal tracking, or as a base for more advanced systems.

---

## 💻 Features

- 🚀 **Fast and Minimalist UI**: Designed using PyQt5 with a simple yet functional layout.
- 🧾 **Inventory List Display**: Shows a table of products with dynamic loading.
- ✍️ **Product Management**: Easily add new items via a dedicated dialog window.
- 🎨 **Custom Icons**: Includes a personalized icon for professional branding.
- 🪄 **Packaged with PyInstaller**: Produces a standalone `.exe` for Windows without requiring Python installation.

---

## 🧠 Technical Details

### 🧱 Framework & Language
- **Python 3.11**
- **PyQt5**: For creating the GUI, including widgets like `QTableWidget`, `QDialog`, and `QPushButton`.

### 🏗️ Structure

- `InventoryApp`: The main window, showing the inventory table and an "Add Product" button.
- `AddProductDialog`: A pop-up dialog that lets the user input new product data (name, quantity, price).
- Icon management using `QIcon` to give the app a custom look and feel in the taskbar and title bar.

### 📁 Code Highlights

```python
self.setWindowIcon(QIcon("icon.ico"))
```
