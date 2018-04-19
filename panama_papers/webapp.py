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
        print("ncouncou")
        simple = graph.data("MATCH (n:entity) WHERE n.name CONTAINS {X} RETURN n", X=dep) #~ '.*{X}.*'
        return render_template('search.html',titre="resultats", dep = simple)
    else:
        #A mettre dans un py
        langDepArray=[];
        langArrArray=[];
        with open('./static/ITA_2000.csv','r') as vol:
            reader = csv.reader(vol)
            nodes = [ n for n in vol][2:]

            node_names = csv.reader(nodes, delimiter = ';')
            for vname in node_names:
                langDepArray.append(vname)#5
                langArrArray.append(vname)#2
            #langDepArray = sorted(set(langDepArray))
            #langArrArray = sorted(set(langArrArray))
        ####################
        # langArray = getArray()
        return render_template('form.html',  langDepArray=langDepArray, langArrArray= langArrArray)


@app.route('/vols')
def simple():
    from py2neo import Graph, DBMS, authenticate
    my_dbms = DBMS("http://localhost:7474/")
    authenticate("localhost:7474", "neo4j", "3789")
    server = "localhost:7474"
    graph = Graph(password="3789")
    sec = graph.data("MATCH (n) RETURN n.nom, n.codepays order by n.codepays")
    return render_template('vols.html',titre="les vols", ville = sec)


## Generate  an array with all the Countries
with open('./static/population1.csv','r') as Countrys:
    reader = csv.reader(Countrys)
    nodes = [ n for n in Countrys][2:]

country_names = csv.reader(nodes, delimiter = ',')
list_of_country = []
for country in country_names:
    list_of_country.append(country)
country_names = []; country_cpays = [];

##########################################

@app.route('/<click_map>')
def test(click_map):
    for i in range(0,len(list_of_country)):
        if click_map == list_of_country[i][1]:
            print(click_map)
            cpays = list_of_country[i][6]
            print(cpays)
            nb_vol_dep = graph.data("match (e) where e.countrycodes={X} return e", X=cpays)
            return render_template('search.html', selected_country=click_map, dep=nb_vol_dep)
    abort(404) ## Message d'erreur


@app.route('/chuwebapp')
def bddjson():
    return render_template('chuwebapp.html')

@app.route('/trendline')
def trend():
    return render_template('trendline.html')


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
