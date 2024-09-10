# 🧾 Salary Slip Management System

Welcome to the **Salary Slip Management System**, a web-based application designed to streamline the process of generating salary slips for employees. This project is built using **Django** for the backend, with a frontend crafted in **HTML**, **CSS**, and **JavaScript**. We also utilize **Pandas** to handle real-time data processing from Excel files, making salary management quick and efficient.

## 🌟 Features

- 📄 **Salary Slip Generation**: Automatically generates salary slips for registered staff.
- 📊 **Real-time Excel Processing**: Upload an Excel sheet with employee salary details, and the system will read and generate slips using **Pandas**.
- 👨‍💼 **Admin Functionality**:
  - Admin can **create new users** and assign them roles.
  - Admin can **reset passwords** for users.
  - Easy **upload and re-upload** of Excel sheets for specific months.
  - View all uploaded salary details and download them for record-keeping.
- 👩‍💻 **User Functionality**:
  - Users can **view all their salary details**.
  - Users can **download their salary slips** for specific months.
  - Users can **change their password** for security.

## 🛠️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Excel Processing**: Pandas

## 🚀 How to Get Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Django
- Pandas
- SQLite (included with Django)

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hkpushpam/Finance-Management-System-NITAP.git
   cd salary-slip-management
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   Install all required Python packages using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrate the Database**:
   Run the following command to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (Admin User):
   Create a superuser account to access the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   - Open your web browser and go to: `http://127.0.0.1:8000/`

### Uploading Excel File for Salary Processing

- Log in to the **admin panel** and navigate to the Excel upload section.
- Upload the file for the specific month in the format provided.
- The system will generate the salary slips automatically!

### 📑 Documentation

For more details and advanced usage, check out the official documentation for the libraries used:

- [Django Documentation](https://docs.djangoproject.com/en/stable/) 📘
- [Pandas Documentation](https://pandas.pydata.org/docs/) 📊
- [SQLite Documentation](https://sqlite.org/docs.html) 🗃️

---
