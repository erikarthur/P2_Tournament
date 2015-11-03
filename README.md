# P2_Tournament
Full Stack Nano Degree - Tournament Project

##Getting Started
---
Getting started on this project is a little involved because of the setting up the vagrant vm and the postgresql database.

1. Clone the https://github.com/erikarthur/P2_Tournament.git repo.  It's a subset of the full stack one
2. Run 'vagrant up --provider=virtualbox' from the cloned directory. This may take a couple of minutes to setup the vm, install PostgreSQL, etc.
3. SSH into the VM once it's running - **cd vagrant; vagrant ssh**
4. Run the setup script to create the database and tables - **./setup.sh**
5. Done.  
	* You can run the unit tests with **python tournament_test.py**
	* Run the 17 player version I supplied with **python myTourney.py**

##What's included
---
+ myTourney.py  
+ setup.sh
+ tournament.py   
+ tournament.sql
+ tournament_test.py

**myTourney.py** 
    creates and runs a 17 player tournament.  Shows odd numbers with byes and non powers of 2 for participants

**setup.sh** 
    sets up the database, tables and views in postgres

**tournament.py**
	code to connect to db, registering players, swiss pairings, reporting matches, etc.  All the code you need to run a swiss pairing style tournament.  See myTourney.py for import syntax

**tournament.sql**
	SQL file to create the tables and views for storing tournament

**tournament_test.py**
	Unit tests from y'all.  Run with 'python tournament_test.py'


###Creator
------------------------
Erik Arthur
erikarthur@gmail.com


