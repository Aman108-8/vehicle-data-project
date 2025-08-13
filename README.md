# Streamlit Project with SQL Database

This project is built using **Python**, **Streamlit**, and an **SQL database**.  
Follow the steps below to set up the environment, import the database, and run the application.

---

## 1. Install dependency

```bash
pip install streamlit

# Create virtual environment
python -m venv myenv

# Activate it
# Windows:
myenv\Scripts\activate

# Mac/Linux:
source myenv/bin/activate

pip install pandas plotly-express  # For data visualization
pip install mysql-connector-python  # For database connections

cd myenv

pip install streamlit

streamlit run main.py

```
## 2. import database in your mysql

## 3. Edit database configuration
db_config = {
    'host': 'localhost',
    'user': 'your user_name',
    'password': 'yourpassword',
    'database': 'vehicle_data'
}

## 4. then copy file of py and paste into myenv

# Picture

<img width="1918" height="965" alt="image" src="https://github.com/user-attachments/assets/4973e0fa-0067-4560-9db1-59934d735dd1" />

<img width="1918" height="967" alt="image" src="https://github.com/user-attachments/assets/faa0999d-2442-4798-adfe-19057d4e7a70" />



