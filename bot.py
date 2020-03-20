"""
rewrite pooh by swapping dialogue around
"""
import sys
import random
from collections import deque

def clean_pooh():
    """
    takes all ~~nasty~~ whitespace out of the book
    """
    with open("pooh.txt", "r") as book:
        pooh = book.read()

    pooh = " ".join(pooh.split())

    with open("pooh.txt", "w+") as book:
        book.write(pooh)


def is_one_letter_caps(letter):
    """
    checks if letter is not whitespace and is infact one character long
    """
    return (len(letter) == 1) and not letter.isspace()

def isnt_title_case(word):
    """
    checks if it's bigger than one character and isn't in title case
    """
    return (len(word) > 1) and not word.istitle()

def chapter_handler(front, title, chapter_titles, non_dialogue, pooh):
    """
    handles replacing ñ with chapter names for intersperse_dialogue()
    """
    while not front.islower():
        if isnt_title_case(front) or is_one_letter_caps(front):
            title += front + " "
        front = pooh.popleft()
    chapter_titles.append(title)
    non_dialogue.append("ñ")

def get_dialogue(pooh):
    """
    gets all dialogue from a given text
    returns list
    """
    pooh = deque(pooh.split())
    dialogue = []
    while pooh:
        front = pooh.popleft()
        quote = ""
        if front:
            if front[0] == "\"":
                while front[-1] != "\"":
                    quote += front + " "
                    front = pooh.popleft()
                quote += front
                dialogue.append(quote)
    return dialogue

def intersperse_dialogue(pooh):
    """
    get all dialogue in a nice little list or something and then randomly swap em around
    """
    pooh = deque(pooh)
    non_dialogue = []
    dialogue = []
    chapter_titles = []

    quote = ""
    while pooh:
        front = pooh.popleft()
        title = ""
        if front:
            if front[0] == "\"":
                non_dialogue.append(quote)
                quote = ""
                while front[-1] != "\"":
                    quote += front + " "
                    front = pooh.popleft()
                quote += front
                dialogue.append(quote)
                quote = ""
            elif front == "CHAPTER":
                chapter_handler(front, title, chapter_titles, non_dialogue, pooh)
            else:
                quote += front + " "

    final = "WINNIE THE POOH \n\n\n A.A. Milne \n\n\n"

    for i in range(len(non_dialogue)):
        non_quote = non_dialogue[i]

        if non_quote == "ñ":
            final += chapter_titles[0] + "\n\n"
            chapter_titles.pop(0)
            non_quote = ""

        if dialogue:
            quote = random.choice(dialogue)
            dialogue.remove(quote)
            final += quote + " " + non_quote + " "
        else:
            final += non_quote + " "

        if i%10 == 0:
            final += "\n\n"

    return final

def rewrite_pooh_ran_dialogue():
    """
    rewrites winnie the pooh so that all dialogue gets thrown around randomly
    """
    clean_pooh()
    with open("pooh.txt", "r") as book:
        pooh = book.read().replace("\n", " ")

    pooh = pooh.split()

    final = intersperse_dialogue(pooh)

    with open("randomDialoguePooh.txt", "w+") as book:
        book.write(final)


def getcha_a_quote():
    """
    getcha a quote
    """
    clean_pooh()
    with open("pooh.txt", "r") as file:
        POO = file.read()
    print(random.choice(get_dialogue(POO)))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        getcha_a_quote()
    else:
        if sys.argv[1] == "rewrite":
            rewrite_pooh_ran_dialogue()
        else:
            getcha_a_quote()
