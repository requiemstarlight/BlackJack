import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

# screen dimensions

WIDTH, HEIGHT = 1000, 700

# colours

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 240)
RUBY = (119, 0, 0)
NAVY = (0, 0, 77)
BEIGE = (153, 153, 102)
CREAM = (255, 255, 179)

# dimensions for the height of top and bottom rectangles showing scores

PLAYER_CARD_START_Y = 110

# locations for dealer card start and placard

DEALER_START_X = 180
DEALER_PLACARD_Y = HEIGHT - 75

# locations for starting point for each player on the screen

PLAYER_1_START = WIDTH / 12
PLAYER_2_START = PLAYER_1_START + WIDTH // 4
PLAYER_3_START = PLAYER_1_START + WIDTH // 2

PLAYERS_START_TUPLE = (PLAYER_1_START, PLAYER_2_START, PLAYER_3_START, DEALER_START_X)

# dimension for cards

CARD_WIDTH = 95
CARD_HEIGHT = 127

# values for rotating cards and for fanning them down across the screen

ADJ_XY_VALUE = 20
MIN_TILT = -10
MAX_TILT = 10

# dimensions for spacings

BOX_SPACING = (WIDTH - CARD_WIDTH * 3) // 4
CARD_GAP = 11

# load images

SILVER_PLACARD = pygame.image.load('images/silver-removebg-preview (1).png')
GOLD_PLACARD = pygame.image.load('images/gold.jpg')
SILVER_PLACARD_SCALED = pygame.transform.scale(SILVER_PLACARD, (200, 100))
GOLD_PLACARD_SCALED = pygame.transform.scale(GOLD_PLACARD, (130, 55))
GOLD_PLACARD_SCORE_SCALED = pygame.transform.scale(GOLD_PLACARD, (240, 90))

TABLE = pygame.image.load('images/table.jpg')
TABLE_SCALED = pygame.transform.scale(TABLE, (WIDTH, HEIGHT))

START_SCREEN = pygame.image.load('images/bjtable2.jpg')
START_SCREEN_SCALED = pygame.transform.scale(START_SCREEN, (WIDTH, HEIGHT))

# load the same logo, but for 2 screens

LOGO = pygame.image.load('images/logo-removebg-preview.png')
LOGO_SCALED = pygame.transform.scale(LOGO, (130, 80))
LOGO_START_SCALED = pygame.transform.scale(LOGO, (180, 110))

# load poker chip images

DEALER_CHIP = pygame.image.load('images/white_dealer-removebg-preview.png')
DEALER_CHIP_SCALED = pygame.transform.scale(DEALER_CHIP, (110, 110))

RED_CHIP = pygame.image.load('images/red_clay.png')
BLUE_CHIP = pygame.image.load('images/bluechip.png')
YELLOW_CHIP = pygame.image.load('images/yellow_clay.png')
GREEN_CHIP = pygame.image.load('images/green-removebg-preview.png')

# size the chips for the main game

CHIP_MAIN_DIAMETER = 100

RED_CHIP_SCALED = pygame.transform.scale(RED_CHIP, (CHIP_MAIN_DIAMETER, CHIP_MAIN_DIAMETER))
BLUE_CHIP_SCALED = pygame.transform.scale(BLUE_CHIP, (CHIP_MAIN_DIAMETER, CHIP_MAIN_DIAMETER))
YELLOW_CHIP_SCALED = pygame.transform.scale(YELLOW_CHIP, (CHIP_MAIN_DIAMETER, CHIP_MAIN_DIAMETER))
GREEN_CHIP_SCALED = pygame.transform.scale(GREEN_CHIP, (CHIP_MAIN_DIAMETER, CHIP_MAIN_DIAMETER))

# size the chips for the start screen

CHIP_DIAMETER = 170

RED_CHIP_START = pygame.transform.scale(RED_CHIP, (CHIP_DIAMETER, CHIP_DIAMETER))
BLUE_CHIP_START = pygame.transform.scale(BLUE_CHIP, (CHIP_DIAMETER, CHIP_DIAMETER))
YELLOW_CHIP_START = pygame.transform.scale(YELLOW_CHIP, (CHIP_DIAMETER, CHIP_DIAMETER))
GREEN_CHIP_START = pygame.transform.scale(GREEN_CHIP_SCALED, (CHIP_DIAMETER, CHIP_DIAMETER))

START_SCREEN_CHIP = [RED_CHIP_START, BLUE_CHIP_START, YELLOW_CHIP_START, GREEN_CHIP_START]

# set x locations for red, yellow and blue chips on the main screen

CONTROL_CHIPS_X = WIDTH - 150

# set dealer card and chip locations

DEALER_CARD_HEIGHT = 100
DEALER_CHIP_X = DEALER_START_X - DEALER_CHIP_SCALED.get_width() - 20
DEALER_CHIP_Y = HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT

# load fonts

