# corporate-tests-search
Search engine for scraping data about covid tests ordered by companies for employees

# How to run
1. Download client secrets json file from the google cloud console (https://console.cloud.google.com/apis/credentials/oauthclient/702218053502-fcrju4976lt0p1dntbln2qdolo72qjki.apps.googleusercontent.com?authuser=1&project=covid-corporate--1589232879130)
2. Rename it as `client_secrets.json` and move it to the root directory of this project
3. Install python 3.8+ 
4. Optional: Create a virtual environment and activate it
5. Install dependencies via `pip install -r requirements.txt`
6. Run the script `python main.py`. The program will prompt you to sign in with a google account, make sure you use an account that has access to the COVID drive (specifically the data team folder) 
7. Check to see if `README.md`  was successfully uploaded to the `Corporate Tests Search Results` folder within the data team folder