dict_file = (open('words_alpha.txt')).readlines()


new_dict = ''
for word in dict_file:
    if(len(word) == 5):
        new_dict += word


# print(new_dict)

new_dict_file = open('FourLetterWords.txt', 'w')
new_dict_file.write(new_dict)