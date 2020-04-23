import csv # модуль для работы с csv-файлами

from datetime import datetime

# импорт всех интерфейсов:
from IDatabaseInterfaces import IDatabaseBRM, IDatabaseAuthService
from IDatabaseInterfaces import IDatabaseFRM, IDatabaseGUI

from Entities.Book import Book
from Entities.User import User
from Entities.Role import Role
from Entities.Author import Author
from Entities.Model import Model

# ПРИМЕЧАНИЕ: для корректной работы методов оформляйте строки в БД правильно.
# При записи любых данных в файлы БД вручную обязательно в конце сделать
# перевод строки на новую.

path = 'src/infrastructure/Database/'

# внешняя функция для подсчёта строк в файле
def NumOfLines(file):
    lines = 0
    for line in open(file):
        lines = lines + 1
    return lines

class CSVDatabase(IDatabaseBRM, IDatabaseAuthService,
                  IDatabaseFRM, IDatabaseGUI):
    # dbRootDir = 'infrastructure/Database/'
    dbRootDir = 'src/infrastructure/Database/'
    
    def __init__(self):
        self.fBooks = self.dbRootDir + 'Books/Books.csv'
        self.fAuthors = self.dbRootDir + 'Books/Authors.csv'
        self.fAuthorship = self.dbRootDir + 'Books/Authorship.csv'
        self.fUsers = self.dbRootDir + 'Users/Users.csv'
        self.fUserRole = self.dbRootDir + 'Users/UserRole.csv'
        self.fRoles = self.dbRootDir + 'Users/Roles.csv'
        self.fModels = self.dbRootDir + 'Users/Models.csv'
        #
        self.dUser = {'user_id': 'user_id', 'phone': 'phone',
                         'first_name': 'first_name', 'last_name': 'last_name',
                         'middle_name': 'middle_name'}
        self.dBook = {'book_id': 'book_id', 'file_path': 'file_path',
                      'title': 'title', 'year': 'year',
                      'publisher': 'publisher', 'authors': 'authors'}
        self.dAuthor = {'author_id': 'author_id', 'first_name': 'first_name',
                        'last_name': 'last_name', 'middle_name': 'middle_name'}
        self.dAuthorship = {'book_id': 'book_id', 'author_id': 'author_id'}
        self.dRole = {'role_id': 'role_id', 'description': 'description'}
        self.dModel = {'model_id': 'model_id', 'file_path': 'file_path',
                       'name_model': 'name_model'}
        #
        self.fieldnamesUser = [self.dUser['user_id'], self.dUser['phone'],
                              self.dUser['first_name'],
                              self.dUser['last_name'],
                              self.dUser['middle_name']]
        self.fieldnamesModel = [self.dModel['model_id'],
                                self.dModel['file_path'],
                                self.dModel['name_model']]
        
    # def GetNewUserID(self, file):
        # lines = 0
        # for line in open(file):
            # lines = lines + 1
        # return lines
    
    def GetNewUserID(self):
        newID = str(datetime.now())
        newID = newID.replace('-', '')
        newID = newID.replace(' ', '')
        newID = newID.replace(':', '')
        newID = newID.replace('.', '')
        return newID
        
    def GetBookCovers(self):
        fileBooksR = open(self.fBooks, newline = '')
        fileAuthorsR = open(self.fAuthors, newline = '')
        fileAuthorshipR = open(self.fAuthorship, newline = '')
        #
        book = []
        authors = []
        #
        readerBooks = csv.DictReader(fileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(fileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(fileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Books.csv
        for lineBooks in readerBooks:
            # захожу в цикл по строкам файла Authorship.csv
            # с фиксированным значением book_id
            fileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship[self.dAuthorship['book_id']] ==
                    lineBooks[self.dBook['book_id']]):
                    # захожу в цикл по строкам файла Authors.csv
                    # с фиксированным значением author_id
                    fileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора
                        # и добавляю его в authors[]
                        if (lineAuthorship[self.dAuthorship['author_id']] ==
                            lineAuthors[self.dAuthor['author_id']]):
                            authors.append(Author(lineAuthors[self.dAuthor['author_id']],
                                                  lineAuthors[self.dAuthor['first_name']],
                                                  lineAuthors[self.dAuthor['last_name']],
                                                  lineAuthors[self.dAuthor['middle_name']]))
                            break
            book.append(Book(lineBooks[self.dBook['book_id']],
                             lineBooks[self.dBook['file_path']],
                             lineBooks[self.dBook['title']],
                             lineBooks[self.dBook['year']],
                             lineBooks[self.dBook['publisher']],
                             authors.copy()))
            authors.clear()
        #
        fileBooksR.close()
        fileAuthorsR.close()
        fileAuthorshipR.close()
        return book
    
    def AddUser(self, user):
        fileUsersR = open(self.fUsers, newline = '')
        fileUsersW = open(self.fUsers, 'a', newline = '')
        # 'a' - дозапись в файл, 'w' - перезапись файла
        reader = csv.DictReader(fileUsersR, delimiter = ',')
        # если такой пользователь уже есть в базе, то raise
        for line in reader:
            if ((user.first_name == line[self.dUser['first_name']]) and
                (user.last_name == line[self.dUser['last_name']]) and
                (user.middle_name == line[self.dUser['middle_name']]) and
                (str(user.phone) == line[self.dUser['phone']])):
                fileUsersR.close()
                fileUsersW.close()
                raise Exception('This user is already registered!')
        #
        writer = csv.DictWriter(fileUsersW, fieldnames = self.fieldnamesUser,
                                delimiter = ',')
        user.user_id = NumOfLines(path + "Users/Users.csv") # id нового пользователя = числу строк в файле Users.csv
        writer.writerow({self.dUser['user_id']: user.user_id,
                         self.dUser['phone']: user.phone,
                         self.dUser['first_name']: user.first_name,
                         self.dUser['last_name']: user.last_name,
                         self.dUser['middle_name']: user.middle_name})
        #
        fileUsersR.close()
        fileUsersW.close()
        return user.user_id
    
    def GetUser(self, user_id):
        # РАЗОБРАТЬСЯ С ENUMERATE!
        fileUsersR = open(self.fUsers, newline = '')
        fileUserRoleR = open(self.fUserRole, newline = '')
        fileRolesR = open(self.fRoles, newline = '')
        # ищу пользователя по user_id
        reader = csv.DictReader(fileUsersR, delimiter = ',')
        user = User(-1, -1, -1, -1, -1)
        for i, line in enumerate(reader, 1):
            if (i == user_id):
                user = User(line[self.dUser['user_id']],
                            line[self.dUser['phone']],
                            line[self.dUser['first_name']],
                            line[self.dUser['last_name']],
                            line[self.dUser['middle_name']])
                break
        reader = csv.DictReader(fileUserRoleR, delimiter = ',')
        role_id = 0
        # зная user_id, нахожу соответсвующее значение role_id
        for i, line in enumerate(reader, 1):
            if (i == user_id):
                role_id = int(line[self.dRole['role_id']])
                break
        # зная role_id, нахожу полную информацию об этой роли
        reader = csv.DictReader(fileRolesR, delimiter = ',')
        role = Role(-1, -1)
        for i, line in enumerate(reader, 1):
            if (i == role_id):
                role = Role(line[self.dRole['role_id']],
                            line[self.dRole['description']])
                break
        #
        fileUsersR.close()
        fileUserRoleR.close()
        fileRolesR.close()
        return (user, role) # tuple()
    
    def GetTrainedModel(self, name_model):
        fileModelsR = open(self.fModels, newline = '')
        reader = csv.DictReader(fileModelsR, delimiter = ',')
        for line in reader:
            if (name_model == line[self.dModel['name_model']]):
                return line[self.dModel['file_path']]
            
        fileModelsR.close()
        raise Exception('This model does not exist!')
    
    def AddModel(self, model):
        fileModelsW = open(self.fModels, 'a', newline = '')
        writer = csv.DictWriter(fileModelsW, fieldnames = self.fieldnamesModel,
                                delimiter = ',')
        writer.writerow({self.dModel['model_id']: model.model_id,
                         self.dModel['file_path']: model.file_path,
                         self.dModel['name_model']: model.name_model})
        #
        fileModelsW.close()
        
    ###########
    
    def AddBook(self, book):
        FileBooksR = open(path + "Books/Books.csv", newline = '')
        # если такая книга уже есть, то вернуть -1
        readerBooks = csv.DictReader(FileBooksR, delimiter = ',')
        for line in readerBooks:
            # file_path не сравниваю, т.к. могут быть 2 разных фото одной книги
            if ((book.title == line["title"]) and (book.year == line["year"]) and (book.publisher == line["publisher"])):
                FileBooksR.close()
                return -1
        FileBooksW = open(path + "Books/Books.csv", "a", newline = '')
        FileAuthorshipW = open(path + "Books/Authorship.csv", "a", newline = '')
        FileAuthorsR = open(path + "Books/Authors.csv", newline = '')
        FileAuthorsW = open(path + "Books/Authors.csv", "a", newline = '')
        new_book_id = NumOfLines(path + "Books/Books.csv") # id новой книги = числу строк в файле Books.csv
        # в таблицу книг дописываю одну новую:
        fieldnamesBooks = ['book_id', 'file_path', 'title', 'year', 'publisher']
        writerBooks = csv.DictWriter(FileBooksW, fieldnames = fieldnamesBooks, delimiter = ',')
        writerBooks.writerow({'book_id': new_book_id, 'file_path': book.file_path, 'title': book.title, 'year': book.year, 'publisher': book.publisher})
        # 
        readerAuthors = csv.DictReader(FileAuthorsR, delimiter = ',')
        fieldnamesAuthors = ['author_id', 'first_name', 'last_name', 'middle_name']
        writerAuthors = csv.DictWriter(FileAuthorsW, fieldnames = fieldnamesAuthors, delimiter = ',')
        fieldnamesAuthorship = ['book_id', 'author_id']
        writerAuthorship = csv.DictWriter(FileAuthorshipW, fieldnames = fieldnamesAuthorship, delimiter = ',')
        for aut in book.authors:
            new_author_id = 0
            for line in readerAuthors:
                # проверяю, есть ли в файле с Authors.csv, автор, который написал книгу, которую мы добавляем
                if ((aut.first_name == line["first_name"]) and (aut.last_name == line["last_name"]) and (aut.middle_name == line["middle_name"])):
                    # если да, то его id будет ассоциироваться с id книги, которую мы добавляем
                    new_author_id = line["author_id"]
            # если нет, то вычислим новый author_id и занесём автора в базу
            if (new_author_id == 0):
                new_author_id = NumOfLines(path + "Books/Authors.csv")
                writerAuthors.writerow({'author_id': new_author_id, 'first_name': aut.first_name, 'last_name': aut.last_name, 'middle_name': aut.middle_name})
            writerAuthorship.writerow({'book_id': new_book_id, 'author_id': new_author_id})
            FileAuthorsR.seek(0)
            FileAuthorsW.seek(0)
        
        FileBooksR.close()
        FileBooksW.close()
        FileAuthorsR.close()
        FileAuthorsW.close()
        FileAuthorshipW.close()
        return new_book_id
    
    
    def GetAllUsers(self):
        FileUsersR = open(path + "Users/Users.csv", newline = '')
        reader = csv.DictReader(FileUsersR, delimiter = ',')
        user = []
        for line in reader:
            user.append(User(line["user_id"], line["phone"], line["first_name"], line["last_name"], line["middle_name"]))
        
        FileUsersR.close()
        return user
    
    
    def GetAllBooks(self):
        return self.GetBookCovers()
    
    def GetBorrowedBooks(self):
        # HELP!
        # пытался реализовать все циклы по строкам файлов при помощи enumerate в целях экономии времени работы методов, но возникают проблемы с возвратом указателя в начало файла
        FileBooksR = open(path + "Books/Books.csv", newline = '')
        FileUsersR = open(path + "Users/Users.csv", newline = '')
        FileAuthorsR = open(path + "Books/Authors.csv", newline = '')
        FileAuthorshipR = open(path + "Books/Authorship.csv", newline = '')
        FileReadersR = open(path + "Readers.csv", newline = '')
        user = []
        book = []
        date1 = []
        date2 = []
        authors = []
        readerReaders = csv.DictReader(FileReadersR, delimiter = ',')
        readerUsers = csv.DictReader(FileUsersR, delimiter = ',')
        readerBooks = csv.DictReader(FileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(FileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(FileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Readers.csv
        for lineReaders in readerReaders:
            # захожу в цикл по строкам файла Books.csv с фиксированным значением user_id
            FileUsersR.seek(0) # возвращаю указатель в начало файла
            for lineUsers in readerUsers:
                # нахожу нужного пользователя и добавляю его данные в user[]
                if (lineUsers["user_id"] == lineReaders["user_id"]):
                    user.append(User(lineUsers["user_id"], lineUsers["phone"], lineUsers["first_name"], lineUsers["last_name"], lineUsers["middle_name"]))
                    break
            # захожу в цикл по строкам файла Authorship.csv с фиксированным значением book_id
            FileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship["book_id"] == lineReaders["book_id"]):
                    # захожу в цикл по строкам файла Authors.csv с фиксированным значением author_id
                    FileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора и добавляю его в authors[]
                        if (lineAuthorship["author_id"] == lineAuthors["author_id"]):
                            authors.append(Author(lineAuthors["author_id"], lineAuthors["first_name"], lineAuthors["last_name"], lineAuthors["middle_name"]))
                            break
            # добавляю нужную дату взятия книги в date1[]
            date1.append(lineReaders["borrow_date"])
            # добавляю нужную дату сдачи книги в date2[]
            date2.append(lineReaders["return_date"])
            #
            # захожу в цикл по строкам файла Books.csv с фиксированным значением book_id
            FileBooksR.seek(0) # возвращаю указатель в начало файла
            for lineBooks in readerBooks:
                # нахожу нужную книгу
                if (lineBooks["book_id"] ==  lineReaders["book_id"]):
                    # добавляю её в book[]
                    new_list = authors.copy() # новый список для устранения проблем с памятью 
                    book.append(Book(lineBooks["book_id"], lineBooks["file_path"], lineBooks["title"], lineBooks["year"], lineBooks["publisher"], new_list))
                    authors.clear()
                    break
                
        FileUsersR.close()
        FileBooksR.close()
        FileAuthorsR.close()
        FileAuthorshipR.close()
        FileReadersR.close()
        return (book, date1, date2, user) # tuple()
        
    def ChangeBookStatus(self, user_id, book_id):
        status = 1
        borrowDate = ""
        FileReadersR = open(path + "Readers.csv", "r", newline = '')
        # статус = 1 - взять книгу
        # статус = 2 - сдать книгу
        # return_date == -1 - книга не сдана
        reader = csv.DictReader(FileReadersR, delimiter = ',')
        for line in reader:
                # нахожу нужную дату по id книги и пользователя
                if (line["book_id"] == str(book_id) and line["user_id"] == str(user_id)):
                    # если эту книгу этот пользователь уже брал, то оформим новую запись
                    if (line["return_date"] != '-1'):
                        continue
                    # если же он книгу не взял, но не вернул, то сдаем книгу
                    borrowDate = line["borrow_date"]
                    status = 2
                    break
        if (status == 1):
            FileReadersW = open(path + "Readers.csv", "a", newline = '')
            fieldnames = ['user_id', 'book_id', 'borrow_date', 'return_date']
            writer = csv.DictWriter(FileReadersW, fieldnames = fieldnames, delimiter = ',')
            writer.writerow({'user_id': user_id, 'book_id': book_id, 'borrow_date': datetime.strftime(datetime.now(), "%d.%m.%Y"), 'return_date': "-1"})
            FileReadersW.close()
        if (status == 2):
            s = str(user_id) + ',' + str(book_id) + ',' + borrowDate + ','
            FileReadersR.seek(0)
            lines = FileReadersR.readlines()
            FileReadersOverW = open(path + "Readers.csv", "w", newline = '')
            for line in lines:
                line = line.strip()
                if line == s + '-1':
                    FileReadersOverW.write(s + datetime.strftime(datetime.now(), "%d.%m.%Y") + '\r' + '\n')
                else:
                    FileReadersOverW.write(line + '\r' + '\n')
            FileReadersOverW.close()
            
        FileReadersR.close()

if __name__ == "__main__":
    CSV = CSVDatabase()
    
    # TEST GetAllBooks()
    # book = CSV.GetAllBooks()
    # for b in book:
    #     b._print()
    
    # TEST GetBookCovers()
    # book = CSV.GetBookCovers()
    # for b in book:
    #     b._print()
    
    # TEST AddUser()
    # user = User(CSV.GetNewUserID(), 10, 'A', 'B', 'C')
    # CSV.AddUser(user)
    
    # TEST GetUser()
    # user = CSV.GetUser(2)[0]
    # role = CSV.GetUser(2)[1]
    # user._print()
    # role._print()
    
    # TEST GetTrainedModel()
    # line = CSV.GetTrainedModel('name_model2')
    # print(line)
    # line = CSV.GetTrainedModel('name')
    
    # TEST AddModel()
    # model = Model(1000, 'new_model_path', 'new_model_name')
    # CSV.AddModel(model)
    """main"""