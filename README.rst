Raspberry Pi Sunrise Alarm
==========================

Use a Raspberry Pi connected to WS2801-based RGB LED strip to
wake you up in the morning.

Development
-----------

Prerequisites
~~~~~~~~~~~~~

Make sure you have the following software packages available
on your system:

 * Python (≥ 3.6) with ``virtualenv``
 * Node.js (≥ 6.x)
 * Redis

Get the source code
~~~~~~~~~~~~~~~~~~~

Clone this repository::

    git clone git@github.com:sebasgo/rp-sunrise-alarm.git

Installation
~~~~~~~~~~~~

Execute the following commands inside your working copy
of the repository:

1.  Setup a new Python virtual environment::

        virtualenv --python python3 venv

2.  Activate the environment::

        source venv/bin/activate

3.  Install the package with its dependencies::

        pip install -e .[dev]

4.  Create the database::

        FLASK_APP=rp_sunrise_alarm flask initdb

5.  Install the dependencies for the frontend::

        cd
        npm install

Running
~~~~~~~

The application consists of three distinct components which
all have to be running at the same time in order to function
properly. Also, you need to start a Redis server.

1.  Redis::

        redis-server

    This command can be executed from any working directory.


2.  Frontend Vue.js application::

        cd rp_sunrise_alarm/frontend
        npm run dev

    This will serve the frontend application at
    http://localhost:8080/ . The application won't work
    properly though because it can't access the backend API.

3.  Backend Flask application::

        FLASK_APP=rp_sunrise_alarm FLASK_DEBUG=1 flask run

    In debug mode the Flask application will act as an
    proxy for the frontend application, so you can test
    changes to the frontend application without the need
    build it every time.

    You can access the web frontend at: http://127.0.0.1:5000/

4.  Execute the daemon::

        DEBUG=1 rp-sunrise-alarm-daemom

    The daemon controls the LED stripe and makes sure it
    lights up at the programmed alarms.

    In debug mode, the daemon won't actually try
    to program a LED stripe. Instead, it will use
    Pygame to display the intended result in a window.
