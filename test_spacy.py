import configparser
from collections import Counter
from nltk.corpus.reader.plaintext import PlaintextCorpusReader as CorpusReader
from nltk.tokenize import RegexpTokenizer as Tokenizer
from spacy import load as load_nlp

#Load Configuration from config-file
config = configparser.ConfigParser()
config.read("text_analysis.cfg")
#Read out configuration parameters
#Filname of text file to analyze
input_file = config["DEFAULT"]["input_file"]
#The nlp model used
nlp_model = config["DEFAULT"]["nlp_model"]
#The output file name
output_file = config["DEFAULT"]["output_file"]

#Load the nlp model
nlp = load_nlp(nlp_model)

#This Section generates a corpus (for nltk) and a string-text (for spacy)
corpus = CorpusReader(".", input_file)
my_text = corpus.raw()


#This section deals with nltk-stuff for analysis
paragraphs=corpus.paras()
sentences=corpus.sents()
words=corpus.words()



tokenizer = Tokenizer(r'\w+')
word_count = 0
counts = Counter()


for sentence in sentences:
    tokens = tokenizer.tokenize(" ".join(sentence))
    word_count = word_count + len(tokens)
    filtered = [w for w in sentence if w.isalnum()]
    counts = counts + Counter(filtered)

nlp_text = nlp(my_text)

#Here, lets put together the infos for text analysis with spacy.
lemma_counter = Counter()
pos_counter = Counter()
tag_counter = Counter()
analysis_dictionary = Counter()

for token in nlp_text:
    lemma_counter = lemma_counter + Counter([token.lemma_])
    pos_counter = pos_counter + Counter([token.pos_])
    tag_counter = tag_counter + Counter([token.tag_])
    my_key = token.lemma_+"_"+token.tag_+"_"+token.pos_
    analysis_dictionary[my_key] += 1


analized_data_str = (config["ANALIZED"]["POS"])
analized_data = (analized_data_str.split(","))
result_dict = {}

diff_str, tot_str = (config["DEFAULT"]["diff_tot_string"]).split(",")


for pos in analized_data:
    instance_counter = 0
    total_counter = 0
    for key in analysis_dictionary.keys():
        try:
            my_lemma, my_tag, my_pos = key.split("_")
        except ValueError:
            print("Warning: Array has a empty line") # add logging
        if pos == my_pos:
            instance_counter +=1
            total_counter = total_counter + analysis_dictionary.get(key)

    result_dict[pos+diff_str] = instance_counter
    result_dict[pos+tot_str] = total_counter

print(result_dict)

with open(output_file, "w+") as f:
    f.write("Number of paragraphes: " + str(len(paragraphs)) + "\n")
    f.write("Number of sentences: " + str(len(sentences)) + "\n")
    f.write("Number of words: " + str(word_count) + "\n")
    f.write("Average words per sentence: " + str(round(word_count / len(sentences), 2)) + "\n")
    f.write("Number of different words: " + str(len(counts)) + "\n")
    f.write("Text variety (different words/total words: " + str(round(len(counts) / word_count, 2)) + "\n")
    f.close()