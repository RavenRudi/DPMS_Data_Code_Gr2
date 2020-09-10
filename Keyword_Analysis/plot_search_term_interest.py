import pandas as pan
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from requests.exceptions import ConnectTimeout
try:
    proxy = ""
    pytrends = TrendReq(hl='en-US', tz=360, retries=10, backoff_factor=0.5, proxies=[proxy])

except ConnectTimeout:
    print("The connection to the proxy", proxy, "timed out. ")
    exit()


# search term or search terms
search_term = ["Bill Gates"]
# search period format YYYY-MM-DD YYYY-MM-DD
search_period = '2020-01-01 2020-05-17'
# platform the trends should be analysed of
search_platform = "youtube"
# csv file for the search term related queries
csv_file = "related_queries_17.05_cleaned.csv"
# number of keywords the search term will be compared to (search interest)
number_keywords = 4


def interest_search_term(term):

    pytrends.build_payload(term, cat=0, timeframe=search_period, geo='', gprop=search_platform)
    interest_time = pytrends.interest_over_time()
    df_interest = pan.DataFrame(interest_time)
    df_interest = df_interest.drop(labels=['isPartial'], axis='columns')

    return df_interest


def get_csv():

    data = pan.read_csv(csv_file, header=0)
    rising = data.Rising.tolist()
    top = data.Top.tolist()
    return rising, top


def save_csv(file,name):
    file.to_csv(name, encoding='utf_8_sig')


def plot_image(data,title,savename):
    image = data.plot(title=title)
    figure = image.get_figure()
    figure.savefig(savename)


def search_term_function(term):
    search_term_interest = interest_search_term(term)
    plot_image(search_term_interest, "Relative interest in a search term on YouTube in a given period of time",
                   "interest_search.png")


def top_query(term):
    top_queries, rising_queries = get_csv()
    for i in range(number_keywords):
        term.append(top_queries[i])

    search_term_queries_top = interest_search_term(term)
    save_csv(search_term_queries_top, "interest_in_top_queries.csv")

    plot_image(search_term_queries_top, "Relative interest of a search term and the Top 4 related queries",
               "interest_top.png")
    for i in range(number_keywords):
        term.remove(top_queries[i])


def rising_query(term):
    top_queries, rising_queries = get_csv()
    for i in range(number_keywords):
        term.append(rising_queries[i])

    search_term_queries_rising = interest_search_term(term)
    save_csv(search_term_queries_rising, "interest_in_rising_queries.csv")

    plot_image(search_term_queries_rising, "Relative interest of a searchterm and the Top 4 related queries",
               "interest_rising.png")

    for i in range(number_keywords):
        term.remove(rising_queries[i])


try:
    search_term_function(search_term)
    top_query(search_term)
    rising_query(search_term)
except ResponseError:
    print("Please adjust the variable number_keywords to a lower value ")









