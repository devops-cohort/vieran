from application import db
from application.models import User, Player, Team
import csv

players = []

with open('application/players.csv', 'r') as csv_file:
    for line in csv_file.readlines():
        data = line.strip().split(',')
        player = Player(last_name = data[0], club = data[1], position = data[2])
        players.append(player)

db.session.bulk_save_objects(players)
db.session.commit()

