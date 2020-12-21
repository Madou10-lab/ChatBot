import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    #luis app conf
    LUIS_APP_ID = "2456bc47-88f2-4a9f-b2cc-4ca2d231a4b9"
    LUIS_API_KEY = "e778cc83929742e0a11001957d34ac3b"
    LUIS_API_HOST_NAME = "https://westus.api.cognitive.microsoft.com/"

    """ Graph Configuration """

    CLIENT_ID = '9b56e5eb-fdf5-44b4-9238-94da18cd38fb'
    CLIENT_SECRET = '670hh~iNB3T-O.T10UY4pjn8o7O3E1P5-w'
    REDIRECT_URI = 'http://localhost:5000/login/authorized'
    URL2 = 'https://login.microsoftonline.com/dafe3bd2-65e2-45b1-aaf2-061bd801564a/oauth2/token'
    #Account parms to get SharePoint data
    MAIL = 'jouiniahmed66@gmail.com'
    PASS = 'RT42020'
    # AUTHORITY_URL ending determines type of account that can be authenticated:
    AUTHORITY_URL = 'https://login.microsoftonline.com/common'
    AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
    TOKEN_ENDPOINT = '/oauth2/v2.0/token'
    RESOURCE = 'https://graph.microsoft.com/'
    API_VERSION = 'v1.0'
    SCOPES = ['User.Read'] # Add other scopes/permissions as needed.
    SITE_ID = 'e704b448-5a15-4366-994b-ebebc681662d'
    PRODUCT_URL = "https://tutcamp/sites/library/SitePages/view.aspx?product="
