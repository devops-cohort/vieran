from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User, Player, Team
from application import login_manager
from flask_login import current_user



class RegistrationForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    first_name = StringField("First Name",
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    last_name = StringField("Last Name",
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    username = StringField('Username',
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField('Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use!')

    def validate_username(self, username):
        user_name = User.query.filter_by(username=username.data).first()
        if user_name:
            raise ValidationError("Someone's already taken that username!")

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField("First Name",
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    last_name = StringField("Last Name",
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )

    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    username = StringField('Username',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already in use - please choose another')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already in use - please choose another')

gkdata = Player.query.filter_by(position="GK").all()
defdata = Player.query.filter_by(position="DEF").all()
middata = Player.query.filter_by(position="MID").all()
fwddata = Player.query.filter_by(position="FWD").all()

gk_choices=[]
def_choices=[]
mid_choices=[]
fwd_choices=[]

for i in range(len(gkdata)):
    gk_choices.append([gkdata[i].last_name, gkdata[i].last_name + ": " + gkdata[i].club])

for i in range(len(defdata)):
    def_choices.append([defdata[i].last_name, defdata[i].last_name + ": " + defdata[i].club])

for i in range(len(middata)):
    mid_choices.append([middata[i].last_name, middata[i].last_name + ": " + middata[i].club])

for i in range(len(fwddata)):
    fwd_choices.append([fwddata[i].last_name, fwddata[i].last_name + ": " + fwddata[i].club])

## Comment out createteamform when creating databases
class CreateTeamForm(FlaskForm):

    team_name = StringField('Team name',
        validators=[
            DataRequired(),
            Length(min=2, max=25)
        ]
    )
    
    goalkeeper = SelectField('Goalkeeper',
        choices=gk_choices,
        validators=[
            DataRequired()
        ]
    )

    defence = SelectField("Defender",
        choices=def_choices,
        validators=[
            DataRequired()
        ]
    )

    midfield = SelectField("Midfielder",
        choices=mid_choices,
        validators=[
            DataRequired()
        ]
    )

    attack = SelectField('Striker',
        choices=fwd_choices,
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Create team')

    def validate_team_name(self, team_name):
        team = Team.query.filter_by(team_name=team_name.data).first()
        if team:
            raise ValidationError('Someone already has that team name, try a different one!')

# This was needed for SelectMultipleForm, didn't use it but may change
##    def validate_gk(self, goalkeeper):
##        if (len(self.goalkeeper.data) != 1):
##            raise ValidationError('You must select one goalkeeper!')
##
##    def validate_def(self, defence):
##        if (len(self.defence.data) != 1):
##            raise ValidationError('You must select one defender!')
##
##    def validate_mid(self, midfield):
##        if (len(self.midfield.data) != 2):
##            raise ValidationError('You must select two midfielders!')
##
##    def validate_fwd(self, attack):
##        if (len(self.attack.data) != 1):
##            raise ValidationError('You must select one striker!')


# transfers page deleted all data in team, not sure why, removed for now
##class TransferForm(FlaskForm):
##
##    team_name = StringField('Team name',
##        validators=[
##            DataRequired(),
##            Length(min=2, max=25)
##        ]
##    )
##    
##    goalkeeper = SelectField('Goalkeeper',
##        choices=gk_choices,
##        validators=[
##            DataRequired()
##        ]
##    )
##
##    defence = SelectField("Defender",
##        choices=def_choices,
##        validators=[
##            DataRequired()
##        ]
##    )
##
##    midfield = SelectField("Midfielder",
##        choices=mid_choices,
##        validators=[
##            DataRequired()
##        ]
##    )
##
##    attack = SelectField('Striker',
##        choices=fwd_choices,
##        validators=[
##            DataRequired()
##        ]
##    )
##
##    submit = SubmitField('Create team')
##
##    def validate_team_name(self, team_name):
##        if team_name.data != current_user.team_name:
##            user = Users.query.filter_by(team_name=team_name.data).first()
##            if user:
##                raise ValidationError('This team name is already in use - please choose another')
