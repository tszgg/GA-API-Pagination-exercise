"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv
from csv import writer

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'momask-6be88e849be7.json'
VIEW_ID = '211112931'

#countrylist = []
#sessionlist = []


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


def get_report (analytics, pgtoken):
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
          'pageToken': pgtoken,
          'pageSize': "1",
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
  clist = []
  slist = []
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        #print (header + ': ' + dimension)
        clist.append(dimension)

      for i, values in enumerate(dateRangeValues):
        #print ('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          #print( metricHeader.get('name') + ': ' + value)
          slist.append(value)
    return clist,slist


def main():
  pgtoken = "0"
  newdict={}
  #countrylist = []
  #sessionlist = []

  while pgtoken is not None:
    print(pgtoken)
    analytics = initialize_analyticsreporting()
    response = get_report(analytics,pgtoken)
    c, s = print_response(response)
    # append to CSV
    print(c, s)


    store_response =(zip(c, s))
    #store_response[pgtoken] = newdict
    print(store_response)

    with open('pagination.csv', 'a', newline='') as myfile:
      writer = csv.writer(myfile)
      writer.writerows(store_response)

    pgtoken = response['reports'][0].get('nextPageToken')  # update the pageToken
    #get_report['reportRequests'][0]['pageToken'] = pgtoken  # update the query






if __name__ == '__main__':
      main()


#newdict=dict(zip(countrylist, sessionslist))
#print(newdict)


#import csv
#test=zip(countrylist, sessionslist)
#myfile= open('api.csv', 'w', newline='')
#with myfile:
#  writer = csv.writer(myfile)
#  writer.writerows(test)





#mydict = {key1: value_a, key2: value_b, key3: value_c}
#with open('dict.csv', 'w', newline="") as csv_file:
 #   writer = csv.writer(csv_file)
  #  for key, value in mydict.items():
   #   writer.writerow([key, value])


