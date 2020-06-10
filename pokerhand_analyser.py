from urllib.request import urlretrieve

class PokerHands(object):

    def __init__(self):
        self.player_one_wins = 0
        self.player_two_wins = 0
        self.card_mapping = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

    def straight(self, hand):
        straight_range = range(min(hand), max(hand)+1)
        straight_check = [value for value in straight_range]
        if hand == straight_check:
            return True


    def evaluate_hand(self, hand):
        hand_values = sorted([value[0] for value in hand])
        hand_suits = [value[1] for value in hand]

        is_straight = self.straight(hand_values)  #True if straight, else None
        is_flush = len(set(hand_suits)) == 1

        if is_straight and is_flush:
            if values[0] == 10:
                return 9, None
            else:
                return 8, max(hand_values) #returns max to find best straight

        pair = False
        trips = False
        trip_value = 0
        pairs = []
        for value in hand_values:
            if hand_values.count(value) == 4:
                return 7, value
            if hand_values.count(value) == 3:
                trips = True
                trip_value = value
            if hand_values.count(value) == 2:
                pair = True
                pairs.append(value)
        if trips and pair:
            return 6, trip_value #stores trip value to find winner
        elif is_flush:
            return 5, hand_values #flush tiebreak needs to iterate whole hand
        elif is_straight:
            return 4, max(hand_values)
        elif trips:
            return 3, trip_value
        elif len(pairs) == 2:
            return 2, (pairs, hand_values) #returns the pair list for checking & H_list for kicker
        elif pair:
            return 1, (pairs, hand_values)
        else:
            return 0, hand_values

    def tie_break(self, rank, hand1, hand2):
        # High card breakers
        if rank == 2 or rank == 1:
            if hand1[0] > hand2[0]:
                self.player_one_wins += 1
            elif hand2[0] > hand1[0]:
                self.player_two_wins += 1
            elif hand1[1] > hand2[1]:
                self.player_one_wins += 1
            else:
                self.player_two_wins += 1

        elif hand1 > hand2:
            self.player_one_wins += 1
        else:
            self.player_two_wins += 1


    def main(self):
        # Downloads the hands from webpage and saves locally
        url = 'https://projecteuler.net/project/resources/p054_poker.txt'
        urlretrieve(url, 'poker.csv')
        # Opens the hands file from local dir
        with open('poker.csv', 'r') as file:
            for line in file:
                line_list = line.strip().split(' ')
                hand_tuples = []
                for card in line_list:
                    hand_tuples.append((self.card_mapping.get(card[0]), card[1]))

                hand1 = hand_tuples[0:5]
                hand2 = hand_tuples[5:10]
                rank1, tie1 = self.evaluate_hand(hand1)
                rank2, tie2 = self.evaluate_hand(hand2)

                if rank1 > rank2:
                    self.player_one_wins += 1
                elif rank2 > rank1:
                    self.player_two_wins += 1
                else:
                    self.tie_break(rank1, tie1, tie2)


        print('Player 1 won {one} hands and player 2 won {two} hands.'.format(one=self.player_one_wins, two=self.player_two_wins))


go = PokerHands()
go.main()

