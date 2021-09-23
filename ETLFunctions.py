def StarshipitAPI(sectionName):
    
    """
        Return Starshipit account API and Subscription key from CFG file
    """

    import configparser

    config = configparser.ConfigParser()
    # Preserves case in ConfigParser
    config.optionxform = str
    # Reads config file
    config.read('StarshipitAPI.cfg')

    try:
        # Assignes value to variable via the config file
        StarShipIT_Api_Key        = config[sectionName]['apiKey']
        Ocp_Apim_Subscription_Key = config[sectionName]['subsKey']
    except:
        # Return 'None' to variable and message if incorrect value is provided
        StarShipIT_Api_Key        = None
        Ocp_Apim_Subscription_Key = None
        print("Incorrect 'Store' name!")
    
    return StarShipIT_Api_Key, Ocp_Apim_Subscription_Key

# ----------------------------------------------------------------
# ----------------------------------------------------------------
def CFGFileSectionNameToList():

    """
        Creates a list from CFG file section names
    """

    import configparser
    import os
        
    # Set directory to access 'StarshipitAPI.cfg'
    os.chdir('/content/gdrive/My Drive/PROJECTS/Colab_Notebooks/Unleashed SO Posting/2nd Stage - ETL/')

    # Defines object
    config = configparser.ConfigParser()
    # Preserves case in ConfigParser
    config.optionxform = str
    # Reads config file
    config.read('StarshipitAPI.cfg')

    # Creates list from section names
    sectionsList = config.sections()

    return sectionsList

# ----------------------------------------------------------------
# ----------------------------------------------------------------
def ConfirmsStarshipitAccount(orderNumber):

    """
        Confirms Starshipit account by order number

        Return: Starshipit Account Name
    """

    import http.client, urllib.request, urllib.parse, urllib.error, base64
    import json

    # Creates list from CFG file key values
    StarshipitAccounts = CFGFileSectionNameToList()

    for AccountName in StarshipitAccounts:

        # Request parameters
        params = urllib.parse.urlencode({
                                        'order_number': orderNumber,
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

            break
    
    return AccountName
