import boto3
import json
import datetime
import os

def lambda_handler(event, context):

    ec2 = boto3.client("ec2")
    RIs = ec2.describe_reserved_instances()["ReservedInstances"]

    # test dummy data
    RIs.append(
      {
        "End": datetime.datetime(2018, 10, 1, 9, 0, 0, tzinfo=datetime.timezone.utc),
        "ReservedInstancesId": "01234567-abcd-efgh-ijkl-mn0123456789"
      }
    )

    expiringRIs = []
    
        indays = [x.strip() for x in os.environ["expireDaysAfter"].split(",")]
    for inday in indays:
        currentTime = datetime.datetime.now(datetime.timezone.utc)
        checkDate = currentTime + datetime.timedelta(days =+ int(inday))

        for RI in RIs:
            if checkDate <= RI["End"] <= checkDate + datetime.timedelta(days =+ 1):
                expiringRIs.append(RI)

    if expiringRIs:
        snsMessage = "End, ReservedInstancesId\n"
        for expiringRI in expiringRIs:
            End = expiringRI["End"].isoformat()
            ReservedInstancesId = expiringRI["ReservedInstancesId"]

            snsMessage = snsMessage + End + "," + ReservedInstancesId + "\n"
        print("snsMessage:", snsMessage)

        sns = boto3.client("sns")
        response = sns.publish(
            TopicArn = os.environ["SNSTopicArn"],
            Subject = os.environ["SNSSubject"],
            #Message = json.dumps(expiringRIs, default=json_serial)
            Message = snsMessage
        )

    return {
        "statusCode": 200,
        "body": json.dumps(expiringRIs, default=json_serial)
    }

def json_serial(obj):
    if isinstance(obj, (datetime.datetime)):
        return obj.isoformat()
    raise TypeError ("TypeError")

# This main block isn't used in AWS Lambda function.
if __name__ == '__main__':
    event = {}
    context = {}

    os.environ["expireDaysAfter"] = "0, 1, 2, 3, 4, 5"
    os.environ["SNSTopicArn"] = "arn:aws:sns:<Region>:<AccountId>:<Topic>"
    os.environ["SNSSubject"] = "Expiring Reserved instances"

    print(lambda_handler(event, context))
