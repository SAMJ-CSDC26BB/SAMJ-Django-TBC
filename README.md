# Initialize 


pip install virtualenv
python3 -m venv env
source bin/activate
pip install django
django-admin startproject samjTBC
cd samjTBC
django-admin startproject samjTBC
python3 manage.py createsuperuser
python3 manage.py migrate
python3 manage.py createsuperuser
 - username
 - email
 - pwd

# start server
 python3 manage.py runserver
 
# verify if working 

http://127.0.0.1:8000/
http://127.0.0.1:8000/admin
 - login
user:admin



