import unittest
from blackjack import *


class MyTestCase(unittest.TestCase):

    def test_check_blackjack(self):
        # check_blackjack(val) -> Boolean
        # Test for both True and False case
        self.assertEqual(check_blackjack(21), True)
        self.assertEqual(check_blackjack(20), False)

    def test_draw(self):
        # draw(player, ai, deck) -> player, ai, deck
        # Given deck of all threes, and empty hands, each player should have 2 [3]'s and the deck will be empty
        self.assertEqual(draw([], [], [1, 2, 3, 4]), ([4, 2], [3, 1], []))
        # We check again with a larger deck, we should be returned a deck with some cards left over
        self.assertEqual(draw([], [], ["K", 10, 4, "A", 9, 3, "Q", 7]), ([7, 3], ["Q", 9], ["K", 10, 4, "A"]))

    def test_hit(self):
        # hit_player(player_hand, deck) -> player, deck
        self.assertEqual(hit_player([4, "Q"], ["K", 10, 4, "A", 9, 3, "Q", 7]),
                         ([4, "Q", 7], ["K", 10, 4, "A", 9, 3, "Q"]))

    def test_get_value(self):
        # get_value(hand) -> int value
        self.assertEqual((get_value(["A", "J"])), 21)
        self.assertEqual((get_value(["A", 4])), 15)
        self.assertEqual((get_value([9, "J"])), 19)
        self.assertEqual((get_value([2, 3])), 5)
        self.assertEqual((get_value(["A", "A", "A"])), 13)
        self.assertEqual((get_value(["A", "A", 6])), 18)
        self.assertEqual((get_value(["A", "A", 6, 10])), 28)

    def test_dealer_ai(self):
        # dealer_ai(dealer_cards, p_val, deck) -> dealer_cards, p_val, deck
        deck = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Dealer is > 21, return value
        self.assertEqual((dealer_ai(["A", 10, 2], 17, deck)), 23)

        # Dealer is 17 <= n <= 21, and > than player, return value
        self.assertEqual((dealer_ai(["A", "A", 6], 17, deck)), 18)

        # Dealer is naturally above player, return value
        self.assertEqual((dealer_ai(["A", 4], 8, deck)), 15)

        # Dealer is < than player, hit -> above 21, return value
        self.assertEqual((dealer_ai(["J", 2], 15, deck)), 22)

        deck = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 4]
        # Dealer is <= than player, hit -> > than player, <= than 21, return value
        self.assertEqual((dealer_ai(["A", 4], 15, deck)), 19)

    def test_check_win(self):
        # check_win(ai, player) -> string message
        self.assertEqual(check_win(22, 20), "Dealer went over 21! You win! New game will start...")
        self.assertEqual(check_win(20, 20), "You win by drawing with the dealer!")
        self.assertEqual(check_win(20, 19), "You lose! Dealer has higher hand value!")
        self.assertEqual(check_win(19, 20), "You win! Dealer has lower hand value")

    def test_draw_board(self):
        # draw our board
        self.assertEqual(draw_board(), True)
        sleep(0.5)

    def test_peek_ai_cards(self):
        # draw 1 card from ai hand
        self.assertEqual((peek_ai_cards(["A", 5])), True)
        sleep(0.5)

    def test_draw_ai_cards(self):
        # draw full ai hand
        self.assertEqual((draw_ai_cards(["A", 5])), True)
        sleep(0.5)

    def test_draw_player_cards(self):
        # draw full player hand
        self.assertEqual((draw_player_cards(["A", 5])), True)
        sleep(0.5)

    def test_show_message(self):
        # draw message on screen given coordinates
        self.assertEqual((show_messages("Test message", (400, 50))), True)
        sleep(0.5)


