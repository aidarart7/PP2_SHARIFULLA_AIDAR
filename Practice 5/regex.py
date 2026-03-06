import re

s = input("1. Enter a string to check 'a' followed by zero or more 'b's: ")
print("Match" if re.fullmatch(r"ab*", s) else "No match")

s = input("2. Enter a string to check 'a' followed by 2-3 'b's: ")
print("Match" if re.fullmatch(r"ab{2,3}", s) else "No match")

s = input("3. Enter a string to check snake_case: ")
print("Match" if re.fullmatch(r"[a-z]+(_[a-z]+)+", s) else "No match")

s = input("4. Enter a string to check one uppercase followed by lowercase letters: ")
print("Match" if re.fullmatch(r"[A-Z][a-z]+", s) else "No match")

s = input("5. Enter a string to check 'a' followed by anything, ending with 'b': ")
print("Match" if re.fullmatch(r"a.*b", s) else "No match")

s = input("6. Enter text to replace spaces, commas, or dots with colon: ")
print("Result:", re.sub(r"[ ,\.]", ":", s))

snake = input("7. Enter snake_case string to convert to camelCase: ")
camel = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), snake)
print("camelCase:", camel)

s = input("8. Enter CamelCase string to split at uppercase letters: ")
print("Split parts:", re.findall(r"[A-Z][a-z]*", s))

s = input("9. Enter CamelCase string to insert spaces before capitals: ")
print("With spaces:", re.sub(r"([A-Z])", r" \1", s).strip())

s = input("10. Enter CamelCase string to convert to snake_case: ")
print("snake_case:", re.sub(r"([A-Z])", r"_\1", s).lower().lstrip("_"))