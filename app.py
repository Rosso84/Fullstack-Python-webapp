from flask import Flask, render_template
from datetime import *;
from dateutil.relativedelta import *
import calendar
import requests
import json

# Feel free to import additional libraries if you like

app = Flask(__name__, static_url_path='/static')

# Paste the API-key you have received as the value for "x-api-key"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/hal+json",
    "x-api-key": ""
}

""" Calculate total average deal values for previous year """
def calculate_average_deals_previuos_year(lime_object):
    values = []

    for data in lime_object:
        value = data['value']

        # If e.g "_timestamp" is the data that provides information of the year the  limeobject "deals"
        timestamp = data['_timestamp']
        convertedDateOfDeal = datetime.fromisoformat(timestamp).date()
        dealYear = convertedDateOfDeal.year
        thisYear = datetime.now().year
        previuosYear = thisYear - 1

        # If the deals year is previous, add value to list
        if dealYear == previuosYear:
            values.append(value)

        # Calculate total average
    valuesLength = len(values)
    sumValues = sum(values)
    averageTotalValuesPreviousYear = sumValues / valuesLength

    # Convert to a whole number
    convertedValue = int(averageTotalValuesPreviousYear)
    print('Average: ', convertedValue)

    return convertedValue


# Example of function for REST API call to get data from Lime
def get_api_data(headers, url):
    # First call to get first data page from the API
    response = requests.get(url=url,
                            headers=headers,
                            data=None,
                            verify=False)

    # Convert response string into json data and get embedded limeobjects
    json_data = json.loads(response.text)
    limeobjects = json_data.get("_embedded").get("limeobjects")

    # Check for more data pages and get those too
    nextpage = json_data.get("_links").get("next")
    while nextpage is not None:
        url = nextpage["href"]
        response = requests.get(url=url,
                                headers=headers,
                                data=None,
                                verify=False)

        json_data = json.loads(response.text)
        limeobjects += json_data.get("_embedded").get("limeobjects")
        nextpage = json_data.get("_links").get("next")

    return limeobjects


# Index page
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/deals')
def example():
    # Example of API call to get deals
    base_url = "https://api-test.lime-crm.com/api-test/api/v1/limeobject/deal/"
    params = "?_limit=50"

    url = base_url + params
    response_deals = get_api_data(headers=headers, url=url)



    """ Calculate number of won deals pr month last year  """

    dealsPrMonth = {
        'january': 0,
        'february': 0,
        'march': 0,
        'april': 0,
        'may': 0,
        'june': 0,
        'july': 0,
        'august': 0,
        'september': 0,
        'october': 0,
        'november': 0,
        'december': 0
    }

    valuesDealsPrMonth = dealsPrMonth.values()

    for key, value in dealsPrMonth.items():
        print(key, value)

    # Avarage
    # letters = {'a': 2, 'b': 4, 'c': 6, 'd': 9, 'a': 20}
    #
    # for x in letters:
    #     print(letters[x])
    #
    # values = letters.values()
    #
    # total = sum(values)

    # average = total / len(letters)

    # print(average)

    # data = (('Franky hansen', '6 ', '9', '12', 'prospekt'),
    #         ('Timmy hansen', '6 ', '9', '12', 'not_interested'),
    #         ('Timmy hansen', '6 ', '9', '12', 'not_interested'),
    #         ('Timmy hansen', '6 ', '9', '12', 'not_interested'),
    #         ('Timmy hansen', '6 ', '9', '12', 'not_interested'),
    #         ('Timmy hansen', '6 ', '9', '12', 'not_interested'),
    #         ('Jhon hansen', '0 ', '0', '0', 'Inactive'))

    payload = [{"name": "Tom hansen"}, {"name": "5"}, {"name": "10"}, {"name": "11"}, {"name": "customer"},
               {'name': 'Franky hansen'}, {'name': '6 '}, {'name': '9'}, {'name': '12'}, {'name': 'prospekt'},
               {'name': 'Timmy hansen'}, {'name': '7 '}, {'name': '10'}, {'name': '13'}, {'name': 'inactive'}]

    # payload = [{"name": "Tom hansen"}, {'name': 'Franky hansen'}, {'name': 'Timmy hansen'},
    #            {"avg": "5"}, {'avg': '6 '}, {'avg': '7 '},
    #            {'num': '10'}, {"num": "10"}, {'num': '9'},
    #            {'stat': 'prospekt'}, {"stat": "customer"}, {'stat': 'inactive'},
    #            {'won': '12'}, {"won": "11"}, {'won': '13'}]

    # count keys occurences for ids
    sumNumberofName = len([k for d in payload for k in d.keys() if k == 'name'])  # should be 3
    # print(sumLettersOfA, '-----number of keys -----')

    # second version of count
    keys_list = []
    for data in payload:
        keys_list += data.keys()
    x = keys_list.count('name')
    # print(keys_list, '-----number of keys -----')

    table_headers = [{'name': 'Companies'}, {'name': 'Status'}]

    average = calculate_average_deals_previuos_year(response_deals)

    if len(data) > 0:
        return render_template('deals.html', deals=data, heads=table_headers, average=average)
    else:
        msg = 'No deals found'
        return render_template('deals.html', msg=msg)


# You can add more pages to your app, like this:
@app.route('/myroute')
def myroute():
    fruits = [{"fruit": "Banana"}, {"fruit": "Banana"}, {"fruit": "Banana"}, {"fruit": "Banana"}]

    """
    For myroute.html to render you have to create the myroute.html
    page inside the templates-folder. And then add a link to your page in the
    _navbar.html-file, located in templates/includes/
    """
    return render_template('myroute.html', deals=fruits)


# DEBUGGING
"""
If you want to debug your app, one of the ways you can do that is to use:
import pdb; pdb.set_trace()
Add that line of code anywhere, and it will act as a breakpoint and halt
your application
"""

if __name__ == '__main__':
    app.secret_key = 'somethingsecret'
    app.run(debug=True)

