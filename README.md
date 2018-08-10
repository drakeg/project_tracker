# project_tracker

## Setting up Django REST Framework

1. Install djangorestframework using pip
2. Add 'restframework' to your INSTALLED_APPS list in settings.py
3. Create serializers.py and add serializers for each model you would like 
to serve via the API
4. Create model ViewSets for each model, which automatically configures 
Create, Read, Update, and Delete (CRUD) endpoints for each model
   * **[Optional]** add create and update methods wherever you want to add or update
   data to/from multiple tables (across ForeignKeys) in the same API request
5. Add the ViewSets to urls.py to configure the endpoints to use

## Configuring Cross Origin Request Security (CORS)
*CORS is a web specification that allows fine-grained control over which
URLs/Hosts/Domains are allowed to serve javascript that fetch data from your 
application.  We are configuring this app to use the most permissive setting,
to avoid issues during development, but when the app nears production, it 
should probably be configured to be much more selective*

1. Install django-cors-headers using pip
2. Add 'corsheaders' to your INSTALLED_APPS list in settings.py
3. Add the line `CORS_ORIGIN_ALLOW_ALL = True` to settings.py
   * This configures the application to allow any host to serve javascript
   which performs CRUD operations in this app
