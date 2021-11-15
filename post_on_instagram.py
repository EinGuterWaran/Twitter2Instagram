import requests
import config
import json


def postInstagramQuote():
#Post the Image
    image_location_1 = 'http:path-to-your-image.com/img/image-name.jpg'
    post_url = 'https://graph.facebook.com/v10.0/{}/media'.format(config.ig_user_id)
    payload = {
        'image_url': image_location_1,
        'caption': 'Get jobs online on https://careers-portal.co.za #career #hiring #jobs #job #jobssouthafrica #hiringnow',
        'access_token': config.user_access_token
        }
    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result:
        creation_id = result['id']
        second_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format(config.ig_user_id)
        second_payload = {
                'creation_id': creation_id,
                'access_token': config.user_access_token
                }
        r = requests.post(second_url, data=second_payload)
        print('--------Just posted to instagram--------')
        print(r.text)
    else:
        print('HOUSTON we have a problem')
postInstagramQuote()
