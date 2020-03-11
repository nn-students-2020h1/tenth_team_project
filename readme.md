# Intel Python Course Telegram Bot
This is a repository for Telegram bot that will be developed during Intel Academic Program Python Course.

## Clone repository
```
git clone https://github.com/nn-students-2020h1/tenth_team.git
cd tenth_team
```

## Set up and activate python environment

Install latest python:
```

python=python3.8
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update --ignore-missing
sudo apt install -y  $python-dev $python-venv
```

Download and install pip (package manager):
```
wget https://bootstrap.pypa.io/get-pip.py
$python get-pip.py
``` 

Create and activate python environment:
```
$python -m venv venv
source venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

## Set up .env variables and run bot

Сreate a .env file containing the bot configuration
```..env
TG_TOKEN = "your_token"
TG_PROXY = "your_proxy_url"
```

Run bot
```
python main.py
```