from datetime import *
from API import companies_api

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
    global deal_year
    if isinstance(closed_date, str):
        date_object = datetime.fromisoformat(closed_date).date()
        deal_year = date_object.year
        print('from is_agreement_last_year inside if statement:', deal_year)

    return deal_status_key == 'agreement' and deal_year == last_year


# Receives data closeddate, deal_status:key from a lime_object 'deal'.
# Returns true if lime_object deal is a won deal and if the deal is before last year.
def is_agreement_in_past(closed_date, deal_status_key):
    deal_year = None
    if closed_date is not None or not closed_date:
        date_object = datetime.fromisoformat(closed_date).date()
        deal_year = date_object.year
        print('from is_agreement_in_past: ', deal_year)

    return deal_status_key == 'agreement' and deal_year < last_year


# Receives data closeddate, deal_status:key from a lime_object 'deal'.
# Returns true if lime_object deal is a won deal and if the deal is this year.
def is_agreement_this_year(closed_date, deal_status_key):
    global deal_year
    if closed_date is not None or not closed_date:
        date_object = datetime.fromisoformat(closed_date).date()
        deal_year = date_object.year
        print('from is_agreement_this_year: ', deal_year)
    return deal_status_key == 'agreement' and deal_year == thisYear


#
# def get_deal_year(deal_date):
#     # Convert date and extract year
#     deal_year = 0
#     if deal_date == None or not deal_date:
#         date_object = datetime.fromisoformat(deal_date.date())
#         deal_year = date_object.year
#         print('from get_dealYear: ', deal_year)
#     return deal_year


def get_updated_company_status(lime_object_deals, current_status_list):
    status_list = current_status_list

    # extract each data from the lime object
    for deal in lime_object_deals:
        deal_status_key = deal['dealstatus']['key']  # 'agreement'
        company = deal['company']
        value = deal['value']
        closed_date = deal['closeddate']  # When the deal was ended

        # If company is null or empty string set value to '-Id missing-'
        # if company == None or not company:
        #     company = "-Id missing-"

        # if the lime object deal was won any date then set status as 'customer'
        if deal_status_key == 'agreement':
            status = "Customer"
            status_list[company] = status
            return

        # if company has bought something in past, but not last year set status to 'inactive'
        elif not is_agreement_last_year(closed_date, deal_status_key) and is_agreement_in_past(closed_date,
                                                                                               deal_status_key):
            status = 'inactive'
            status_list[company] = status

        # If never bought anything set to status to "prospekt" unless it has buying status "notinterested"
        elif (
                not is_agreement_last_year(closed_date, deal_status_key) == False
                and is_agreement_in_past(closed_date, deal_status_key) == False
                and is_agreement_this_year(closed_date, deal_status_key) == False
                and status_list[company] is not 'notinterested'
        ):
            status = "prospekt"
            status_list[company] = status

    return status_list
