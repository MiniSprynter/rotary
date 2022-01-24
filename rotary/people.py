"""
people.py

Module for collecting, storing and manipulating data for each person in the
rota.

Lawrence 23/08/21
"""

import datetime as dt


class Person(object):
    def __init__(self, name, surname, skills, role, frequency, absences=[]):
        # Ensure absences is a list
        if not absences:
            absences = []

        # Save parameters
        self.name = name
        self.surname = surname
        self.skills = skills
        self.role = role
        self.frequency = frequency
        self.absences = absences

        # Ensure data is valid
        self._is_valid()

        # Generate ID
        self.id_ = self._gen_id()

    @staticmethod
    def __valid_str(string):
        if type(string) is not str:
            raise TypeError("String must be of type 'str'")
        elif not string:
            raise ValueError("String must not be empty")

    @staticmethod
    def __valid_dict(dictionary):
        if type(dictionary) is not dict:
            raise TypeError("Dictionary must be of type 'dict'")
        elif not dictionary.keys():
            raise ValueError("Dictionary must not be empty")
        elif not all([type(x) for x in dictionary.keys()] == str):
            raise TypeError("Dictionary keys must be strings")

    @staticmethod
    def __valid_pos_num(number):
        if not (type(number) is int or type(number) is float):
            raise TypeError("Number must be of type 'int' or 'float'")
        elif number < 0:
            raise ValueError("Number must not be negative")

    @staticmethod
    def __valid_absences(absences):
        if type(absences) is not list:
            raise TypeError("Absences must be of type 'list'")
        elif not all([type(x) for x in absences] == dt.date):
            raise TypeError("Absences must be of type 'datetime.date'")

    def _is_valid(self):
        # Check validity of string parameters
        for string in [self.name, self.surname, self.role]:
            self.__valid_str(string)

        # Check validity of dictionary parameters
        self.__valid_dict(self.skills)

        # Check validity of numerical parameters
        self.__valid_pos_num(self.frequency)

        # Check validity of absences list
        self.__valid_absences(self.absences)

    def _gen_id(self):
        return (self.name + "_" + self.surname).lower()

    def change_name(self, name):
        # Check name validity
        self.__valid_str(name)

        # Replace current name
        self.name = name

    def change_surname(self, surname):
        # Check surname validity
        self.__valid_str(surname)

        # Replace current surname
        self.surname = surname

    def add_skills(self, skills):
        # Ensure skills are valid
        self.__valid_dict(skills)

        # Add skills to dictionary
        for skill, score in skills.items():
            self.skills[skill] = score

    def remove_skills(self, skills):
        # Ensure skills is a valid list
        self.__valid_list(skills)

        # Remove skills from dictionary
        for skill in skills:
            self.skills.pop(skill, None)

    def change_roll(self, role):
        # Ensure role is a valid string
        self.__valid_str(role)

        # Replace existing role string
        self.role = role

    def change_frequency(self, frequency):
        # Ensure frequency is a valid number
        self.__valid_num(frequency)

        # Replace existing frequency number
        self.frequency = frequency

    def add_absences(self, absences):  # TODO: check validity
        for absence in absences:
            self.absences.append(absence)

    def remove_absences(self, absences):  # TODO: check validity
        for date in [x for x in absences if x in self.absences]:
            self.absences.remove(date)

    def fullname(self):
        return self.name + " " + self.surname


class People(object):
    def __init__(self, people):
        self.people = {}

        self.add(people)

    def _get_ids(self):
        return list(self.people.keys())

    def add(self, people):
        # Ensure people objects are in a list
        if type(people) is not list:  # TODO: remove and always use list?
            people = [people]

        # Add people individually
        for person in people:
            self.people[person.id_] = person

    def count(self):
        return len(self.people)

    def get_name(self, id_):
        return self.people[id_].fullname()

    def get_names(self, ids):
        # Ensure IDs are in a list
        if type(ids) is not list:
            ids = [ids]

        # Create list of full names
        names = []
        for id_ in ids:
            names.append(self.people[id_].fullname())

        return names

    def get_roles(self):
        roles = {}
        # Determine roles for each ID
        for id_ in self._get_ids():
            # Determine role
            role = self.people[id_].role
            if role in roles:
                # Add ID to existing list
                roles[role].append(id_)
            elif role:
                # Create new list with ID
                roles[self.people[id_].role] = [id_]

        return roles


if __name__ == "__main__":
    import data_tools

    Tom = Person("Tom", "Endersby", {"guitar": 9, "drums": 6}, "leader", 3)
    people = People([Tom])
    data_tools.save(people, "people")
    people_saved = data_tools.load("people")
