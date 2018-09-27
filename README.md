# RIAlert
# Alert expiring AWS Reserved Instances

RIAlert will alert expiring RIs.

User can set multiple "expiring days after" by environment variable.
This function publish a SNS Topic when there are some expiring RIs.
You can get SNS Notification.

## Environment Variable

expireDaysAfter:
  0,1,2,3,4,5,6 (in a week)
  7,30,60 (one week, one month and two month before expiring)

SNSSubject: Expiring Reserved Instances (your favaorite subject)

SNSTopcArc: arn:aws:sns:ap-northeast-1:123456789012:MailToMe

## Requirements

This function required describe reserved instances and SNS publish.
See a sample policy. (RIAlertPolicy.json)

## Usage

- Create Policy
- Create Role
- Create Lambda function with three Environment Variable aboce
- You can call this lambda function periodically via CloudWatch Event
cron or rate configuration.
