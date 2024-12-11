# reddit-inactivity
Python script using praw to search your subreddits for inactivity

# Requirements
- You need a reddit account
- You need to register an application as a developer
- Python 3

## Create a reddit applicaiton
- Go [here](https://www.reddit.com/prefs/apps/) to create a reddit app.
- Select script from the app type options.
- set the redirect uri to localhost:8080.
- Fill in the rest of the information however you want.
- Take note of the client id and client secret you'll need this for configuration.

## Configure app
- Open pyproject.toml and fill in the client_id, client_secret, and user_agent according to the reddit application's values.
- Add your reddit username and password

## Setup Python
### Set up a venv (Recommended)
```
python3 -m venv .venv
source .venv/bin/activate
```

### Install Requirements
```
pip install -r requirements.txt
```

## Execute
### List CLI options
```
python run.py -h
```

### Get all subreddits you follow that haven't posted in the last six months
```
python run.py 6
```

### Launch inactive subreddits as browser tabs
```
python run.py 6 -b
```