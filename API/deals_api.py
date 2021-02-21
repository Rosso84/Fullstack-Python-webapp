from datetime import *

counter = 0
thisYear = datetime.now().year
last_year = thisYear - 1


# Receives a limeObject
# Calculate total average deal values for previous year.
# Returns an average value of total won deals previous year.
def get_average_deal_values_won_last_year(lime_object_deals):
    all_won = get_list_of_all_won_deal_values_last_year(lime_object_deals)

    # Calculate total average
    valuesLength = len(all_won)
    sumValues = sum(all_won)
    average = sumValues / valuesLength

    # Remove decimals and convert to a whole number (optional)
    convertedValue = int(average)

    return convertedValue


# Receives limeObject,
# Returns a list of customers and total values won per customer
def get_list_of_values_won_pr_customer_last_year(lime_object_deals):
    global counter
    all_values_won = []

    # extract each data from the lime object, sort them in a tuple and add to list
    for deal in lime_object_deals:
        deal_status_key = deal['dealstatus']['key']
        company = deal['company']
        name = deal['name']
        value = deal['value']

        # When the deal was ended
        closed_date = deal['closeddate']

        # counts number of limetypes retrieved
        counter += 1

        # If company is null or empty string set value to '-Id missing-'
        if company == None or not company:
            company = "-Id missing-"

        # if the lime object deal was won and the deal was ended
        # last year then add customer,value and name of deal
        if is_agreement_last_year(closed_date, deal_status_key):
            customer = (company, value, name)
            all_values_won.append(customer)

    print('Number of deals retrieved: ', counter)
    counter = 0
    return all_values_won


# Receives limeObject
# Calculates and returns sum of total values for previous year
def get_total_values_won_last_year(lime_object_deals):
    list_of_values = get_list_of_all_won_deal_values_last_year(lime_object_deals)
    total = sum(list_of_values)
    return total


# Receives limeObject
# Returns a list of won deal values previous year.
def get_list_of_all_won_deal_values_last_year(lime_object_deals):
    won_deals = []

    for deal in lime_object_deals:
        dealstatus_key = deal['dealstatus']['key']
        deal_value = deal['value']

        # timestamp = deal['_timestamp'] #gives average value: 7880225
        # closeddate gives average value: 1479.

        '''Some dates are null even though the deal has values '''
        closed_date = deal['closeddate']

        if is_agreement_last_year(closed_date, dealstatus_key):
            won_deals.append(deal_value)

    return won_deals


# Receives limeObject.
# Calculates number of won deals pr month last year.
# Returns a dictionary with months and its values.
def get_list_of_won_deals_pr_month_last_year(lime_object_deals):
    deals_pr_month = {'january': 0, 'february': 0, 'march': 0, 'april': 0, 'may': 0, 'june': 0, 'july': 0, 'august': 0,
                      'september': 0, 'october': 0, 'november': 0, 'december': 0}
    for deal in lime_object_deals:
        dealstatus_key = deal['dealstatus']['key']
        closed_date = deal['closeddate']
        # timestamp = data['_timestamp']

        deal_year = 0
        deal_month = 0
        if closed_date != None:
            date_of_deal = datetime.fromisoformat(closed_date).date()
            deal_year = date_of_deal.year
            deal_month = date_of_deal.month

        # if a deal is won and the year of the deal is previous year, update deals for each month
        if dealstatus_key == 'agreement' and deal_year == last_year:
            if deal_month == 1:
                deals_pr_month['january'] += 1
            elif deal_month == 2:
                deals_pr_month['february'] += 1
            elif deal_month == 3:
                deals_pr_month['march'] += 1
            elif deal_month == 4:
                deals_pr_month['april'] += 1
            elif deal_month == 5:
                deals_pr_month['may'] += 1
            elif deal_month == 6:
                deals_pr_month['june'] += 1
            elif deal_month == 7:
                deals_pr_month['july'] += 1
            elif deal_month == 8:
                deals_pr_month['august'] += 1
            elif deal_month == 9:
                deals_pr_month['september'] += 1
            elif deal_month == 10:
                deals_pr_month['october'] += 1
            elif deal_month == 11:
                deals_pr_month['november'] += 1
            elif deal_month == 12:
                deals_pr_month['december'] += 1

    return deals_pr_month


# Receives a limeObject
# Returns average deal pr month
def get_average_number_of_won_deals_pr_month_last_year(lime_object_deals):
    deals_pr_month = get_list_of_won_deals_pr_month_last_year(lime_object_deals)

    total = get_total_number_of_won_deals_last_Year(lime_object_deals)
    length = len(deals_pr_month)
    average_pr_month = total / length

    return average_pr_month


