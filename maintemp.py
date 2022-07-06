import pandas as pd
from submissions import Submissions
import time

user = 'John Doe'

sub = Submissions(user)

t1 = time.time()
my_filings = sub.get_filings(ciks=[1065280,320193,1326801,1543151,789019], form_type='10-k', start_date='2020-12-31')
t2 = time.time()
print(t2-t1)
filings_df = pd.DataFrame(my_filings)

print(filings_df)

t1 = time.time()
parsed_10k_filings = sub.parse_10k(my_filings)
t2 = time.time()
print(t2-t1)

print(pd.DataFrame(parsed_10k_filings))

print(pd.DataFrame(parsed_10k_filings).iloc[0])

