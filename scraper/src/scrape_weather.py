import requests
import itertools
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def get_monthly_table_html(year, month):
    '''
    Fetches the Weather Underground (wunderground.com) data for a given month
    and year in raw HTML form

    Parameters
    ----------
    year : int, str
        the year which we're interested in scraping data for
    month : int, str
        the month which we're interested in scraping data for

    Returns
    -------
    table : bs4.element.Tag
        the HTML table containing the weather data for the month and year which
        we're interested in
    '''
    month = str(month).zfill(2)

    # url = ('https://www.wunderground.com/history/airport/EGLL/'
    #        '{0}/{1}/1/MonthlyHistory.html'.format(year, month))

    url = ('https://www.wunderground.com/history/airport/KFTY/'
        '{0}/{1}/1/MonthlyHistory.html?req_city=Atlanta%20Fulton&req_state=GA&reqdb.zip=30336&reqdb.magic=6&reqdb.wmo=99999'.format(year, month))

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml", from_encoding='utf-8')
    table = soup.find('table', attrs={'id': 'obsTable'})

    if table is None:
        raise ValueError('missed {0}-{1}'.format(year, month))

    return table


def get_headers(table):
    '''
    The raw <th> table header elements in wunderground's HTML do not include
    the second line, denoting the daily high, average and low values for each
    measurement. get_headers() returns the full list of headers, including
    these high, average and low sub-headings.

    Parameters
    ----------
    table : bs4.element.Tag
        the HTML table containing the weather data for the month and year which
        we're interested in

    Returns
    -------
    all_headers : list
        a list of strings denoting the column headings for our table
    '''
    headers = [header.text for header in table.find_all('th')]
    high_low_headers = [[head + ' HIGH', head + ' AVG', head + ' LOW']
                        for head in headers[1:-2]]

    all_headers = list(itertools.chain(*[[headers[0]]]
                                       + high_low_headers
                                       + [headers[-2:]]))
    return all_headers


def clean_up(text):
    '''
    The scraping process seems to transform values into bytestrings, and then
    return the string form of those bytestrings, including what would be
    escaped newlines, tabs, etc.
    clean_up() tidies this ugly data so that it's more easily interpretable

    Parameters
    ----------
    text : str
        the text to be cleaned

    Returns
    -------
    text : str
        the cleaned text
    '''
    replace_list = ['b', '\n', '\'', '\t', '\xa0', 'c2a0']
    for r in replace_list:
        text = text.replace(r, '')
    return text


def html_table_to_dataframe(table):
    '''
    takes an html table, finds and collects all of its headers and rows, and
    zips them into a pandas dataframe so that they can be more easily
    concatenated, manipulated, analysed and stored

    Parameters
    ----------
    table : bs4.element.Tag
        the HTML table containing the weather data for the month and year which
        we're interested in

    Returns
    -------
    df : pd.DataFrame
        The pandas dataframe form of the scraped table
    '''
    headers = get_headers(table)
    rows = [[clean_up(datapoint.text) for datapoint in row.find_all('td')]
            for row in table.find_all('tr')]

    return pd.DataFrame([dict(zip(headers, row)) for row in rows])


def get_date(year, month, day):
    '''
    return the appropriate string form of the date so that it can be parsed by
    the necessary things

    Parameters
    ----------
    year : int, str
    month : int, str
    day : int, str

    Returns
    -------
    date : str
        pretty string form of date
    '''
    return '-'.join([str(year), str(month).zfill(2), str(day).zfill(2)])


def _get_weather(year, month):
    '''
    scrape a particular page on wunderground.com which gives a table of daily
    weather data for a supplied month and year.

    Parameters
    ----------
    year : int, str
    month : int, str

    Returns
    -------
    df : pd.DataFrame
        the full table of data in pandas dataframe format
    '''
    try:
        table = get_monthly_table_html(year, month)
        df = html_table_to_dataframe(table)

        df = df.drop([0, 1])
        df['Date'] = np.vectorize(get_date)(year, month, df[str(year)])
        df = (df.drop(str(year), axis=1)
                .set_index('Date')
                .convert_objects(convert_dates=True,
                                 convert_numeric=True))
        df.index = pd.to_datetime(df.index)
        return df

    except ValueError:
        return None


def get_weather(years, months=list(range(1, 13))):
    '''
    collects weather data a specified set of months and years. if multiple
    years are supplied or no months are specified, the function will collect
    data for the full year (ie all 12 months) of the supplied year(s).

    Parameters
    ----------
    years : list, int, str
        the list of years for which we'll be collecting data

    months : list, int, str
        the list of months for which we'll be collecting data

    Returns
    -------
    df : pd.DataFrame
        the full table of data in pandas dataframe format
    '''
    if type(months) != list:
        months = [months]

    if type(years) != list:
        years = [years]

    if len(years) > 1:
        months = list(range(1, 13))

    all_months = [(year, month) for year in years for month in months]
    return pd.concat([_get_weather(year, month) for year, month in all_months])
