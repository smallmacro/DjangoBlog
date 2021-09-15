# DjangoBlog
The `environment.yml` indicates the tools I used in this practice.

This project is my second django project. It is a step-by-step practice associtated to the [youtube tutorial by Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p).

The author tries to introduce the some common concepts within django framework and guide audiences to build a blog system hand-by-hand. [Source code](https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog) .

### Day 9 Updates:
We have added basic display blog  and support user to modify profile with username, email, profile image.
New concepts used:
  - introduce `django-crispy-form` module to handle the form feedbacks and validation. [Set up tutorial](https://django-crispy-forms.readthedocs.io/en/latest/install.html#installing-django-crispy-forms).
  - Profile and User is one-to-one relationship. `models.OneToOneField(on_delete=models.CASCADE)`
  - use Pillow module to handle the ImageField type. [Pillow documentation](https://pillow.readthedocs.io/en/stable/reference/Image.html).
  - Resize the uploaded image by overriding the `save()` method in `Profile` Class using the `user.profile.image.path`
  - Decorator `@login_required` from `from django.contrib.auth.decorators` used  when displaying user profile
  - `enctype="multipart/form-data"` needed to save image file by form POST method


### Day 10 Updates:
Implement the blog post list,post detail,post create,post update, post delete by using class based view (`ListView`,`DeteailView`,`CreateView`,`UpdateView`,`DeleteView`)

New concepts introduced:
  - Classes inheriting from class-based view have its default attribute and method as well as its default template name.
      1. `ListView` and `DetailView` will search for `<app_name>/<model_name>_viewtype.html`, while `CreateView` and `Update` will locate `<app_name>/<model_name>_form.html`, `DeleteView` will look for `<app_name>/<model_name>_confirm_delete.html`.
      2. `model = <Model_name>` is the same with `query_set = <Model_name>.objects.all()`, 'fields' will indicate the form fields in the `UpdateView` and `CreateView`
      3. After creating (`CreateView`)a post, the `Post` should define its `get_absolute_url`to indicate the url that will redirect to.
      4. When updating and creating a post, need to set the author of the post  to the login user(Foreign Key) within the overriding `form_valid()`method.
      5. `UpdateView` and `DeleteView` need to require the user authentication in which the author of post needs to be equal with the login user. `UserPassesTestMixin` and overriding `test_func()` do the job.


### Day 11 updates:
Introduce  and implement the pagination in Blog. Create new `ListView` with custom filted queries and an useful route for posts written by specific author.

New concepts:
- `django.views.generic.list.ListView` provides a builtin way to paginate the displayed list. You can do this by adding a `paginate_by` attribute to your view class.This limits the number of objects per page and adds a `paginator` and `page_obj` to the context.`ordering` can indicate the displaying sequence.

- By overriding the `get_queryset()` method, we can add customized filter to the object in the context. Paring with defining filter route, we can implement other customized filter . 


### Day 12 updates:
Email and password reset.Send a email with a link to reset password to gmail account.

Mail is sent using the SMTP host and port specified in the `EMAIL_HOST` and `EMAIL_PORT` settings. The `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` settings, if set, are used to authenticate to the SMTP server, and the `EMAIL_USE_TLS` and `EMAIL_USE_SSL` settings control whether a secure connection is used.

New concepts:
- `PasswordResetView` from auth.views : reset password through email 
- `PasswordResetDoneView` from auth.views : indicate the action when the request is done.
- `PasswordResetConfirmView`  : this view generates `uidb64` and `token`parameters for security check every time. So the route needs to consider these parameters.
- `PasswordResetCompleteView` show the render template when the reset is complete. 
- The email that the reset link will send to must be the same with user.email inthe database. Otherwise, Django will not send the email.
- set environment variable .`conda env config vars [list/set/unset]` and reactivate the environment to make  changes take effect.

#### Need to improve:

      


### Day 13 updates:
How to deploy the application to web server. [Django deployment checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)
Options:
1. Linux server:([Linode](https://linode.com/coreyschafer))
   - The first thing we need to do is set up the remote server environment:`adduser`,change directory and files mode, collect the package requirement and dependency. 
   - Install webserver: `Apache` or `nginx`. `sudo apt-get install apache2`,`sudo apt-get install libapache2-mod-wsgi-py3`.
   - Then configure the webserver: `cd /etc/apache2/sites-avaiable` and copy the `000-default.conf` to project directory and rename `project_name.conf`.Set `Alias /static  /home/<username>/<project_name>/static`
   - Add <Directory <path_topath>> Require all granted </Directory>  `static`,`media`,`wsgi.py`,  `WSGIScriptAlias / <full_path_to_wsgi.py>` , `WSGIDaemon Process django_app python-path=<full_path_to> pyt$ python-home=<full_path_to_enve>`  ,`WSGIProcessGroup django_app`
   -  `sudo a2ensite <django_project_name>` enable the site and disable the `000-default.conf`
   - change the owner of `<project_name>/db.sqlite3` : `sudo chown :www-data <project_name>/db.sqlite3` and `sudo chmod 664 <project_name>/db.sqlite3` and change the group owner to `www-data` : `sudo chown :www-data <project_name>`.And the same process to `media` folder .
   
Setting changes in Django project:
1. `ALLOW_HOSTS`
2. In production, we need to set up the `STATIC_ROOT`= `os.path.join(BASE_DIR,'static')` and run `pyhton manage.py collectstatic`
3. create a configure json file to handle secret info:`SECRET_KEY` and the environment variables `EMAIL_USER`, `EMAIL_PASS` in this project.
4. load the json file in `settings.py` : 
     ```python
     with open('<JSON_FILE>') as config_file:
        config = json.load(config_file)
     ```
5. Set `SECRET_KEY = congif['SECRET_KEY']`, `DEBUG=False` and update other environment virables(`EMAIL_USER` and `EMAIL_PASS`) 




### Day 14&15 updates:
Use a custom domain name for our application and enbale HTTPS with a free SSL/TLS Certificate using [Let's Encrypt](https://letsencrypt.org/) 
1. register a domain, set the domain DNS server. and add DNS records(`*`,`www`) in server manager.
2. add the domain name to `ALLOWED_HOSTS` in `settings.py`
3. [Start](https://letsencrypt.org/getting-started/) to select the webserver framework and operating system. [Get your site on HTTPS](https://certbot.eff.org/). Follow the instructions to install neccessary packages.
4. Update the Apache configure file: `<project_name>.conf`: add the `ServerName :....`  comment out the `WSGISCriptAlias`,`WSGIDaemonProcess`, `WSGIProcessGroup`
5. `sudo cerbot --apache`  
6. add the `https` to utf allow.
7. Since the certificate needs to be renewed every 90 days, so we need to automatically renew the task: 

       ```sh
       sudo cerbot renew --dry-run
       sudo crontab -e
       #m h dom mon dow   command
       30 4 1 * * sudo cerbot renew --quiet
       
       ```


### Day 16 updates:
Using AWS S3 for File Uploads.[Django storage S3 Docs](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)

Save the secret info from AWS S3 in the configure file.
Change the `settings.py`:
```python
# add the INSTALLED_APP: storages
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_ACCESS_ACCESS_KEY = os.environ.get('AWS_ACCESS_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE =  False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

``` 
Need to remove the `save()`method in `users` models since the `Pillow` conflicts with usage of AWS S3 storages.

#### Deploy the application using Heroku.
[Configuring Django Apps for Heroku](https://devcenter.heroku.com/articles/django-app-configuration)

Remember to add `sudo` when facing permission denied issues!!!



##### Steps:
1. [Download and install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) 

2. [Get a Heroku acount](https://www.heroku.com/) and Login `sudo heroku login`(Open the browser to login) or `sudo heroku login -i`(Login in the CLI)

3. Create and upload the website.
```sh
    heroku create <app_name>
```
This creates a git remote ("pointer to a remote repository") named `heroku` in our local git environment.


4. Push file to Heroku
```sh
    git push heroku main
```
will push the files to the heroku remote,it will intall all packages in `requirements.txt`. 

In order to execute your application `Heroku` needs to be able to set up the appropriate environment and dependencies, and also understand how it is launched. For Django apps we provide this information in a number of text files:

   - `runtime.txt`: the programming language and version to use.
   - `requirements.txt`: the Python component dependencies, including Django.
   - `Procfile`: A list of processes to be executed to start the web application. For Django this will usually be the Gunicorn web application server (with a .wsgi script).
   - `wsgi.py`: WSGI configuration to call our Django application in the Heroku environment.

`requirements.txt`:
```txt
django==3.1.2
dj-database-url==0.5.0
django-crispy-forms==1.12.0
django-heroku
```

Most importantly, Heroku web applications require a `Procfile`.
This file is used to explicitly declare your application’s process types and entry points. It is located in the root of your repository.This Procfile requires `Gunicorn`, the production web server that we recommend for Django applications.


Set `Procfile`:
```
web:gunicorn <project_name>.wsgi

```

```
Be sure to add gunicorn to your requirements.txt file as well.

```
5. install and use `git`.set `.gitignore` file [Github gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore) add `.DS_Store` to ignore file. Commit all the file to local tree. 


6. On Heroku, sensitive credentials are stored in the environment as `config vars`.The `django-heroku` package automatically configures your Django application to work on Heroku. It is compatible with Django 2.0 applications.

Django-heroku Installer: `conda install -c conda-forge django-heroku`

```
Be sure to add django-heroku to your requirements.txt file as well.

```
Set heroku configure: `heroku config:set <VARS_NAME> = <VARS_VALUE>`

Add the following `import` statement to the top of settings.py:

```python
import django_heroku
# Activate Django-Heroku.
django_heroku.settings(locals())




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

Django won’t automatically create the target directory (STATIC_ROOT) that collectstatic uses, if it isn’t available. You may need to create this directory in your codebase, so it will be available when collectstatic is run. Git does not support empty file directories, so you will have to create a file inside that directory as well.



8. We use `sqlite3` in development environment and transfer to `Postgres` in production. `heroku addons:create ` can create any database heroku supports.
`heroku pg` will show the detail about `postgresql` heroku has installed

`heroku run python manage.py migrate` can migrate the database tables that already exists in the dev environment. 
or use the heroku bash command line:
```sh
   heroku run bash
   python manage.py createsuperuser
   exit
   heroku open

```

9. Add the `<project_name>.herokuapp.com` to `ALLOWED_HOSTS`


10. Debugging.The Heroku client provides a few tools for debugging:
```sh

# Show current logs
heroku logs

# Show current logs and keep updating with any new results
heroku logs --tail

# Add additional logging for collectstatic (this tool is run automatically during a build)
heroku config:set DEBUG_COLLECTSTATIC=1

# Display dyno status
heroku ps
```



















