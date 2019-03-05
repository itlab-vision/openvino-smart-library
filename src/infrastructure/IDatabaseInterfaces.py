from abc import ABC, abstractmethod

class IDatabaseBRM(ABC):
    @abstractmethod
    def GetBookCovers(self):
        """Get book covers"""
        
class IDatabaseAuthService(ABC):
    @abstractmethod
    def AddUser(self, user):
        """Add user"""
        
class IDatabaseFRM(ABC):
    @abstractmethod
    def GetUser(self, user_id):
        """Get user"""
    
    @abstractmethod
    def GetTrainedModel(self, name_model):
        """Get trained model"""
        
    def AddModel(self, model):
        """Add model"""
        
class IDatabaseGUI(ABC):
    @abstractmethod
    def AddBook(self, book):
        """Add book"""
    
    @abstractmethod
    def GetAllUsers(self):
        """Get all users"""
    
    @abstractmethod
    def GetAllBooks(self):
        """Get all books"""
    
    @abstractmethod
    def GetBorrowedBooks(self):
        """Get borrowed books"""
    
    @abstractmethod
    def ChangeBookStatus(self, user_id, book_id, status):
        """Change book status"""