DEALER_FONT = pygame.font.SysFont('rockwell', 22)
TOP_OF_CARD_FONT = pygame.font.SysFont('century gothic', 18)
PLAYER_FONT = pygame.font.SysFont('rockwell', 19)
BUST_FONT = pygame.font.SysFont('stencil', 55)
CHIP_FONT = pygame.font.SysFont('Segoe UI', 15, True, True)
DEALER_CHIP_FONT = pygame.font.SysFont('Segoe UI', 18, True, True)
START_PLAYER_FONT = pygame.font.SysFont('Segoe UI', 30, True, True)
RESULTS_FONT = pygame.font.SysFont('Segoe UI', 17, True, True)
PLAYER_CHIP_FONT = pygame.font.SysFont('rockwell', 22, False, True)
ROUND_NUMBER_FONT = pygame.font.SysFont('Segoe UI', 24, True, True)

# load sounds

DOUBLE_SOUND = pygame.mixer.Sound('sounds/double.mp3')
STAY_SOUND = pygame.mixer.Sound('sounds/stay.wav')
HIT_SOUND = pygame.mixer.Sound('sounds/hit.wav')
SHUFFLE_CARDS = pygame.mixer.Sound('sounds/card shuffle.wav')
DEALER_SOUND = pygame.mixer.Sound('sounds/dealer.wav')
CROWD_NOISE = pygame.mixer.Sound('sounds/crowd-talking-10.wav')

# Frame per second variable

FPS = 60

# bet per hand

BET = 10

# create screen

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Jack")


class Deck:
    def __init__(self, win):
        self.win = win
        self.cards = []
        self.suits = ['heart', 'diamond', 'club', 'spade']
        self.face_cards = ['jack', 'queen', 'king']

    def load_cards(self):
        back = pygame.image.load('cards/back.png')
        back_of_card = pygame.transform.scale(back, (CARD_WIDTH, CARD_HEIGHT))

        for suit in self.suits:
            # start with number cards 1 to 10
            for card in range(1, 11):
                # load the image of each card from cards
                new_image = pygame.image.load('cards/{}_{}.png'.format(str(card), suit))
                new_image_scaled = pygame.transform.scale(new_image, (CARD_WIDTH, CARD_HEIGHT))

                # create a Card object for the new card and append to the list of cards  with the following indexes:
                # 0. Value 1. X-value 2. Y-value 3. Rotation 4. Card Image 5. Back of card image 6. Window

                # if the card is an ace, add 10, as it will start at 11.

                if card == 1:
                    new_card = Card(card + 10, 0, 0, 0, new_image_scaled, back_of_card, self.win, True)
                    self.cards.append(new_card)

                else:
                    new_card = Card(card, 0, 0, 0, new_image_scaled, back_of_card, self.win)
                    self.cards.append(new_card)

            # now add the face cards, giving each face card a value of 10
            for face in self.face_cards:
                # load the image of each card from cards
                other_image = pygame.image.load('cards/{}_{}.png'.format(face, suit))
                other_image_scaled = pygame.transform.scale(other_image, (CARD_WIDTH, CARD_HEIGHT))

                # create a Card object for the new card and append to the list of cards with the following indexes:
                # 0. Value 1. X-value 2. Y-value 3. Rotation 4. Card Image 5. Back of card image 6. Window

                other_card = Card(10, 0, 0, 0, other_image_scaled, back_of_card, self.win)
                self.cards.append(other_card)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        player_card = self.cards.pop(0)
        return player_card


class Card:
    def __init__(self, value, x, y, rotation, up_img, down_img, win, ace=False):
        self.value = value
        self.x = x
        self.y = y
        self.rotation = rotation
        self.up_img = pygame.transform.rotate(up_img, self.rotation)
        self.down_img = pygame.transform.rotate(down_img, self.rotation)
        self.turned = False
        self.win = win
        self.ace = ace

    def draw_card_on_window(self):
        if self.turned:
            up_img_rotated = pygame.transform.rotate(self.up_img, self.rotation)
            self.win.blit(up_img_rotated, (self.x + CARD_GAP / 2, self.y + CARD_GAP / 2))
        else:
            down_img_rotated = pygame.transform.rotate(self.down_img, self.rotation)
            self.win.blit(down_img_rotated, (self.x + CARD_GAP / 2, self.y + CARD_GAP / 2))


