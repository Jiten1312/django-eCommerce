# DJango ECommerce
This is a simple e-commerce website created using Django. The project is associated with the University of Windsor. The project is built using the concepts tought in the Internet Application/Distributed System course.
</br>Instructor: Dr. Saja Al Mamoori

## Running the project
Clone the repository to your local machine. To run the project you can create virtual environment and install the dependencies using following command.
```
pip install -r requirements.txt
```

### Commands for migrations:
Tools &srarr; Run manage.py Task
In manage.py window:
```
makemigrations myapp
```
Check latest file in migrations dir
```
sqlmigrate myapp 0001
```
```
migrate
```

### Starting the server
```
python manage.py runserver
```

## The project follows MTC(Model Template Controller) architecture
### Model
The models are defined in models.py file 
- Client (extends User model from Django)
- Category
- Product
- Order
</br> This models are registered in `admin.py` file.

### Template
Templates can be found in `templates/myapp` directory. The configuration of the path can be found in `DIRS` variable of `settings.py` file.
- Templates are the text file and can generate any text based format(here, HTML).
- Taking input from user: Forms are created using `forms.py` file. Those forms can be rendered as paragraph(`form.as_p`) from the templates.
- All templates extends `base.html` file.
- base.html
</br>&srarr; This base file renders dynamic templates.
</br>&srarr; The Header and Footer are written in this file. 
</br>&srarr; This file is used to load JavaScript and Styles using CDN (i.e, JQuery Data Tables, BootStrap). 
</br>&srarr; Static assets are served using `{% load static %}` tag. static variable `STATIC_URL` is configured in settings.py file

### Controller
Controller is implemented using `views.py` file.
The controller implements following features:
- Authentication(Register, Login, Reset Password)
</br>&srarr; If you want to execute forgot password functionality, you have to setup `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` variables either in your os or using `.env` file and get your SMTP credentials from Google Developer Console.
- Manage Profile
</br>&srarr; Updating client profile such as Name, profile image, interests, address
- View Products(The templates are using JQuery Data Tables for search, sort and pagination)
- Place Order
- Login Redirect for unothorized access(using `login_required` decorator).
- Redirecting to pages according to requests after successful login using `next` parameter.

## Extending admin panel
In this project we have extended features of Django admin panel by implementing following actions in `admin.py` file.
- Refill the stock of the selected product.
- Viewing all the attributes of Client table.
- Viewing all the attributes of Client table.
