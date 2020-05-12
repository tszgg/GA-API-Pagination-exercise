"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'momask-6be88e849be7.json'
VIEW_ID = '211112931'

countrylist=[]
sessionslist=[]
newdict={}

pageTokenVariable="whatever"

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          #"pageToken": pageTokenVariable,
          #'pageSize': 2,
          'dateRanges': [{'startDate': '90daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        #print (header + ': ' + dimension)
        countrylist.append(dimension)

      for i, values in enumerate(dateRangeValues):
        #print ('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          #print( metricHeader.get('name') + ': ' + value)
          sessionslist.append(value)






def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()

newdict=dict(zip(countrylist, sessionslist))
print(newdict)


#import csv
test=zip(countrylist, sessionslist)
myfile= open('api.csv', 'w', newline='')
with myfile:
  writer = csv.writer(myfile)
  writer.writerows(test)


print(test)
#https://stackoverflow.com/questions/31587784/python-list-write-to-csv-without-the-square-brackets




