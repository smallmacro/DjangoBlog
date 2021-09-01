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
      3. After creating a post, the `Post` should define its `get_absolute_url`toindicate the url that will redirect to.
      4. When updating and creating a post, need to set the author of the post  to the login user(Foreign Key) within the overriding `form_valid()`method
      