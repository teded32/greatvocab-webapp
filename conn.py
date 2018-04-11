import boto3
from flask import Flask, render_template
import datetime
from boto3.dynamodb.conditions import Key, Attr

from creds import aws_key
from creds import aws_id

app = Flask(__name__)

ACCESS_ID = aws_id
ACCESS_KEY = aws_key

dynamodb = boto3.resource('dynamodb', 
		region_name='us-east-1', 
		aws_access_key_id=ACCESS_ID,
        aws_secret_access_key=ACCESS_KEY)


def get_word_details():
	words_table = dynamodb.Table('Words')
	wordstatus_table = dynamodb.Table('WordStatus')

	r2 = wordstatus_table.scan()

	word_list = []
	word_details = []

	statuses = {0:"Not Learned",1:"In Review", 2:"Learned"}
	nums = {"Not Learned":0 ,"In Review":1, "Learned":2}

	for row in r2['Items']:
		word_list.append(row['Word'])

		unixtime = float(row['LastSeen'])
		if unixtime < 315532800:
			lastseen = "-"
		else:
			lastseen = datetime.datetime.fromtimestamp(unixtime).strftime('%m-%d-%Y %H:%M')

		status_num =int(row['WStatus'])
		word_status = statuses[status_num]

		detail = [row['Word'], word_status,lastseen]

		word_details.append(detail)

	word_details.sort(key = lambda x: x[0])
	word_details.sort(key = lambda x: nums[x[1]], reverse=True)

	return word_details



@app.route("/table")
def template_test():
	word_dets = get_word_details()
	return render_template('ed_template.html', word_details=word_dets)


