import sys
import os
import inquirer
from revChatGPT.V1 import Chatbot
import glob

questions = [
    inquirer.List('auth', message='Please Choose your authentication method. ', choices=['Email/Password', 'Access Token']),
]

answers = inquirer.prompt(questions)

os.system('cls' if os.name=='nt' else 'clear')

if answers['auth'] == 'Email/Password':
    # Login Method Email/Password
    email = input("Please input your Email Here : ")
    
    password = input("Please input your Password Here : ")

    os.system('cls' if os.name=='nt' else 'clear')
   
    # Asking the ChatGPT Model
    
    questions2 = [
        inquirer.List('model', message='Please choose your ChatGPT Model.', choices=['GPT-3.5', 'GPT-4']),
    ]
    
    answers2 = inquirer.prompt(questions2)

    if answers2['model'] == 'GPT-3.5':
        model = "None"
    else:
        model = 'gpt-4'
    # Setting up the ChatGPT
    chatbot = Chatbot(config={
        "email": email,
        "password": password,
        "model": model,
    })
elif answers['auth'] == 'Access Token':
    # Login Method Access Token
    print("Please Get Access token at Following Link : ")
    print("https://chat.openai.com/api/auth/session")
    acc_token = input("and Paste at here : ")    
    os.system('cls' if os.name=='nt' else 'clear')

    # Asking the ChatGPT Model
    questions2 = [
        inquirer.List('model', message='Please choose your ChatGPT Model.', choices=['GPT-3.5', 'GPT-4']),
    ]
    
    answers2 = inquirer.prompt(questions2)
    
    if answers2['model'] == 'GPT-3.5':
        model = "None"
    else:
        model = 'gpt-4'
    # Setting up the ChatGPT
    
    chatbot = Chatbot(config={
        "access_token": acc_token,
        "model": model,
    })
else:
    print("How did you find this message?")


questions3 = [
        inquirer.List('Tools', message='Did you use the Tool Python-Formatter?', choices=['Yes', 'No']),
    ]

answers3 = inquirer.prompt(questions3)

python_formatter_usage = answers3['Tools']

if python_formatter_usage.lower() == 'yes':
    folder_path = input("Please input your output of Python-Formatter Folder in here: ")
    file_dict = {}  # create an empty dictionary
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Filter for text files
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as f:
                content = f.read()
                var_name = f"file_{len(file_dict) + 1}"  # create a variable name for each file
                file_dict[var_name] = content  # store the content in the dictionary with the variable name as the key

else:
    transcript_file = input("Please input your transcript file here (Characters Max Value: 4096): ")
    transcript_variable = Path(transcript_file).read_text()
    if len(transcript_variable) > 4096:
        print("Your transcript file has too many Characters. Please try using Python-Formatter to split it into different files.")
        print("https://github.com/blusewill/Python-Formatter")
        sys.exit(0)
    else:
        print("The transcript file has been imported. Loading GPT-Translator")

from_lang = input("Please type your input file Language : ")

out_lang = input("Please type the Language that you are going to translate to : ")

setup_chat = f"Please translate the stuff I just pasted from {from_lang} to {out_lang}"

print("Testing the key and ChatGPT Response")

def test_chat():
        response = ""

        for data in chatbot.ask(
                setup_chat
        ):
            response = data["message"]

        print(response)

os.system('cls' if os.name=='nt' else 'clear')
test_chat()

questions4= [
    inquirer.List('output', message="Did you see the ChatGPT's Output?", choices=['Yes', 'No']),
]

answers4 = inquirer.prompt(questions4)

output_setup = answers4['output']

if output_setup.lower() == 'yes':
    if python_formatter_usage.lower() == 'yes':
        file = open("Translated.txt", "w")
        transcript_variable_count = 1
        def start_translating():
            trans = ""
            global transcript_variable_count

            transcript_variable = file_dict[file,(transcript_variable_count)]
            for translation in chatbot.ask(
                globals()[transcript_variable],
                auto_continue=True
            ):
                trans = translation["message"]
        
            transcript_variable_count += 1

            return trans
        while True:
            output_trans = start_translating()
            file.write(output_trans + '\n')

            if transcript_variable not in globals():
                break
                file.close
                sys.exit(0)

    else:
        def start_translating():
            trans = ""

            for translation in chatbot.ask(
                    transcript_variable,
                    auto_continue=True
            ):

                trans = translation["message"]
        
            return trans
    output_trans = start_translating()
 
    file = open("Translated.txt", "w")
    file.write(output_trans)
    file.close
