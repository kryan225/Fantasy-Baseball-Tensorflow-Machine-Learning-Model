Following through the tutorial: https://www.youtube.com/watch?v=ovql0Ui3n_I&t=1156s&ab_channel=CSDojo

To run a new server session:
    1. Open a conda prompt 
    2. Navigate to E:/Github/Fantasy-Baseball...
    3. 'pipenv shell'
    4. 'python manage.py runserver'
Now go to the url and it will start

To interact with the DB
    1. Open a conda prompt
    2. Navigate to Github repo
    3. 'pipenv shell'
    4. 'python manage.py shell'
    5. 'from hello.models import [class_name]'

To run a DB migration
    0. Make whatever changes you want to models.py
    1. Opem Conda prompt
    2. Navite to Github repo
    3. 'pipenv shell'
    4. 'python manage.py makemigrations'
    5 Confirm changes if prompted 
    6. 'python manage.py migrate'

Making queries: https://docs.djangoproject.com/en/3.1/topics/db/queries/

Views.py:
    Where backend communicates with front end

models:
    Where DB schema is made

urls:
    url and path to code to cover it

test.html
    /sayHello html page


Ryan TODO: (1/23/2021)
    Done:
    - Create DB schema to support python classes xxx
        - you will do this in models.py, can start by googling 'django models'
----------------------------------------------------------------------
    - Display a team from the front end 
        - List out all players in correct positions
    - Display all teams from a league View (want this to be the home page)
        - Allow the ability to click on a team view it all 
    - Add ability for a team to draft a player and remove a player 
    - Show all players drafted/not drafted
    - Create a way to load in csv of projections to paste into DB
    - Add a draft board functionality
        - This is broad, you can put on new page or from league view
    - {finish draft functionality}
    - Add data analysis, aka the smart draft options