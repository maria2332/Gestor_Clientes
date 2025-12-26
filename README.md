<h1 align="center">👥 Gestor de Clientes (Python)</h1>

<p align="center">
  Academic project developed in <strong>Python</strong> focused on object-oriented programming,
  modular design, data persistence, and basic testing practices.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Architecture-Modular-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Testing-pytest-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Data-CSV-lightgrey?style=for-the-badge"/>
</p>

<p align="center">
  <a href="https://deepwiki.com/maria2332/Gestor_Clientes" target="_blank">
    <img src="https://img.shields.io/badge/DeepWiki-Documentation-purple?style=for-the-badge"/>
  </a>
</p>

---

## 📚 Project Documentation (External)

An automatically generated documentation view of this repository is available via DeepWiki:

👉 https://deepwiki.com/maria2332/Gestor_Clientes
---

## 🎓 Academic Context

This repository contains an academic project designed to practice fundamental
software development concepts using Python, including:

- Object-oriented programming
- Modular architecture
- Data persistence
- Basic automated testing
- Code documentation and UML representation

---

## 🎯 Project Features

- Client entity modeled using Python classes
- CRUD-like operations (create, search, list, save)
- CSV-based persistence as a lightweight database
- Clear separation of responsibilities across modules
- Automated tests using `pytest`
- UML class diagram for structural understanding

---

## 🧠 Project Structure

```text
├── database.py              # Data access layer (CSV read/write)
├── config.py                # Configuration and constants
├── helpers.py               # Helper functions
├── menu.py                  # Menu and application flow
├── ui.py                    # User interaction layer
├── run.py                   # Application entry point
├── clientes.csv             # CSV data storage
├── tests/                   # Automated tests (pytest)
├── uml/
│   └── diagrama_clases.puml # UML class diagram
└── README.md
````

---

## 🗄️ Data Persistence

Client data is stored in a **CSV file**, acting as a simple persistence layer.
All file access logic is encapsulated in `database.py`, allowing future migration
to an SQL-based database (e.g. SQLite) without major changes to the application logic.

---

## ▶️ How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/maria2332/Gestor_Clientes.git
cd Gestor_Clientes
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies (if required):

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python run.py
```

---

## ✅ Run Tests

To execute the automated tests:

```bash
pytest -q
```

---

## 📌 Key Learnings

* Designing a small application using **modular architecture**
* Applying **object-oriented principles** in Python
* Managing structured data through a persistence layer
* Writing and running basic automated tests
* Using UML to document and reason about code structure

---

## 🔍 Final Remarks

This project represents a clean academic implementation of a customer management system,
with emphasis on clarity, maintainability, and good development practices.



