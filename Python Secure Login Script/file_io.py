# This class deals with file I/0
import user


# Read and sanitize the database file, and then put the contents into a dictionary for main() use
def readUserDB(file):
    with open(file, 'r') as file:
        contents = file.readlines()

    # Strip nonessential characters from read lines
    contents = [x.strip() for x in contents]

    # Instantiate the empty database
    userDB = {}
    for line in contents:
        # Split the line, and feed them into the user dictionary
        userVarList = line.split(":")
        newUser = user.User(userVarList[0], userVarList[1], userVarList[2], userVarList[3])
        userDB[userVarList[0]] = newUser

    return userDB


# Write the runtime user dictionary to our database file for persistence
# Assumption here is that we will always have a complete list of users during runtime, so any changes can be made...
# and then overwritten without problems
def writeUserDBtoFile(file, userDB):
    with open(file, 'w') as file:
        for key in userDB.keys():
            line = userDB[key].userName+':'+str(userDB[key].userPermissions)+':'+userDB[key].userSalt+':'+userDB[key].userPassHash+'\n'
            file.write(line)
