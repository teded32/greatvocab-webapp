import boto3
from flask import Flask, render_template
import datetime
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)


ACCESS_ID = "id"
ACCESS_KEY = "key"

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

	for row in r2['Items']:
		word_list.append(row['Word'])

		unixtime = float(row['LastSeen'])

		lastseen = datetime.datetime.fromtimestamp(unixtime).strftime('%m-%d-%Y %H:%M')

		detail = [row['Word'], int(row['WStatus']),lastseen]

		if detail == "0":
			word_details.append("Not Seen")
		elif detail == "1":
			word_details.append("In Review")
		else:
			word_details.append("Learned")

	return word_details



@app.route("/table")
def template_test():
	word_dets = get_word_details()
	return render_template('ed_template.html', word_details=word_dets)


