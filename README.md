# Auntie's Cool Club

Description

the purpose of this app is to communicate with my Nephews in North America and to teach them to code. The home Page reflects a Django Chat. however, more code subject chats are to follow. 

[**Live site**]([https://gloss-37a7c75fa1bb.herokuapp.com/](https://aunties-coolclub-6c09b0cba0e7.herokuapp.com/))

![Device Mockups]()


## Heroku Deployment

The site was deployed to Heroku. The steps to deploy are as follows:

- Navigate to heroku and create an account
- Click the new button in the top right corner
- Select create new app
- Enter app name
- Select region and click create app
- Click the resources tab and search for Heroku Postgres
- Select hobby dev and continue
- Go to the settings tab and then click reveal config vars
- Add the following config vars:
  - AWS_SECRET_ACCESS_KEY: (Your secret key)
  - AWS_ACCESS_KEY_ID: (This should already exist with add on of postgres)
  - EMAIL_HOST_USER: (email address)
  - EMAIL_HOST_PASS: (email app password)
  - CLOUNDINARY_URL: (cloudinary api url)
- Click the deploy tab
- Scroll down to Connect to GitHub and sign in / authorize when prompted
- In the search box, find the repositoy you want to deploy and click connect
- Scroll down to Manual deploy and choose the main branch
- Click deploy

The app should now be deployed.

## Run Locally

~~~bash

# Clone the project

  git clone https://github.com/CodeConnoisseur74/aunties-cool-club.git

# Go to the project directory

  cd aunties-cool-club

# Install dependencies

  pip3 install -r requirements.txt

# Start the server
  python3 manage.py runserver

~~~

Note that you will have to setup your own database and API connections using these steps:

1. Create a file name "env.py" in the projects root directory.
2. Copy and paste this code in the env.py file and replace values with your own:

~~~python

import os

os.environ["AWS_ACCESS_KEY_ID"]=YOUR_AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"]=YOUR_AWS_SECRET_ACCESS_KEY
os.environ["AWS_STORAGE_BUCKET_NAME "]=AWS_STORAGE_BUCKET_NAME
os.environ["SECRET_KEY"]=YOUR_SECRET_KEY

~~~

## Technologies

- HTML
  - The structure of the Website was developed using HTML as the main language.
- CSS
  - The Website was styled using custom CSS in an external file.
- Python
  - Python was the main programming language used for the application using the Django Framework.
- GitHub
  - Source code is hosted on GitHub
- Git
  - Used to commit and push code during the development of the Website
- Font Awesome
  - This was used for various icons throughout the site
- Favicon.io
  - favicon files were created at <https://favicon.io/favicon-converter/>
- Canva
  - wireframes were created using Canva <https://canva.com/>

## External Python Modules

- asgiref==3.7.2 - Used for building asynchronous Python web applications, especially with django.
- cloudinary==1.29.0 - Cloundinary was set up for use but no custom uploads were made, settings remain for future development
- crispy-bootstrap5==0.6 - This was used to allow bootstrap5 use with crispy forms
- dj-database-url==0.5.0 - Used to parse database url for production environment
- Django==4.2.10 - Framework used to build the application
- django-allauth==0.57.2 - Used for the sites authentication system, sign up, sign in, logout, password resets ect.
- django-crispy-forms==2.1 - Used to style the forms on render
- gunicorn==20.1.0 - Installed as dependency with another package
- oauthlib==3.2.0 - Installed as dependency with another package
- psycopg2==2.9.9 - Needed for heroku deployment
- python3-openid==3.2.0 - Installed as dependency with another package
- requests-oauthlib==1.3.1 - Installed as dependency with another package (allauth authentication)
- sqlparse==0.4.4 - Installed as dependency with another package
- urllib3==1.26.18 - Installed as dependency with another package
- whitenoise==5.3.0 - Used to serve static files directly without use of static resource provider like cloundinary

## Security

### Cross-Site Request Forgery (CSRF) Protection

- Implementing CSRF protection helps prevent malicious websites from executing unauthorized actions on behalf of authenticated users.
- Django provides built-in CSRF protection by including a CSRF token with each form submission and verifying it on the server side.

### Django Allauth for Authentication and Authorization

- Django Allauth is an authentication and authorization framework that provides features like registration, login, password management, and social authentication.
- It ensures secure user authentication and authorization processes.

### Restricted Features for Authenticated Users

- Certain features, such as creating, editing, or deleting notes , are reserved for authenticated users only.
- By requiring users to be logged in to access these features, the application enhances security and ensures that sensitive operations are performed by authorized individuals only.

## Credits

**Media**:
- Fontawesome for icons

**Other Credits**:

- ChatGPT has been used for content text ONLY. No code has been written with ChatGPT

- This is a Pybites PDM Project. https://pybit.es/
