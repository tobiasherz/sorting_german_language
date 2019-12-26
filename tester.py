from TextCalculator import TextCalculator
from TextAnalizer import TextAnalizer
from collections import Counter

my_analizer = TextAnalizer("test_werther.txt")
my_values = my_analizer.analize_nlp()
print(my_values)
#my_analizer.write_output()

#values_sent = Counter(ADJ_diff=1, ADJ_tot=2, MEAN_WORDS_PER_SENTENCE=16, WORDS=2, NOUN=1)
#my_calculator = TextCalculator(values_sent)
my_calculator = TextCalculator(my_values)
my_calculator.norm_vector()
my_result = my_calculator.get_percentage()
print(my_result)



