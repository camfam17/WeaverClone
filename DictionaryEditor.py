# take a dictionary of words and create a textfile of all the words contianing four letters

dict_file = open('wordlist1.txt')
lines = dict_file.readlines()
dict_file.close()

new_dict = ''
for word in lines:
    if(len(word) == 5):
        new_dict += word

new_dict_file = open('fourletterwordlist1.txt', 'w')
new_dict_file.write(new_dict)
new_dict_file.close()