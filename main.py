from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, value):
        if not len(value) > 0:
            raise ValueError('The info is not correct. Name must not be blank')
        super().__init__(value)
        
class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if not value.isdigit() or len(value) < 10:
            raise ValueError('The info is not correct. Please provide correct phone number')
        super().__init__(value)
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу

    def add_birthday(self, birthday):
        self.birthday = birthday.date


    def add_phone(self, phone:str):
        """add phone to self.phones"""
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone:str):
        for obj_phone in self.phones:
            if obj_phone.value == phone:
                self.phones.remove(obj_phone)
                return
        raise ValueError('Number not found') 
    
    def edit_phone(self, old_phone:str, new_phone:str):
        for i, obj_phone in enumerate(self.phones):
            if obj_phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
            
        raise ValueError('Number not found')
            
    def find_phone(self, phone:str):
        for obj_phone in self.phones:
            if obj_phone.value == phone:
                return obj_phone
        return None
    
    
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name:str):
        return self.data.get(name, None)
        
    def delete(self, name:str):
        self.data.pop(name)

    def get_upcoming_birthday(self):
        '''Calculate the number of days between a given date (YYYY-MM-DD) and today'''

        def adjust_for_weekend(birthday):
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)
            return birthday
        
        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        upcoming_birthdays = []
        days = 7
        today = date.today()
        for user in self.data:
            if self.data[user].birthday:
                current_user = self.data[user].name.value
                current_user_birthday = (self.data[user].birthday)#
                birthday_this_year = current_user_birthday.replace(year = today.year)
                if birthday_this_year.date() < today:
                    birthday_this_year = current_user_birthday.replace(year = today.year + 1)
                #
                if 0 <= (birthday_this_year.date() - today).days <= days:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)

                gz_date = birthday_this_year.strftime('%m/%d/%Y')
                upcoming_birthdays.append({current_user:gz_date})
        return upcoming_birthdays
    
    def show_birthdays(self):
        result = []
        for record in self.data.values():
            if record.birthday:
                birthday_str = record.birthday.strftime("%d.%m.%Y")
                result.append(f"{record.name.value}: {birthday_str}")
        return "\n".join(result) if result else "No birthdays found."

    def __str__(self) -> str:
        return '\n'.join(str(record) for record in self.data.values())
    


class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            self.date = datetime.strptime(value, "%d.%m.%Y")
            

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args,book))

        elif command == "change":
            print(change_phone(args, book))
            ...
        elif command == "phone":
            print(show_phone(args, book))
            ...
        elif command == "all":
            # реалізація
            print(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            # реалізація
            print(show_birthday(args, book))
        elif command == "birthdays":
            # реалізація
            print(birthdays(book))
        else:
            print("Invalid command.")

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments provided."
        except ValueError as ve:
            return f"Value error: {ve}"
        except KeyError:
            return "Name not found."
        except Exception as e:
            return f"An error occurred: {e}"
    return wrapper

def parse_input(user_input):
    '''parsing user's input'''
    cmd, *args = user_input.split() #separates command from users additional info -  name, number
    cmd = cmd.strip().lower() 
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args  # add birthday!!!!!!!
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record) 
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    message = ''
    if record:
        record.edit_phone(old_phone, new_phone)
        message = 'Phone updated'
    else:
        message = 'Phone doesnt exist'
    return message

@input_error
def show_phone(args, book: AddressBook):
    name , *_ = args  # add birthday!!!!!!!
    record = book.find(name)
    if record:
        return record
    else:
        return 'Phone not found'

@input_error
def add_birthday(args, book):
    name, birthday, *_ =args
    record = book.find(name)
    message = 'User doesnt exist'
    if record:
        message = 'Birthday updated'
        record.birthday = birthday
    return message

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    message = 'User doesnt exists'
    if record:
        message = f"{name}'s birthday: {record.birthday}"
    return message

def birthdays(book: AddressBook):
    all_birthdays = []
    for record in book.data.values():
        if record.birthday:
            birthday_str = record.birthday
            all_birthdays.append(f"{record.name.value}: {birthday_str}")
    return "\n".join(all_birthdays) if all_birthdays else "No birthdays found."



if __name__ == "__main__":
    main()