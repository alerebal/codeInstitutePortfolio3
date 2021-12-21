class Kid():
    def __init__(self, name, last_name, age, tutor, contact, allergies):
        self.name = name
        self.last_name = last_name
        self.age = age
        self.tutor = tutor
        self.contact = contact
        self.allergies = allergies
        
    def _get_id(self, last_id):
        self.kid_id = last_id + 1

    def _group(self):
        if self.age == 1:
            return "Blue"
        elif self.age == 2:
            return "Yellow"
        elif self.age == 3:
            return "Green"
        else:
            return None

    def kid_info(self):
        return [self.kid_id ,self.name, self.last_name, self.age, self.tutor, self.contact, self.allergies, self._group()]

    def kid_description(self):
        return f"The kid {self.name} {self.last_name} has been created with id: {self.kid_id}"