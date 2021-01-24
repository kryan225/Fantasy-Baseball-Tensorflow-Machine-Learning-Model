Following through the tutorial: https://www.youtube.com/watch?v=ovql0Ui3n_I&t=1156s&ab_channel=CSDojo

To run a new server session:
    1. Open a conda prompt 
    2. Navigate to E:/Github/Django-test/
    3. 'pipenv shell'
    4. 'python manage.py runserver'
Now go to the url and it will start

Views.py:
    Where backend communicates with front end

models:
    Where DB schema is made

urls:
    url and path to code to cover it

test.html
    /sayHello html page


Ryan TODO: (1/23/2021)
    - Create DB schema to support python classes
        - you will do this in models.py, can start by googling 'django models'
    - translate old python to talk with DB instead of .csv's
    - Create a way to load in csv of projections to paste into DB
    - Show a leage in the UI 
    - Show a specific team in the UI (should pass team id through URL *look at deleteTodo*)
    