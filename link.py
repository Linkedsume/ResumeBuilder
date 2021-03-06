from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
import json
import keys
# from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication, PERMISSIONS)


CLIENT_ID = keys.CLIENT_ID
CLIENT_SECRET = keys.SECRET
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'
RETURN_URL = 'https://localhost:5000/'


if __name__ == '__main__':
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=RETURN_URL)
    linkedin = linkedin_compliance_fix(linkedin)
    authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
    print 'Please go here and authorize,', authorization_url
    redirect_response = raw_input('Paste the full redirect URL here:')
    linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=redirect_response)
    info = linkedin.get("https://api.linkedin.com/v1/people/~:(id,email-address,first-name,last-name,industry,positions,summary,headline,location)/?format=json")
    infoJson = json.loads(info.content)
    file = open('resume.json','w+')
    file.write(info.content)
    file.close()



def author():
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=RETURN_URL)
    linkedin = linkedin_compliance_fix(linkedin)
    authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
    return authorization_url

def make_json(redirect_response):
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=RETURN_URL)
    linkedin = linkedin_compliance_fix(linkedin)
    linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=redirect_response)
    info = linkedin.get("https://api.linkedin.com/v1/people/~:(id,email-address,first-name,last-name,industry,positions,summary,headline,location)/?format=json")
    infoJson = json.loads(info.content)
    file = open('resume.json','w+')
    file.write(info.content)
    file.close()
