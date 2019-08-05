# PoPS (Pest or Pathogen Spread) Forecast and Control System Django and Web Interface

This is the repository for the dashboard for the PoPS forecast and control system. 

## Overview

## Contributing

This section is designed to clarify the branch structure of this repository and where new features and bug fixes should go.

### Branch Structure

1. **master** is the stable version of the model that is used for official releases and is the production branch of this repository. 
2. **staging** is the branch used to test new functionality in a live testing (i.e. the same as production) environment. This is where new functionality is implemented and testing before being merged with Master and 
2. **bugfix/thingnotworking** are branched off of **master** then merged back via a pull request once the bug is fixed.
3. **feature/new_feature** is where new features are developed before they are merged into **staging** via a pull request. For example, we are adding steering (aka adapative management) but this dramatically changes the dashboard and database so it is being built to test in **staging** before going to production.

### Bug Fixes

Most bugs/issues will be found in the **master** branch as it is the branch being used in production. Thus bug fixes should be merged into **master** once tested. Bug fixes should be released as minor versions (e.g. if major release is 1.0 then the first bug fix would be released as version 1.1).

### New Features

When creating new features create a branch from **master** using the following syntax **feature/new_feature**. For example, we want to add a transportation network model for human assisted dispersal, the branch created would be named feature/transportation_network_model (or similar). New features will be merged into **master** once tested based on the priorities of our stakeholders first. Once new features are tested in a live testing environment with any other new features being included in the next major release we will merge them into **master** and create an official major release version (e.g. update from version 1.1 to version 2.0). 

If you are interested in contributing to PoPS development and are not a core developer on the model, please take a look at following
documents to make the process as seamless as possible.

1. [Contributor Code of Conduct](contributing_docs/CODE_OF_CONDUCT.md)
1. [PoPS Style Guide](contributing_docs/STYLE_GUIDE.md)
1. [Contributor Guide](contributing_docs/CONTRIBUTING.md)

## Virtual Environment
We are using Pipenv for our virtual environment. To use, install on your system:
```
pip install pipenv
```
To run use
```
pipenv install
pipenv shell
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

## To edit the database using the admin site
First, create an admin user:
```python
cd PoPS_Project
python manage.py createsuperuser
```
Follow the prompts to create the admin user.

Then log in to the admin site at http://localhost:8000/admin
