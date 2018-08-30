import httplib, json, os

subscription_key = os.environ['AZURE_SUBSCRIPTION_KEY']
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# person_group_id = 'yt-faces-30-5'
person_group_id = 'all-faces'
location = 'uksouth'

# people_name_collection = os.listdir(os.environ['FACES_COLLECTION_PATH'])
people_name_collection = os.listdir('C:\Users\gbt638\Documents\mgr\moto_real_faces\detected')

# create personGroup
try:
    conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/persongroups/%s" % person_group_id, "{'name':'%s'}" % person_group_id, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

for person_name in people_name_collection:
    # create person for personGroup
    try:
        conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/" + person_group_id + "/persons", "{'name': '%s'}" % person_name,
                     headers)
        response = conn.getresponse()
        data = response.read()
        print('%s created with response ' % person_name + data)
        data_dict = json.loads(data)
        person_id = data_dict['personId']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # add faces to person
    for picture_number in range(0, 5):
        try:
            conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/persongroups/" + person_group_id + "/persons/%s/persistedFaces" % person_id,
                         # "{'url': 'https://s3.amazonaws.com/yt-faces/%s/%s_%s_face.jpg'}"
                         "{'url': 'https://s3.amazonaws.com/gbt638-moto-real-faces/%s/%s_%s_face.jpg'}"
                         % (person_name, person_name, picture_number), headers)
            response = conn.getresponse()
            data = response.read()
            print('%s face no %s added with response ' % (person_name, picture_number) + data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    print('')
