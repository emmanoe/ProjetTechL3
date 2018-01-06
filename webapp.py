import time
from flask import *
import json
import sys
import csv

#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
app.secret_key = 'projettechnologique'


@app.route("/")
def homepage():
    return render_template("main.html")

@app.route('/search',methods=['GET', 'POST'])
def index():
    if request.method == 'POST' :
        dep = request.form['depart'];
        arr = request.form['destination'];
        from py2neo import Graph, DBMS, authenticate
        my_dbms = DBMS("http://localhost:7474/")
        authenticate("localhost:7474", "neo4j", "3789")
        graph = Graph(password="3789")
        sec = graph.data("match (v:ville)-[r]-(varr:ville) where v.nom = {X} and varr.nom = {Y}  return r.nb_passagers, r.distance_KM",X= dep,Y= arr)
        simple = graph.data("match (vdep:ville)-[resc]-(escal:ville)-[r]-(varr:ville) where vdep.nom = {X} and varr.nom = {Y}  return escal.nom",X= dep,Y= arr)
        return render_template('search.html',titre="les vols", ville = sec, resultat = simple)
    else:
        #A mettre dans un py 
        langArray = [];
        with open('./static/ITA_2000.csv','r') as vol:
            reader = csv.reader(vol)
            nodes = [ n for n in vol][2:]

            node_names = csv.reader(nodes, delimiter = ';')
            for name in node_names:
                langArray.append(name[2])
            langArray = sorted(set(langArray))
            print(len(langArray))
        ####################
        # langArray = getArray()
        return render_template('form.html', langArray=langArray)


@app.route('/vols')
def simple():
    from py2neo import Graph, DBMS, authenticate
    my_dbms = DBMS("http://localhost:7474/")
    authenticate("localhost:7474", "neo4j", "3789")
    server = "localhost:7474"
    graph = Graph(password="3789")
    sec = graph.data("MATCH (n) RETURN n.nom, n.codepays order by n.codepays")
    return render_template('vols.html',titre="les vols", ville = sec)



@app.route('/world-50m.json')
def d3js():
    return render_template('graph.json')

@app.route('/population.csv')
def d3s():
    return render_template('population.csv')

