import unittest

from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import User, Player, Team

class TestBase(TestCase):

    def create_app(self):
        #pass in test configurations
        config_name = "testing"
        app.config.update(
                SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+getenv('FF_USER')+':'+getenv('FF_PASSWORD')+'@'+getenv('FF_HOST')+'/'+getenv('FF_DB_TEST'))
        return app

    def setUp(self):
        # Will be called every test

        db.session.commit()
        db.drop_all()
        db.create_all()

        #create test admin and normal user
        admin = User(email="admin@admin.com", first_name="admin", last_name="admin", username="admin", password="admin")
        user = User(email="test@user.com", first_name="test", last_name="user", username="test", password="test")

        #save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # Annihilate tables after every test

        db.session.remove()
        db.drop_all()

class UnitTest(TestBase):

    def test_homepage_view(self):
        # Test homepage is accessible while logged out
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_create_team(self):
        # Test number of teams in team table

        # create test team
        team = Team(team_name="test", user_id=2, goalkeeper="test_gk", defence="test_def", midfield="test_mid", attack="test_fwd")

        # save team to database
        db.session.add(team)
        db.session.commit()

        self.assertEqual(Team.query.count(), 1)

    def test_create_player(self):
        # Test number of players in player table

        # create test player
        player = Player(last_name="kebe", first_name="jimmy", club="REA", position="mid")

        # save player to database
        db.session.add(player)
        db.session.commit()

        self.assertEqual(Player.query.count(), 1)

    def test_login_view(self):
        # test login page is accessible without login
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_view(self):
        # test user page is inaccessible without login
        target_url = url_for('account')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
