# FundamentalProject
## Presentation
![Presentation](https://github.com/devops-cohort/vieran/blob/test/Documentation/Fantasy_Football_Presentation.pptx)

## The Scope
The aim of this project was to create an application with full CRUD functionality, which utilised version control, continuous integration and automated deployment

## My Application
To satisfy this brief, I designed a fantasy football application, in which users could create and edit and account, create teams, view their teams, and delete teams or delete their account

## Planning
To plan this project, I used a Trello board to design the functionality that the app would provide:
![Trello board](https://github.com/devops-cohort/vieran/blob/test/Documentation/Trello_board.png)

An Entity Relationship Diagram was made to describe the tables, and their relationship to each other:
![ERD](https://github.com/devops-cohort/vieran/blob/test/Documentation/ERD.png)

A use case diagram was also made, to show the interactions between the user and the database for all of the functionality of the application:

![Use case diagram](https://github.com/devops-cohort/vieran/blob/test/Documentation/Use_case.png)

Finally, a risk assessment was undertaken, to analyse any potential problems which would be faced in creating, deploying, and maintaining the application, and minimising these risks:

| Risk      | Impact         | Likelihood  | Mitigation measure |
| :-------------: |:-------------:| :-----:|:------: |
| Losing code     | Medium | Medium | Regular uploads to GitHub |
| Website malfunctions from bad code     | Medium | High | Regular testing of code and website, throughout creation of application |
| External database manipuation    | High | Medium | No database information is stored in code, through use of environmental variables |
| Passwords compromised through database hack    | High | Medium | All passwords are hashed before being stored in database, so no plaintext passwords are stored in the database |
| External SSH into VM     | High | Low | Tolerate - Google security is most likely better than any solution I can make |

## Creation and Deployment
The backend code was written in Python, using Flask as the web development framework, and HTML for the front end. SQLAlchemy was utilised to link the Python code to the MySQL database, and Jinja2 was used to link the Python code to the HTML code. Trello was used as the project tracking tool, with Git as the version control system. Jenkins to used as the CI server, with Pytest used for unit testing and Gunicorn for the deployment of the application. A webhook was created so any pushes to GitHub from the source code would trigger the Jenkins build, and deployment via Gunicorn would be automated through this process. A CI Pipeline was created to illustrate this process:
![CI Pipeline](https://github.com/devops-cohort/vieran/blob/test/Documentation/CI_Pipeline.png)
