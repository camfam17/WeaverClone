
four_letter_words = open('fourletterwordlist3.txt').readlines()

string = ''



def differs_by_one(word1, word2):
    
    differ = 0
    for i in range(4):
        if not word1[i] == word2[i]:
            differ += 1
    
    return differ == 1


# n^2 for n = 7186
for i, word1 in enumerate(four_letter_words):
    string += '\n' + str(i) + ' ' + word1[:-1] + ' '
    for j, word2 in enumerate(four_letter_words):
        
        if differs_by_one(word1, word2):
            string += str(j) + ', '
        

print(string)

output_file = open('AdjacencyList3.txt', 'w')
output_file.write(string)

# Can use an adjacency matrix instead? Warshalls algorithm?