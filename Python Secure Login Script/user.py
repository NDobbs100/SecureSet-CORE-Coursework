# This file defines a user object


# This class defines the user object
class User:
    def __init__(self, userName, userPermissions, salt, userPassHash):
        self.userName = userName
        self.userPermissions = int(userPermissions)
        self.userSalt = salt
        self.userPassHash = userPassHash
