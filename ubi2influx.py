import urllib.request
from jsonpath_ng import jsonpath, parse
import influxdb
import json
import time
import datetime

#channel_id = "20002"
channels = ["20002", "20003", "20004", "20005", "20006", "20007", "20008", "20009", "20010", "20321", "18378"]
acc_key = "f90c94103d04abedaad2edebc38a3662"
olddate = datetime.datetime.strftime(datetime.datetime.utcnow()-datetime.timedelta(3), "%Y-%m-%d")
oldtime = datetime.datetime.strftime(datetime.datetime.utcnow()-datetime.timedelta(3), "%H:%M:%S")

for channel_id in channels:
  response = urllib.request.urlopen(f"https://api.ubibot.com/channels/{channel_id}/feeds.json?parameters&account_key={acc_key}&start={olddate}%20{oldtime}")
  d = json.loads(response.read())
  if parse('$.result').find(d) != 'success':
    print('result fail')
  
  expr = parse('$.feeds[*]')
  points = []
  for feed in [match.value for match in expr.find(d)]:
    if 'wifi' in feed:
      feed.pop('wifi')
    body = {}
    body['measurement'] = 'ubibot'
    body['tags'] = {'channel': channel_id}
    body['time'] = feed.pop('created_at')
    for bit in feed:
      feed[bit] = float(feed[bit])
    body['fields'] = feed
    if len(body['fields']) > 0:
      points.append(body)

  client = influxdb.InfluxDBClient('niflheim', 8086, 'telegraf', 'campari', 'ubibot')
  client.create_database('ubibot')
  try:
    client.write_points(points)
  except:
    print('error')
  time.sleep(1)

#for point in points:
#  print(point)
#  client.write_points([point,])
