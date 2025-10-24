
# Airport Flight Management System 

> “Data is a precious thing and will last longer than the systems themselves.” – Tim Berners-Lee  

A **Database Management System (DBMS)** project designed to manage airport flight operations efficiently.  
This project focuses on **PostgreSQL database design** for flight, passenger, and employee management — integrated with a **Streamlit-based role-based dashboard** built using **Python**.

---

## 🏷️ Project Badges

![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-ff4b4b)
![Python](https://img.shields.io/badge/Language-Python_3.8+-yellow)
![Docker](https://img.shields.io/badge/Container-Docker-2496ed)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)



## 🧠 Overview

The **Airport Flight Management System** was developed as a semester project for the **Database Management Systems (DBMS)** course.  
It demonstrates how relational databases can streamline complex airport operations such as:
- Flight scheduling  
- Passenger data management  
- Employee and admin control  
- Data visualization via dashboard  

The backend is built using **PostgreSQL**, dummy data is inserted through **Python (psycopg2)**, and an optional **Streamlit dashboard** enables interactive access for admins and staff.

---

## 🚀 Features

- 🗃️ **PostgreSQL Database** with normalized relational schema  
- 👥 **Role-Based Access Control (RBAC)** through Streamlit dashboard  
- 🧠 **Python-Powered Dummy Data Insertion** using `psycopg2`  
- 🐳 **Dockerized PostgreSQL Setup** for easy deployment  
- 🖥️ **ER Diagram** and **Data Flow Diagram (DFD)** for clear system understanding  
- 📈 **Professional Visualization Dashboard** (optional)  
- 🔗 **Admin Management Functions** for CRUD operations  

---

## 🧰 Technology Stack

| Category | Tool / Technology |
|-----------|------------------|
| **Database** | PostgreSQL |
| **Database Driver** | psycopg2 |
| **Programming Language** | Python 3.x |
| **Visualization / Dashboard** | Streamlit |
| **Containerization** | Docker |
| **IDE / Database Client** | DBeaver |
| **Documentation** | Markdown, Draw.io |

---

## ⚙️ System Architecture

```text
                ┌───────────────────┐
                │  Streamlit UI     │  ← Optional Dashboard
                └────────┬──────────┘
                         │
                         ▼
               ┌───────────────────┐
               │  Python Backend   │
               │ (psycopg2 Scripts)│
               └────────┬──────────┘
                         │
                         ▼
               ┌───────────────────┐
               │  PostgreSQL DBMS  │
               └───────────────────┘
````

---

## 🗂️ Database Design

### 📘 Key Entities

* **Flights** — flight ID, origin, destination, schedule, gate, pilot info
* **Passengers** — passenger details linked to flights
* **Employees/Admins** — assigned roles and permissions
* **Tickets/Bookings** — relations between flights and passengers

### 📈 ER Diagram

Refer to `ER detailed.pdf` or `AirportFlightManagement - public.png` for the complete ER model.

### 🔄 Data Flow Diagram (DFD)

Visual representation available in:

* `Semester Project DFD.drawio`
* `Semester Project DFD.drawio.png`

---

## 📁 Project Structure

```
📦 Airport-Flight-Management-System
├── 📂 dashboard/                      # Streamlit dashboard files
│   └── 📂 auth
│   └── 📂 config
│   └── 📂 modules
│   └── 📂 utils
│   └── 📜 app.py
│   └── 📜 image.py
│   └── 📜 requirements.txt

│
├── 📜 admin_insertion.py              # Handles admin role setup and insertion
├── 📜 generating_table.sql            # SQL script for creating tables and relationships
├── 📜 inserting_dummy_data.py         # Inserts dummy data into PostgreSQL using psycopg2
│
├── 📜 AirportFlightManagement - public.png  # ER Diagram (visual)
├── 📜 ER detailed.pdf                 # Detailed Entity-Relationship model
├── 📜 Semester Project DFD.drawio     # DFD editable file
├── 📜 Semester Project DFD.drawio.png # DFD image for quick reference
│
└── 📜 README.md                       # Project documentation
```

---

## ⚙️ Setup Instructions

### 🧩 Prerequisites

Ensure the following are installed:

* 🐍 Python 3.8+
* 🐳 Docker Desktop
* 🗃️ DBeaver (or any PostgreSQL client)
* 📦 PostgreSQL Docker image

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### 1️⃣ Run PostgreSQL Container in Docker

```bash
docker run --name postgres-airport -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres
```

### 2️⃣ Connect to Database Using DBeaver

Use these details:

* Host: `localhost`
* Port: `5432`
* Database: `airport_db`
* Username: `postgres`
* Password: `yourpassword`

### 3️⃣ Create Tables

Open **`generating_table.sql`** in DBeaver, copy all SQL commands, and execute to create tables and relationships.

### 4️⃣ Insert Dummy Data

Before running the dummy data script, **edit your PostgreSQL credentials** inside:

```python
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="your_database_name",
    user="your_username",
    password="your_password"
)
```

Then execute:

```bash
python inserting_dummy_data.py
```

This will populate the database with dummy values.

### 5️⃣ Insert Admin Roles

```bash
python admin_insertion.py
```

### 6️⃣ Run Streamlit Dashboard (Optional)

```bash
streamlit run dashboard/app.py
```

Then open the provided localhost URL (usually `http://localhost:8501`) in your browser.

---

## 💡 Future Enhancements

* 🔐 Implement secure user authentication
* 🌐 Integrate real-world flight data APIs
* 📊 Add visual reports and analytics
* 🤖 Predict delays using ML models
* 📄 Enable export to CSV/PDF

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it with attribution.



## 🤝 Contribution  

<div align="center">

We welcome contributions that make this project better!  
If you have suggestions, feel free to **fork the repo**, make changes, and create a **pull request**.  

</div>


### 🧭 Contribution Steps

1. **Fork** the repository  
2. **Create** a new branch  
   ```bash
   git checkout -b feature-name


3. **Make your changes** and **commit**

   ```bash
   git commit -m "Add: meaningful message here"
   ```
4. **Push** to your branch

   ```bash
   git push origin feature-name
   ```
5. **Open a Pull Request** for review

---

<div align="center">

⭐ If you find this project useful, consider giving it a star to show your support!

</div>




---
##  Summary

This project integrates:

* **Database Design (PostgreSQL)**
* **Backend Logic (Python & psycopg2)**
* **Optional UI (Streamlit Dashboard)**
* **Data Documentation (ER & DFD Diagrams)**

> A complete demonstration of **database design, backend integration, and modern visualization** — built for practical and academic excellence.

---

## 👨‍💻 Author  

<div align="center">

### **Yasir Ahmed**

<a href="https://github.com/YasirAhmed2" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-YasirAhmed2-181717?style=for-the-badge&logo=github" alt="GitHub Profile">
</a>

</div>

---
---

<div align="center">

### © 2025 Yasir Ahmed — All Rights Reserved

</div>







