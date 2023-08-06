=====
Monitor
=====

Monitor exposes a JSON endpoint to your system to check on system information


Quick start
-----------

1. Add "monitor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'monitor',
    ]

2. Include the monitor URLconf in your project urls.py like this::

    url(r'^stats/', include('monitor.urls')),

4. Start the development server and GET http://127.0.0.1:8000/stats/
   to get the JSON (You may want to enable CORS, if consuming directly from a browser).
