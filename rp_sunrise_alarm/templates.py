NGINX_CONF = """server {{
    listen 80;

    server_name {server_name};

    error_log  /var/log/nginx/error.log;

    location / {{
        proxy_pass         http://127.0.0.1:5000/;
        proxy_redirect     off;

        proxy_set_header   Host                 $host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }}
}}
"""

WEB_SERVICE = """[Unit]
Description=Raspberry Pi Sunrise Alarm Web Service

[Service]
Environment=FLASK_APP=rp_sunrise_alarm
ExecStart={bin_path}/flask run
User={user}

[Install]
WantedBy=multi-user.target
"""

MAIN_SERVICE = """[Unit]
Description=Raspberry Pi Sunrise Alarm Service

[Service]
ExecStart={bin_path}/rp-sunrise-alarm-daemon
User={user}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""
