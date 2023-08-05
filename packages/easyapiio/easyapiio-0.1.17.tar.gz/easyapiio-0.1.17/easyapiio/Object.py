import json
import requests

class Object:
    def __init__(self, apiKey, appId):
        self.apiKey = apiKey
        self.appId = appId


    def getAPIKey(self):
        return self.apiKey

    def getAppId(self):
        return self.appId

    # Create
    # args:
    # 1. data
    # 2. isPublic
    # 3. type
    # 4. replaceId
    # 5. path
    def create(self, *args):
        if (len(args) == 0):
            return { 'success': False, 'message': 'Error: Invalid parameters' }
        data = args[0]

        isPublic = False
        if (len(args) >= 2):
            isPublic = args[1]

        typeStr = ''
        if (len(args) >= 3):
            typeStr = args[2]

        path = ''
        if (len(args) >= 4):
            path = args[3]

        replaceId = ''
        if (len(args) >= 5):
            replaceId = args[4]

        headers = { 'Content-type': 'application/json', 'Authorization': self.apiKey }
        post_fields = {
            'app': self.appId,
            'object': json.dumps(data),
            'isPublic': isPublic,
            'type': typeStr,
            'replaceId': replaceId,
            'path': path
        }
        result = requests.post(('https://easyapi.io/api/v1/objects/create'), data=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.', 'result': result }

    # Delete
    def delete(self, objectId):
        headers = { 'Content-type': 'application/json', 'Authorization': self.apiKey }
        post_fields = { 'app': self.appId, 'objectId': objectId }
        result = requests.post(('https://easyapi.io/api/v1/objects/delete'), data=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }

    # Get
    def get(self, objectId):
        headers = { 'Content-type': 'application/json', 'Authorization': self.apiKey }
        post_fields = { 'app': self.appId, 'objectId': objectId }
        result = requests.post(('https://easyapi.io/api/v1/objects/search'), data=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }
    # List
    def list(self):
        headers = { 'Content-type': 'application/json', 'Authorization': self.apiKey }
        post_fields = { 'app': self.appId }
        result = requests.post(('https://easyapi.io/api/v1/objects/list'), data=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }

    # Search
    def search(self, keyValues):
        headers = { 'Content-type': 'application/json', 'Authorization': self.apiKey }
        post_fields = { 'app': self.appId, 'keyValues': keyValues }
        result = requests.post(('https://easyapi.io/api/v1/objects/search'), data=post_fields, headers=headers)
        if (result.status_code == 200):
            return result.json()
        else:
            return { 'statusCode': result.status_code, 'success': False, 'message': 'Status error.' }
