import httplib, urllib, os, json, sys

subscription_key = os.environ['AZURE_SUBSCRIPTION_KEY']
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

location = 'uksouth'
person_group_id = 'yt-faces-30-5'
container_name = 'yt-movies-frames'
person_to_identify_name = sys.argv[1]

yt_movies_person_frames_path = os.environ['YT_MOVIES_FRAMES_PATH'] + '/' + person_to_identify_name
yt_movies_person_frames = os.listdir(yt_movies_person_frames_path)

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true'
})

for person_frame in yt_movies_person_frames:
    # print('frame no ' + person_frame)

    # detect face
    try:
        conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params,
                     "{'url': 'https://mgrfaces.blob.core.windows.net/%s/%s/%s'}"
                     % (container_name, person_to_identify_name, person_frame),
                     headers)
        response = conn.getresponse()
        data = response.read()
        # print('%s detected with response ' % person_to_identify_name + data)
        data_dict = json.loads(data)
        face_id = data_dict[0]['faceId']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    # identify face
    try:
        conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/identify", "{"
                                                    "'personGroupId': '%s', "
                                                    "'faceIds': ['%s'], "
                                                    "}" % (person_group_id, face_id),
                     headers)
        response = conn.getresponse()
        data = response.read()
        # print('identify face response data ' + data)
        data_dict = json.loads(data)
        for candidate in range(0, len(data_dict[0]['candidates'])):
            candidate_person_id = data_dict[0]['candidates'][candidate]['personId']
            candidate_confidence = data_dict[0]['candidates'][candidate]['confidence']

            # get person name
            conn = httplib.HTTPSConnection(location + '.api.cognitive.microsoft.com')
            conn.request("GET", "/face/v1.0/persongroups/%s/persons/%s" % (person_group_id, candidate_person_id), "{}",
                         headers)
            response = conn.getresponse()
            data = response.read()
            data_dict = json.loads(data)
            candidate_person_name = data_dict['name']
            # print('candidate no ' + str(candidate) + ' was identified as ' + candidate_person_name
            #       + ' with confidence ' + str(candidate_confidence))
            print(person_frame + ' ' + str(candidate) + ' ' + candidate_person_name + ' ' + str(candidate_confidence))
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
