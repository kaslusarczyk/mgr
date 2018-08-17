# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import sys

client = boto3.client('rekognition')

paginationToken = ''

finished = False
jobId = sys.argv[1]

print('Timestamp ExternalImageId Similarity')
while finished == False:
    # get face search
    response = client.get_face_search(JobId=jobId,
                                      NextToken=paginationToken)

    print('JobStatus: ' + response['JobStatus'])

    for personMatch in response['Persons']:
        if 'FaceMatches' in personMatch:
            for faceMatch in personMatch['FaceMatches']:
                print(str(personMatch['Timestamp']) + ' '
                      + faceMatch['Face']['ExternalImageId'] + ' '
                      + str(faceMatch['Similarity']))
        else:
            print(str(personMatch['Timestamp']))
    if 'NextToken' in response:
        paginationToken = response['NextToken']
    else:
        finished = True
