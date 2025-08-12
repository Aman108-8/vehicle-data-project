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

# Then install streamlit
pip install streamlit

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
