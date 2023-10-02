# E-Commerce Web API
This is E-Commerece web api demo built using python and fastapi.
# Setup Instructions
## 1. Environment variables setup
Create `.env` file and copy the below content and paste it into it and fill all the environment variables.
```
DATABASE_NAME=""
DATABASE_FILE=""
HOST=""
USER=""
PASSWORD=""
SECRET_KEY=""
ACCESS_TOKEN_EXPIRE_MINS=30
```
## 2. Environment setup
### Method A. Using setup script
Run `setup.ps1` and it will setup all the envionment.
To run the app run `setup.ps1` script with `-Run` parameter. Like `setup.ps1 -Run`
### Method B. Manual
1. Create python virtual environment using `python.exe -m venv <virtual env name>`
2. Activate virtual environment using `./<virtual env name>/Scripts/Activate.ps1`
3. Install the dependencies using `python.exe -m pip install -r ./requirements.txt`
4. To run the api use `uvicorn main:app`
5. Lastly, open the provided url to locally hosted app and naviagate to `<url>/docs`. This will open swagger docs where you can test the api.