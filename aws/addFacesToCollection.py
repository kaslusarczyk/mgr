# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import os
import boto3

bucket = 'gbt638-yt-faces'
collectionId = 'YouTubeFaces'

people_name_collection = os.listdir(os.environ['FACES_COLLECTION_PATH'])

client = boto3.client('rekognition')

for person_name in people_name_collection:
    # index faces
    for picture_number in range(0, 5):
        response = client.index_faces(CollectionId=collectionId,
                                      Image={
                                          'S3Object': {
                                              'Bucket': bucket,
                                              'Name': person_name + '/' + person_name + '_' + str(
                                                  picture_number) + '_face.jpg'
                                          }
                                      },
                                      ExternalImageId=person_name,
                                      DetectionAttributes=['ALL'])

        print ('Faces in ' + person_name + ' ' + str(picture_number))
        for faceRecord in response['FaceRecords']:
            print (faceRecord['Face']['FaceId'])
    print('')
