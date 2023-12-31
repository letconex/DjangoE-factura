python.exe -m pip install --upgrade pip
pip freeze > requirements.txt
pip install --upgrade -r requirements.txt

You can use multiple SQLite databases in your Django application.
You can create a separate database for your CRM data and another one for user administration 1.
To use multiple databases in Django, you need to define the databases in your settings.py file.
You can define the databases using the DATABASES setting 2.
Here is an example of how you can define two databases in your settings.py file:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'vendors': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'vendors.sqlite3',
    }
}
python manage.py migrate --run-syncdb
--run-syncdb - Creates tables for apps without migrations.
python manage.py makemigrations app
python manage.py migrate app
python manage.py --database=vendors
manage.py schemamigration research --auto

    python manage.py migrate (app name)
    python manage.py makemigrations
    python manage.py makemigrations (app name)

In this example, we have defined two databases: default and vendors. The default database is the default database that Django uses.
The vendors database is the database that we will use for our CRM data.
To use the vendors database in your Django application, you can specify the database name in your model’s Meta class
class CRMModel(models.Model):
    # fields

    class Meta:
        db_table = 'crm_table'
        app_label = 'crm_app'
        managed = False
        using = 'vendors'

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add =True)
    first_name = models.CharField(max_length =50)
    last_name = models.CharField(max_length =50)
    email = models.CharField(max_length =100)
    phone = models.CharField(max_length =15)
    address = models.CharField(max_length =100)
    city = models.CharField(max_length =50)
    state = models.CharField(max_length =50)
    zipcode = models.CharField(max_length =20)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
class ParentModel(models.Model):
    parent_field_1 = models.CharField(max_length=10)
    parent_field_2 = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['parent_field_1', 'parent_field_2'],
                name='unique_parent'
            )
        ] 

class ChildModel(ParentModel):
    child_field_2 = models.CharField(max_length=10, unique=true)
    # this being unique means that only one parent can have a child like this 

class UnInheritedChild(models.Model):
    child_field_1 = models.CharField(max_length=10)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)