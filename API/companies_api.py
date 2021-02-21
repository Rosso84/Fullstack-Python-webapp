# Receives a company limeobject
# Return a list of company names and its status
def get_all_current_company_status_list(lime_object_company):
    status_list = {}

    for data in lime_object_company:
        company_name = data['name']
        buyingstatus = data['buyingstatus']['key']

        status_list[company_name] = buyingstatus

    # for k, v in status_list.items():
    #     print('****** current status: ', k, v)

    return status_list