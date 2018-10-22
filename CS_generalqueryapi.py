#!/usr/bin/env python3
 
__author__ = "Aspen Lindblom"
__version__ = "2018.08.01"
__contact__ = "aspen.lindblom@crowdstrike.com"
 
# On Mac or Linux systems you must mark this script as executable using the "chmod +x FalconQueryAPI.py" command before
#  the whole shebang will have any effect.
 
import json
import sys
import csv
import argparse
 
try:
    import requests
except ImportError as err:
    print(err)
    print('Python\'s Requests library is required to run FalconQueryAPI.py. Please run "python3 -m pip install '
          'request" command on Mac or Linux systems, "py -m pip install" on Windows to install this library.')
 
 
def get_host_details(ids):
    """
    The main purpose of this function is to gather the host details based on the AIDs collected from the other functions.
 
    :param ids:
    :return:
    """
 
    print('Gathering host details. This could take time depending on the number of hosts.')
 
    # Variables used.
    headers = {'Content-Type': "application/json"}
    fn = 0
    # Get Device Details API has a maximum limit of 5000 ids that can be used in a single API call.
    ln = 5000
    # Creating an empty list to append results of the response to.
    json_arr = list()
    # Store the AIDs in a dictionary and pass 5000 AIDs at a time as a parameter in the GET request
    payload = {'ids': ids[fn:ln]}
 
    # Getting host details
    while len(ids) >= fn:
        uri = 'https://falconapi.crowdstrike.com/devices/entities/devices/v1'
        response = requests.get(uri, headers=headers, auth=(args.user, args.passwd), params=payload)
        print(response.url)
        if response.status_code == 200:
            data = response.json()
            json_arr.extend(data.get('resources'))
        else:
            print('Failed to get host IDs. Response: {0}.\nResponse code: {1}'.format(response.text,
                                                                                      response.status_code))
            sys.exit()
        fn += 5000
        ln += 5000
        payload = {'ids': ids[fn:ln]}
 
    print('Writing host details to CSV.')
 
    # Specifying what will be displayed the header row
    keys = ['Agent ID', 'Agent Version', 'Host Name', 'First Seen', 'Last Seen', 'Local IP', 'Host Type',
            'Operating System', 'Platform', 'Prevention Policy ID', 'Sensor Update Policy ID', 'Group ID',
            'Containment Status']
 
    # Writing csv file to disk
    with open('query_results.csv', 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        dict_writer = csv.DictWriter(output_file, keys,
                                     extrasaction='ignore')
        dict_writer.writeheader()
 
        # Storing the values of specific keys as a variable then writing those variables to the csv file
        for v in json_arr:
            device_id = v.get('device_id', '')
            agent_version = v.get('agent_version', '')
            hostname = v.get('hostname', '')
            first_seen = v.get('first_seen', '')
            last_seen = v.get('last_seen', '')
            local_ip = v.get('local_ip', '')
            os_version = v.get('os_version', '')
            platform = v.get('platform_name', '')
            groups = v.get('groups', 'Unassigned')
            product_type_desc = v.get('product_type_desc', '')
            prevention_policy_id = v.get('device_policies', {}).get('prevention', {}).get('policy_id', 'Unassigned')
            sensor_policy_id = v.get('device_policies', {}).get('sensor_update', {}).get('policy_id', 'Unassigned')
            status = v.get('status', '')
            csv_writer.writerow([device_id, agent_version, hostname, first_seen, last_seen, local_ip, platform,
                                os_version, product_type_desc, prevention_policy_id, sensor_policy_id, groups, status])
 
    output_file.close()
 
 
def get_host_ids():
    """
    The main purpose of this function is to gather all of the AIDs into a list of dictionaries and call the
    get_host_details() functions to collect details on those hosts.
 
    :return:
    """
 
    print('Gathering Host IDs (aka Agent IDs)')
 
    # Variables used.
    offset = 0
    total = 1
    headers = {'Content-Type': "application/json"}
    limit = 5000
    host_id = list()
    uri = f'https://falconapi.crowdstrike.com/devices/queries/devices/v1?limit={limit}&offset={offset}'
 
    # Geting host_id
    while total > offset:
        response = requests.get(uri, headers=headers, auth=(args.user, args.passwd))
        if response.status_code == 200:
            data = response.json()
            host_id.extend(data.get('resources'))
            total = int(data.get('meta', {}).get('pagination', {}).get('total'))
        else:
            print("Failed to get host IDs. Response: {0}.\nResponse code: {1}".format(response.text,
                                                                                      response.status_code))
            sys.exit()
        offset += 5000
        uri = f'https://falconapi.crowdstrike.com/devices/queries/devices/v1?limit={limit}&offset={offset}'
 
    # Calling get details helper function
    print(f'Finished gathering host IDs. Total number of hosts is {total}')
    get_host_details(host_id)
 
 
def get_prevention_id():
    """
    The main purpose of this function is to collect the host ID (aka Agent ID or AID for short), based on the specified
    prevention policy_id and store the results into a list of dictionaries that will be used by the
    get_host_details() function.
 
    :return:
    """
 
    print('Gathering Host IDs (aka Agent IDs) from Prevention Policy.')
 
    # Variables used.
    offset = 0
    total = 1
    headers = {'Content-Type': "application/json"}
    limit = 5000
    host_id = list()
    uri = 'https://falconapi.crowdstrike.com/devices/queries/devices/v1?filter=device_policies.prevention.policy_id' \
          ':\'{0}\'&limit={1}&offset={2}'.format(args.prevention, limit, offset)
 
    # Getting host_id
    while total > offset:
        response = requests.get(uri, headers=headers, auth=(args.user, args.passwd))
        if response.status_code == 200:
            data = response.json()
            host_id.extend(data.get('resources'))
            total = int(data.get('meta', {}).get('pagination', {}).get('total'))
        else:
            print(f'Failed to get host IDs. Response: {response.text}.\nResponse code: {response.status_code}')
            sys.exit()
        offset += 5000
        uri = 'https://falconapi.crowdstrike.com/devices/queries/devices/v1?filter=device_policies.prevention' \
              '.policy_id:\'{0}\'&limit={1}&offset={2}'.format(args.prevention, limit, offset)
 
    # Calling get details helper function
    print(f'Finished gathering host IDs. Total number of hosts seen in prevention policy is {total}')
    get_host_details(host_id)
 
 
def get_sensor_id():
    """
    he main purpose of this function is to collect the host ID (aka Agent ID or AID for short), based on the specified
    sensor update policy_id and store the results into a list of dictionaries that will be used by the
    get_host_details() function.
 
    :return:
    """
 
    print('Gathering Host IDs (aka Agent IDs) from Sensor Update Policy.')
 
    # Variables used.
    offset = 0
    total = 1
    headers = {'Content-Type': "application/json"}
    limit = 5000
    host_id = list()
    uri = 'https://falconapi.crowdstrike.com/devices/queries/devices/v1?filter=device_policies.sensor_update' \
          '.policy_id:\'{0}\'&limit={1}&offset={2}'.format(args.sensor, limit, offset)
 
    # Getting host_id
    while total > offset:
        response = requests.get(uri, headers=headers, auth=(args.user, args.passwd))
        if response.status_code == 200:
            data = response.json()
            host_id.extend(data.get('resources'))
            total = int(data.get('meta', {}).get('pagination', {}).get('total'))
        else:
            print(f'Failed to get host IDs. Response: {response.text}.\nResponse code: {response.status_code}')
            sys.exit()
        offset += 5000
        uri = 'https://falconapi.crowdstrike.com/devices/queries/devices/v1?filter=device_policies.sensor_update' \
              '.policy_id:\'{0}\'&limit={1}&offset={2}'.format(args.sensor, limit, offset)
 
    # Calling get details helper function
    print(f'Finished gathering host IDs. Total number of hosts seen in sensor update policy is {total}.')
    get_host_details(host_id)
 
 
def get_group_id():
    """
    The main purpose of this function is to collect the host ID (aka Agent ID or AID for short), based on the specified
    group policy_id and store the results into a list of dictionaries that will be used by the
    get_host_details() function.
 
    :return:
    """
 
    print('Gathering Host IDs (aka Agent IDs) from Group.')
 
    # Variables used.
    offset = 0
    total = 1
    headers = {'Content-Type': "application/json"}
    limit = 5000
    host_id = list()
    uri = 'https://falconapi.crowdstrike.com/devices/queries/devices/v1?filter=groups:\'{0}\'&limit={1}' \
          '&offset={2}'.format(args.group, limit, offset)
 
    # Getting host_id
    while total > offset:
        response = requests.get(uri, headers=headers, auth=(args.user, args.passwd))
        if response.status_code == 200:
            data = response.json()
            host_id.extend(data.get('resources'))
            total = int(data.get('meta', {}).get('pagination', {}).get('total'))
        else:
            print(f'Failed to get host IDs. Response: {response.text}.\nResponse code: {response.status_code}')
            sys.exit()
        offset += 5000
        uri = 'https://falconapi.crowdstrike.com/devices/queries/devices/v1?filter=groups:\'{0}\'&limit={1}' \
              '&offset={2}'.format(args.group, limit, offset)
 
    # Calling get details helper function
    print(f"Finished gathering host IDs. Total number of hosts seen in group is {total}")
    get_host_details(host_id)
 
 
def main():
    if args.user and args.passwd and args.prevention:
        get_prevention_id()
    elif args.user and args.passwd and args.sensor:
        get_sensor_id()
    elif args.user and args.passwd and args.group:
        get_group_id()
    else:
        get_host_ids()
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Query API client')
    parser.add_argument('user', metavar='USERNAME', help='Type in Query API user name.')
    parser.add_argument('passwd', metavar='PASSWORD', help='Type in Query API password.')
    parser.add_argument('--prevention', '-p',
                        help='Type in prevention policy_id if you only want to return host details from hosts in a '
                             'specific prevention policy.')
    parser.add_argument('--sensor', '-s',
                        help='Type in sensor policy_id if you only want to return host details from hosts in a '
                             'specific sensor update policy.')
    parser.add_argument('--group', '-g',
                        help='Type in group_id if you only want to return host details from hosts in a specific group.')
    args = parser.parse_args()
    main()