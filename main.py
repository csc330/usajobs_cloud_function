""" Microservice (Google Cloud Function) that retrieves jobs posted on the
    US Government Jobs site.  The function uses the search API,
    see https://developer.usajobs.gov/General.

    ***** REQUEST API KEY *****
    You must first request an API key by filling out this form:
        https://developer.usajobs.gov/APIRequest/Index
    ***************************

    Indicate that the application you're building is purely academic.
    You will receive an API key that you need to include in the code
    (in headers) and the email address that's associated with the API key.
"""

import requests
import json

class JobInfo:
    def __JobInfo__(title, URI, location):
        self.title = title
        self.URI = URI
        self.location = location

def search(request):
    """Search the Govt Jobs API (triggered by HTTP GET request)
    Args:
        city, state, keyword
    Returns:
        JSON object (list of dictionaries) of matching jobs: title, location, URI

    Examples of searching for jobs in DC with keyword "Python". Use the function URL
    provided by Google.

    Browser: https://CLOUD_FUNCTION_URL/?city=washington&state=DC&keyword=python

    From a terminal window using curl:
    curl -G -d 'city=Washington' -d 'state=DC' -d 'keyword=python' CLOUD_FUNCTION_URL
    """

    headers =   {'Host': 'data.usajobs.gov',
                'User-Agent': 'YOUR_EMAIL_ADDRESS',
                'Authorization-Key': 'YOUR_API_KEY'}

    API_URL = 'https://data.usajobs.gov/api/search'
    city_state = request.args['city'] + '%20' + request.args['state']
    keyword = request.args['keyword']

    full_URL = f'{API_URL}?LocationName={city_state}&Keyword={keyword}&ResultsPerPage=50'
    response = requests.get(full_URL, headers = headers)

    # Extract only title, location and URI and package as a list of JobInfo objects.
    response_json = response.json()
    job_results = []
    for item in response_json['SearchResult']['SearchResultItems']:
      job = JobInfo()
      job.URI = item['MatchedObjectDescriptor']['PositionURI']
      job.title = item['MatchedObjectDescriptor']['PositionTitle']
      job.location = item['MatchedObjectDescriptor']['PositionLocationDisplay']
      job_results.append(job)

    # Convert list of objects to list of dictionaries
    job_results_json = json.dumps([ob.__dict__ for ob in job_results])
    return job_results_json
