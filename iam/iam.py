import boto3
import json
from datetime import datetime


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



class IamPolicy:
    def __init__(self):
        self.iam = boto3.client('iam')

    def get_policy(self, policy_name):
        response = self.iam.get_policy(
            PolicyArn=f'arn:aws:iam::aws:policy/{policy_name}'
        )
        return response['Policy']

    def attach_policy(self, policy_name, role):
        self.iam.attach_role_policy(
            PolicyArn=f'arn:aws:iam::aws:policy/{policy_name}',
            RoleName=role
        )

    def attach_policy(self, policy_name, role):
        self.iam.detach_role_policy(
            PolicyArn=f'arn:aws:iam::aws:policy/{policy_name}',
            RoleName=role
        )

    def create_policy(self, statements, policy_name):
        #the below one is how the statement is supposed to look like
        # [{
        #     "Effect": "Allow",
        #     "Action": [
        #         "dynamodb:DeleteItem",
        #         "dynamodb:GetItem",
        #         "dynamodb:PutItem",
        #         "dynamodb:Scan",
        #         "dynamodb:UpdateItem"
        #     ],
        #     "Resource": resource_arn}]
        my_managed_policy = {
            "Version": datetime.now().strftime('%Y-%m-%d'),
            "Statement": statements
        }
        response = self.iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(my_managed_policy)
        )
        return response

