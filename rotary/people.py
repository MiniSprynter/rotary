"""
people.py

Module for collecting, storing and manipulating data for each person in the
rota.

Lawrence 23/08/21
"""

import datetime as dt


class Person(object):
    def __init__(self, name, surname, skills, role, frequency, absences=None):
        if absences is None:
            absences = []

        self.name = name
        self.surname = surname
        self.skills = skills
        self.role = role
        self.frequency = frequency
        self.absences = absences

        self.id_ = self._gen_id()

    def _gen_id(self):
        return (self.name + "_" + self.surname).lower()

    def _is_valid(self):  # TODO
        pass

    def change_name(self, name):
        self.name = name

    def change_surname(self, surname):
        self.surname = surname

    def add_skills(self, skills):
        for skill, score in skills.items():
            self.skills[skill] = score

    def remove_skills(self, skills):
        for skill in skills:
            self.skills.pop(skill, None)

    def change_roll(self, role):
        self.role = role

    def change_frequency(self, frequency):
        self.frequency = frequency

    def add_absences(self, absences):
        for absence in absences:
            self.absences.append(absence)

    def remove_absences(self, absences):
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
