from os import system, name

def clear():
    if name == 'nt':
        _ = system('clear')

def word_to_numbers():
    system('clear')
    word = input('Please enter a word: ').lower()
    # word_list = list(word)
    presses = 0
    for letter in word:
        if letter in ('adgjmptw '):
            presses +=1
        elif letter in ('behknqux'):
            presses +=2
        elif letter in ('cfilorvy'):
            presses +=3
        elif letter in ('sz'):
            presses +=4
        else:
            print('Your word is invalid you failure of a human.')
    # system('clear')
    print(f'\n\nThe number of Nokia presses required to type {word} is: {presses}\n\n')
word_to_numbers()
