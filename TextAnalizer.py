import configparser
from collections import Counter
from nltk.corpus.reader.plaintext import PlaintextCorpusReader as CorpusReader
from nltk.tokenize import RegexpTokenizer as Tokenizer
from spacy import load as load_nlp


class TextAnalizer:

    def __init__(self, my_input_file):
        self.config = configparser.ConfigParser()
        self.config.read("text_analysis.cfg")
        self.input_file = my_input_file
        self.nlp_model = self.config["DEFAULT"]["nlp_model"]
        #The output file name
        self.output_file = self.config["DEFAULT"]["output_file"]
        self.nlp = load_nlp(self.nlp_model)
        self.corpus = CorpusReader(".", self.input_file)
        self.raw_text = self.corpus.raw()
        self.nlp_text = self.nlp(self.raw_text)
        # Here, lets put together the infos for text analysis with spacy.
        self.analysis_dictionary = Counter()
        self.word_count = 0
        self.get_word_count_nltk()

    def get_paragraph(self):
        return self.corpus.paras()

    def get_sentence(self):
        return self.corpus.sents()

    def get_word(self):
        return self.corpus.words()


    def get_word_count_nltk(self):
        tokenizer = Tokenizer(r'\w+')
        counts = Counter()
        sentences = self.get_sentence()
        for sentence in sentences:
            tokens = tokenizer.tokenize(" ".join(sentence))
            self.word_count = self.word_count + len(tokens)
            filtered = [w for w in sentence if w.isalnum()]
            counts = counts + Counter(filtered)
        return counts, self.word_count

    def analize_nlp(self):
        analized_data_str = (self.config["ANALIZED"]["POS"])
        analized_data = (analized_data_str.split(","))
        result_dict = {}
        diff_str, tot_str = (self.config["DEFAULT"]["diff_tot_string"]).split(",")
        lemma_counter = Counter()
        pos_counter = Counter()
        tag_counter = Counter()

        for token in self.nlp_text:
            lemma_counter = lemma_counter + Counter([token.lemma_])
            pos_counter = pos_counter + Counter([token.pos_])
            tag_counter = tag_counter + Counter([token.tag_])
            my_key = token.lemma_+"_"+token.tag_+"_"+token.pos_
            self.analysis_dictionary[my_key] += 1
        for pos in analized_data:
            instance_counter = 0
            total_counter = 0
            for key in self.analysis_dictionary.keys():
                try:
                    my_lemma, my_tag, my_pos = key.split("_")
                except ValueError:
                    print("Warning: Array has a empty line") # add logging
                if pos == my_pos:
                    instance_counter +=1
                    total_counter = total_counter + self.analysis_dictionary.get(key)
            result_dict[pos+diff_str] = instance_counter
            result_dict[pos+tot_str] = total_counter
        #add the stuff from nltk
        diff_word, word_count = self.get_word_count_nltk()
        result_dict["WORDS"+tot_str] = word_count
        result_dict["WORDS" + diff_str] = len(diff_word)
        result_dict["PARAGRAPHS"] = len(self.get_paragraph())
        result_dict["SENTENCES"] = len(self.get_sentence())

        return result_dict


    def write_output(self):
        with open(self.output_file, "w+") as f:
            f.write("Number of paragraphes: " + str(len(self.get_paragraph())) + "\n")
            f.write("Number of sentences: " + str(len(self.get_sentence())) + "\n")
            f.write("Number of words: " + str(self.word_count) + "\n")
            f.write("Average words per sentence: " + str(round(self.word_count / len(self.get_sentence()), 2)) + "\n")
            f.write("Number of different words: " + str(len(self.get_word_count_nltk())) + "\n")
            f.write("Text variety (different words/total words: " + str(round(len(self.get_word_count_nltk()) / self.word_count, 2)) + "\n")
            f.close()








