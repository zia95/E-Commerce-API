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
NOTE: Make sure whatever the name of the database you use, it exists. Using shell/workbench, to create a database execute query `CREATE DATABASE <database_name>;` to confirm it exists use query `SHOW DATABASES;`

## 2. Initialization
### Method A. Manual (RECOMMENDED)
1. Create python virtual environment using `python.exe -m venv <virtual env name>`
2. Activate virtual environment using `./<virtual env name>/Scripts/Activate.ps1`
3. Install the dependencies using `python.exe -m pip install -r ./requirements.txt`
4. Sync database state by using `alembic history` to list all the revision and then to sync use `alembic upgrade <rev_id_from_history_command>` 
5. To run the api use `uvicorn main:app`
6. Open the provided url to locally hosted app and naviagate to `<url>/docs`. This will open swagger docs where you can test the api.
7. Now run `/resetdb` endpoint and after this run `/loaddummy` to load test data.

### Method B. Using setup script (NOT FULLY TESTED OR UPDATED)
1. Run `setup.ps1` and it will setup all the envionment.
2. Activate the virtual environment using `./<virtual env name>/Scripts/Activate.ps1`
3. Sync database state by using `alembic history` to list all the revision and then to sync use `alembic upgrade <rev_id_from_history_command>` 
4. To run the api use `uvicorn main:app`
5. Open the provided url to locally hosted app and naviagate to `<url>/docs`. This will open swagger docs where you can test the api.
6. Now run `/resetdb` endpoint and after this run `/loaddummy` to load test data.

# Technologies
1. FastAPI: WebAPI framework.
2. MySQL: As a database
3. SqlAlchemy: As an ORM to store and retrive data
4. Alembic: Handle migration, track orm changes

# Design
## Users
Users related endpoints store registered users and jwt authorization.

## Post
Comments/review of users on product page.

## Logs
Diagnostics logs related to any errors, crashes and performance issues.

## Inventory
Store inventory related information such as products, price history etc...

## Sales
Store information such as sales, revenue, orders, products etc...
 
# Usage
## Reset/Clear
1. Use `/resetdb` endpoint to delete all the entries in tables.

## Load dummy data
1. Use `/loaddummy` endpoint to load dummy test data.

## Inventory
1. Endpoints to view stocks
2. Ability to view all the products and register new products
3. Ability to view price history and add new price for a specific products

## Sales
1. Calculate revenue
2. View orders
3. View order details (such as products associated with particular order)
4. Create orders.