__author__ = 'erik'

from tournament import *
import math
import random
import decimal


db = connect()
deletePlayers()
deleteMatches()

registerPlayer("Ace")
registerPlayer("Jimmy")
registerPlayer("Phil")
registerPlayer("Sport")
registerPlayer("Ed")
registerPlayer("Lucy")
registerPlayer("Jake")
registerPlayer("Adam")
registerPlayer("Ace2")
registerPlayer("Jimmy2")
registerPlayer("Phil2")
registerPlayer("Sport2")
registerPlayer("Ed2")
registerPlayer("Lucy2")
registerPlayer("Jake2")
registerPlayer("Adam2")
registerPlayer("Jake3")
# registerPlayer("Adam3")

count = countPlayers()
rounds = int(math.ceil(math.log(count,2)))

currentRound = 0

for x in range(0, rounds):

    print 'Round {0} Matches\n'.format(x+1)

    playerPairings = swissPairings()

    for playerPair in playerPairings:

        if playerPair[0] == -1 or playerPair[2] == -1:
            # this is a bye match
            if playerPair[0] != -1:
                reportMatch(playerPair[0], playerPair[2])
                print 'Winner: {0}\tLoser: {1}'.format(playerPair[1], playerPair[3])
            else:
                reportMatch(playerPair[2], playerPair[0])
                print 'Winner: {0}\tLoser: {1}'.format(playerPair[3], playerPair[1])
        elif random.random() < .5:
            # first player won
            reportMatch(playerPair[0], playerPair[2])
            print 'Winner: {0}\tLoser: {1}'.format(playerPair[1], playerPair[3])

        else:
            # second player won
            reportMatch(playerPair[2], playerPair[0])
            print 'Winner: {0}\tLoser: {1}'.format(playerPair[3], playerPair[1])

    standings = playerStandings()

    # create local variable for calculating rank
    rank = 0
    currentWins = -1

    print "\nCurrent Tournament Standings\n"
    print 'Rank\tName\tPoints'

    for row in standings:
        # check each players wins against wins from prior players.
        # increment rank if necessary.  Rank is just for tourney rank
        if currentWins != row[2]:
            rank = rank + 1
            currentWins = row[2]

        print '{0}\t{1}\t{2}'.format(rank, row[1], row[2])

    print '\n-----------------------------\n'

    #return results


