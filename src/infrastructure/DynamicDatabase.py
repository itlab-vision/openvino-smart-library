from Entities.User import *
from Entities.Book import *

class DynamicBD():
    
    def __init__(self):
        self.Users = []
        self.Books = []

    def addUser(self, n):
        user = User(n, '', 'User# ' +str(n), '', '')
        user._print()
        self.Users.append(user)
    
    def deleteUser(self):
        ''' '''
    
    def addBook(self):
        ''' '''
    
    def deleteBook(self):
        ''' '''    
     
    def getRetBook(self):
        ''' '''
    def printUsers(self):
        print('id', ' '*10, 'First Name')
        for user in self.Users:
            print(user.user_id, ' '*10, user.first_name)

    def printBooks(self):
        ''' '''
    def printBorrowBookS(self):
        ''' '''