class HandleBets:
    def __init__(self, game_number):
        self.game_number = game_number
        self.hand_complete = False

        # dictionary managing: [0] amount bet by players [1] whether they have doubled up

        self.handscores_double = [
            [0, False],
            [0, False],
            [0, False],
            [0, False]
        ]

    def double_up(self):
        self.handscores_double[player_index][1] = True

    def calculate_winnings(self, victors):
        for index, win in enumerate(victors):

            if win == 0:
                # player wins
                if self.handscores_double[index][1]:
                    win = BET * 4

                    players_wins_and_dollars_total[players[index]][1] += win
                    players_wins_and_dollars_total[players[3]][1] -= win

                    self.handscores_double[index][0] += win
                    self.handscores_double[3][0] -= win

                else:
                    win = BET * 2

                    players_wins_and_dollars_total[players[index]][1] += win
                    players_wins_and_dollars_total[players[3]][1] -= win

                    self.handscores_double[index][0] += win
                    self.handscores_double[3][0] -= win

            elif win == 1:
                # dealer wins
                loss = BET * 2
                if self.handscores_double[index][1]:
                    players_wins_and_dollars_total[players[index]][1] -= loss
                    players_wins_and_dollars_total[players[3]][1] += loss

                    self.handscores_double[index][0] -= loss
                    self.handscores_double[3][0] += loss

                else:
                    players_wins_and_dollars_total[players[index]][1] -= BET
                    players_wins_and_dollars_total[players[3]][1] += BET

                    self.handscores_double[index][0] -= BET
                    self.handscores_double[3][0] += BET

            elif win == 2:
                # this is a tie - do nothing
                continue

    def display_results(self):
        chip_gap = round((WIDTH - RED_CHIP_START.get_width() * 4) / 5)

        WIN.blit(TABLE_SCALED, (0, 0))
        WIN.blit(RED_CHIP_START, (chip_gap, HEIGHT / 2 - RED_CHIP_START.get_height() / 2))
        WIN.blit(BLUE_CHIP_START,
                 (chip_gap * 2 + RED_CHIP_START.get_width(), HEIGHT / 2 - BLUE_CHIP_START.get_height() / 2))
        WIN.blit(YELLOW_CHIP_START, (chip_gap * 3 + RED_CHIP_START.get_width() * 2,
                                     HEIGHT / 2 - RED_CHIP_START.get_height() / 2))
        WIN.blit(GREEN_CHIP_START, (chip_gap * 4 + RED_CHIP_START.get_width() * 3,
                                    HEIGHT / 2 - GREEN_CHIP_START.get_height() / 2))

        WIN.blit(GOLD_PLACARD_SCORE_SCALED, (WIDTH / 2 - GOLD_PLACARD_SCORE_SCALED.get_width() / 2, HEIGHT / 8))

        round_results_label = RESULTS_FONT.render("Winnings for Hand Number:", True, RUBY)
        WIN.blit(round_results_label, (WIDTH / 2 - round_results_label.get_width() / 2, HEIGHT / 8
                                       + GOLD_PLACARD_SCORE_SCALED.get_height() / 2 - round_results_label.get_height()))
        round_number = ROUND_NUMBER_FONT.render(str(self.game_number), True, NAVY)
        WIN.blit(round_number, (WIDTH / 2 - round_number.get_width() / 2, HEIGHT / 8
                                + GOLD_PLACARD_SCORE_SCALED.get_height() / 2))

        # blit the players and dealer's dollar winnings/ losing for the round

        for index, player in enumerate(players):

            player_text = PLAYER_CHIP_FONT.render(players[index], True, WHITE)
            winnings = self.handscores_double[index][0]

            if winnings >= 0:
                winning_text = PLAYER_CHIP_FONT.render(f"${winnings}", True, WHITE)
            else:
                winning_text = PLAYER_CHIP_FONT.render(f"${winnings}", True, CREAM)

            x_location_pyr_text = (index + 1) * chip_gap + index * RED_CHIP_START.get_height()\
                                  + RED_CHIP_START.get_width() / 2 - player_text.get_width() / 2
            y_location_pyr_text = HEIGHT / 2 - winning_text.get_height()
            x_location_win_text = (index + 1) * chip_gap + index * RED_CHIP_START.get_height() \
                                  + RED_CHIP_START.get_width() / 2 - winning_text.get_width() / 2
            y_location_win_text = HEIGHT / 2 + 5

            WIN.blit(player_text, (x_location_pyr_text, y_location_pyr_text))
            WIN.blit(winning_text, (x_location_win_text, y_location_win_text))

        pygame.display.update()


