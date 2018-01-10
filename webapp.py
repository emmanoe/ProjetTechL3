import time
from flask import *
import json
import sys
import csv

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
        dep = request.form['depart'];
        arr = request.form['destination'];
        dist = graph.data("match (v:ville)-[r:vol_vers]->(varr:ville) where v.nom = {X} and varr.nom = {Y}  return r.distance_KM",X= dep,Y= arr)
        nbpass = graph.data("match (v:ville)-[r:vol_vers]->(varr:ville) where v.nom = {X} and varr.nom = {Y}  return r.nb_passagers",X= dep,Y= arr)
        simple = graph.data("match (vdep:ville)-[resc:vol_vers]->(escal:ville)-[r:vol_vers]->(varr:ville) where vdep.nom = {X} and varr.nom = {Y}  return escal, resc",X= dep,Y= arr)
        return render_template('search.html',titre="les vols", dist = dist, nbpass = nbpass, escal = simple, dep=dep, arr=arr)
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


@app.route('/population.csv')
def d3s():
    return render_template('population.csv')


## Generate  an array with all the Countries
with open('./static/population.csv','r') as Countrys:
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
        if click_map in list_of_country[i][1]:
            cpays = list_of_country[i][6]
            nb_vol_dep = graph.data("match (vdep:ville)-[r]->(varr:ville) where vdep.codepays = {X} return vdep, varr", X = cpays)
            nb_vol_arr = graph.data("match (vdep:ville)-[r]->(varr:ville) where varr.codepays = {X} return vdep, varr", X = cpays)
            return render_template('search.html',selected_country=click_map, dep=nb_vol_dep, arr = nb_vol_arr)
    abort(404)
