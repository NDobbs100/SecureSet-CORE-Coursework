# Main class for the SYS200 Capstone Project
# Import statements
from helpers import *
import time
from authenticated_functions import *


# Defining our main function here
def main():
    # Configure the logging tool
    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    # Try to make the runtime user database from the persistent database file
    try:
        userDB = readUserDB('userDB.txt')
        logging.info('User database successfully loaded at runtime.')
    # If the file isn't found, we want to prompt the user to add themselves and create a new DB file
    except FileNotFoundError:
        # Make runtime dictionary of users & get inputs
        userDB = {}
        print('No users on local system. Please make a root user.\n')
        newUserName = input('Enter a username [Alpha]: ').strip()
        newUserPass = getpass.getpass('Enter a password [ASCII]: ').strip()
        checkUserPass = getpass.getpass('Re-enter password [ASCII]: ').strip()

        # Check that both passwords match before adding the user to the official list
        if newUserPass == checkUserPass:
            # Set superuser permissions, generate salt and instantiate user object.
            newUserPermissions = 0
            salt = gen_salt()
            userDB[newUserName] = addUser(newUserName, newUserPermissions, salt, gen_hash(newUserPass, salt))
            logging.info('Created root user with alias {}.'.format(newUserName))
            # Save the user now
            writeUserDBtoFile('userDB.txt', userDB)
        else:
            print('Passwords did not match. Please try again.')

    # Instantiate the login instance variables
    login_attempts = 0
    max_login_attempts = 3
    failed_login_sessions = 0

    # Start the login instance
    while login_attempts <= max_login_attempts:
        # If we reach the maximum login attempts for the session, lock the terminal
        if login_attempts == max_login_attempts:
            failed_login_sessions += 1
            tOut = str(((300*failed_login_sessions)/60))
            logging.warning('Too many consecutive failed login attempts. Locking system for {} minutes.'.format(tOut))
            print('Too many consecutive failed login attempts. Locking system for {} minutes.'.format(tOut))
            login_attempts = 0
            # We want to lock the session for an increasing length of time
            time.sleep(300 * failed_login_sessions)

        # Take user inputs, strip whitespaces
        userName = input('Username: ').strip()
        # We use getpass, since we're not total n00bs, strip whitespaces
        userPassword = getpass.getpass('Password: ').strip()

        # Check to see that inputs are valid character sets
        if userName.isalpha() & userPassword.isascii():
            # Check to see if the inputs are valid
            if authenticated(userName, userPassword, userDB):
                logging.info('User {} authenticated.'.format(userName))
                print('User {} authenticated.'.format(userName))
                print('Enter commands below. Type h for list of possible commands.\n')
                status = True
                while status:
                    # Take user input in pseudo-terminal
                    args = input('> ').lower().split()
                    # Allows the user to terminate the process
                    if args[0] == 'quit':
                        print('Quitting program...')
                        quit()
                    elif args:
                        # Update runtime status as we go, checking for logout
                        status = runtimeLogic(args, userDB, userName)
                    else:
                        status = True
            else:
                logging.warning('Invalid credential(s): {}: {}'.format(userName, userPassword))
                print('Invalid credential(s).', str((max_login_attempts-1) - login_attempts),
                      ' login attempt(s) remaining.')
                login_attempts += 1
        else:
            logging.warning('Invalid input(s): {}: {}'.format(userName, userPassword))
            print('Invalid input(s).', str((max_login_attempts-1) - login_attempts),
                  ' login attempt(s) remaining.')
            login_attempts += 1


if __name__ == '__main__':
    main()
