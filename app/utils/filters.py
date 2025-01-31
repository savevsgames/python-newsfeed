# utility functions
from datetime import datetime

# example output: 01/31/25
def format_date(date):
    return date.strftime('%m/%d/%y')

# Testing format_date function
print(format_date(datetime.now()))

# strips extra characters from domain name
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# Testing format_url function - output - google.com
print(format_url('http://google.com/test/'))
print(format_url('https://www.google.com?q=test'))

# adds an s to entries with counts higher than one
def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word

# Testing format_plural function - output - cats, dog
print(format_plural(2, 'cat'))
print(format_plural(1, 'dog'))
