import sys
import pygame
import random
from pynput.keyboard import Controller
from time import sleep

pygame.init()

keyboard = Controller()

M1_POS = (400, 50)
M2_POS = (400, 350)

AI_START_POS = (100, 100)
PLAYER_START_POS = (100, 400)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlackJack")

CARD_WIDTH = 150
CARD_HEIGHT = 225

pygame.font.init()
FONT = pygame.font.SysFont('Ariel', 30)
CONTROLS = FONT.render("Controls:", True, (0, 0, 0))
HIT = FONT.render("[H]IT", True, (0, 0, 0))
STAY = FONT.render("[S]TAY", True, (0, 0, 0))
NEW_GAME = FONT.render("[N]EW GAME", True, (0, 0, 0))

BG = pygame.transform.scale(pygame.image.load("images/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

card_A = pygame.transform.scale(pygame.image.load("images/A.png"), (CARD_WIDTH, CARD_HEIGHT))
card_2 = pygame.transform.scale(pygame.image.load("images/2.png"), (CARD_WIDTH, CARD_HEIGHT))
card_3 = pygame.transform.scale(pygame.image.load("images/3.png"), (CARD_WIDTH, CARD_HEIGHT))
card_4 = pygame.transform.scale(pygame.image.load("images/4.png"), (CARD_WIDTH, CARD_HEIGHT))
card_5 = pygame.transform.scale(pygame.image.load("images/5.png"), (CARD_WIDTH, CARD_HEIGHT))
card_6 = pygame.transform.scale(pygame.image.load("images/6.png"), (CARD_WIDTH, CARD_HEIGHT))
card_7 = pygame.transform.scale(pygame.image.load("images/7.png"), (CARD_WIDTH, CARD_HEIGHT))
card_8 = pygame.transform.scale(pygame.image.load("images/8.png"), (CARD_WIDTH, CARD_HEIGHT))
card_9 = pygame.transform.scale(pygame.image.load("images/9.png"), (CARD_WIDTH, CARD_HEIGHT))
card_10 = pygame.transform.scale(pygame.image.load("images/10.png"), (CARD_WIDTH, CARD_HEIGHT))
card_J = pygame.transform.scale(pygame.image.load("images/J.png"), (CARD_WIDTH, CARD_HEIGHT))
card_Q = pygame.transform.scale(pygame.image.load("images/Q.png"), (CARD_WIDTH, CARD_HEIGHT))
card_K = pygame.transform.scale(pygame.image.load("images/K.png"), (CARD_WIDTH, CARD_HEIGHT))

FULL_DECK = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
cards_dict = {"A": card_A,
              2: card_2,
              3: card_3,
              4: card_4,
              5: card_5,
              6: card_6,
              7: card_7,
              8: card_8,
              9: card_9,
              10: card_10,
              "J": card_J,
              "Q": card_Q,
              "K": card_K}


def check_blackjack(val):
    if val == 21:
        message = "You got BlackJack! You WIN!"
        show_messages(message, M1_POS)
        keyboard.press("n")
        keyboard.release("n")


def draw_board():
    screen.blit(BG, (0, 0))
    screen.blit(CONTROLS, (1000, 50))
    screen.blit(HIT, (1000, 300))
    screen.blit(STAY, (1000, 350))
    screen.blit(NEW_GAME, (1000, 400))


def peek_ai_cards(ai_hand):
    screen.blit(cards_dict[ai_hand[-1]], (AI_START_POS[0], AI_START_POS[1]))


def draw_ai_cards(ai_hand):
    offset = 0
    for card in ai_hand:
        screen.blit(cards_dict[card], (AI_START_POS[0] + offset, AI_START_POS[1]))
        offset += 30
    pygame.display.update()
    sleep(0.25)


def draw_player_cards(player_hand):
    offset = 0
    for card in player_hand:
        screen.blit(cards_dict[card], (PLAYER_START_POS[0] + offset, PLAYER_START_POS[1]))
        offset += 30


def draw(player, ai, deck):
    for i in range(2):
        player.append(deck.pop())
        ai.append(deck.pop())
    return player, ai


def hit_player(player_hand, deck):
    card = deck.pop()
    player_hand.append(card)
    return player_hand, deck


def get_value(hand):
    total = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total


def dealer_ai(dealer_cards, p_val, deck):
    dealer_value = 0
    for card in dealer_cards:
        if card == "J" or card == "Q" or card == "K":
            dealer_value += 10
        elif card == "A":
            if dealer_value <= 10:
                dealer_value += 11
            else:
                dealer_value += 1
        else:
            dealer_value += card

    draw_ai_cards(dealer_cards)

    if dealer_value > 21:
        return dealer_value

    if 17 <= dealer_value <= 21:
        return dealer_value

    if p_val < dealer_value <= 21:
        return dealer_value

    if dealer_value <= p_val and dealer_value <= 17:
        dealer_cards, deck = hit_player(dealer_cards, deck)
        return dealer_ai(dealer_cards, p_val, deck)
    return dealer_value


def show_messages(m, xy):
    message = FONT.render(m, True, (0, 0, 0))
    screen.blit(message, xy)
    pygame.display.update()
    sleep(2)


def check_win(ai, player):
    if ai > 21:
        message = "Dealer went over 21! You win! New game will start..."
    elif ai == player:
        message = "You win by drawing with the dealer!"
    elif ai > player:
        message = "You lose! Dealer has higher hand value!"
    else:
        message = "You win! Dealer has lower hand value"
    return message


def game():
    draw_board()
    card_deck = FULL_DECK * 8
    random.shuffle(card_deck)
    player_cards = []
    ai_cards = []
    player_cards, ai_cards = draw(player_cards, ai_cards, card_deck)
    draw_player_cards(player_cards)
    peek_ai_cards(ai_cards)
    player_total = get_value(player_cards)
    check_blackjack(player_total)

    run_game = True

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    game()
                if event.key == pygame.K_h:
                    player_cards, card_deck = hit_player(player_cards, card_deck)
                    draw_player_cards(player_cards)
                    player_total = get_value(player_cards)
                    if player_total > 21:
                        message = "You went over 21! New game will start..."
                        show_messages(message, M2_POS)
                        sleep(0.5)
                        game()
                if event.key == pygame.K_s:
                    draw_ai_cards(ai_cards)
                    ai_total = dealer_ai(ai_cards, player_total, card_deck)
                    message = check_win(ai_total, player_total)
                    show_messages(message, M2_POS)
                    sleep(0.5)
                    game()

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    game()
