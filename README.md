# mgr
## Azure
### Steps to perform identification
1. Create PersonGroup
1. Create person for PersonGroup
1. Detect faces (it is done by Haar cascade - training images are already with detected faces)
1. Add face to person => in response there is unique personId received which can be returned when face is identified in final step
1. Train PersonGroup
1. Identify a face against a defined PersonGroup
	* Detect face to identify - received faceId is passed to identify API as argument
	* Identify face
	* Get candidate person name