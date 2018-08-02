import httplib, urllib, base64, json, os

subscription_key = os.environ['AZURE_SUBSCRIPTION_KEY']
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

person_name = 'cate_blanchett'

# create person for personGroup
try:
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/test-person-group/persons", "{'name': '%s'}" % person_name, headers)
    response = conn.getresponse()
    data = response.read()
    print('%s created with response' % person_name + data)
    data_dict = json.loads(data)
    person_id = data_dict['personId']
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# print(person_id)

# add faces to person
for picture_number in range(0, 5):
    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/test-person-group/persons/%s/persistedFaces" % person_id,
                     "{'url': 'https://s3.amazonaws.com/yt-faces/%s/%s_%s_face.jpg'}"
                     % (person_name, person_name, picture_number), headers)
        response = conn.getresponse()
        data = response.read()
        print('%s face no %s added with response ' % (person_name, picture_number) + data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
