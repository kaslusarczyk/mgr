# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import sys

import boto3

movies_bucket = 'gbt638-yt-movies'
collectionId = 'YouTubeFaces'
person_name = sys.argv[1]

client = boto3.client('rekognition')

# start face search
response = client.start_face_search(CollectionId=collectionId,
                                    Video={
                                        'S3Object': {
                                            'Bucket': movies_bucket,
                                            'Name': person_name + '.mp4'
                                         }
                                    },
                                    FaceMatchThreshold=10)

print (person_name + ' ' + response['JobId'])
