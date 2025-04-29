# Placement Eligibility Application (PEA) - Streamlit App

The **Placement Eligibility Application (PEA)** is a Streamlit-based web tool designed to help manage and assess student placement eligibility data. It provides an intuitive interface for coordinators or administrators to input and analyze student records stored in a MySQL database.

## 🚀 Features

- Clean and interactive UI with Streamlit
- Evaluates student eligibility for placements based on customizable criteria
- Connects to a MySQL database using `mysql-connector-python`
- Modular structure for easy maintenance and expansion

## 🛠 Tech Stack

- Python 3.x
- Streamlit
- mysql-connector-python
- MySQL

## 📁 Project Structure
placement-eligibility-app/
├── app.py              # Main Streamlit app – user interface and flow
├── PEA.py              # Business logic: data processing and database queries
├── db_config.py        # MySQL database configuration (host, user, etc.)
├── README.md           # Documentation (what you're building now)


## ✅ Requirements

- Python 3.7+
- MySQL server
- pip (Python package manager)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/placement-eligibility-app.git
   cd placement-eligibility-app


2. **Install dependencies**:
  pip install streamlit mysql-connector-python

3. Configure the database: Edit db_config.py with your MySQL credentials
```
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database'
}
```

▶️ Running the App

To start the Streamlit app, run:
``streamlit run app.py``

Then open your browser to:
``Then open your browser to:``

