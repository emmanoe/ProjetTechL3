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
        simple = graph.data("match (vdep:ville)-[resc]-(escal:ville)-[r]-(varr:ville) where vdep.nom = {X} and varr.nom = {Y}  return escal, resc",X= dep,Y= arr)
        return render_template('search.html',titre="les vols", info_vol = sec, escal = simple, dep=dep, arr=arr)
    else:
        #A mettre dans un py 
        langDepArray=[];
        langArrArray=[]; 
        with open('./static/ITA_2000.csv','r') as vol:
            reader = csv.reader(vol)
            nodes = [ n for n in vol][2:]

            node_names = csv.reader(nodes, delimiter = ';')
            for vname in node_names:
                langDepArray.append(vname[2].replace('*',''))
                langArrArray.append(vname[5].replace('*',''))
            langDepArray = sorted(set(langDepArray))
            langArrArray = sorted(set(langArrArray))
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



@app.route('/world-50m.json')
def d3js():
    return render_template('graph.json')

@app.route('/population.csv')
def d3s():
    return render_template('population.csv')

