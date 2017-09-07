tuiuiu.io
=========

Saas application based on Wagtail.oi using django_tenants.


# Up & Running
   
etc/hosts
---------

    127.0.0.1       tuiuiu.io
    127.0.0.1       staging.tuiuiu.io
    127.0.0.1       prod.tuiuiu.io
    127.0.0.1       qa.tuiuiu.io    
    127.0.0.1       tenant.tuiuiu.io
    
   
create postgres database 
------------------------
      
    $ docker run -ti -e POSTGRES_PASSWORD=tuiuiutenant -e POSTGRES_USER=tuiuiutenant -e POSTGRES_DB=tuiuiutenant -p 5432:5432 -d postgres
    
git clone
---------
    
    $ git clone git@github.com:caputomarcos/tuiuiu.io.git
    $ cd tuiuiu.io 
    $ virtualenv env --python=python3 && source env/bin/activate
    $ make develop 
    $ cd app 
    $ python manage.py migrate_schemas
    $ python manage.py runserver 
        
or 
    
    $ virtualenv env --python=python3 && source env/bin/activate
    $ pip install git+https://github.com/caputomarcos/tuiuiu.io.git
    $ tuiuiu start app       
    $ cd app 
    $ python manage.py migrate_schemas
    $ python manage.py runserver 
    
credentials
-----------

    user: admin
    pass: admin

    
Credits
-------

Thank you for the wonderful work, Great Job!

   1. Tom Turner under the name `django-tenants`_.
   2. Bernardo Pires under the name `django-tenant-schemas`_.
   3. Vlada Macek under the name of `django-schemata`_.
   4. Tom Dyson under the name `wagtail`_
