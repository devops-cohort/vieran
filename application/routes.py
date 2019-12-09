from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import User, Player, Team
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateTeamForm, TransferForm  # Comment out createteamform when creating database
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", title = "Home")

@app.route("/leaderboard")
def leaderboard():
    team_data = Team.query.order_by(Team.points.desc()).all()
    return render_template("leaderboard.html", title = "Leaderboard", teams=team_data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    login_fields = [form.email, form.password, form.remember]
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template("login.html", title = "Login", form=form, fields=login_fields)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    register_fields = [form.email, form.first_name, form.last_name, form.username, form.password, form.confirm_password]
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('create_team'))
    else:
        print(form.errors)
        return render_template("register.html", title = "Register", form=form, fields=register_fields)

@app.route("/createteam", methods=["GET", "POST"])
@login_required
def create_team():
    form = CreateTeamForm()
    createteam_fields = [form.team_name, form.goalkeeper, form.defence, form.midfield, form.attack]
    if form.validate_on_submit():
        team = Team(
            team_name=form.team_name.data,
            manager=current_user,
            goalkeeper=form.goalkeeper.data,
            defence=form.defence.data,
            midfield=form.midfield.data,
            attack=form.attack.data
        )
        db.session.add(team)
        db.session.commit()
        return redirect(url_for("view_teams"))
    else:
        print(form.errors)
        return render_template("create_team.html", title="Create team", form=form, fields=createteam_fields)

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    update_fields = [form.first_name, form.last_name, form.email, form.username]
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        db.session.commit()
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.username.data = current_user.username
    return render_template('account.html', title='Account', form=form, fields=update_fields)

@app.route('/viewteams', methods=['GET', 'POST'])
@login_required
def view_teams():
    user = current_user.id
    teams = Team.query.filter_by(user_id=user)
    return render_template('view_teams.html', title='My Teams', teams=teams)

'''Couldn't get transfers to work, it just removed all data from the team. Will try to fix'''
@app.route('/transfers/<int:teamid>', methods=['GET','POST'])
@login_required
def transfers(teamid):
    team = Team.query.filter_by(team_id=teamid).first()
    form = TransferForm()
    transfer_fields = [form.team_name, form.goalkeeper, form.defence, form.midfield, form.attack]
    if form.validate_on_submit:
        team.team_name = form.team_name.data
        team.goalkeeper = form.goalkeeper.data
        team.defence = form.defence.data
        team.midfield = form.midfield.data
        team.attack = form.attack.data
        db.session.commit()
        return redirect(url_for('view_teams'))
    elif request.method == 'GET':
        form.team_name.data = team.team_name
        form.goalkeeper.data = team.goalkeeper
        form.defence.data = team.defence
        form.midfield.data = team.midfield
        form.attack.data = team.attack
    return render_template('transfers.html', title='Transfer', form=form, team_id=teamid, fields=transfer_fields)

@app.route("/deleteteam/<int:team_id>", methods=["GET", "POST"])
@login_required
def delete_team(team_id):
    team = Team.query.filter_by(team_id=team_id).first()
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('view_teams'))

@app.route('/deleteaccount', methods=['GET', 'POST'])
@login_required
def delete_account():
    user = current_user.id
    teams = Team.query.filter_by(user_id=user)
    for team in teams:
        db.session.delete(team)
    account = current_user
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('home'))
