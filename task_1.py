from collections import UserDict
from typing import List


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)

        if not self.is_valid():
            raise ValueError

    def is_valid(self):
        return len(self.value) == 10 and self.value.isdigit()


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    def __str__(self):
        return f"Contact name: {self.name}, phones: {"; ".join(list(map(lambda phone: str(phone), self.phones)))}"

    def __find_phone_index__(self, phone_str):
        phone_index = None

        for i in range(len(self.phones)):
            if self.phones[i].value == phone_str:
                phone_index = i

        return phone_index

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        phone_index = self.__find_phone_index__(phone)

        if phone_index is None:
            raise ValueError
        else:
            del self.phones[phone_index]

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_index = self.__find_phone_index__(old_phone)

        if phone_index is None:
            raise ValueError
        else:
            self.phones[phone_index] = Phone(new_phone)

    def find_phone(self, phone: str):
        phone_index = self.__find_phone_index__(phone)

        if phone_index is None:
            raise ValueError
        else:
            return self.phones[phone_index]


class AddressBook(UserDict[str, Record]):
    def __str__(self):
        return "\n".join(list(map(lambda value: str(value), self.data.values())))

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data.keys():
            return self.data[name]
        else:
            return None

    def delete(self, name: str):
        if name in self.data.keys():
            del self.data[name]


def input_error(func):
    def inner(args, book):
        try:
            return func(args, book)
        except ValueError:
            return "Invalid arguments."
        except IndexError:
            return "Give me a username."
        except KeyError:
            return f"{args} doesn't exist."

    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def get_greeting():
    return "How can I help you?"


@input_error
def add_contact(args: List[str], book: AddressBook):
    name, phone = args
    record = book.find(name)

    if not record:
        record = Record(name)

    record.add_phone(phone)
    book.add_record(record)

    return "Contact added."


@input_error
def change_phone(args: List[str], book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)

    if not record:
        return f"{name} doesn't exists. Add it before changing it."

    record.edit_phone(old_phone, new_phone)

    return "Contact updated."


@input_error
def get_phones(args: list[str], book: AddressBook):
    name = args[0]
    record = book.find(name)

    if not record:
        return f"{name} doesn't exist."

    return record.phones


def get_all_contacts(book: AddressBook):
    if len(book.data) == 0:
        return "Contacts list is empty."

    return book


def get_good_bye():
    return "Good bye!"


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        cmd, *args = parse_input(user_input)

        if cmd == "hello":
            print(get_greeting())
        elif cmd == "add":
            print(add_contact(args, book))
        elif cmd == "change":
            print(change_phone(args, book))
        elif cmd == "phone":
            print(get_phones(args, book))
        elif cmd == "all":
            print(get_all_contacts(book))
        elif cmd == "close" or cmd == "exit":
            print(get_good_bye())
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
