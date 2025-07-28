# student .py

# student.py

class Student:
    def __init__(self, name, section, spanish, english, social, science):
        self.name = name
        self.section = section
        self.spanish = float(spanish)
        self.english = float(english)
        self.social = float(social)
        self.science = float(science)

    def get_average(self):
        return (self.spanish + self.english + self.social + self.science) / 4

    def to_dict(self):
        return {
            "name": self.name,
            "section": self.section,
            "spanish": self.spanish,
            "english": self.english,
            "social": self.social,
            "science": self.science
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["section"],
            data["spanish"],
            data["english"],
            data["social"],
            data["science"]
        )
