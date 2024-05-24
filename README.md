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



# [Creating a virtualenv with preinstalled packages as in requirements.txt](https://stackoverflow.com/questions/41427500/creating-a-virtualenv-with-preinstalled-packages-as-in-requirements-txt)
1. Clone Repo
    ```bash
    git clone https://github.com/SAMJ-CSDC26BB/SAMJ-Django-TBC.git
    ```
2. Switch to Cloned Repo
    ```bash
    cd SAMJ-Django-TBC
    ```
3. (if you don't already have virtualenv installed)
    ```bash
    pip install virtualenv
    ```
   Update pip if needed
    ```bash
    pip install --upgrade pip
    ```
4. To create your new environment (called 'env' here)
    ```bash
    python -m virtualenv env
    ```
5. To enter the virtual environment
    - For Mac/Linux
      ```bash
      source env/bin/activate
      ```
    - For Windows
      ```bash
      source env/bin/activate.ps1
      ```
6. To install the requirements in the current environment
    ```bash
    pip install -r requirements.txt
    ```