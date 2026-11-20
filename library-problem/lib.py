from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod

class CopyStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    LOST = "lost"

class MembershipType(Enum):
    REGULAR = "regular"
    PREMIUM = "premium"
    STUDENT = "student"

# All the details about a particular Book
class Book:
    def __init__(self,title: str,author: str,year: int,isbn: str):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn

# All the details about the copy of a particular Book
class BookCopy():
    def __init__(self, book: Book,copy_id: str, status: CopyStatus):
        self.book = book
        self.status = status
        self.copy_id = copy_id

    def mark_borrowed(self):
        if self.status != CopyStatus.AVAILABLE:
            raise ValueError("A copy thats not avaible cant beborrowed")
        self.status = CopyStatus.BORROWED

    def mark_available(self):
        if self.status == CopyStatus.LOST:
            raise ValueError("A lost Copy can't be made available")
        self.status = CopyStatus.AVAILABLE
    def mark_reserved(self):
        if self.status == CopyStatus.RESERVED:
            raise ValueError("The copy is already reserved")
        self.status = CopyStatus.RESERVED
    def mark_lost(self):
        self.status = CopyStatus.LOST
        

class Member:

    LIMITS = {
        MembershipType.STUDENT : 3,
        MembershipType.REGULAR: 5,
        MembershipType.PREMIUM : 10,
    }

    def __init__(self, name: str, member_id: str, membership_type: MembershipType):
        self.name = name
        self.member_id = member_id
        self.membership_type = membership_type
        self.borrow_limit = self.LIMITS[self.membership_type]

class Loan:
    def __init__(self, book_copy: BookCopy, member: Member, loan_date: datetime, due_date: datetime):
        self.book_copy = book_copy
        self.member = member
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = None

    @property    
    def is_active(self)->bool:
        return self.return_date is None

    def close(self, return_date:datetime) -> None:
        if not self.is_active:
            raise ValueError("Loan Already Closed")
        self.return_date = return_date

    def days_overdue(self,as_of : datetime):
        return max(0,(as_of - self.due_date).days)

class Fine(ABC):
    @abstractmethod
    def calculate_fine(self):
        pass

class FlatPerDayRate(Fine):
    def __init__(self,fine_amount: int,days_overdue: int):
        self.fine_amount = fine_amount
        self.days_overdue = days_overdue

    def calculate_fine(self):
        return self.fine_amount * self.days_overdue

class LoanRegistry:
    def __init__(self):
        # self.loans = []
        self.active_by_copy = {}
        self.active_by_member = {}

    def add(self,loan: Loan):
        self.active_by_copy[loan.book_copy.copy_id] = self.active_by_copy.get(loan.book_copy.copy_id,[]).append(loan)
        self.active_by_member[loan.member.member_id]= self.active_by_member.get(loan.member.member_id,[]).append(loan)

    def close(self,copy_id:str):
        if self.active_by_copy.get(copy_id,[]):
            loan :Loan = self.active_by_copy[copy_id]
            self.active_by_copy.pop(copy_id,None)
            self.active_by_member.pop(loan.member.member_id,None)
        else:
            raise ValueError("Loan Not Found")

    def get_active_loan(self,copy_id):
        return self.active_by_copy[copy_id] if self.active_by_copy[copy_id] else None

    def active_count(self,member:Member):
        return len(self.active_by_member[member.member_id]) if self.active_by_member[member.member_id] else 0


        
        


class Library:
    pass
