from os import path, listdir
from PyPDF2 import PdfReader
from sys import argv
from termcolor import colored
from datetime import datetime, timedelta

if "--help" in argv:
    print("usage: python main.py [path/to/file or path/to/folder]")
    quit()
target = argv[1]
keywords_file_path = "./keywords/keywords_anwendungsentwicklung.txt"
with open(keywords_file_path, "r") as keywords_file: # read keywords file
    user_conditions = keywords_file.read().split("\n")

language_weights = ("A1","A2","A3","B1","B2","B3","C1","C2")
qualifications_weights = ("Mittelschule", "Mittlere Reife", ("Fachhochschulreife", "Fachabitur"), ("Allgemeine Hochschulreife", "Abitur", "Gymnasium"), "Universität" ) 

keyword_db = {("Name"):(""), "Staatsangehörigkeit":"", ("Tel.", "Telefon"):("+", "/"), ("E-Mail", "Mail"):("@"), ("Adresse", "Hausnummer"): ("str.", "Straße"),
("Englisch", "Deutsch"): language_weights, ("Schulabschluss", "Schulbildung"): qualifications_weights, ("Ausbildung"):("Ausbildung als", "Ausbildung zum")}

def extract_lines(path:str):
    global results
    global berufserfahrung
    global ausbildungsstellen
    global found_keyword
    results = {}
    berufserfahrung = []
    ausbildungsstellen = []
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    for i in range (0, number_of_pages):
        page = reader.pages[i]
        for user_condition in user_conditions:
            found_keyword = False
            user_condition_value = None
            is_expression = False
            if True in [expression in user_condition for expression in ["<", ">"]]:
                is_expression = True
                user_condition, user_condition_value = user_condition.split(" ")[0], user_condition.split(" ")[2]
            for line in page.extract_text().split("\n"):
                if line != " " and line != "":
                    check_line(user_condition, line, user_condition_value, is_expression)
            if user_condition not in results:
                results[user_condition] = f"{user_condition} [{colored("?", "yellow")}]"
    display_results()
        

def check_line(user_condition, line, user_condition_value, is_expression=False):
    global split_line
    split_line = "".join(line.split(":")).split(" ")
    for keywords in keyword_db:
        if user_condition in keywords:
            check_conditions(user_condition, line, user_condition_value, keywords, is_expression, None)

def check_conditions(user_condition, line, user_condition_value, keywords, is_expression, original_keywords):
    global found_keyword
    if original_keywords is None:
        original_keywords = keywords
    if isinstance(keywords, tuple):
        for keyword in keywords:
            check_conditions(user_condition, line, user_condition_value, keyword, is_expression, original_keywords)
    else:
        for part in split_line:
            if part != "":
                try:
                    if user_condition == part and split_line[split_line.index(part)+1] != "":
                        evaluate(original_keywords, user_condition, user_condition_value, split_line[split_line.index(part)+1], is_expression)
                        found_keyword = True
                        return True
                except IndexError:
                    pass
            for value in keyword_db[original_keywords]:
                if not found_keyword:
                    check_values(user_condition, line, user_condition_value, value, is_expression, original_keywords)
                

def check_values(user_condition, line, user_condition_value, value, is_expression, original_keywords):
    if isinstance(value, tuple):
        for part in value:
            check_values(user_condition, line, user_condition_value, part, is_expression, original_keywords)
    else:
        if value in line and value != "":
            for part in split_line:
                if user_condition == "Schulabschluss":
                    if value == part:
                        if user_condition not in results.keys():
                            evaluate(original_keywords, user_condition, user_condition_value, part, is_expression)
                elif user_condition == "Ausbildung":
                    if value in line:
                        if user_condition not in results or line not in results[user_condition]:
                            ausbildungsstellen.append(line)
                            evaluate(original_keywords, user_condition, user_condition_value, ausbildungsstellen, is_expression)
                elif user_condition == "Berufserfahrung":
                    symbols = ("/", ".")
                    for word in split_line:
                        for symbol in symbols:
                            if symbol in word:
                                try:
                                    month, year = map(int, word.split("/"))
                                    dates.append((month, year))
                                except ValueError:
                                    continue
                            elif "heute" in word:
                                dates.append((date.now()[1], date.now()[0]))
                        
                        if len(dates) == 2:
                            berufserfahrung += ((dates[1][1] - dates[0][1]) * 12) + (dates[1][0] - dates[0][0])
                            print("this cunt should be sent for evaluation")
                            evaluate(original_keywords, user_condition, user_condition_value, berufserfahrung, is_expression)
                else:
                    if value in part:
                        evaluate(original_keywords, user_condition, user_condition_value, part, is_expression)


def evaluate(condition_family, user_condition, user_condition_value, value, is_expression):
    value_found = False
    if isinstance(value, str):
        value = value.replace(",", "")
    if is_expression:
        if user_condition == "Berufserfahrung": # these are numbers. Do not try to index.
            x, y = value, user_condition_value
        else:
            try:
                x, y = keyword_db[condition_family].index(value), keyword_db[condition_family].index(user_condition_value) # the tuple indexes act as weights to compare below (cannot handle subvalues -> probably fixable by running original tuple through it from check_tuple with some bool)
            except ValueError: # for stuff like "Englisch: (Fließend)"
                results[user_condition] = f"{user_condition}: {user_condition_value} [{colored("?", "yellow")}] -> {value}"
                value_found = True
                return True
        if not value_found:
            if x > y:
                results[user_condition] = f"{user_condition}: {user_condition_value} [{colored("<", "green")}] -> {value}"
            if x == y:
                results[user_condition] = f"{user_condition}: {user_condition_value} [{colored("=", "green")}] -> {value}"
            elif x < y:
                results[user_condition] = f"{user_condition}: {user_condition_value} [{colored(">", "red")}] -> {value}"
    elif value != "": # check for safety
        results[user_condition] = f"{user_condition} [{colored("✓", "green")}] -> {value}"

def display_results():
    for result in results.values():
       print(result)

print(target[-4:])
if path.isdir(target):
    for filename in listdir(target):
        if filename[-4:] == ".pdf" and "lebenslauf" in filename.lower():
            work_experience = 0
            section_parsing = False
            print(filename)
            extract_lines(f"{target}/{filename}")
elif path.isfile(target) and target[-4:] == ".pdf":
    work_experience = 0
    section_parsing = False
    extract_lines(target)
else:
    print("not a valid file!")