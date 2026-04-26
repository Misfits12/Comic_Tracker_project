"""
COMIC TRACKER MAIN FILE
"""

import datetime
from comic_book import ComicBook

DATA_FILE = "collection.txt"
PUBLISHERS = ("DC", "Marvel", "Image", "Dark Horse")


def get_user():
    return input("Enter your name: ").title()


def create_comic():
    title = input("Title: ")
    issue = input("Issue: ")

    print("Publishers:", PUBLISHERS)
    publisher = input("Publisher: ")

    condition = input("Condition (Mint/Good/Fair/Poor): ")

    return ComicBook(title, issue, publisher, condition)


def save(user, comic):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, "a") as file:
        file.write(f"\n[{time}] {user}\n")
        file.write(f"{comic.title}\n")
        file.write(f"Issue: {comic.issue}\n")
        file.write(f"Publisher: {comic.publisher}\n")
        file.write(f"Condition: {comic.condition}\n")
        file.write(f"Value: ${comic.get_value():.2f}\n")
        file.write("----------------------\n")


def main():
    user = get_user()

    while True:
        comic = create_comic()
        comic.display()
        save(user, comic)

        again = input("Add another? (yes/no): ").lower()
        if again != "yes":
            break

    print("Done.")


main()