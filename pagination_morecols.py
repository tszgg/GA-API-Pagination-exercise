"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv
from csv import writer

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'venv/Scripts/momask-6be88e849be7.json'
VIEW_ID = '211112931'


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


def get_report(analytics, pgtoken):
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
                    'pageSize': "2",
                    'dateRanges': [{'startDate': '90daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:users'},
                                {'expression': 'ga:percentNewSessions'}],
                    'dimensions': [{'name': 'ga:userType'},
                                   {'name': 'ga:sessionCount'},
                                   {'name': 'ga:daysSinceLastSession'},
                                   {'name': 'ga:userDefinedValue'},
                                   {'name': 'ga:userBucket'}]

                }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    headerlist = []
    cdict = {}
    sdict = {}

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                # print (header + ': ' + dimension)
                cdict.setdefault(header, []).append(dimension)
                if header not in headerlist:
                    headerlist.append(header)
                # cdict[header]=dimension
                # print(cdict)

            for i, values in enumerate(dateRangeValues):
                # print ('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    # print( metricHeader.get('name') + ': ' + value)
                    #slist.append(value)
                    sdict.setdefault(metricHeader.get('name'), []).append(dimension)
                    if (metricHeader.get('name')) not in headerlist:
                        headerlist.append(metricHeader.get('name'))
                    # sdict[metricHeader]=value
                    # print(slist)
        return headerlist, cdict, sdict


def main():
    pgtoken = "0"
    # countrylist = []
    # sessionlist = []


    # clean csv if exist as used append function to do one by one export
    clean = []
    with open('venv/Scripts/pagination1.csv', 'w', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(clean)

    while pgtoken is not None:
        print(pgtoken)
        analytics = initialize_analyticsreporting()
        response = get_report(analytics, pgtoken)
        headerlist, cdict, sdict = print_response(response)
        print(cdict, sdict)


        # for i in range(len(cdict.keys())):
        #     col = list(cdict.values())[i]
        #     print(col)

        # col1=list(cdict.values())[0]
        # col2 = list(cdict.values())[1]
        # col3 = list(cdict.values())[2]


        # accumulate data if export all record to csv
        # countrylist.append(c)
        # sessionlist.append(s)

        #  store_response =(zip(cdict.values(),slist))
        # # # store_response[pgtoken] = newdict
        #  print(store_response)


        if pgtoken == "0":
          with open('venv/Scripts/pagination1.csv', 'a', newline='') as myfile:
            writer = csv.writer(myfile)
            writer.writerow(headerlist)
            writer.writerows(zip(*cdict.values(),*sdict.values()))

        else:
            with open('venv/Scripts/pagination1.csv', 'a', newline='') as myfile:
                writer = csv.writer(myfile)
                writer.writerows(zip(*cdict.values(),*sdict.values()))

        pgtoken = response['reports'][0].get('nextPageToken')  # update the pageToken
# get_report['reportRequests'][0]['pageToken'] = pgtoken  # update the query


if __name__ == '__main__':
    main()
