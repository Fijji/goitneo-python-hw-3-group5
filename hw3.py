from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid birthday format. Please use DD.MM.YYYY.")
        super().__init__(value)
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday already exists for this contact")
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        return [p.value for p in self.phones if p.value == phone]

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result

class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError(f"Contact with name {record.name.value} already exists in the address book")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            
    def add_birthday(self, name, birthday):
        record = self.find(name)
        if record:
            record.add_birthday(birthday)
        else:
            raise ValueError(f"Contact with name {name} not found in the address book")

    def show_birthday(self, name):
        record = self.find(name)
        if record and record.birthday:
            print(f"{name}'s birthday: {record.birthday.value}")
        else:
            print(f"No birthday found for {name}")

    def birthdays(self):
        today = datetime.today()
        next_week_start = today + timedelta(days=(6 - today.weekday()) + 1)
        next_week_end = next_week_start + timedelta(days=6)

        birthdays_next_week = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y')
                if next_week_start <= birthday_date <= next_week_end:
                    birthdays_next_week.append(record)

        return birthdays_next_week

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."
        except Exception as e:
            return str(e)
    return inner

@input_error
def hello():
    return "How can I help you?"

@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args, book):
    name, = args
    record = book.find(name)
    if record:
        return f"Phone number for {name}: {record.phones[0].value}"
    else:
        raise KeyError

@input_error
def show_all(args, book):
    if book.data:
        result = "All contacts:\n"
        for record in book.data.values():
            result += f"{record}\n"
        return result.strip()
    else:
        return "No contacts found."

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    else:
        return f"No birthday found for {name}"

@input_error
def birthdays(args, book):
    next_week_birthdays = book.birthdays()
    if next_week_birthdays:
        result = "Birthdays next week:\n"
        for record in next_week_birthdays:
            result += f"{record.name.value}: {record.birthday.value}\n"
        return result.strip()
    else:
        return "No birthdays next week."

def main():
    book = AddressBook()

    while True:
        user_input = input("Enter command: ")
        command_parts = user_input.split()
        command = command_parts[0].strip().lower()
        args = command_parts[1:]

        if command == "hello":
            print(f"Welcome to the assistant bot! \nHow can I help you?")
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command in ["close", "exit"]:
            print("Goodbye!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()