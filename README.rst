Pi Dawn
=======

Use a Raspberry Pi connected to WS2801-based RGB LED strip to
wake you up in the morning.

Setup
-----

Hardware
~~~~~~~~

...

Software
~~~~~~~~

1.  Download Raspbian, flash it to a SD card and configure the system
    to your liking (basic network configuration, SSH access, locale etc.)

2.  Configure the correct time zone::

        sudo raspi-config

    Select *Localisation Options* → *Change Timezone*. Pick your
    timezone from the list.

3.  Enable the SPI interface::

        sudo raspi-config

    Select *Interfacing Options* → *P4 SPI*. Answer *Yes*.

5.  Allow the the user ``pi`` to access the SPI interface::

        sudo gpasswd -a pi spi

    In order to become effective, you have to log in again.

6.  Install Python 3 with the ``venv`` module , if not yet available::

        sudo apt-get install python3 python3-venv

7.  Install the Redis::

    sudo aptitude install redis-server

8.  Create an virtual Python environment for the Pi Dawn::

        cd ~
        python3 -m venv pi-dawn

9.  Install Pi Dawn::

        ./pi-dawn/bin/pip install pi_dawn

10. Create the database::

        mkdir pi-dawn/var
        FLASK_APP=pi_dawn ./pi-dawn/bin/flask initdb

11. Install NGINX::

        sudo apt-get install nginx

12. Setup NGINX::

        sudo -s
        FLASK_APP=pi_dawn ./pi-dawn/bin/flask setup_nginx

    The command will add a new site to act as a proxy for the
    Flask web application, disable the conflicting default site,
    validate the NGINX configuration for good measure and reload
    NGINX to make the changes effective.

13. Setup services:

        sudo -s
        FLASK_APP=pi_dawn ./pi-dawn/bin/flask install_services

    This command will install Systemd service units for the web
    frontend and the alarm daemon. After this, it starts the
    services and enables them so they are automatically started
    at boot.

That's it. You can access the web interface on port 80 of your
Raspberry Pi. Use it to configure your alarms or as a light
switch.

Development
-----------

Prerequisites
~~~~~~~~~~~~~

Make sure you have the following software packages available
on your system:

 * Python (≥ 3.5) with ``virtualenv``
 * Node.js (≥ 6.x)
 * Redis

Get the source code
~~~~~~~~~~~~~~~~~~~

Clone this repository::

    git clone git@github.com:sebasgo/pi-dawn.git

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

        FLASK_APP=pi_dawn flask initdb

5.  Install the dependencies for the frontend::

        cd pi_dawn/frontend
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

        cd pi_dawn/frontend
        npm run dev

    This will serve the frontend application at
    http://localhost:8080/ . The application won't work
    properly though because it can't access the backend API.

3.  Backend Flask application::

        FLASK_APP=pi_dawn FLASK_DEBUG=1 flask run

    In debug mode the Flask application will act as an
    proxy for the frontend application, so you can test
    changes to the frontend application without the need
    build it every time.

    You can access the web frontend at: http://127.0.0.1:5000/

4.  Execute the daemon::

        DEBUG=1 pi-dawn-daemon

    The daemon controls the LED stripe and makes sure it
    lights up at the programmed alarms.

    In debug mode, the daemon won't actually try
    to program a LED stripe. Instead, it will use
    Pygame to display the intended result in a window.
