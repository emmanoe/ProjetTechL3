# -*- coding:utf-8 -*-

import time
from flask import *
import json
import sys
import csv
from model import graph

#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
app.secret_key = 'projettechnologique'

from py2neo import Graph, DBMS, authenticate
my_dbms = DBMS("http://localhost:7474/")
authenticate("localhost:7474", "neo4j", "3789")
graph = Graph(password="3789")

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route('/search',methods=['GET', 'POST'])
def index():
    if request.method == 'POST' :
        dep = request.form['recherche'];
        simple = graph.data("MATCH (n:entity) WHERE n.name CONTAINS {X} RETURN n", X=dep) #~ '.*{X}.*'
        return render_template('search.html',titre="resultats", dep = simple)
    else:
        return render_template('form.html')


@app.route('/vols')
def simple():
    from py2neo import Graph, DBMS, authenticate
    my_dbms = DBMS("http://localhost:7474/")
    authenticate("localhost:7474", "neo4j", "3789")
    server = "localhost:7474"
    graph = Graph(password="3789")
    sec = graph.data("MATCH (n) RETURN n.nom, n.codepays order by n.codepays")
    return render_template('vols.html',titre="les vols", ville = sec)


## Genere un tableau avec le nom tous les pays
## impliqués dans l'affaire des panama papers
## ils sont stockés dans un fichier population csv
with open('./static/population1.csv','r') as Countrys:
    reader = csv.reader(Countrys)
    nodes = [ n for n in Countrys][2:]

country_names = csv.reader(nodes, delimiter = ',')
list_of_country = []
for country in country_names:
    list_of_country.append(country)

## /<click_map> est une route variable
## apres avoir selctionné un pays sur
## la carte une route est automatiquement
## générée.
## On vérifie que le pays cliqué appartient
## fait bien parti des pays impliqués.
@app.route('/<click_map>')
def test(click_map):
    for i in range(0,len(list_of_country)):
        if click_map == list_of_country[i][1]: #Complexité non optimale (O(len))
            cpays = list_of_country[i][6] #les cases [i][j] correspodent au infos sur le pays dont le code du pays(cpays) pour j = 6
            infos_pays = graph.data("match (e) where e.countrycodes={X} return e", X=cpays) #on récupére toutes les infos sur ce pays
            return render_template('search.html', selected_country=click_map, dep=infos_pays)
    return render_template('about.html')


@app.route('/graph')
def holla():
    from flask import request
    from py2neo import Graph, DBMS, authenticate
    my_dbms = DBMS("http://localhost:7474/")
    authenticate("localhost:7474", "neo4j", "3789")
    server = "localhost:7474"
    graph = Graph(password="3789")
    ent= request.args['var']
    sec = graph.data("match(a)-[r1]->(n:entity)  where n.name={X} return r1", X=ent)
    sec1 = graph.data("match(a)-[r1]->(n:entity)  where n.name={X} return n", X=ent)
    sec2 = graph.data("match(a)-[r1]->(n:entity)  where n.name={X} return a", X=ent)
    return render_template('graph.html',titre="les vols", nodes = sec, nodes1 = sec1, nodes2 = sec2 )
