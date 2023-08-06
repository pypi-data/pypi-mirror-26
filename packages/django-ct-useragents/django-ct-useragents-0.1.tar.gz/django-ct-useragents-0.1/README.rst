=====
Useragents
=====

Useragents is a simple app to track the user agents, ips and other info
of the various visitors of your django site. The information is stored in
the database for easy reference and exporting.

Quick start
-----------

1. Add "useragents" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'useragents',
    ]
    
2. Add useragents to the middleware:
	MIDDLEWARE_CLASSES = [
		...
		'useragents.utils.UserAgentsMiddleware',
		...
	]

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   see the info on your visitors

