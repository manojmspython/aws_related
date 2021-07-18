import boto3
from pprint import pprint


class IamUser:
    def __init__(self):
        self.iam = boto3.client('iam')

    def create_user(self, user_name):
        try:
            response = self.iam.create_user(
                UserName=user_name
            )
            return response
        except self.iam.exceptions.EntityAlreadyExistsException:
            print('user already present')

    def list_users(self):
        all_users = []
        paginator = self.iam.get_paginator('list_users')
        for response in paginator.paginate():
            all_users.append(response)
        return all_users

    def delete_user(self, user_name):
        try:
            self.iam.delete_user(
                UserName=user_name
            )
        except self.iam.exceptions.NoSuchEntityException:
            print('user doesnt exist')



