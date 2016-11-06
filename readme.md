# haproxy-config-generator

`haproxy-config-generator` is a simple Django app that will enable system and network administrators alike to manage their haproxy configuration within the Django admin. This project aims at giving more insight into the haproxy configuration and letting administrators edit their configurations more easily.

Furthermore, the base configuration template (as can be found and modified in `haproxy/config/templates/config.tpl`) has support for the excellent LetsEncrypt implementation provided by janeczku's [haproxy-acme-validation-plugin](https://github.com/janeczku/haproxy-acme-validation-plugin) and supports Outlook Anywhere (RPC over HTTP)

## Installation

Installation is as straight-forward as cloning the repository, optionally creating a virtual environment and installing Django.

```
# Optional: create and activate a virtualenv
virtualenv env/
source env/bin/activate

# Install dependencies (Django)
pip install -r requirements.txt

# Create a database and a user that can log in to the admin panel
cd haproxy/haproxy
python manage.py migrate
python manage.py createsuperuser

# Run the server
python manage.py runserver 
```

## Usage

After installation you can start the server with Django's built-in `manage.py runserver` command. The server will start on localhost, port 8000 by default. Alternatively, you can use other server software if you desire so.

You can update your configuration through the Django admin panel, located at http://localhost:8000/admin.

You can fetch your haproxy.cfg through the front page, located at http://localhost:8000/. Please note that you should first log in through the admin panel. You will not be able to fetch your configuration if you have not yet logged in.