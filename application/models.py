from application import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    team = db.relationship('Team', backref='manager', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Email: ', self.email, '\r\n',
            'Name: ', self.first_name, ' ', self.last_name
        ])

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Player(db.Model):
    
    player_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    club = db.Column(db.String(3), nullable=False)
    position = db.Column(db.String(3), nullable=False)
    current_points = db.Column(db.Integer, nullable=False, default=0)
## needed for link table, will add later
##    team = db.relationship('Link', backref='player', lazy=True)

    def __repr__(self):
        return "{0}, {1}, {2}".format(self.last_name, self.club, self.position)


class Team(db.Model):

    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(25), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    remaining_transfers = db.Column(db.Integer, nullable=False, default=30)
    goalkeeper = db.Column(db.String(25), nullable=False)
    defence = db.Column(db.String(25), nullable=False)
    midfield = db.Column(db.String(25), nullable=False)
    attack = db.Column(db.String(25), nullable=False)
## code for link table, may add later
##    player = db.relationship('Link', backref='team', lazy=true)

    def __repr__(self):
        return ''.join([
            'Team Name: ', self.team_name
        ])
## code to create table to link players and teams, will add once basic stuff is done
##class Link(db.Model):
##
##    team_id = db.Column(
##        db.Integer,
##        db.ForeignKey('team.team_id'),
##        primary_key = True)
##
##    player_id = db.Column(
##        db.Integer,
##        db.ForeignKey('player.player_id'),
##        primary_key = True)
