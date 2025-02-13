# Python by example

## Intro 
The reference material is a bit old and a few modifications were required to get this working. Future plans to 
extend it further with some extra features.

## References
* https://realpython.com/flask-by-example-part-1-project-setup/
    * NOTE: set up the project without using heroku
* https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
* https://realpython.com/flask-by-example-part-3-text-processing-with-requests-beautifulsoup-nltk/
* https://realpython.com/flask-by-example-implementing-a-redis-task-queue/

## Setup new virtual env and install modules
* python3 -m venv venv
* source venv/bin/activate

## Setup from requirements.txt
* python -m pip install -r requirements.txt

## Empty requirements? try:
* python -m pip install Flask
* python -m pip install psycopg2 Flask-SQLAlchemy Flask-Migrate
* python -m pip install python-dotenv
* python -m pip install requests beautifulsoup4 nltk
* python -m pip install redis rq
* python -m pip install rq-dashboard
* python -m pip freeze > requirements.txt

## Do you need to fix psycog2 wheel issues? 
Note: if there is an error with installing / building wheel with psycopg2 : 
* sudo apt update:
* sudo apt install -y libpq-dev python3-dev

## Running dependencies: postgres, pgadmin4, redis
* make startTestEnv

## Initialise postgres schema from scatch
* make createdb
* make migrateInit

## Migrations after initialise
* make migrate

## Download nltk_data
https://www.nltk.org/ natural language tool kit
* create toolkit data folder in your virtual env folder
    * mkdir /home/<your user folder/<repo folder>/flask-by-example/venv/nltk_data
* python -m nltk.downloader
    * setup the download dir config using c (Config)
    * d and choose dir for <repo abs path>/venv/nltk_data
    * select d for download 
    * type : punkt after the Identifiers prompt.
* for some reason the app is looking for punkt_tab? https://github.com/nltk/nltk/issues/3293 to fix:
    * python prompt: 
        * import nltk
        * nltk.download('punkt_tab')  

## Running app
In separate terminals:
* make server
* make worker

## Check redis queue
In a separate terminal:
* rq-dashboard
* open browser for http://0.0.0.0:9181



