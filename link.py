from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
import json

# from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication, PERMISSIONS)


CLIENT_ID = '78g6r3uc6qymtt'
CLIENT_SECRET = 'kEvy5XZy8rvjL93e'
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
    # email = linkedin.get("https://api.linkedin.com/v1/people/~/email-address/?format=json
    info = linkedin.get("https://api.linkedin.com/v1/people/~:(id,email-address,first-name,last-name,industry,positions,summary,headline,location)/?format=json")
    infoJson = json.loads(info.content)
    # print email.content
    print info.content
    # json schema for json resume
    data = {
    "basics": {
    "name": "",
    "label": "",
    "picture": "",
    "email": "",
    "phone": "",
    "website": "",
    "summary": "",
    "location": {
    "address": "",
    "postalCode": "",
    "city": "",
    "countryCode": "",
    "region": ""
    },
    "profiles": []
    },
    "work": [],
    "volunteer": [],
    "education": [],
    "awards": [],
    "publications": [],
    "skills": [],
    "languages": [],
    "interests": [],
    "references": []
    }
    data["basics"]["email"] = infoJson["emailAddress"]
    data["basics"]["name"] = infoJson["firstName"] + " " + infoJson["lastName"]
    data["basics"]["location"] = infoJson["location"]["name"]
    data["basics"]["countryCode"] = infoJson["location"]["country"]["code"]
    if "summary" in infoJson:
        data["basics"]["summary"] = infoJson["summary"]
        data["basics"]["label"] = infoJson["headline"]
    if infoJson["positions"]["_total"]>0:
        data["work"] = [
        {
        "company": infoJson["positions"]["values"][0]["company"]["name"],
        "position": infoJson["positions"]["values"][0]["title"],
        "website": "",
        "startDate": str(infoJson["positions"]["values"][0]["startDate"]["month"]) + "/" + str(infoJson["positions"]["values"][0]["startDate"]["year"]),
        "endDate": "present",
        "summary": infoJson["positions"]["values"][0]["summary"],
        "highlights": []
        }]
        if(not infoJson["positions"]["values"][0]["isCurrent"]):
            data["work"]["endDate"] = str(infoJson["positions"]["values"][0]["endDate"]["month"]) + "/" + str(infoJson["positions"]["values"][0]["endDate"]["year"])
    print str(data)