class SingleRound:
    CARD_COOL_DOWN = 55
    DEALER_COOL_DOWN = 150
    DOUBLE_BET_TIMER = 80
    DISPLAY_RESULTS_TIMER = 375

    def __init__(self, win):
        self.win = win
        self.deck = Deck(win)
        self.deck.load_cards()
        self.deck.shuffle_deck()

        self.index = 0
        self.round_one_dealt = False
        self.round_two_dealt = False
        self.dealer_finished = False
        self.players_finished = False
        self.turn = None

        # create variables to handle pauses

        self.card_cool_down_counter = 1

        self.dealer_finished_cool_down_counter = 1
        self.dealer_finished_counter = 0

        self.display_results_counter = 0
        self.display_results_finished = False

        self.hand_complete = False
        self.scores_totalled = False

        self.new_hand = HandleBets(hands_played)

        #  create a list of list, managing the scores in a single hand of cards containing the following indexes:
        #  0. Player name 1. Current score 2. Current hand 3. Bust 4. Blackjack 5. Double Up

        self.scores_hands_in_single_game = [
            ['Player A', 0, [], False, False, False],
            ['Player B', 0, [], False, False, False],
            ['Player C', 0, [], False, False, False],
            ['Dealer', 0, [], False, False, False]
        ]

        # Create a dictionary with keys referring to the round being dealt
        # containing dictionaries containing keys referring to the players (including dealer)
        # which contain tuples of tuples contain information about:
        # 0. x value 1. y value 2. card turned 3. rotation 4. index

        self.card_locations_orientations = {
            1: {'Player A': (PLAYERS_START_TUPLE[0], PLAYER_CARD_START_Y, True, 0, 0),
                'Player B': (PLAYERS_START_TUPLE[1], PLAYER_CARD_START_Y, True, 0, 1),
                'Player C': (PLAYERS_START_TUPLE[2], PLAYER_CARD_START_Y, True, 0, 2),
                'Dealer': (DEALER_START_X, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True, 0, 3)
                },
            2: {'Player A': (PLAYERS_START_TUPLE[0] + ADJ_XY_VALUE, PLAYER_CARD_START_Y + ADJ_XY_VALUE,
                             True, random.randint(MIN_TILT, MAX_TILT), 4),
                'Player B': (PLAYERS_START_TUPLE[1] + ADJ_XY_VALUE, PLAYER_CARD_START_Y + ADJ_XY_VALUE,
                             True, random.randint(MIN_TILT, MAX_TILT), 5),
                'Player C': (PLAYERS_START_TUPLE[2] + ADJ_XY_VALUE, PLAYER_CARD_START_Y + ADJ_XY_VALUE,
                             True, random.randint(MIN_TILT, MAX_TILT), 6),
                'Dealer': (DEALER_START_X + ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, False,
                           random.randint(MIN_TILT, MAX_TILT), 7)
                },
            3: {'Player A': [PLAYERS_START_TUPLE[0] + 2 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 2 * ADJ_XY_VALUE, True,
                             0],
                'Player B': [PLAYERS_START_TUPLE[1] + 2 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 2 * ADJ_XY_VALUE, True,
                             0],
                'Player C': [PLAYERS_START_TUPLE[2] + 2 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 2
                             * ADJ_XY_VALUE, True, 0, 2],
                'Dealer': (DEALER_START_X + 2 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True, 0)
                },
            4: {'Player A': [PLAYERS_START_TUPLE[0] + 3 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 3
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Player B': [PLAYERS_START_TUPLE[1] + 3 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 3
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Player C': [PLAYERS_START_TUPLE[2] + 3 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 3
                             * ADJ_XY_VALUE, True,
                             random.randint(MIN_TILT, MAX_TILT)],
                'Dealer': (DEALER_START_X + 3 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True,
                           random.randint(MIN_TILT, MAX_TILT))
                },
            5: {'Player A': [PLAYERS_START_TUPLE[0] + 4 * ADJ_XY_VALUE, PLAYER_CARD_START_Y
                             + 4 * ADJ_XY_VALUE, True, 0],
                'Player B': [PLAYERS_START_TUPLE[1] + 4 * ADJ_XY_VALUE, PLAYER_CARD_START_Y
                             + 4 * ADJ_XY_VALUE, True, 0],
                'Player C': [PLAYERS_START_TUPLE[2] + 4 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 4
                             * ADJ_XY_VALUE, True, 0, 2],
                'Dealer': (DEALER_START_X + 4 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True, 0)
                },
            6: {'Player A': [PLAYERS_START_TUPLE[0] + 5 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 5
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Player B': [PLAYERS_START_TUPLE[1] + 5 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 5
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Player C': [PLAYERS_START_TUPLE[2] + 5 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 5
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Dealer': (DEALER_START_X + 5 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True,
                           random.randint(MIN_TILT, MAX_TILT))
                },
            7: {'Player A': [PLAYERS_START_TUPLE[0] + 6 * ADJ_XY_VALUE, PLAYER_CARD_START_Y
                             + 6 * ADJ_XY_VALUE, True, 0],
                'Player B': [PLAYERS_START_TUPLE[1] + 6 * ADJ_XY_VALUE, PLAYER_CARD_START_Y
                             + 6 * ADJ_XY_VALUE, True, 0],
                'Player C': [PLAYERS_START_TUPLE[2] + 6 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 6
                             * ADJ_XY_VALUE, True, 0, 2],
                'Dealer': (DEALER_START_X + 6 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True, 0)
                },
            8: {'Player A': [PLAYERS_START_TUPLE[0] + 7 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 7
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Player B': [PLAYERS_START_TUPLE[1] + 7 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 7
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Player C': [PLAYERS_START_TUPLE[2] + 7 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 7
                             * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                'Dealer': (DEALER_START_X + 7 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True,
                           random.randint(MIN_TILT, MAX_TILT))
                },
            9: {'Player A': [PLAYERS_START_TUPLE[0] + 8 * ADJ_XY_VALUE, PLAYER_CARD_START_Y
                             + 8 * ADJ_XY_VALUE, True, 0],
                'Player B': [PLAYERS_START_TUPLE[1] + 8 * ADJ_XY_VALUE, PLAYER_CARD_START_Y
                             + 8 * ADJ_XY_VALUE, True, 0],
                'Player C': [PLAYERS_START_TUPLE[2] + 8 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 8
                             * ADJ_XY_VALUE, True, 0],
                'Dealer': (DEALER_START_X + 8 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True, 0)
                },
            10: {'Player A': [PLAYERS_START_TUPLE[0] + 9 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 9
                              * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                 'Player B': [PLAYERS_START_TUPLE[1] + 9 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 9
                              * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                 'Player C': [PLAYERS_START_TUPLE[2] + 9 * ADJ_XY_VALUE, PLAYER_CARD_START_Y + 9
                              * ADJ_XY_VALUE, True, random.randint(MIN_TILT, MAX_TILT)],
                 'Dealer': (DEALER_START_X + 9 * ADJ_XY_VALUE, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, True,
                            random.randint(MIN_TILT, MAX_TILT))
                 }
        }

    def assess_winners(self):
        # Function will return list with three digits, representing who has won between the dealer and each player
        # The first digit will represent Player A vs Dealer, second digit, Player B... etc
        # 0 represents Player win, 1 reps Dealer win, 2 reps a tie

        winners = []

        for idx, player in enumerate(self.scores_hands_in_single_game):
            if idx < 3:
                if self.scores_hands_in_single_game[idx][4]:
                    winners.append(0)
                elif self.scores_hands_in_single_game[idx][3]:
                    winners.append(1)
                elif self.scores_hands_in_single_game[3][3]:
                    winners.append(0)
                elif self.scores_hands_in_single_game[idx][1] == self.scores_hands_in_single_game[3][1]:
                    winners.append(2)
                elif self.scores_hands_in_single_game[idx][1] > self.scores_hands_in_single_game[3][1]:
                    winners.append(0)
                else:
                    winners.append(1)

        return winners

    def deal_card_to_player(self, player, x, y, turned, rotation):
        for card_player in self.scores_hands_in_single_game:
            if card_player[0] == player:
                card = self.deck.deal_card()

                card.turned = turned
                card.x = x
                card.y = y
                card.rotation = rotation
                card_player[2].append(card)

                # if the card is an ace, update self.scores_and_hands to show the player has another ace.
                if card.value == 1:
                    card_player[4] += 1
                break

    def card_cool_down(self):
        if self.card_cool_down_counter >= self.CARD_COOL_DOWN:
            self.card_cool_down_counter = 0
        elif self.card_cool_down_counter > 0:
            self.card_cool_down_counter += 1

    def dealer_finished_cool_down(self):
        if self.dealer_finished_cool_down_counter >= self.DEALER_COOL_DOWN:
            self.dealer_finished_cool_down_counter = 0
        elif self.dealer_finished_cool_down_counter > 0:
            self.dealer_finished_cool_down_counter += 1

    def deal_round(self, round_number):
        # deal 1 card to each play in sequence, including the dealer.
        # Cards must be given x and y positions based on where they will be drawn, rotations and a turned value,
        # where appropriate

        for player, value in self.card_locations_orientations[round_number].items():
            if self.index == value[4] and self.card_cool_down_counter == 0:
                self.deal_card_to_player(player, value[0], value[1], value[2], value[3])
                self.card_cool_down_counter = 1
                self.index += 1

                # if round one is dealt, mark True, so round 2 can start.

                if self.index == 4:
                    self.round_one_dealt = True

                elif self.index == 8:
                    self.round_two_dealt = True

    def play_further_rounds(self, player):
        global further_round
        global choice
        global player_index

        if choice == 'stay':

            player_index += 1

            STAY_SOUND.play()

            if not self.scores_hands_in_single_game[player_index][3]:
                further_round = 3
                choice = None

            else:
                player_index += 1

        elif choice == 'double':
            if not self.scores_hands_in_single_game[player_index][5]:
                self.new_hand.double_up()
                self.scores_hands_in_single_game[player_index][5] = True

                DOUBLE_SOUND.play()

                for contestant, value in self.card_locations_orientations[further_round].items():
                    if contestant == player:
                        # change the card orientation and x and y locations to reflect a double up
                        self.card_locations_orientations[further_round][contestant][0] -= 30
                        self.card_locations_orientations[further_round][contestant][1] += 25
                        self.card_locations_orientations[further_round][contestant][3] += 90

                        self.deal_card_to_player(player, value[0], value[1], value[2], value[3])

                        if not self.scores_hands_in_single_game[player_index][3]:
                            further_round += 1
                            choice = None

        elif choice == 'hit':

            HIT_SOUND.play()

            for contestant, value in self.card_locations_orientations[further_round].items():
                if contestant == player:
                    self.deal_card_to_player(player, value[0], value[1], value[2], value[3])

                    if not self.scores_hands_in_single_game[player_index][3]:
                        further_round += 1
                        choice = None

    def deal_dealer(self, round_number):
        global further_round

        if self.scores_hands_in_single_game[3][1] <= 16:

            for player, value in self.card_locations_orientations[round_number].items():
                if player == 'Dealer' and self.card_cool_down_counter == 0:
                    self.deal_card_to_player(player, value[0], value[1], value[2], value[3])
                    self.card_cool_down_counter = 1
                    further_round += 1

    def update_scores(self):
        # this function will continually loop through players' cards updating the scores
        # if a player or dealer exceeds 21, their 'bust' variable will change to True

        for index, card_player in enumerate(self.scores_hands_in_single_game):
            score = 0

            for card in card_player[2]:
                if card.turned:
                    value = card.value
                    score += value

            # if the player scores 21, Blackjack is set to True

            if score > 21:

                # loop through player's cards to check they do not have an ace.

                for card in card_player[2]:
                    if card.ace:
                        score -= 10
                        if score <= 21:
                            break

                else:
                    # change the 'bust' variable to True
                    card_player[3] = True

            if score == 21:
                self.scores_hands_in_single_game[index][4] = True

            # update the 'score' variable with the newly calculated score
            card_player[1] = score

            if self.scores_hands_in_single_game[3][3] \
                    or self.scores_hands_in_single_game[3][1] > 16 \
                    or ((self.scores_hands_in_single_game[0][3] or self.scores_hands_in_single_game[0][4])
                        and (self.scores_hands_in_single_game[1][3] or self.scores_hands_in_single_game[1][4])
                        and (self.scores_hands_in_single_game[2][3] or self.scores_hands_in_single_game[2][4])):
                if self.dealer_finished_counter == 15:
                    self.dealer_finished = True
                    self.dealer_finished_counter = 0
                else:
                    self.dealer_finished_counter += 1

    def draw_board(self, win):

        win.blit(TABLE_SCALED, (0, 0))

        # blit the logo on the board

        win.blit(LOGO_SCALED, (WIDTH - 10 - LOGO_SCALED.get_width(), 10))

        # if it is the dealer's turn blit the dealer chip

        if self.turn == 'Dealer':
            win.blit(DEALER_CHIP_SCALED, (DEALER_CHIP_X, DEALER_CHIP_Y))
            dealer_chip_text = DEALER_CHIP_FONT.render('Click', True, NAVY)
            win.blit(dealer_chip_text, (DEALER_CHIP_X + DEALER_CHIP_SCALED.get_width() / 2
                                        - dealer_chip_text.get_width() / 2, DEALER_CHIP_Y
                                        + DEALER_CHIP_SCALED.get_height() / 2 - dealer_chip_text.get_height() / 2))

        # blit poker chips for 'hit', 'double' and 'stay' on board

        win.blit(BLUE_CHIP_SCALED, (CONTROL_CHIPS_X, HEIGHT * 0.45))
        win.blit(RED_CHIP_SCALED, (CONTROL_CHIPS_X, HEIGHT * 0.8))
        win.blit(YELLOW_CHIP_SCALED, (CONTROL_CHIPS_X, HEIGHT * 0.625))

        # If it is a player's turn blit the words on top of the chips

        if self.turn is not None and self.turn != 'Dealer':
            red_chip_text = CHIP_FONT.render('Hit', True, WHITE)
            win.blit(red_chip_text, (CONTROL_CHIPS_X + RED_CHIP_SCALED.get_width() / 2 - red_chip_text.get_width() / 2,
                                     HEIGHT * 0.8 + RED_CHIP_SCALED.get_height() / 2 - red_chip_text.get_height() / 2))

            yellow_chip_text = CHIP_FONT.render('Stay', True, WHITE)
            win.blit(yellow_chip_text,
                     (CONTROL_CHIPS_X + YELLOW_CHIP_SCALED.get_width() / 2 - yellow_chip_text.get_width() / 2,
                      HEIGHT * 0.625 + YELLOW_CHIP_SCALED.get_height() / 2
                      - yellow_chip_text.get_height() / 2))

            blue_chip_text = CHIP_FONT.render('Double', True, WHITE)
            win.blit(blue_chip_text,
                     (CONTROL_CHIPS_X + BLUE_CHIP_SCALED.get_width() / 2 - blue_chip_text.get_width() / 2,
                      HEIGHT * 0.45 + BLUE_CHIP_SCALED.get_height() / 2 - blue_chip_text.get_height() / 2))

        for position, player in enumerate(self.scores_hands_in_single_game):

            # draw rectangles where player cards will be placed

            if position < 3:
                pygame.draw.rect(win, BLACK, (PLAYERS_START_TUPLE[position], round(PLAYER_CARD_START_Y),
                                              CARD_WIDTH + CARD_GAP, CARD_HEIGHT + CARD_GAP), 2, 5)

                # draw placards for the player's score

                placard_offset = (SILVER_PLACARD_SCALED.get_width() - CARD_WIDTH - CARD_GAP * 2) / 2

                win.blit(SILVER_PLACARD_SCALED, ((PLAYERS_START_TUPLE[position] - placard_offset,
                                                  PLAYER_CARD_START_Y - SILVER_PLACARD_SCALED.get_height() - 10)))

                # Set the colour to 'Ruby', if it is the player's turn. Else 'Navy'

                if self.turn == player[0]:

                    score_text = PLAYER_FONT.render(player[0] + ' :   ' + str(player[1]), True, RUBY)
                else:
                    score_text = PLAYER_FONT.render(player[0] + ' :   ' + str(player[1]), True, NAVY)

                win.blit(score_text, (PLAYERS_START_TUPLE[position] + CARD_GAP + CARD_WIDTH / 2
                                      - score_text.get_width() / 2, PLAYER_CARD_START_Y
                                      - SILVER_PLACARD_SCALED.get_height() / 2 - score_text.get_height() / 2 - 10))

            # draw a rectangle for the dealer's cards
            if position == 2:
                pygame.draw.rect(win, BLACK, (DEALER_START_X, HEIGHT - DEALER_CARD_HEIGHT - CARD_HEIGHT, CARD_WIDTH
                                              + CARD_GAP, CARD_HEIGHT + CARD_GAP), 2, 5)

        # Draw all the cards on the screen

        for player in self.scores_hands_in_single_game:
            for card in player[2]:
                card.draw_card_on_window()

        # Blit the dealer's placard and score under their cards

        dealer_score_text = DEALER_FONT.render(self.scores_hands_in_single_game[3][0] + ' :   '
                                               + str(self.scores_hands_in_single_game[3][1]), True, RUBY)
        win.blit(GOLD_PLACARD_SCALED, (DEALER_START_X + CARD_GAP / 2 + CARD_WIDTH / 2 - GOLD_PLACARD_SCALED.get_width()
                                       / 2, DEALER_PLACARD_Y))
        win.blit(dealer_score_text, (DEALER_START_X - 10, DEALER_PLACARD_Y + GOLD_PLACARD_SCALED.get_height() / 2
                                     - dealer_score_text.get_height() / 2))

        # If the dealer is BUST, blit on cards

        if self.scores_hands_in_single_game[3][3]:
            dealer_score_text = BUST_FONT.render('BUST', True, BLUE)
            dealer_bust_rotated = pygame.transform.rotate(dealer_score_text, 25)
            self.win.blit(dealer_bust_rotated, (DEALER_START_X - 10, HEIGHT - 80 - dealer_bust_rotated.get_height()))

        # if the dealer has Blackjack, blit on cards

        if self.scores_hands_in_single_game[3][4]:
            black_text = BUST_FONT.render('BlACK', True, RUBY)
            black_text_rotated = pygame.transform.rotate(black_text, 25)
            win.blit(black_text_rotated, (DEALER_START_X - 10, HEIGHT - 80 - black_text_rotated.get_height() - 30))
            jack_text = BUST_FONT.render('JACK', True, RUBY)
            jack_text_rotated = pygame.transform.rotate(jack_text, 25)
            win.blit(jack_text_rotated, (DEALER_START_X - 10, HEIGHT - 80 - jack_text_rotated.get_height() + 30))

        for index, plyr in enumerate(self.scores_hands_in_single_game):

            if plyr[3] and index < 3:
                bust_text = BUST_FONT.render('BUST', True, BLUE)
                bust_text_rotated = pygame.transform.rotate(bust_text, 25)
                win.blit(bust_text_rotated, (PLAYERS_START_TUPLE[index] - 20,
                                             round(1.25 * PLAYER_CARD_START_Y)))

            if self.scores_hands_in_single_game[index][4] and index < 3:
                black_text = BUST_FONT.render('BlACK', True, RUBY)
                black_text_rotated = pygame.transform.rotate(black_text, 25)
                win.blit(black_text_rotated, (PLAYERS_START_TUPLE[index] - 20,
                                              round(1.25 * PLAYER_CARD_START_Y) - 30))
                jack_text = BUST_FONT.render('JACK', True, RUBY)
                jack_text_rotated = pygame.transform.rotate(jack_text, 25)
                win.blit(jack_text_rotated, (PLAYERS_START_TUPLE[index] + 20,
                                             round(1.25 * PLAYER_CARD_START_Y) + 30))

    def update(self):
        global player_index
        global choice
        global further_round

        self.update_scores()

        if not self.dealer_finished:
            self.draw_board(self.win)

        if self.dealer_finished and self.dealer_finished_cool_down_counter == 0 and not self.hand_complete:
            winners = self.assess_winners()
            self.new_hand.calculate_winnings(winners)

            self.new_hand.display_results()
            self.hand_complete = True
            self.dealer_finished_cool_down_counter = 1

        # cool_down ensure that their is a pause in between cards and after dealer finishes

        self.card_cool_down()

        if self.dealer_finished:
            self.dealer_finished_cool_down()

        # deal the first cards to all players

        self.deal_round(1)

        # Once round 1 is done, deal second cards - dealer's face down.

        if self.round_one_dealt:
            self.deal_round(2)

        # Now players choosing rounds starts

        if self.round_two_dealt:
            self.turn = players[player_index]

        if self.turn is not None and self.turn != 'Dealer' and choice is not None:
            self.play_further_rounds(self.turn)

        # check of players have gone bust and if so, turn will move to the next player by incrementing the index

        if self.scores_hands_in_single_game[player_index][3] or self.scores_hands_in_single_game[player_index][4]:
            choice = None
            further_round = 3

            if player_index != 3:
                player_index += 1

        if self.turn == 'Dealer':

            # turn all dealers cards

            for card in self.scores_hands_in_single_game[3][2]:
                card.turned = True

        if self.turn == 'Dealer' and further_round < 11 and choice == 'deal':
            self.deal_dealer(further_round)

        if self.hand_complete:
            if self.display_results_counter >= self.DISPLAY_RESULTS_TIMER:
                self.display_results_finished = True
            else:
                self.display_results_counter += 1

        # update the wins and money exchanged on
        # players_wins_and_dollars_total

        if self.display_results_finished and self.hand_complete and not self.scores_totalled:
            hand_winners = self.assess_winners()

            for index, winner in enumerate(hand_winners):

                if winner == 0:
                    players_wins_and_dollars_total[players[index]][0] += 1
                elif winner == 1:
                    players_wins_and_dollars_total[players[3]][0] += 1

            self.scores_totalled = True

        pygame.display.update()


def get_chip_from_mouse(pos):
    # create variables showing the centre points of the 4 chips

    red_chip_x, red_chip_y = CONTROL_CHIPS_X + RED_CHIP_SCALED.get_width() / 2, HEIGHT * 0.8 + RED_CHIP_SCALED.get_height() / 2
    yellow_chip_x, yellow_chip_y = CONTROL_CHIPS_X + YELLOW_CHIP_SCALED.get_width() / 2, HEIGHT * 0.625 \
                                   + YELLOW_CHIP_SCALED.get_height() / 2
    blue_chip_x, blue_chip_y = CONTROL_CHIPS_X + BLUE_CHIP_SCALED.get_width() / 2, HEIGHT * 0.45 + BLUE_CHIP_SCALED.get_height() / 2

    # white_chip_x, white_chip_y = DEALER_START_X - 120 + DEALER_CHIP_SCALED.get_width() / 2,\
    #                              HEIGHT - 60 - CARD_HEIGHT + DEALER_CHIP_SCALED.get_height() / 2

    white_chip_centre_x, white_chip_centre_y = DEALER_CHIP_X + DEALER_CHIP_SCALED.get_width() / 2, \
                                               DEALER_CHIP_Y + DEALER_CHIP_SCALED.get_height() / 2,

    x, y = pos

    if red_chip_x - 45 < x < red_chip_x + 45 and red_chip_y - 45 < y < red_chip_y + 45:
        return 'hit'

    elif yellow_chip_x - 45 < x < yellow_chip_x + 45 and yellow_chip_y - 45 < y < yellow_chip_y + 45:
        return 'stay'

    elif blue_chip_x - 45 < x < blue_chip_x + 45 and blue_chip_y - 45 < y < blue_chip_y + 45:
        return 'double'

    elif white_chip_centre_x - DEALER_CHIP_SCALED.get_width() / 2 < x < white_chip_centre_x \
            + DEALER_CHIP_SCALED.get_width() / 2 and white_chip_centre_y - \
            DEALER_CHIP_SCALED.get_height() / 2 < y < white_chip_centre_y + DEALER_CHIP_SCALED.get_height() / 2:
        return 'deal'


def reset_round():
    global further_round
    global choice
    global player_index

    further_round = 3
    choice = None
    player_index = 0


# create a global variable to control which card round the players are on, for the choice rounds.

further_round = 3
choice = None

hands_played = 1

# create a variable and a list to manage whose turn it is after everyone has been dealt

player_index = 0
players = ['Player A', 'Player B', 'Player C', 'Dealer']

players_wins_and_dollars_total = {'Player A': [0, 500], 'Player B': [0, 500], 'Player C': [0, 500], 'Dealer': [0, 3000]}


def main():
    global choice
    global hands_played

    run = True

    if hands_played % 3 == 0:
        CROWD_NOISE.play()

    # create a game objects

    game = SingleRound(WIN)

    SHUFFLE_CARDS.play()

    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        game.update()

        if game.scores_totalled:
            del game
            reset_round()
            hands_played += 1
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                choice = get_chip_from_mouse(pos)


def starting_screen():
    run = True

    CROWD_NOISE.play()

    # load images and fonts required for the start screen

    poker_chip = pygame.image.load('images/nice_blue-removebg-preview.png')
    poker_chip_scaled = pygame.transform.scale(poker_chip, (220, 220))
    chip_font = pygame.font.SysFont('rockwell', 20, False, True)
    player_font = pygame.font.SysFont('rockwell', 24, False, True)

    while run:

        # blit the images on screen

        WIN.blit(START_SCREEN_SCALED, (0, 0))
        WIN.blit(LOGO_START_SCALED, (WIDTH / 2 - LOGO_SCALED.get_width() / 2, 20))

        chip_text = chip_font.render('Click to Play', True, WHITE)
        WIN.blit(poker_chip_scaled, (WIDTH / 2 - poker_chip_scaled.get_width() / 2, (4 * HEIGHT) / 7))
        WIN.blit(chip_text, (WIDTH / 2 - chip_text.get_width() / 2, (4 * HEIGHT) / 7
                             + poker_chip_scaled.get_height() / 2 - chip_text.get_height() / 2))

        for index, player in enumerate(players):
            current_wins_score = players_wins_and_dollars_total[player][0]
            total_dollars = players_wins_and_dollars_total[player][1]

            chip_gap = round(WIDTH - RED_CHIP_START.get_width() * 4) / 5

            player_text = player_font.render(player, True, WHITE)
            WIN.blit(START_SCREEN_CHIP[index], (chip_gap * (index + 1) + index * RED_CHIP_START.get_width(), 150))
            WIN.blit(player_text, (chip_gap * (index + 1) + index * RED_CHIP_START.get_width()
                                   + RED_CHIP_START.get_width() / 2 - player_text.get_width() / 2,
                                   150 + RED_CHIP_START.get_height() + 5))

            wins_score_text = PLAYER_CHIP_FONT.render('Wins:  ' + str(current_wins_score), True, WHITE)
            dollars_score_text = PLAYER_CHIP_FONT.render('$' + str(total_dollars), True, WHITE)
            WIN.blit(wins_score_text, (chip_gap * (index + 1) + index * RED_CHIP_START.get_width()
                                       + RED_CHIP_START.get_width() / 2 - wins_score_text.get_width() / 2,
                                       150 + RED_CHIP_START.get_height() / 2 - 20))
            WIN.blit(dollars_score_text, (chip_gap * (index + 1) + index * RED_CHIP_START.get_width()
                                          + RED_CHIP_START.get_width() / 2 - dollars_score_text.get_width() / 2,
                                          150 + RED_CHIP_START.get_height() / 2 + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


if __name__ == '__main__':
    # add music track

    pygame.mixer.music.load('sounds/jazzpiano.mp3')
    pygame.mixer.music.play(-1)

    starting_screen()
