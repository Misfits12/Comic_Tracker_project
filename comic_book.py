"""
COMIC BOOK CLASS
"""

class ComicBook:
    def __init__(self, title, issue, publisher, condition):
        self.title = title
        self.issue = issue
        self.publisher = publisher
        self.condition = condition

    def set_title(self, value):
        self.title = value

    def set_issue(self, value):
        self.issue = value

    def set_publisher(self, value):
        self.publisher = value

    def set_condition(self, value):
        self.condition = value

    def get_value(self):
        base = 10.0

        if self.condition.lower() == "mint":
            return base * 2
        elif self.condition.lower() == "good":
            return base * 1.5
        elif self.condition.lower() == "fair":
            return base
        else:
            return base * 0.5

    def display(self):
        print("\n--- COMIC ---")
        print(f"Title: {self.title}")
        print(f"Issue: {self.issue}")
        print(f"Publisher: {self.publisher}")
        print(f"Condition: {self.condition}")
        print(f"Value: ${self.get_value():.2f}")