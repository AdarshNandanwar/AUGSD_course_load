# AUGSD Course Load Project

The Course Load Project is a web portal built to automate the process of course load generation in various formats for the AUGSD office, BITS Pilani, K. K. Birla Goa Campus.
The frontend is built on React.js and the backend is built using Django python. The database used is PostgreSQL. Hosted using Heroku and AWS.

## Installation
Clone this repository into your system
```bash
git clone https://github.com/AdarshNandanwar/augsd-course-load.git
```
## Usage
1. Create and activate a virtualenv.
    ```bash
    sudo apt-get install python3-pip
    sudo pip3 install virtualenv 
    virtualenv venv 
    source venv/bin/activate
    ```
2. Install required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
3. Initial setup
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python populate.py
    cd client
    npm install
    npm run build
    cd ..
    ```
4. For AWS S3 setup (optional): Set up all environment variables and uncomment the code for boto3 and whitenoise in settings.py.
    ```
    export SECRET_KEY=""
    export DEBUG_VALUE="True"
    export DISABLE_COLLECTSTATIC="1"
    export AWS_ACCESS_KEY_ID=""
    export AWS_SECRET_ACCESS_KEY=""
    export AWS_STORAGE_BUCKET_NAME=""
    ```
    Note- Admin panel might not work without this properly (Server Error 500) setting up the AWS S3 storage bucket environment variables.
4. Run the server.
    ```bash
    python manage.py runserver <PORT_NUMBER> --insecure
    ```

---

## Contribute
### Create fork (one time)
- Press **Fork** button from [this](https://github.com/AdarshNandanwar/augsd-course-load) repository and select your account.
- In your GitHub fork, press **Clone or Download** and copy the url.
- Open the terminal and type: 
    ```bash
    git clone <copied_url>
    git remote add origin <copied_url>
    git remote add upstream https://github.com/AdarshNandanwar/augsd-course-load
    ```
- **IMPORTANT**: Create a branch development where you can do the changes, accepted changes will get merged with master branch
- **IMPORTANT**: Do the following to disable push on upstream handle
    ```bash
    git remote set-url --push upstream no_push
    ```

### Submiting PR
```bash
git add <filename>
# or to add everything using "git add ."
git commit -m <commit_message>
git pull upstream master
# Resolve merge conflicts (if any)
git push origin master
```
On your GitHub development branch, press **Compare & pull request** and then **Create Pull Request** on the next page

---
## Deployment
### AWS Deployment Guide
1. Clone the repo.
2. Run the server process in the new screen session window. Replace port_number with the port number available in the server.
  ```
  sudo venv/bin/python3 manage.py runserver 0.0.0.0:{port_number} --insecure
  ```
### Heroku Deployment Guide
#### Initial settings
1. Make sure to setup staticfiles app for css, js, images to load properly:
    1. Add all the STATICFILES_DIRS in settings.py:
        eg.
        ```python
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'client/build/static'),
            os.path.join(BASE_DIR, 'course_load/static'),
        ]
        ```
    2. Run:
        ```bash
        $ python manage.py collectstatic
        ```
        This will create an app named staticfiles containing all the static files of the project
    4. Disable collectstatic for deployment:
        ```bash
        $ heroku config:set DISABLE_COLLECTSTATIC=1
        ```
        - For React, read [this](https://librenepal.com/article/django-and-create-react-app-together-on-heroku/).
    5. Commit and push to heroku master.
2. Set environment variables in heroku console.
    ```bash
    export SECRET_KEY=""
    export DEBUG_VALUE="True"
    export DISABLE_COLLECTSTATIC="1"
    export AWS_ACCESS_KEY_ID=""
    export AWS_SECRET_ACCESS_KEY=""
    export AWS_STORAGE_BUCKET_NAME=""
    ```

#### Updating in production
Follow these steps to retain database after modification in the database schema.
1. Do all the changes in the development branch. Make sure all the new fields in the schema have some default value.
2. Merge in the development branch in master.
3. Delete local database [see steps below].
3. Download and load the database dump from heroku to local [see steps below].
4. Check if everything is working.
5. Push the changes to heroku master.
6. Check if everything is working, If yes, yay! We are done.
7. Else, dump the working local database to heroku.

#### Delete local database
1. Delete the sqlite database file (often named `db.sqlite3`) in your django project folder (or wherever you placed it).
2. Delete everything except `__init__.py` file from migration folder in all django apps.
3. Make changes in your models (`models.py`).
4. Run the command `python manage.py makemigrations` or `python3 manage.py makemigrations`.
5. Then run the command `python manage.py migrate`.

#### Dump Database: Heroku to Local
1. Delete the sqlite database file (often named `db.sqlite3`) in your django project folder (or wherever you placed it).
2. Delete everything except `__init__.py` file from migration folder in all django apps.
3. Run the following commands. Replace file name in th3 loaddata command with the latest file name of the database dump.
    ```bash
    $ heroku run python manage.py dumpdata --natural-foreign -- > data_dump_$(date +"%Y%m%d_%H%M%S").json
    
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py loaddata ${file_name}.json
    ```
#### Dump Database: Local to Heroku
1. Delete the sqlite database file (often named `db.sqlite3`) in your django project folder (or wherever you placed it).
2. Delete everything except `__init__.py` file from migration folder in all django apps.
3. 
    ```bash
    $ python manage.py dumpdata > data_dump_local_$(date +"%Y%m%d_%H%M%S").json
    
    $ heroku pg:reset
    $ heroku restart
    $ heroku run python manage.py makemigrations
    $ heroku run python manage.py migrate
    $ cat ${file_name}.json | heroku run --no-tty -a augsd-course-load -- python manage.py loaddata --format=json -
    ```