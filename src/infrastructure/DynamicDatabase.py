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
        self.rdate = publisher

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
            if book.bookID ==  bookID and userID == book.userID:
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
        print('ID', ' '*10, 'First Name')
        for user in self.Users:
            print(user.user_id, ' '*10, user.first_name)

    def printBooks(self):
        authorsStr = ''
        print('ID',' '*10, 'Author',' '*10, 'Title',' '*10, 'Publisher',' '*10, 'Publication date')
        for book in self.Books:
            for j in enumerate(book.authors):
                if (j[0] == len(book.authors) - 1):
                    c = ''
                authorsStr += (book.authors[j[0]].first_name + ' ' +
                            book.authors[j[0]].last_name + ' ' +
                            book.authors[j[0]].middle_name + c)
            print(book.book_id, ' '*10, authorsStr,' '*10, book.title, book.publisher, book.year)

    def printBBooks(self):
        print('User ID',' '*10, 'Book ID',' '*10, 'First name',' '*10, 'Title', ' '*10, 'Borrow date',' '*10,'Return date')
        for bbook in self.BBooks:
            for book in self.Books:
                for user in self.Users:
                        if bbook.userID == user.user_id and bbook.bookID == book.book_id:
                            s = user.user_id + ' '*10 + book.bookID + ' '*10 + user.first_name + ' '*10 + book.title + ' '*10 + bbook.bdate +  ' '*10 + bbook.rdate
                            print(s)
                        
 