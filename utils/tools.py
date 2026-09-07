import shutil
import string
from termcolor import colored

def progress_bar(current, total, model,comment="", length=50):
    fill = length * current * (len(model)) // total
    print('\r'f"[{model * fill}{" " * (length - fill)}] {current}/{total} {comment}", end='', flush=True)


def separator(model="-"):
    width = shutil.get_terminal_size().columns
    print(model * (width - len(model)))

def remove_punctuation(s="") -> str:
    return "".join([el for el in s if el not in string.punctuation])

def printc(text, color, attrs=None):
    print(colored(text, color, attrs=attrs))

def bold(text):
    return colored(text, attrs=["bold"])

def top_10(tab) ->list[bool]:
    top = sorted(tab, reverse=True)[:10]
    return [True if x in top else False for x in tab]