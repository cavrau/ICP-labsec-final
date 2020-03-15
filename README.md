# ICP-LABSEC

This is an python repo used to be part of the admission process of UFSC's LabSec

## Site

The web service is published at <https://ipc-front.herokuapp.com/> with the front-end. And it communicates with the backend. With all 4 funcionalities.

## How to install and run the backend

You should use a python virtual environment.

First you should download python3 with pip3.

Then to install a virtual environment creating tool use the command:

``` bash
pip3 install virtualenv
```

Use the following command to create a virualenv:

``` bash
virtualenv -p python3 .env
```

Then activate it by using:

``` bash
source .env/bin/activate
```

Download project dependencies with:

``` bash
pip install -r requirements.txt
```

Then you should enter the webservice directory:

``` bash
cd webservice
```

Remove the actual database:

``` bash
rm db.sqlite3
```

Create a new database:

``` bash
python manage.py migrate
```

Run the app:

``` bash
python manage.py runserver
```

The commands from running the front are in the md file of the ipc-labsec directory.
