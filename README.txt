README
======

Le site que nous avons mis en place est un serveur Flask permettant aux utilisateurs de requetter un serveur de base données neo4j décrivant des lignes aériennes. 

Mise en route
--------------

Pour démarrer le serveur il vous faut:

1. Lancez neo4j et importez y la base de donnée csv 
2. Entrer vos identifiants et mdp neo4j dans le fichier webapp.py:
* ligne 22: authenticate("localhost:7474", "identifiants", "mdp") // Avec les guillemets.
* ligne 35: authenticate("localhost:7474", "identifiants", "mdp") // Avec les guillemets.
* ligne 37: graph = Graph(password="mdp") // Avec les guillemets.
3. Lancer le serveur Flask:
* ./flask_run
4. Dans un navigateur, lancez http://127.0.0.1:5000/
5. Quitter le serveur en tapant Ctrl-C dans la console.


Importer la base de donnée csv dans Neo4j 
=========================================

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'http://emmanoe.delar.emi.u-bordeaux.fr/ITA_2000.save' AS line
FIELDTERMINATOR ';'
WITH line

MERGE (vdep:ville {codeville:line.`CVIL1`}) 
SET vdep.nom = line.`VIL1` SET vdep.codepays = line.`CPAYS1`

MERGE (varr:ville {codeville:line.`CVIL2`})
SET varr.nom = line.`VIL2` SET varr.codepays = line.`CPAYS2`

MERGE (vdep)-[r:vol_vers]->(varr)

SET r.nb_passagers = line.`NBPA2000`
SET r.distance_KM = line.`DKM`;