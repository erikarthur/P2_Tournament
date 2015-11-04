#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
import contextlib


def connect():
    """Connect to the PostgreSQL database.  Returns a
    database connection."""
    db = psycopg2.connect("dbname='tournament'")

    return db

@contextlib.contextmanager
def get_cursor():
    """
    Helper function for using cursors.  Helps to avoid a lot of connect,
    execute, commit code
    """
    conn = connect()
    cur = conn.cursor()
    try:
        yield cur
    except:
        raise
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE from standings")

def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as cursor:
        cursor.execute("DELETE from players;")

def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as cursor:
        cursor.execute("select count(name) from players")
        rows = cursor.fetchall()
        return rows[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    with get_cursor() as cursor:
        cursor.execute('INSERT INTO players VALUES (default, %s);', (name,))

        # this select is to get the ID for the standings table
        cursor.execute('select * from players where name = %s', (name,))
        rows = cursor.fetchall()

        cursor.execute(
            'INSERT INTO standings VALUES (default, %s, %s, %s, %s, %s, %s);',
            (rows[0][0], 0, 0, 0, 0, 'FALSE'))


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
    with get_cursor() as cursor:
        cursor.execute("select * from player_standings_view;")
        rows = cursor.fetchall()

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
    with get_cursor() as cursor:
        cursor.execute(
        'update standings set matches = matches + 1, wins = wins + 1  '
        'where player_id = %s;', (winner,))

        # -1 means this was a BYE match so don't record a loser
        if loser != -1:
            cursor.execute(
                'update standings set matches = matches + 1, '
                'losses = losses + 1 where player_id = %s;', (loser,))



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
    # get the sorted list of players using a view
    with get_cursor() as cursor:
        cursor.execute('select * from swiss_pairings_view;')
        rows = cursor.fetchall()

    # check number of players and add a bye if number is odd
    if countPlayers() % 2 != 0:
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
            with get_cursor() as cursor:
                cursor.execute(
                    'update standings set used_bye = NOT used_bye '
                    'where id = %s;', (test_item[0],))

            # inserts bye into rows list
            if pos % 2 == 0:
                # position is even.  add bye at pos + 1
                bye_tuple = (-1, 'BYE', 0, 0, 0, True)
                rows.insert(pos + 1, bye_tuple)
            else:
                # pos is odd.  Need to swap pos and pos + 1,
                # then insert bye at pos + 2
                bye_tuple = (-1, 'BYE', 0, 0, 0, True)
                swap_tuple = rows[pos]
                rows.remove(swap_tuple)
                rows.insert(pos + 1, swap_tuple)
                rows.insert(pos + 2, bye_tuple)
    return rows
