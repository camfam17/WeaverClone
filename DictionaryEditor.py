# take a dictionary of words and create a textfile of all the words contianing four letters

dict_file = (open('words_alpha.txt')).readlines()


new_dict = ''
for word in dict_file:
    if(len(word) == 5):
        new_dict += word

dict_file.close()
# print(new_dict)

new_dict_file = open('FourLetterWords.txt', 'w')
new_dict_file.write(new_dict)
new_dict_file.close()