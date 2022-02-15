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
        elif not all([type(x) == str for x in dictionary.keys()]):
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
        elif not all([type(x) == dt.date for x in absences]):
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


class Group(object):
    def __init__(self, people=[]):
        self.people = {}

        self.add(people)

    def _get_ids(self):
        return list(self.people.keys())

    def _get_name(self, id_):
        if id_ in self.people:
            return self.people[id_].fullname()
        else:
            return None

    def join(self, group):
        # Ensure type is valid
        if type(group) is not Group:
            raise TypeError("Group must be of type 'Group'")

        # Combine dictionaries
        self.people = {**self.people, **group.people}

    def add(self, people):
        # Ensure people objects are in a list
        if not isinstance(people, (list, tuple)):
            people = [people]

        # Add people individually
        for person in people:
            # Ensure object type is valid
            if type(person) is Person:
                self.people[person.id_] = person
            
    def remove(self, ids):
        # Ensure IDs are in a list
        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        # Remove people individually
        for id_ in ids:
            self.people.pop(id_, None)

    def count(self):
        return len(self.people)

    def get_names(self, ids):
        # Check whether ids is a list
        if isinstance(ids, (list, tuple)):
            # Return a list of names
            return [self._get_name(id_) for id_ in ids]
        else:
            # Return a single name
            return self._get_name(ids)

    def get_roles(self):
        # Create empty dictionary for items
        roles = {}

        # Iterate through each ID
        for id_ in self._get_ids():
            role = self.people[id_].role

            # Add data to roles dictionary
            if role in roles:
                # Add ID to existing key value
                roles[role].append(id_)
            else:
                # Create new key with ID as value
                roles[role] = [id_]
                
        return roles

    def get_skills(self):
        # Create empty dictionary for skills
        skills = {}

        # Iterate through each ID
        for id_ in self._get_ids():
            for key, value in self.people[id_].skills.items():
                # Add data to skills dictionary
                if key in skills:
                    # Add dataset to existing skill
                    skills[key][id_] = value
                else:
                    # Create skill with dataset
                    skills[key] = {id_: value}

        return skills


if __name__ == "__main__":
    import data_tools

    # Create some dummy data
    Tom = Person("Tom", "Endersby", {"guitar": 9, "drums": 6}, "leader", 3)

    # Test data
    people = Group([Tom])
    people.get_roles()
    people.get_skills()

    # Ensure data can be saved and read again
    data_tools.save(people, "people")
    people_saved = data_tools.load("people")
