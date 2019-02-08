# UPSMON
UPSMON is a tool to monitor upses, will be able to send warnings, display everything in a web interface and check multiple upses

## Virtual Enviroment
You should create and activate virtual environment:

```
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
```

If there is a problem [consult this](https://virtualenv.pypa.io/en/stable/installation/)

## Install dependecises

When in your virtualenviroment just run

```
pip install -r requirements.txt
```

## Install application
To install the required configs for this application just run the install.py script.

## Run application

open the terminal and write ```flask run``` then browse to [locaclhost:5000](http://localhost:5000)