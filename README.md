# P2_Tournament
Full Stack Nano Degree - Tournament Project

Runs a swiss pair style tournament.  This code supports:
* non power of 2 participants - you can do whatever number GREATER than 1.
* non-even numbers of participants so in an odd number case, one use will get a BYE in each round.

**Note:**  If you deviate too far from a power of 2 then you are not guanranteed a non-tie when running log(players, 2) rounds.  This would happen most frequently for numbers of players just beyond a power of 2.  In that case you should examine the output of **playerStandings()** and run additional rounds if you want to get a single winner.  You will not experience this use case if you restrict yourself to numbers of players that are a power of 2.

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


