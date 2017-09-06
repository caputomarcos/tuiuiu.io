tuiuiu.io
=========

Saas application based on Wagtail.oi using django_tenants.


# Up & Running
   
create postgres database 
------------------------
      
    $ docker run -ti -e POSTGRES_PASSWORD=tuiuiutenant -e POSTGRES_USER=tuiuiutenant -e POSTGRES_DB=tuiuiutenant -p 5432:5432 -d postgres
    
git clone
---------
    
    $ git clone git@github.com:caputomarcos/tuiuiu.io.git && \
    cd tuiuiu && \ 
    virtualenv env --python=python3 && \
    source env/bin/activate && \
    python setup.py install && \
    make develop && \
    cd app && \ 
    python manage.py migrate_schemas
        

Credits
-------

Thank you for the wonderful work, Great Job!

   1. Tom Turner under the name `django-tenants`_.
   2. Bernardo Pires under the name `django-tenant-schemas`_.
   3. Vlada Macek under the name of `django-schemata`_.
   4. Tom Dyson under the name `wagtail`_
