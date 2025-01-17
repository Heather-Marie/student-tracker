import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("student", help="Creates a student")
@click.argument("id", default=9)
@click.argument("name", default="bill")
def create_user_command(id, name):
    create_student(id, name)
    print(f'{id} created!')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("review", help="Creates a review")
@click.argument("message", default="peepeepoopoo")
@click.argument("id", default=9)
@click.argument("upvote", default=1)
@click.argument("downvote", default=0)
def create_review_command(message, id, upvote,downvote):
    create_review( message, id, upvote, downvote)
    print(f'{message} created!')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("student_get", help="Creates a student")
def get_user_command( ):
    print(get_all_students())

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("f", help="Creates a f")
# def get_f( ):
#     myapp.db.session.commit()   #<--- solution!
#     myapp.db.drop_all()
#     print(get_all_students())

app.cli.add_command(user_cli) # add the group to the cli


'''
Generic Commands
'''

@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)