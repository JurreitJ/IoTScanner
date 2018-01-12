"""
File to test new functionalities, before implementing;
Not Unit tests;
"""

user_file = open("wordlists/user.txt", "r")
wordlist = open("wordlists/wordlist.txt", "w")
for username in user_file:
    password_file = open("wordlists/password.txt", "r")
    for password in password_file:
        line = str(username).rsplit("\n", 1)[0] + ":" + str(password)
        wordlist.write(line)
wordlist.close()
