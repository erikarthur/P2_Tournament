#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()

    tournament_cursor = db.cursor()

    tournament_cursor.execute("DELETE from standings")

    db.commit()

    db.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a
    database connection."""
    db = psycopg2.connect("dbname='tournament'")

    return db


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()

    tournament_cursor = db.cursor()

    tournament_cursor.execute("DELETE from players;")

    db.commit()

    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()

    tournament_cursor = db.cursor()

    tournament_cursor.execute("select count(name) from players")

    rows = tournament_cursor.fetchall()

    db.close()

    [count] = [row[0] for row in rows]

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    tournament_cursor = db.cursor()
    tournament_cursor.execute(
        'INSERT INTO players VALUES (default, %s);', (name,))

    # this select is to get the ID for the standings table
    tournament_cursor.execute(
        'select * from players where name = %s', (name,))

    rows = tournament_cursor.fetchall()

    tournament_cursor.execute(
        'INSERT INTO standings VALUES (default, %s, %s, %s, %s, %s, %s);',
        (rows[0][0], 0, 0, 0, 0, 'FALSE'))

    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()

    tournament_cursor = db.cursor()
    tournament_cursor.execute(
        "select * from player_standings_view;")

    rows = tournament_cursor.fetchall()

    # close connection
    db.close()

    # output list
    current_standings = []

    for row in rows:
        # add tuple standings list
        current_standings.append((row[0], row[1], row[2], row[3]))

    return current_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    tournament_cursor = db.cursor()

    # tournament_cursor.execute(
    #     'insert into matches values (default, %s, %s);', (winner, loser,))
    tournament_cursor.execute(
        'update standings set matches = matches + 1, wins = wins + 1  '
        'where player_id = %s;', (winner,))

    # -1 means this was a BYE match so don't record a loser
    if loser != -1:
        tournament_cursor.execute(
            'update standings set matches = matches + 1, losses = losses + 1 '
            'where player_id = %s;', (loser,))

    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    tournament_cursor = db.cursor()

    tournament_cursor.execute('select * from swiss_pairings_view;')

    rows = tournament_cursor.fetchall()

    db.close()

    if countPlayers() % 2 != 0:
        # player count is odd need to add a bye to a player
        insertByeMatch(rows)

    # simplify the results dataset to just id1, name1, id2, name2
    results = []
    for x in xrange(0, len(rows), 2):
        results.append((rows[x][0], rows[x][1], rows[x+1][0], rows[x+1][1]))

    return results


def insertByeMatch(rows):
    found_player_accepting_bye = False
    while not found_player_accepting_bye:

        # generate a random number and that players gets the bye unless
        # they have already used their bye.
        pos = random.randrange(0, len(rows)-1)

        # get the tuple in that position
        test_item = rows[pos]

        # check it he/she used the bye.  This would be better as a constant
        if not test_item[5]:
            # updates the bye boolean for selected user in results set
            found_player_accepting_bye = True

            # update the bye boolean for selected user in the database
            db = connect()
            tournament_cursor = db.cursor()

            # create a string for the update query
            sql_query = 'update standings set used_bye = NOT used_bye \
                        where id = {0};'.format(test_item[0])

            # execute query, commit and close the connection
            tournament_cursor.execute(sql_query)
            db.commit()
            db.close()

            # inserts bye into rows list
            if pos % 2 == 0:
                # position is even.  add bye at pos + 1
                bye_tuple = (-1, 'BYE', 0, 0, 0, True)
                rows.insert(pos + 1, bye_tuple)
            else:
                # pos is odd.  Need to swap pos and pos + 1,
                # then insert bye at pos + 1
                bye_tuple = (-1, 'BYE', 0, 0, 0, True)
                swap_tuple = rows[pos]
                rows.remove(swap_tuple)
                rows.insert(pos+1, swap_tuple)
                rows.insert(pos + 2, bye_tuple)
    return rows
