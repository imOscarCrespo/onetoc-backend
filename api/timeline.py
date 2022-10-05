from typing import List
from django.http import JsonResponse
from datetime import datetime
from .models import Action
import boto3
class Timeline():
    def __init__(self, match_id: int, user: str, actions: List[Action]):
        self.match = match_id
        self.user = user
        self.actions = actions
    def generate(self):
        res = JsonResponse({'actions': list(self.actions)})
        s3 = boto3.resource('s3')
        s3_client = boto3.client('s3')
        now = datetime.now()
        expiration = 518400
        json_name = '%s %s %s %s %s %s' % (self.match, "_", self.user, "_", now, '.json')
        s3.Bucket('onetoc-timelines').put_object(Key=json_name, Body=res.content)
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'onetoc-timelines',
                                                            'Key': json_name},
                                                    ExpiresIn=expiration)
        return response