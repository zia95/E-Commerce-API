# E-Commerce Web API
This is E-Commerce web api demo built using python and fastapi.
# Setup Instructions
## 1. Environment variables setup
Create `.env` file and copy the below content and paste it into it and fill all the environment variables.
```
DATABASE_NAME="ecomtest"
DATABASE_FILE="./ecomtest.db"
port=3306
HOST="localhost"
USER="root"
PASSWORD="password"
SECRET_KEY="09f26e402586e2faa8da4c98a35f1b20d6b033c6097befa8be3486a829587fe2f90a832bd3ff9d42710a4da095a2ce285b009f0c3730cd9b8e1af3eb84df6611"
ACCESS_TOKEN_EXPIRE_MINS=30
```
Make sure whatever the name of the database you use, it exists. Using shell/workbench, to create a database execute query `CREATE DATABASE <database_name>;` to confirm it exists use query `SHOW DATABASES;`
## 2. Initialization
### Method A. Manual (RECOMMENDED)
1. Create python virtual environment using `python.exe -m venv <virtual env name>`
2. Activate virtual environment using `./<virtual env name>/Scripts/Activate.ps1`
3. Install the dependencies using `python.exe -m pip install -r ./requirements.txt`
4. Sync database state by using `alembic history` to list all the revision and then to sync use `alembic upgrade <rev_id_from_history_command>` 
5. To run the api use `uvicorn main:app`
6. Lastly, open the provided url to locally hosted app and naviagate to `<url>/docs`. This will open swagger docs where you can test the api.

### Method B. Using setup script
1. Run `setup.ps1` and it will setup all the envionment.
2. Activate the virtual environment using `./<virtual env name>/Scripts/Activate.ps1`
3. Sync database state by using `alembic history` to list all the revision and then to sync use `alembic upgrade <rev_id_from_history_command>` 
4. To run the api use `uvicorn main:app`
5. Lastly, open the provided url to locally hosted app and naviagate to `<url>/docs`. This will open swagger docs where you can test the api.