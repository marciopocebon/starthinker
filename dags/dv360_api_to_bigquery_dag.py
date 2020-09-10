###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu	
    l) Install All

--------------------------------------------------------------

DV360 API To BigQuery

Write the current state of advertisers, campaigns, sites, insertion orders, and line items to BigQuery for a given list of DV360 accounts.

Specify the name of the dataset, several tables will be created here.
If dataset exists, it is unchanged.
Add DV360 advertiser ids for the accounts to pull data from.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'endpoint': '',
  'dataset': '',  # Google BigQuery dataset to create tables in.
  'auth_read': 'user',  # Credentials used for reading data.
  'auth_write': 'service',  # Credentials used for writing data.
  'advertisers': [],  # Comma separated advertisers ids.
  'partners': [],  # Comma separated partners ids.
}

TASKS = [
  {
    'dv360_api': {
      'endpoints': {
        'field': {
          'choices': [
            'advertisers',
            'advertisers.campaigns',
            'advertisers.channels',
            'advertisers.channels.sites',
            'advertisers.creatives',
            'advertisers.insertionOrders',
            'advertisers.lineItems',
            'advertisers.lineItems.targetingTypes',
            'advertisers.locationLists',
            'advertisers.locationLists.assignedLocations',
            'advertisers.negativeKeywordLists',
            'advertisers.negativeKeywordLists.negativeKeywords',
            'advertisers.targetingTypes.assignedTargetingOptions',
            'combinedAudiences',
            'customBiddingAlgorithms',
            'customLists',
            'firstAndThirdPartyAudiences',
            'floodlightGroups',
            'googleAudiences',
            'inventorySourceGroups',
            'inventorySourceGroups.assignedInventorySources',
            'inventorySources',
            'partners',
            'partners.channels',
            'partners.channels.sites',
            'floodlightActivityGroups',
            'partners.targetingTypes.assignedTargetingOptions',
            'targetingTypes.targetingOptions',
            'users'
          ],
          'name': 'endpoint',
          'default': '',
          'kind': 'choice'
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'out': {
        'auth': {
          'field': {
            'description': 'Credentials used for writing data.',
            'kind': 'authentication',
            'name': 'auth_write',
            'order': 1,
            'default': 'service'
          }
        },
        'dataset': {
          'field': {
            'description': 'Google BigQuery dataset to create tables in.',
            'kind': 'string',
            'name': 'dataset',
            'order': 1,
            'default': ''
          }
        }
      },
      'partners': {
        'values': {
          'field': {
            'description': 'Comma separated partners ids.',
            'kind': 'integer_list',
            'name': 'partners',
            'order': 2,
            'default': [
            ]
          }
        },
        'single_cell': True
      },
      'advertisers': {
        'values': {
          'field': {
            'description': 'Comma separated advertisers ids.',
            'kind': 'integer_list',
            'name': 'advertisers',
            'order': 2,
            'default': [
            ]
          }
        },
        'single_cell': True
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('dv360_api_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()