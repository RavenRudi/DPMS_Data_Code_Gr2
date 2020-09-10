from CsvAction import CsvAction
from WordNet import WordNet

comments_file = "comments.csv"


def main():
    def sentiment_function(comments):
        comment_sentiment = WordNet.swn_polarity(comments)
        return comment_sentiment

    csv_file = CsvAction.read_csv(comments_file)

    csv_file['Sentiment'] = csv_file.apply(lambda x: sentiment_function(x['Comments']), axis=1)
    csv_file.to_csv("sentiment.csv")


if __name__ == "__main__":
    main()


