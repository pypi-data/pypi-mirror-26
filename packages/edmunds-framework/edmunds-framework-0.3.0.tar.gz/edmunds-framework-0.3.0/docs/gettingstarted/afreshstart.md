
# A Fresh Start

### 1. Create a new project

Let's first get an Edmunds Instance to kick-start your
project. Download it from:
> [https://github.com/LowieHuyghe/edmunds-instance/archive/master.zip](https://github.com/LowieHuyghe/edmunds-instance/archive/master.zip)

Unzip it, move it and rename it after your project.

### 2. Setup a virtual environment

Now setup a virtual environment for your project. If you
need some help with that, you can take a look at
[The Hitchhiker's guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Now activate your project's virtual environment.

### 3. Install the dependencies

First install some required setup packages:
```bash
pip install setuptools_scm
``` 

Now install all other dependencies:
```bash
pip install -r requirements.txt
```

### 4. Take it for a spin!

Let's take it for a spin and run the application:
```bash
python manage.py run
```

### 5. Google App Engine (optional)

If you want to develop for and run in Google App Engine
you'll first need to install the [App Engine SDK](https://cloud.google.com/appengine/docs/standard/python/download).

Then install the dependencies in the lib-directory:
```bash
pip install -r requirements.txt -t lib
```

Now start the development server and you are good to go:
```bash
dev_appserver.py app.yaml
```
