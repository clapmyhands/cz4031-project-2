# #################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2016, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
# ##################################################################

import json

from pgadmin.utils.route import BaseTestGenerator
from regression import test_utils as utils
from regression import test_server_dict
from pgadmin.browser.server_groups.servers.tests import utils as server_utils
from . import utils as database_utils


class DatabaseAddTestCase(BaseTestGenerator):
    """This class will test the ADD database API"""

    scenarios = [
        # Fetching default URL for database node.
        ('Check Databases Node URL', dict(url='/browser/database/obj/'))
    ]

    def setUp(self):
        pass

    def runTest(self):
        """ This function will add database under 1st server of tree node. """
        self.db_name = ''
        server_id = test_server_dict["server"][0]["server_id"]
        server_response = server_utils.connect_server(self, server_id)
        if server_response["info"] == "Server connected.":
            db_owner = server_response['data']['user']['name']
            self.data = database_utils.get_db_data(db_owner)
            self.db_name = self.data['name']
            response = self.tester.post(self.url + str(utils.SERVER_GROUP) +
                                        "/" + str(server_id) + "/",
                                        data=json.dumps(self.data),
                                        content_type='html/json')
            self.assertEquals(response.status_code, 200)
            response_data = json.loads(response.data.decode('utf-8'))
            db_id = response_data['node']['_id']
            db_dict = {"db_id": db_id, "db_name": self.db_name}
            utils.write_node_info(int(server_id), "did", db_dict)
        else:
            raise Exception("Error while connecting server to add the"
                            " database.")

    def tearDown(self):
        """
        This function delete the database from server added in SQLite.
        """
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'])
        utils.drop_database(connection, self.db_name)
