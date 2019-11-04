from datetime import datetime, date, time
from Entities.User import *
from Entities.Author import *
from Entities.Book import *

class BorrowedBooks():
    def __init__(self, book_id, userID, borrowed, bdate, rdate):
        self.book_id = book_id
        self.userID = userID
        self.borrowed = borrowed
        self.bdate = date
        self.rdate = rdate

class DynamicBD():
    
    def __init__(self):
        self.Users = []
        self.Books = []
        self.BBooks = []

    def addUser(self, userID):
        user = User(userID, '', 'User# ' +str(userID), '', '')
        user._print()
        self.Users.append(user)
    
    def deleteUser(self):
        ''' '''
    
    def addBook(self, bookID, title, date, publisher, author):
        authors = []
        fname = ''
        lname = ''
        mname = ''
        flag = 0

        for c in author:
            if(flag == 4):
                flag = 0
                if(c == ' '):
                    continue
            if(c == ' '):
                flag = flag + 1
                continue
            if(c == ','):
                flag = 4
                authors.append(Author(-1, fname, lname, mname))
                fname = ''
                lname = ''
                mname = ''
                continue
            if(flag == 0):
                fname += c
                continue
            if(flag == 1):
                lname += c
                continue
            if(flag == 2):
                mname += c
                continue
        authors.append(Author(-1, fname, lname, mname))

        book = Book(bookID, '', title, date, publisher, authors,)
        book._print()
        self.Books.append(book)
    
    def deleteBook(self):
        ''' '''    
     
    def getRetBook(self, userID, bookID):
        dateNow = str(datetime.now())
        find = False
        for book in self.BBooks:
            if book.bookID ==  bookID and userID == book.userID and not book.borrowed: 
                book.borrowed = not book.borrowed
                book.rdate = dateNow
                find = True
                break
        
        if not find and not book.borrowed:
            bbook = BorrowedBooks(bookID, userID, False, dateNow, '' )
            find = True
            self.BBooks.append(bbook)
    
        return find
           
    def printUsers(self):
        print('{:<10}{:<10}'.format('ID', 'Name'))
        for user in self.Users:
            print('{:<10}{:<10}'.format(user.user_id, user.first_name))


    def printBooks(self):
        authorsStr = ''
        print('{:<10}{:<20}{:<10}{:<10}{:<10}'.format('ID', 'Author','Title',
        'Publisher', 'Publication date'))
        for book in self.Books:
            for j in enumerate(book.authors):
                if (j[0] == len(book.authors) - 1):
                    c = ''
                authorsStr += (book.authors[j[0]].first_name + ' ' +
                            book.authors[j[0]].last_name + ' ' +
                            book.authors[j[0]].middle_name + c)
            print('{:<10}{:<20}{:<10}{:<10}{:<10}'.format(book.book_id, authorsStr,
                book.title, book.publisher, book.year))

    def printBBooks(self):
        print('{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}'.format('User ID', 'Book ID', 'First name',
             'Title',  'Borrow date','Return date'))
        for bbook in self.BBooks:
            for book in self.Books:
                for user in self.Users:
                        if bbook.userID == user.user_id and bbook.bookID == book.book_id:
                            print('{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}'.format(user.user_id, book.bookID,
                                 user.first_name, book.title, bbook.bdate, bbook.rdate))
                        
 