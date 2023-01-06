# take a dictionary of words and create a textfile of all the words contianing four letters

dict_file = open('wordlist3.txt')
lines = dict_file.readlines()
dict_file.close()

new_dict = ''
for word in lines:
    if(len(word) == 5 and word[-1] == '\n'):
        new_dict += word

new_dict_file = open('fourletterwordlist3.txt', 'w')
new_dict_file.write(new_dict)
new_dict_file.close()