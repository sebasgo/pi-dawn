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

These instructions install Pi Dawn for the default Raspbian user ``pi``. Run all command as this user.

1.  Download Raspbian, flash it to a SD card and configure the system
    to your liking (network configuration, SSH access, locale etc.)

2.  Setup Raspbian for Pi Dawn

    Run::

        sudo raspi-config

    Then select *Localisation Options* → *Change Timezone*. Pick the
    timezone you are living in from the list.

    Then select *Interfacing Options* → *P4 SPI*. Answer *Yes* to
    enable the SPI interface.

3.  Allow the user ``pi`` to access the SPI interface::

        sudo gpasswd -a pi spi

    In order to become effective, you have to log in again.

4.  Install required Raspbian packages::

        sudo apt -y install python3 python3-venv redis-server nginx vlc-nox

    This installs Python 3 with the ``venv`` module, Redis and Nginx.

5.  Create an virtual Python environment for Pi Dawn::

        cd ~
        python3 -m venv pi-dawn

6.  Install Pi Dawn::

        ./pi-dawn/bin/pip install pi_dawn

7.  Create the database::

        mkdir pi-dawn/var
        FLASK_APP=pi_dawn ./pi-dawn/bin/flask initdb

8.  Setup services::

        sudo -s
        FLASK_APP=pi_dawn ./pi-dawn/bin/flask setup-nginx
        FLASK_APP=pi_dawn ./pi-dawn/bin/flask install-services
        exit

    The first command will add a new site to act as a proxy for the
    Flask web application, disable the conflicting default site,
    validate the NGINX configuration for good measure and reload
    NGINX to make the changes effective.

    This second command will install Systemd service units for the
    web frontend and the alarm daemon. After this, it starts the
    services and configures them for automatic launch at boot.

That's it. You can access the web interface on port 80 of your
Raspberry Pi. Use it to configure alarms or as a light switch.

Development
-----------

Prerequisites
~~~~~~~~~~~~~

Make sure you have the following software packages available
on your system:

* Python (≥ 3.5)
* Node.js (≥ 10.x)
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

        python3 -m venv venv

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


2.  Backend Flask application::

        FLASK_APP=pi_dawn FLASK_DEBUG=1 flask run

    While developing the Flask application only serves the backend API.

3.  Frontend Vue.js application::

        cd pi_dawn/frontend
        npm run serve

    You can access the web frontend at: http://127.0.0.1:8081/

4.  Execute the daemon::

        DEBUG=1 pi-dawn-daemon

    The daemon controls the LED stripe and makes sure it
    lights up at the programmed alarms.

    In debug mode, the daemon won't actually try
    to program a LED stripe. Instead, it will use
    Pygame to display the intended result in a window.
