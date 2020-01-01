# This class holds all of our helping functions
import hashlib
import random


# Function to generate a salt for our passwords. It returns a random selection of 16 characters.
def gen_salt():
    alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(alpha))
    return ''.join(chars)


# This function generates a seasoned hash of the input password
def gen_hash(userPassword, salt):
    pepper = 'securityisfun'
    seasoned = salt + userPassword + pepper
    return hashlib.sha256(seasoned.encode('utf-8')).hexdigest()


# This function checks the validity of the user input from main function
def authenticated(userName, userPassword, userDB):
    # If the username is in the runtime user dictionary...
    if userName in userDB.keys():
        # If the password matches the username...
        if gen_hash(userPassword, userDB[userName].userSalt).lower() == userDB[userName].userPassHash.lower():
            # Then we want to authenticate the user
            return True
        else:
            return False
    else:
        return False
