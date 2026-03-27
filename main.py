from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import nltk

nltk.download('punkt')
nltk.download('stopwords')

text = input("Enter your text:\n")

stop_words = set(stopwords.words("english"))
words = word_tokenize(text)

freq_table = {}
for word in words:
    word = word.lower()
    if word not in stop_words:
        freq_table[word] = freq_table.get(word, 0) + 1

sentences = sent_tokenize(text)
sentence_scores = {}

for sent in sentences:
    for word in word_tokenize(sent.lower()):
        if word in freq_table:
            sentence_scores[sent] = sentence_scores.get(sent, 0) + freq_table[word]

summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
summary = " ".join(summary_sentences)

print("\nSummary:\n", summary)