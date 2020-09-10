import pandas as pan
from pytrends.request import TrendReq
pytrends = TrendReq()

search_term = "Bill Gates"
kw_list = [search_term]
search_period = '2020-01-01 2020-05-17'
search_platform = "youtube"

pytrends.build_payload(kw_list, cat=0, timeframe=search_period, gprop=search_platform)


related_queries = pytrends.related_queries()
df_queries = pan.DataFrame(related_queries)

df_queries.to_csv('related_queries.csv', encoding='utf_8_sig')




