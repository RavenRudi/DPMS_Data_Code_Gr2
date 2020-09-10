from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag


class WordNet:
    lemmatizer = WordNetLemmatizer()

    @staticmethod
    def penn_to_word_net(tag):
        #  Converting PennTreebank to Wordnet tags

        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return None

    @staticmethod
    def swn_polarity(text):
        # Return a sentiment: 0 = negative, 1 = positive
        sentiment = 0.0
        tokens_count = 0
        str_text = str(text)
        raw_sentences = sent_tokenize(str_text)
        for raw_sentence in raw_sentences:
            tagged_sentence = pos_tag(word_tokenize(raw_sentence))

            for word, tag in tagged_sentence:
                wn_tag = WordNet.penn_to_word_net(tag)
                if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                    continue

                lemma = WordNet.lemmatizer.lemmatize(word, pos=wn_tag)
                if not lemma:
                    continue

                synsets = wn.synsets(lemma, pos=wn_tag)
                if not synsets:
                    continue

                synset = synsets[0]
                swn_synset = swn.senti_synset(synset.name())

                sentiment += swn_synset.pos_score() - swn_synset.neg_score()
                tokens_count += 1

        if not tokens_count:
            return 0

        if sentiment >= 0:
            return 1

        return 0
