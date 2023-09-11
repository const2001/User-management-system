# User-management-system
## Clone and run project
```bash
git clone https://github.com/const2001/User-management-system
python -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```
## Modify the database url to your settings 
```vim
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
```

# run flask server
```bash
python app.py
```
