import random
import string

# List of reserved words, operators, and valid characters
reserved_words = ["and", "array", "bool", "chillax", "elif", "else", "end", "false", "if", "input", "int", "let", "main", "not", "or", "output", "program", "rem", "return", "true", "while"]
operators = ["{", "}", "(", ")", "*", ",", "-", "..", "/", "/=", ":", ";", "<", "<=", "=", ">", ">=", "[", "]", "+"]

# Function to generate random code
def generate_code():
    code = ""

    # Continue adding text with a certain probability
    while random.random() > 0.007:
        # Choose randomly between strings, numbers, operators, and reserved words
        element_choice = random.choice(["string", "number", "operator", "reserved_word", "spaces", "other", "comment"])

        if element_choice == "string":
            # Add strings
            code += '"' + "".join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(1, 20))) + '"\n'

        elif element_choice == "number":
            # Add integers as numbers
            code += str(random.randint(1, 100)) + "\n"

        elif element_choice == "operator":
            # Add operators
            code += random.choice(operators) + "\n"

        elif element_choice == "reserved_word":
            # Add reserved words and user-defined words
            code += random.choice(reserved_words + ["_" + "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))]) + "\n"
        elif element_choice == "other":
            if (random.random() > 0.01):
                code += random.choice("_abcd") + "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10))) + "\n"
            else:
                code += random.choice(["!", ".", "%", "#"])
        elif element_choice == "spaces":
            for i in range(5):
                code += random.choice("\n\t\v\r\f ")
        elif element_choice == "comment":
            code += "{"
            
            if random.random() < 0.3:
                code += "      {   }"
            elif random.random() < 0.3:
                code += "    \n     { \n \t \t \n }"
            elif (random.random() < 0.05):
                code += " { \n"
            
            
            code += "}"
    return code

# Generate and write code to files
num_files = 1000  # You can adjust this number
for i in range(31, num_files):
    with open(f"tests/{i}.ampl", "x") as file:
        file.write(generate_code())

