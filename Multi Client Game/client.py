import pygame
from network import Network
import sys

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.name = self.text.upper()[0]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (0, 0, 0))
        surface.blit(
            text,
            (
                self.x + round(self.width / 2) - round(text.get_width() / 2),
                self.y + round(self.height / 2) - round(text.get_height() / 2),
            ),
        )

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawWindow(surface, game, p):
    surface.fill((0, 0, 0))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting For Opponent...", 1, (0, 255, 255), True)
        surface.blit(
            text,
            (
                round(width / 2 - text.get_width() / 2),
                round(height / 2 - text.get_height() / 2),
            ),
        )
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        surface.blit(text, (50, 200))

        text = font.render("Opponent", 1, (0, 255, 255))
        surface.blit(text, (390, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (255, 255, 255))
            text2 = font.render(move2, 1, (255, 255, 255))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255, 255, 255))
            elif game.p1Went:
                text1 = font.render("Ready", 1, (255, 255, 255))
            else:
                text1 = font.render("Waiting...", 1, (255, 255, 255))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255, 255, 255))
            elif game.p2Went:
                text2 = font.render("Ready", 1, (255, 255, 255))
            else:
                text2 = font.render("Waiting...", 1, (255, 255, 255))

        if p == 1:
            surface.blit(text2, (70, 350))
            surface.blit(text1, (410, 350))

        else:
            surface.blit(text1, (70, 350))
            surface.blit(text2, (410, 350))

        for btn in btns:
            btn.draw(surface)

    pygame.display.update()


btns = [
    Button("Rock", 50, 500, (200, 0, 0)),
    Button("Paper", 250, 500, (0, 200, 0)),
    Button("Scissors", 450, 500, (0, 0, 200)),
]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except Exception:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except Exception:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if game.winner() == player:
                text = font.render("Round Won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Round!", 1, (255, 0, 0))
            else:
                text = font.render("Round Lost...", 1, (255, 0, 0))

            win.blit(
                text,
                (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2),
            )
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    if btn.isOver(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

            if event.type == pygame.MOUSEMOTION:
                for btn in btns:
                    if game.connected():
                        if btn.isOver(pos):
                            if btn.name == "R":
                                btn.color = (255, 0, 0)
                            elif btn.name == "S":
                                btn.color = (0, 0, 255)
                            else:
                                btn.color = (0, 255, 0)
                        else:
                            if btn.name == "R":
                                btn.color = (200, 0, 0)
                            elif btn.name == "S":
                                btn.color = (0, 0, 200)
                            else:
                                btn.color = (0, 200, 0)

        redrawWindow(win, game, player)


def menu_screen():
    mRun = True
    clock = pygame.time.Clock()

    while mRun:
        clock.tick(60)
        win.fill((0, 0, 0))
        fontT = pygame.font.SysFont("comicsans", 80)
        font = pygame.font.SysFont("comicsans", 60)
        textT = fontT.render("Rock Paper Scissors", 1, (0, 255, 255))
        win.blit(textT, (round(width / 2 - textT.get_width() / 2), 100))
        text = font.render("Click to Play!", 1, (255, 255, 255))
        win.blit(
            text,
            (
                round(width / 2 - text.get_width() / 2),
                round(height / 2 - text.get_height() / 2),
            ),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                mRun = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mRun = False

    main()


while True:
    menu_screen()
