from flask import Flask, render_template
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


# Example page
@app.route('/deals')
def example():
    # Example of API call to get deals
    base_url = "https://api-test.lime-crm.com/api-test/api/v1/limeobject/deal/"
    params = "?_limit=50"

    # uncomment these 2#######
    # url = base_url + params
    # response_deals = get_api_data(headers=headers, url=url)

    heads = [{'name': 'Name'}, {'name': 'avg_deals_pr_month'}, {'name': 'num_deals_pr_mon'},{'name': 'deals_pr_customer'}, {'name': 'status'}]

    print()
    print(heads)
    print()

    data = (('Franky hansen', '6 ', '9', '12', 'prospekt'),
            ('Timmy hansen', '6 ', '9', '12', 'not_interested'),
            ('Jhon hansen', '0 ', '0', '0', 'Inactive'))

    payload = [{"name": "Tom hansen"}, {'name': 'Franky hansen'}, {'name': 'Timmy hansen'},
               {"avg": "5"}, {'avg': '6 '}, {'avg': '7 '},
              {'num': '10'}, {"num": "10"}, {'num': '9'},
               {'stat': 'prospekt'},{"stat": "customer"},{'stat': 'inactive'},
               {'won': '12'}, {"won": "11"}, {'won': '13'}]

    a = {'a': 2, 'b': 4, 'c': 6, 'd': 9}

    i = 0
    for x in a:
        print(a[x])

    values = a.values()

    total = sum(values)

    avarage = total/4
    print(avarage)


    # payload = [{"name": "Tom hansen"}, {"name" : "5"}, {"name": "10"}, {"name": "11"}, {"name": "customer"},
    #            {'name': 'Franky hansen'}, {'name': '6 '}, {'name': '9'}, {'name': '12'}, {'name': 'prospekt'},
    #            {'name': 'Timmy hansen'}, {'name': '7 '}, {'name': '10'}, {'name': '13'}, {'name': 'inactive'}]


    if len(data) > 0:
        return render_template('deals.html', deals=payload, heads=heads)
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
