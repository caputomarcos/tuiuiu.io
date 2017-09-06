tuiuiusaas
===========

Saas application based on Wagtail.oi using django_tenants.


#Up & Running
   
create postgres database 
------------------------
      
    $ docker run -ti -e POSTGRES_PASSWORD=tuiuiutenant -e POSTGRES_USER=tuiuiutenant -e POSTGRES_DB=tuiuiutenant -p 5432:5432 -d postgres
    
git clone
---------
    
    $ git clone git@github.com:caputomarcos/tuiuiu.git && \
    cd tuiuiu && \ 
    virtualenv env --python=python3 && \
    source env/bin/activate && \
    python setup.py install && \
    tuiuiu start app && \
    cd app && \ 
    python manage.py migrate_schemas
    

tenants 
-------

    $ python manage.py shell << EOF
    from customers.models import Client    
    # mobb.io
    Client(domain_url='mobb.io',
    schema_name='public',
    name='mobb.io',
    description='Mobb io').save()   
    # devel1.mobb.io 
    Client(domain_url='devel1.mobb.io',
    schema_name='tenant1',
    name='Tenant1 - Awesome',
    description='Our first real tenant, awesome!').save()    
    # devel2.mobb.io 
    Client(domain_url='devel2.mobb.io',
    schema_name='tenant2',
    name='Tenant2 - Even Awesome-r',
    description='A second tenant, even more awesome!').save()
    EOF

createsuperuser
---------------

    $ python manage.py createsuperuser
    Enter Tenant Schema ('?' to list schemas): ?
    public - mobb.io
    tenant1 - devel1.mobb.io
    tenant2 - devel2.mobb.io
    Enter Tenant Schema ('?' to list schemas): public
    Username (leave blank to use 'root'): admin
    Email address:
    Password:
    Password (again):
    Superuser created successfully.


# Credits

