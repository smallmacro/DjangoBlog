# DjangoBlog
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
       ```shell
       sudo cerbot renew --dry-run
       sudo crontab -e
       #m h dom mon dow   command
       30 4 1 * * sudo cerbot renew --quiet

       ```
