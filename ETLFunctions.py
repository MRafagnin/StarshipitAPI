def StarshipitAPI(AccountName):
    
    '''
        Return Starshipit account API and Subscription key from CFG file
    '''

    import configparser

    config = configparser.ConfigParser()
    # Preserves case in ConfigParser
    config.optionxform = str
    # Reads config file
    config.read('StarshipitAPI.cfg')

    try:
        # Assignes value to variable via the config file
        StarShipIT_Api_Key        = config['StarshipitAPI'][AccountName].split("|")[0]
        Ocp_Apim_Subscription_Key = config['StarshipitAPI'][AccountName].split("|")[1]
    except:
        # Return 'None' to variable and message if incorrect value is provided
        StarShipIT_Api_Key        = None
        Ocp_Apim_Subscription_Key = None
        print("Incorrect 'Store' name!")
    
    return StarShipIT_Api_Key, Ocp_Apim_Subscription_Key

# ------------------------------------------------------------------
# ------------------------------------------------------------------
def CreateInputOrdersSet():
    
    '''
        Creates Set from input Order numbers
    '''

    OrderNoInput = input()
    OrderNoSet = set(OrderNoInput.split(' '))

    return OrderNoSet

# ------------------------------------------------------------------
# ------------------------------------------------------------------
def CFGFileKeyValuesToList():

    '''
        Creates a list from CFG file key values
    '''

    import configparser

    # Defines object
    config = configparser.ConfigParser()
    # Preserves case in ConfigParser
    config.optionxform = str
    # Reads config file
    config.read('StarshipitAPI.cfg')

    # Creates list from key values
    KeysList = list(config._sections['StarshipitAPI'].keys())

    return KeysList

# ------------------------------------------------------------------
# ------------------------------------------------------------------
def RetrieveStarshipitData(OrderNumber):

    '''
        - Iterates orders through Starshipit Accounts to find data
        - Retrieve order data from Starshipit by order number
        - Updates ['sender_details']['company'] with Account Name
    '''

    import http.client, urllib.request, urllib.parse, urllib.error, base64
    import json

    # Creates list from CFG file key values
    StarshipitAccounts = CFGFileKeyValuesToList()

    for AccountName in StarshipitAccounts:

        # Request parameters
        params = urllib.parse.urlencode({
                                        'order_number': OrderNumber,
                                        })


        # Retrieve Starshipit account API keys from CFG file
        StarShipIT_Api_Key, Ocp_Apim_Subscription_Key = StarshipitAPI(AccountName)

        # Request headers
        headers = {
            'StarShipIT-Api-Key': StarShipIT_Api_Key,
            'Ocp-Apim-Subscription-Key': Ocp_Apim_Subscription_Key,
        }

        conn = http.client.HTTPSConnection('api.starshipit.com')
        conn.request("GET", "/api/orders?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        StarshipitOrderData = json.loads(data.decode('utf-8'))

        if StarshipitOrderData['success'] == True:

            StarshipitOrderData['order']['sender_details']['company'] = AccountName

            break
    
    return StarshipitOrderData

# ------------------------------------------------------------------
# ------------------------------------------------------------------
def CreateStarshipitOrderDict(OrderNoSet):
    
    '''
        - Loop through OrderNo Set
        - Retrieve Order data from Starshipit
        - Adds data to dictionary 
    '''

    from progressbar import ProgressBar

    pbar = ProgressBar()

    StarshipitOrderDict = {}

    for OrderNumber in pbar(OrderNoSet):

        # Retrieve order data from Starshipit
        StarshipitOrderData = RetrieveStarshipitData(OrderNumber)

        # Adds data to dictionary
        StarshipitOrderDict[OrderNumber] = StarshipitOrderData
    
    return StarshipitOrderDict

# ------------------------------------------------------------------
# ------------------------------------------------------------------