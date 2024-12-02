import yaml
from neo4j import GraphDatabase
import pandas as pd
import random

# Cargar configuración desde el archivo YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Datos de conexión a Neo4j desde el archivo YAML
uri = config["neo4j"]["uri"]
username = config["neo4j"]["username"]
password = config["neo4j"]["password"]

driver = GraphDatabase.driver(uri, auth=(username, password))

csv_path = "C:/Users/jesus/Desarrollo/Big Data/Jugadoras y Equipos.csv"

data = pd.read_csv(csv_path, encoding='latin1')

def insert_player_team_and_league(tx, player, squad):
    query = """
    MERGE (l:League {name: 'Mini Liga'})
    MERGE (t:Team {name: $squad})
    MERGE (p:Player {name: $player})
    MERGE (t)-[:PARTICIPATES_IN]->(l)
    MERGE (p)-[:BELONGS_TO]->(t)
    """
    tx.run(query, player=player, squad=squad)

def create_games_and_plays(tx, team1, team2, game_number):
    query = """
    MATCH (t1:Team {name: $team1})
    MATCH (t2:Team {name: $team2})
    MERGE (g:Game {number: $game_number})
    MERGE (t1)-[:PLAYS_IN]->(g)
    MERGE (t2)-[:PLAYS_IN]->(g)
    
    WITH t1, t2, g
    MATCH (p1:Player)-[:BELONGS_TO]->(t1)
    MATCH (p2:Player)-[:BELONGS_TO]->(t1)
    MATCH (p3:Player)-[:BELONGS_TO]->(t1)
    MATCH (p4:Player)-[:BELONGS_TO]->(t1)
    WHERE p1 <> p2 AND p2 <> p3 AND p3 <> p4 AND p1 <> p3 AND p1 <> p4 AND p2 <> p4
    WITH t1, t2, g, p1, p2, p3, p4, rand() AS random_result
    LIMIT 3
    CREATE (play:Play {
        number: toString($game_number) + '-' + t1.name + '-' + toInteger(1000000 * rand()),
        team: t1.name,
        result: CASE WHEN random_result < 0.5 THEN 'Gol' ELSE 'No Gol' END
    })
    MERGE (play)-[:BELONGS_TO_GAME]->(g)
    MERGE (play)-[:MADE_BY]->(t1)
    CREATE (p1)-[:MAKES_PASS {order: 1}]->(play)
    CREATE (p2)-[:MAKES_PASS {order: 2}]->(play)
    CREATE (p3)-[:MAKES_PASS {order: 3}]->(play)
    FOREACH (_ IN CASE WHEN random_result < 0.5 THEN [1] ELSE [] END |
        CREATE (p4)-[:SCORES_GOAL]->(play)
        CREATE (p4)-[:MAKES_PASS {order: 4}]->(play)
    )
    
    WITH t1, t2, g
    MATCH (p1:Player)-[:BELONGS_TO]->(t2)
    MATCH (p2:Player)-[:BELONGS_TO]->(t2)
    MATCH (p3:Player)-[:BELONGS_TO]->(t2)
    MATCH (p4:Player)-[:BELONGS_TO]->(t2)
    WHERE p1 <> p2 AND p2 <> p3 AND p3 <> p4 AND p1 <> p3 AND p1 <> p4 AND p2 <> p4
    WITH t1, t2, g, p1, p2, p3, p4, rand() AS random_result
    LIMIT 3
    CREATE (play:Play {
        number: toString($game_number) + '-' + t2.name + '-' + toInteger(1000000 * rand()),
        team: t2.name,
        result: CASE WHEN random_result < 0.5 THEN 'Gol' ELSE 'No Gol' END
    })
    MERGE (play)-[:BELONGS_TO_GAME]->(g)
    MERGE (play)-[:MADE_BY]->(t2)
    CREATE (p1)-[:MAKES_PASS {order: 1}]->(play)
    CREATE (p2)-[:MAKES_PASS {order: 2}]->(play)
    CREATE (p3)-[:MAKES_PASS {order: 3}]->(play)
    FOREACH (_ IN CASE WHEN random_result < 0.5 THEN [1] ELSE [] END |
        CREATE (p4)-[:SCORES_GOAL]->(play)
        CREATE (p4)-[:MAKES_PASS {order: 4}]->(play)
    )
    """
    tx.run(query, team1=team1, team2=team2, game_number=game_number)

with driver.session() as session:
    for _, row in data.iterrows():
        session.execute_write(insert_player_team_and_league, row["Player"], row["Squad"])
    
    teams = data["Squad"].unique().tolist()
    
    games = []
    team_games = {team: 0 for team in teams}
    
    game_number = 1
    while len(games) < 6:
        available_teams = [team for team in teams if team_games[team] < 2]
        if len(available_teams) < 2:
            break
            
        team1 = random.choice(available_teams)
        available_teams.remove(team1)
        team2 = random.choice(available_teams)
        
        if (team1, team2) not in games and (team2, team1) not in games:
            games.append((team1, team2))
            team_games[team1] += 1
            team_games[team2] += 1
            
            session.execute_write(create_games_and_plays, team1, team2, game_number)
            game_number += 1

driver.close()
