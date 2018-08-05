import httplib, json, os, time

subscription_key = os.environ['AZURE_SUBSCRIPTION_KEY']
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

person_group_id = 'test4'
location = 'westcentralus'

people_name_collection = os.listdir(os.environ['FACES_COLLECTION_PATH'])

for person_name in people_name_collection:
    # create person for personGroup
    try:
        conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/" + person_group_id + "/persons", "{'name': '%s'}" % person_name,
                     headers)
        time.sleep(3)
        response = conn.getresponse()
        time.sleep(3)
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
                         "{'url': 'https://s3.amazonaws.com/yt-faces/%s/%s_%s_face.jpg'}"
                         % (person_name, person_name, picture_number), headers)
            response = conn.getresponse()
            data = response.read()
            print('%s face no %s added with response ' % (person_name, picture_number) + data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
