import sqlite3

db = sqlite3.connect('database.db', check_same_thread=False)


class NoSuchUser(Exception):
    pass


class InsufficientFunds(Exception):
    pass


class OutOfStock(Exception):
    pass


def dispense(coil):
    print("Would despense from", coil)


def getUserBalance(username):
    c = db.cursor()
    c.execute(
        "SELECT balance FROM USERS where username = ?", [username])

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
