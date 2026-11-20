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
    def __init__(self, book: Book,copy_id: str):
        self.book = book
        self.status = CopyStatus.AVAILABLE
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
    def calculate_fine(self,days_overdue:int):
        pass

class FlatPerDayRate(Fine):
    def __init__(self,fine_amount: int):
        self.fine_amount = fine_amount

    def calculate_fine(self,days_overdue: int):
        return self.fine_amount * days_overdue

class LoanRegistry:
    def __init__(self):
        self.active_by_copy = {}
        self.active_by_member = {}

    def add(self,loan:Loan):
        if loan.book_copy.copy_id in self.active_by_copy:
            raise ValueError(f'This Copy is already borrowed. Cant borrow again')
        else:
            self.active_by_copy[loan.book_copy.copy_id] = loan
            loans_for_member = self.active_by_member.get(loan.member.member_id,[])
            loans_for_member.append(loan)
            self.active_by_member[loan.member.member_id] = loans_for_member
        
    def close(self,copy_id:str):
        if copy_id in self.active_by_copy:        
            loan : Loan = self.active_by_copy.pop(copy_id)
            member_loans = self.active_by_member.get(loan.member.member_id,None)
            if len(member_loans):
                member_loans.remove(loan)
                self.active_by_member[loan.member.member_id] = member_loans
            else:
                del self.active_by_member[loan.member.member_id]
            return loan
        else:
            raise ValueError(f"Cant close copy that hasnt been borrowed")
        

    def get_active_loan(self,copy_id:str):
        return self.active_by_copy.get(copy_id,None)

    def active_count(self,member:Member):
        return len(self.active_by_member.get(member.member_id,[]))



        
        


class Library:
    def __init__(self,loan_registry: LoanRegistry,fine: Fine):
        self.loan_registry = loan_registry
        self.fine = fine
    def borrow(self,copy_id):
        pass
    def return_copy(self):
        pass        
