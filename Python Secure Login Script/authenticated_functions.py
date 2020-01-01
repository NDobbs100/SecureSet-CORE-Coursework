# This class contains functions that can only be run by authenticated users
from user import *
from helpers import gen_hash, gen_salt
from file_io import *
import os
import logging
import getpass


# This function returns a user to the runtime dictionary
def addUser(userName, userPermissions, salt, userPassHash):
    return User(userName, userPermissions, salt, userPassHash)


# This code allows for the authenticated user to do limited file I/O
def runtimeLogic(args, userDB, userName):
    try:
        # This statement allows the admin user to add new users
        if args[0] == 'adduser':
            if userDB[userName].userPermissions == 0:
                newUserName = args[1].strip()
                newUserPass = getpass.getpass('Enter a password [ASCII]: ').strip()
                checkUserPass = getpass.getpass('Re-enter password [ASCII]: ').strip()

                if newUserPass == checkUserPass:
                    newUserPermissions = int(input('Enter permissions for the user [0/1/2]: '))
                    newUserSalt = gen_salt()
                    userDB[newUserName] = addUser(newUserName, newUserPermissions, newUserSalt, gen_hash(newUserPass, newUserSalt))
                    logging.info('User {} added by {}'.format(newUserName, userName))
                    writeUserDBtoFile('userDB.txt', userDB)
                    return True
                else:
                    print('Passwords did not match. Please try again.')
                    return True
            else:
                print('Insufficient permissions to add users.')
                return True

        # This code allows the admin user to delete users
        elif args[0] == 'deluser':
            if userDB[userName].userPermissions == 0:
                confirm = input('Are you sure you want to delete user {}? [y/n]> '.format(args[1]))
                if confirm == 'y':
                    try:
                        del userDB[args[1]]
                        writeUserDBtoFile('userDB.txt', userDB)
                        logging.info('User {} deleted by {}.'.format(args[1], userName))
                        return True
                    except:
                        logging.info('User {} does not exist. Unable to delete.'.format(args[1]))
                        return True
                else:
                    return True
            else:
                print('Insufficient permissions to delete users.')
                return True

        # This statements allows the current user to change their password
        elif args[0] == 'chngpwd':
            # Get PW hash
            currentPW = getpass.getpass().strip()
            # Make hash of the input password
            currentPWHash = gen_hash(currentPW, userDB[userName].userSalt)
            # If the input matches the one stored in the DB, then proceed to update
            if currentPWHash == userDB[userName].userPassHash:
                # Get and validate new password for the user
                newUserPass = getpass.getpass('Enter a new password [ASCII]: ').strip()
                checkUserPass = getpass.getpass('Re-enter the new password [ASCII]: ').strip()
                # If they match...
                if newUserPass == checkUserPass:
                    # update the user information, and write it to the db file
                    userDB[userName].userPassHash = gen_hash(newUserPass, userDB[userName].userSalt)
                    writeUserDBtoFile('userDB.txt', userDB)
                    logging.info('{} password updated.'.format(userName))
                    print('Password updated.')
                    return True
                else:
                    print('Passwords do not match. Try again.')
                    return True
            else:
                print('Incorrect password. Try again.')
                return True

        # This code allows the admin user to change the permissions of any other user
        elif args[0] == 'chngperm':
            if userDB[userName].userPermissions == 0:
                userDB[args[1]].userPermissions = args[2]
                writeUserDBtoFile('userDB.txt', userDB)
                logging.info('{} permissions changed to {}.'.format(args[1], args[2]))
                return True
            else:
                print('Insufficient permissions to change user permissions.')
                return True

        # Allows any user to make a file
        elif args[0] == 'mkfile':
            try:
                file = 'Documents/' + args[1]
                flptr = open(file, 'w+')
                logging.info('User {} created file {}.'.format(userName, args[1]))
                return True
            except FileExistsError:
                logging.info('File {} already exists. Unable to make file.'.format(args[1]))
                return True

        # This statement allows the admin user to delete files
        elif args[0] == 'delfile':
            if userDB[userName].userPermissions == 0:
                try:
                    os.remove('Documents/' + args[1])
                    logging.info('File {} deleted by {}.'.format(args[1], userName))
                    return True
                except FileNotFoundError:
                    logging.info('File', args[1], 'not found. Unable to delete.')
                    return True
            else:
                print('Insufficient permissions to delete files.')
                return True

        # This statement allows any user to read files
        elif args[0] == 'r':
            try:
                with open('Documents/' + args[1], 'r') as file:
                    contents = file.readlines()

                for line in contents:
                    print(line)
                    return True
            except FileNotFoundError:
                print('File {} not found. Unable to read.'.format(args[1]))
                return True

        # This statement allows for any regular or admin user to write to files
        elif args[0] == 'w' and userDB[userName].userPermissions <= 1:
            try:
                with open('Documents/' + args[1], 'a') as file:
                    writing = True
                    print('Opening {}. Begin writing below. Type :wq to quit.'.format(args[1]))
                    while writing:
                        lineToWrite = input('> ')
                        if lineToWrite == ':wq':
                            print('Closing file...')
                            lineToWrite = ''
                            writing = False
                        else:
                            file.write(lineToWrite)
                            logging.info('User {} wrote < {} > to file {}'.format(userName, lineToWrite, args[1]))
                    return True
            except FileNotFoundError:
                logging.info('File {} not found. Unable to write.'.format(args[1]))
                return True

        #elif args[0] == 'x':
            #try:
                #os.system('python ' + args[1])
                #return True
            #except FileNotFoundError:
                #logging.info('File', args[1], 'not found. Unable to execute.')
                #return True

        # This statement allows any user to view the contents of the documents folder
        elif args[0] == 'pcd':
            files = os.listdir('Documents/')
            if len(files) > 0:
                for file in files:
                    print(file)
                    return True
            else:
                print('No files found in Documents/ folder.')
                return True

        # This statement prints the list of possible commands
        elif args[0] == 'h':
            print('''
            adduser  == add a new user [adduser <username>]
            deluser  == delete user [deluser <username>]
            chngpwd  == change current user password [chngpwd]
            chngperm == change user permissions []
            mkfile   == make a file [mkfile <filename.ext>]
            delfile  == delete a file [delfile <filename.ext>]
            r        == read contents of a file [r <filename.ext>]
            w        == append to a file [w <filename.ext>]
                        -> :wq to write and quit
            pcd      == print contents of current directory [pcd]
            logout   == logs out the current user [logout]
            quit     == closes program [quit]''')
            return True

        # This statement allows the user to logout, and log back in as another user
        elif args[0] == 'logout':
            print('Logging out user {}.'.format(userName))
            return False
        else:
            print('Invalid Argument(s). Type h for info.')
            return True
    except:
        print('Invalid argument(s). Type h for info.')
        return True
