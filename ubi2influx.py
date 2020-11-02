import urllib
from jsonpath_ng import jsonpath, parse
import influxdb
import json

channel_id = "20002"
acc_key = ""
response = urllib.urlopen(f"https://api.ubibot.com/channels/{channel_id}/feeds.json?parameters&account_key={acc_key}")
d = json.loads(response.read())
if parse('$.result').find(d) != 'success':
	print('result fail')

expr = parse('$.feeds[*]')
points = []
for feed in [match.value for match in expr.find(d)]:
  feed.pop('wifi')
  body = {}
  body['measurement'] = ubibot
  body['tags'] = {'channel': channel_id}
  body['time'] = feed.pop('created_at')
  body['fields'] = feed
  points.append(body)

client = InfluxDBClient(influxhost, 8086, 'ubibot', 'ubibot', 'ubibot')
client.create_database('ubibot')
client.write_points(points)