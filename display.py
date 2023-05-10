import sqlite3
import pygame

db = sqlite3.connect('database.db', check_same_thread=False)


class NoSuchUser(Exception):
    pass


class InsufficientFunds(Exception):
    pass


class OutOfStock(Exception):
    pass


def dispense(coil):
    print("Would despense from", coil)


def getUserBalance(id):
    c = db.cursor()
    c.execute(
        "SELECT balance FROM USERS where id = ?", [id])

    result = c.fetchone()

    if (result == None):
        raise NoSuchUser

    c.close()
    return result[0]


def getCoilNamePriceCalsStock(coil):
    c = db.cursor()
    c.execute(
        "SELECT name, price, calories, qty_remain FROM items WHERE location = ?", [coil])

    result = c.fetchone()

    if (result == None):
        raise OutOfStock

    c.close()
    return result


def transact(username, coil):
    balance = getUserBalance(username)
    (_, price, _, stock) = getCoilNamePriceCalsStock(coil)
    if (price > balance):
        raise InsufficientFunds

    if (stock < 1):
        raise OutOfStock

    # We are now cleared to continue with the transaction
    c = db.cursor()
    c.execute("UPDATE users SET balance = ? WHERE username = ?",
              [balance - price, username])
    c.execute("UPDATE items SET qty_remain = ? WHERE location = ?",
              [stock - 1, coil])
    db.commit()

    # Now the database has been updated, we can dispense
    dispense(coil)


pygame.init()
pygame.font.init()
font25 = pygame.font.Font(pygame.font.get_default_font(), 25)
font15 = pygame.font.Font(pygame.font.get_default_font(), 15)
screen = pygame.display.set_mode((320, 240))
running = True

current_stage = "login"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_stage == "login":
        screen.fill("black")
        title = font25.render('Enter user ID', False, (255, 255, 255))
        screen.blit(title, dest=(50, 0))

    pygame.display.flip()
