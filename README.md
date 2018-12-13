# PoPS (Pest or Pathogen Spread) Model Django backend

## Overview

## Virtual Environment
We are using Pipenv for our virtual environment. To use, install on your system:
```
pip install pipenv
```
## To work on the PoPS Django backend
Clone the PoPS_Project repository. Check out the develpment branch.
```python
cd PoPS_Project  
pipenv install #create virtual environment and install dependencies  
pipenv shell #launch virtual environment  
python manage.py makemigrations #make migrations instructions for database  
python manage.py migrate #create or modify database  
python manage.py runserver #launch the server  
```
Launch browser to check if the website is running at: http://localhost:8000
