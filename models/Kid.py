class Kid():
    def __init__(self, name, last_name, age, tutor, contact, allergies):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.tutor = tutor
        self.contact = contact
        self.allergies = allergies

    def _get_id(self, last_id):
        """
        Set the kid_id property adding 1 to the last kid_id in worksheet
        """
        self.kid_id = last_id + 1

    def _group(self):
        """
        Set the group property to the kid according to the kid's age
        """
        if self.age == 1:
            return "Blue"
        elif self.age == 2:
            return "Yellow"
        elif self.age == 3:
            return "Green"
        else:
            return None

    def kid_info(self):
        """
        Return the necessary data to create a row in the worksheet
        """
        return [self.kid_id, self.name, self.last_name, self.age, self.tutor,
                self.contact, self.allergies, self._group()]

    def kid_description(self):
        """
        Return the success message to show to the user
        """
        return f"The data of {self.name} {self.last_name} has been created"
