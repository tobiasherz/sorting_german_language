def count_words(my_list): #counts words in a list and creates a dictionary out of it. Key: Word, Value: Number of occurences
    word_count = []

    for my_word in my_list:
        my_word = my_word.lower()
        try:
            if type(word_count.index(my_word)) == int:
                word_count[word_count.index(my_word)+1] = word_count[word_count.index(my_word)+1] + 1
        except ValueError:
            word_count.append(my_word)
            word_count.append(1)

    print(word_count)
    my_dictionary = {}
    i = 0
    while i < len(word_count):
        my_word = word_count[i]
        i += 1
        my_occurence = word_count[i]
        i += 1
        my_dictionary[my_word] = my_occurence

    return my_dictionary

def remove_characters(my_list, unwanted_characters): #returns a list without the elements in unwanted_characters
    for character in unwanted_characters:
        try:
            while type(my_list.index(character)) == int:
                my_list.remove(character)
        except ValueError:
                #do nothing in this case
                print(ValueError)
    return my_list


def analize_sentences(sentence): #returns a list of words
    wordList = []
    for my_word in sentence:
        split_string = my_word.split(" ")
        for my_word2 in split_string:
            stripped_word = my_word2.strip(",-/!?\"")
            wordList.append(stripped_word)

    return wordList

def split_sentences(text_list, my_deliminators): #returns a list of textfragments where the deliminator was my_deliminator
    sentence_list = []
    for line1 in text_list:
        for my_deliminator in my_deliminators:
            if (line1.find(my_deliminator) >=0):
                split_string = line1.split(my_deliminator)
                #print(split_string)
                for line2 in split_string:
                    sentence_list.append(line2)

    return sentence_list
