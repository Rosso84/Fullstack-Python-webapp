from datetime import *
from flask import Flask, render_template
import requests
import json
from API import deals_api
from API import companies_api

# Feel free to import additional libraries if you like


app = Flask(__name__, static_url_path='/static')

# Paste the API-key you have received as the value for "x-api-key"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/hal+json",
    "x-api-key": ""
}


def get_api_data(headers, url):
    # First call to get first data page from the API
    response = requests.get(url=url,
                            headers=headers,
                            data=None,
                            verify=False)

    # Convert response string into json data and get embedded limeobjects
    json_data = json.loads(response.text)
    print(type(json_data))
    limeobjects = json_data.get("_embedded").get("limeobjects")
    print(type(limeobjects))

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
def deals():
    companies = "company/"
    deal = "deal/"
    limit = "?_limit=10"
    offset = "&_offset=10"

    base_url = "https://api-test.lime-crm.com/api-test/api/v1/limeobject/"
    deals_url = base_url + deal + limit
    next_deals_url = deals_url + limit + offset

    company_url = base_url + companies + limit

    response_deals = get_api_data(headers=headers, url=deals_url)
    #next_deal = get_api_data(headers=headers, url=next_url)

    response_companies = get_api_data(headers=headers, url=company_url)


    average_values = \
        deals_api.get_average_deal_values_won_last_year( response_deals )

    total_values_previous_year = \
        deals_api.get_total_values_won_last_year( response_deals )

    deals_pr_month = \
        deals_api.get_list_of_won_deals_pr_month_last_year( response_deals )

    average_deals = \
        deals_api.get_average_number_of_won_deals_pr_month_last_year( response_deals )

    total_number_of_deals_won = \
        deals_api.get_total_number_of_won_deals_last_Year( response_deals )

    customer_and_values = \
        deals_api.get_list_of_values_won_pr_customer_last_year( response_deals )

    current_company_status_list = \
        companies_api.get_all_current_company_status_list( response_companies )

    updated_company_status = \
         deals_api.get_updated_company_status( response_deals,
                                                current_company_status_list )



    if updated_company_status is None:
        updated_company_status = {"Empty": "Empty"}

    thisYear = datetime.now().year
    last_year = thisYear - 1

    if len(response_deals) > 0:
        return render_template('deals.html',
                               average_values=average_values,
                               total_values=total_values_previous_year,
                               deals_pr_month=deals_pr_month,
                               average_deals=average_deals,
                               total_deals=total_number_of_deals_won,
                               customer_and_values=customer_and_values,
                               updated_company_status=updated_company_status,
                               #next_url=next_deal,
                               year=last_year)
    else:
        msg = 'No deals found'
        return render_template('deals.html', msg=msg)


# You can add more pages to your app, like this:
@app.route('/companies')
def company():

    response_companies = {}

    if len(response_companies) > 0:
        return render_template('companies.html',
                               )
    else:
        msg = 'No companies found'
        return render_template('companies.html', msg=msg)


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