# Receives a Deals limeObject
# Returns the total number of won deals  last year
def get_total_number_of_won_deals_last_Year(lime_object_deals):
    deals_pr_month_list = get_list_of_won_deals_pr_month_last_year(lime_object_deals)

    values = []
    for key, value in deals_pr_month_list.items():
        values.append(value)

    total = sum(values)

    return total


# Receives data closeddate and key from a lime_object 'deal'.
# Returns a boolean value true if lime_object deal is a won deal and if the deal is from last year.
def is_agreement_last_year(closed_date, deal_status_key):
    deal_year = get_deal_year(closed_date)
    return is_agreement(deal_status_key) and deal_year == last_year


# Receives data closeddate, deal_status:key from a lime_object 'deal'.
# Returns true if lime_object deal is a won deal and if the deal is before last year.
def is_agreement_in_past(closed_date, deal_status_key):
    deal_year = get_deal_year(closed_date)
    return is_agreement(deal_status_key) and deal_year < last_year


# Receives data closeddate, deal_status:key from a lime_object 'deal'.
# Returns true if lime_object deal is a won deal and if the deal is this year.
def is_agreement_this_year(closed_date, deal_status_key):
    deal_year = get_deal_year(closed_date)
    return is_agreement(deal_status_key) and deal_year == thisYear


def is_agreement(deal_status_key):
    return deal_status_key == 'agreement'


def get_deal_year(closed_date):
    global deal_year
    if isinstance(closed_date, str):
        date_object = datetime.fromisoformat(closed_date).date()
        deal_year = date_object.year
    return deal_year


# Receives
# Returns a list of status only of customers that HAS registered deals. If no deal is found,
# status will be set to -no deals found-
def get_updated_company_status(lime_object_deals, limeobject_customer_status_list):
    status_customer = "customer"
    status_not_found = "deal not found"
    status_inactive = 'inactive'
    status_prospect = "prospect"
    status_not_interested = 'notinterested'
    status_active = 'active'
    customer_status_list = limeobject_customer_status_list

    # extract each data we need from the 'Deal' lime_object and update them
    for deal in lime_object_deals:

        # 'status: key' is either agreement' or other
        deal_status_key = deal['dealstatus']['key']
        # assuming data 'company' is the name of the company
        company = deal['company']
        # date the deal was ended
        closed_date = deal['closeddate']

        print('agreement?: ', deal_status_key)
        print('company?: ', company)
        print('date?: ', closed_date)

        # if company is null or empty string
        if company is None or not company:
            company = 'deal missing id'

        # Some of the date values was None or not string.
        # if date is null or set as 'null' or not a string or empty string, set a date with year 1111
        # This will allow convertion of date in is_agreements. Might need to change if
        if not isinstance(closed_date, str) or closed_date is None or not closed_date or 'null':
            closed_date = '1111-02-22T00:00:00+01:00'
            print('Date was not a valid date and set to default date: ', closed_date)

        # if the lime object deal was won any date then set status as 'customer'
        if is_agreement(deal_status_key):
            customer_status_list[company] = status_customer

        # if company has bought something in past, but not last year set status to 'inactive'.
        # Note: spaces in parentheses must stay tis way, otherwise it will fail
        elif (
                not is_agreement_last_year(closed_date, deal_status_key)
                and not is_agreement_this_year(closed_date, deal_status_key)
                and is_agreement_in_past(closed_date, deal_status_key)
        ):
            customer_status_list[company] = status_inactive

        # If never bought anything set to status to "prospekt" unless it has buying status "notinterested"
        elif (
                is_agreement_last_year(closed_date, deal_status_key)
                and not is_agreement_in_past(closed_date, deal_status_key)
                and not is_agreement_this_year(closed_date, deal_status_key)
                and customer_status_list[company] is not status_not_interested
        ):
            customer_status_list[company] = status_prospect

    # Change existing status from previous fetched data from lime_object 'customer'
    # that does not match any deals to -deal not found- unless it is active.
    # If buying_status is 'active' set to customer.
    for company_name, buying_status in customer_status_list.items():
        if buying_status == status_active:
            customer_status_list[company_name] = status_customer
        # some registered buying status in lime_object 'Customer' was set to number such as '108001'
        # and are not associated to any company names in limeobject Deals. These statuses will be set to 'no deals found'
        # elif buying_status != status_active or buying_status != status_prospect or buying_status != status_customer or buying_status != status_not_interested:
        #     customer_status_list[company_name] = status_not_found

    return customer_status_list


def deal_exists(deal_name, company_list):
    for company_name, buying_status in company_list.items():
        return company_name == deal_name
