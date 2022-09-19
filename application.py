from flask import Flask, request
import requests
from yelp.client import Client

YELP_BUSINESS_SEARCH = "https://api.yelp.com/v3/businesses/search"
YELP_BUSINESS_DETAIL = "https://api.yelp.com/v3/businesses/"
YELP_API_KEY = "qJ6RmBo3IqhUb085M9zWHCtC1eAWFhuQzr0l6WMqf8KhRiOCx3CejA8iG3UGGY6bmW26wCOILcDaIGN6t6HvNGSYwm5HO2ir775HWiplpquxb_YL2RQXuPuu6MseY3Yx"
MILE_TO_METER_FACTOR = 1609.344

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/')
def root():
    return application.send_static_file('business.html')


@application.route('/search')
def search():
    # get search params from web
    print(request.url)
    keyword = request.args.get("keyword")
    distance = request.args.get("distance")
    category = request.args.get("category")
    # location = request.args.get("location", "")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    print(keyword, distance, category, latitude, longitude)
    if category == "default":
        category = "all"
    radius = float(distance) * MILE_TO_METER_FACTOR

    # send request to yelp business search
    search_params = {"term": keyword, "latitude": float(latitude), "longitude": float(longitude),
                     "categories": category, "radius": int(radius)}
    req_search = requests.get(url=YELP_BUSINESS_SEARCH, params=search_params,
                              headers={"Authorization": "Bearer " + YELP_API_KEY})
    # print(req_search.url)
    # if req_search.status_code == 200:
    #     print(req_search.text)
    # return json
    return req_search.text

@application.route('/detail')
def detail():
    # print(request.url)
    business_id = request.args.get("id")
    # print(business_id)
    req_detail = requests.get(url=YELP_BUSINESS_DETAIL+business_id,
                              headers={"Authorization": "Bearer " + YELP_API_KEY})
    # print(req_detail.url)
    # if req_detail.status_code == 200:
    #     print(req_detail.text)
    return req_detail.text


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
