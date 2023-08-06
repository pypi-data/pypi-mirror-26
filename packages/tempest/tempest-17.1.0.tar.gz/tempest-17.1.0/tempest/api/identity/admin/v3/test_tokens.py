# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import six

from tempest.api.identity import base
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc

CONF = config.CONF


class TokensV3TestJSON(base.BaseIdentityV3AdminTest):

    @decorators.idempotent_id('0f9f5a5f-d5cd-4a86-8a5b-c5ded151f212')
    def test_tokens(self):
        # Valid user's token is authenticated
        # Create a User
        u_name = data_utils.rand_name('user')
        u_desc = '%s-description' % u_name
        u_password = data_utils.rand_password()
        user = self.create_test_user(
            name=u_name, description=u_desc, password=u_password)
        # Perform Authentication
        resp = self.token.auth(user_id=user['id'],
                               password=u_password).response
        subject_token = resp['x-subject-token']
        self.client.check_token_existence(subject_token)
        # Perform GET Token
        token_details = self.client.show_token(subject_token)['token']
        self.assertEqual(resp['x-subject-token'], subject_token)
        self.assertEqual(token_details['user']['id'], user['id'])
        self.assertEqual(token_details['user']['name'], u_name)
        # Perform Delete Token
        self.client.delete_token(subject_token)
        self.assertRaises(lib_exc.NotFound, self.client.check_token_existence,
                          subject_token)

    @decorators.idempotent_id('565fa210-1da1-4563-999b-f7b5b67cf112')
    def test_rescope_token(self):
        """Rescope a token.

        An unscoped token can be requested, that token can be used to request a
        scoped token. The scoped token can be revoked, and the original token
        used to get a token in a different project.

        """

        # Create a user.
        user_password = data_utils.rand_password()
        user = self.create_test_user(password=user_password)

        # Create a couple projects
        project1_name = data_utils.rand_name(name='project')
        project1 = self.setup_test_project(name=project1_name)

        project2_name = data_utils.rand_name(name='project')
        project2 = self.setup_test_project(name=project2_name)
        self.addCleanup(self.projects_client.delete_project, project2['id'])

        # Create a role
        role = self.setup_test_role()

        # Grant the user the role on both projects.
        self.roles_client.create_user_role_on_project(project1['id'],
                                                      user['id'],
                                                      role['id'])

        self.roles_client.create_user_role_on_project(project2['id'],
                                                      user['id'],
                                                      role['id'])

        # Get an unscoped token.
        token_auth = self.token.auth(user_id=user['id'],
                                     password=user_password)

        token_id = token_auth.response['x-subject-token']
        orig_expires_at = token_auth['token']['expires_at']
        orig_user = token_auth['token']['user']

        self.assertIsInstance(token_auth['token']['expires_at'], six.text_type)
        self.assertIsInstance(token_auth['token']['issued_at'], six.text_type)
        self.assertEqual(['password'], token_auth['token']['methods'])
        self.assertEqual(user['id'], token_auth['token']['user']['id'])
        self.assertEqual(user['name'], token_auth['token']['user']['name'])
        self.assertEqual(CONF.identity.default_domain_id,
                         token_auth['token']['user']['domain']['id'])
        self.assertIsNotNone(token_auth['token']['user']['domain']['name'])
        self.assertNotIn('catalog', token_auth['token'])
        self.assertNotIn('project', token_auth['token'])
        self.assertNotIn('roles', token_auth['token'])

        # Use the unscoped token to get a scoped token.
        token_auth = self.token.auth(
            token=token_id,
            project_name=project1_name,
            project_domain_id=CONF.identity.default_domain_id)
        token1_id = token_auth.response['x-subject-token']

        self.assertEqual(orig_expires_at, token_auth['token']['expires_at'],
                         'Expiration time should match original token')
        self.assertIsInstance(token_auth['token']['issued_at'], six.text_type)
        self.assertEqual(set(['password', 'token']),
                         set(token_auth['token']['methods']))
        self.assertEqual(orig_user, token_auth['token']['user'],
                         'User should match original token')
        self.assertIsInstance(token_auth['token']['catalog'], list)
        self.assertEqual(project1['id'],
                         token_auth['token']['project']['id'])
        self.assertEqual(project1['name'],
                         token_auth['token']['project']['name'])
        self.assertEqual(CONF.identity.default_domain_id,
                         token_auth['token']['project']['domain']['id'])
        self.assertIsNotNone(token_auth['token']['project']['domain']['name'])
        self.assertEqual(1, len(token_auth['token']['roles']))
        self.assertEqual(role['id'], token_auth['token']['roles'][0]['id'])
        self.assertEqual(role['name'], token_auth['token']['roles'][0]['name'])

        # Revoke the unscoped token.
        self.client.delete_token(token1_id)

        # Now get another scoped token using the unscoped token.
        token_auth = self.token.auth(
            token=token_id,
            project_name=project2_name,
            project_domain_id=CONF.identity.default_domain_id)

        self.assertEqual(project2['id'],
                         token_auth['token']['project']['id'])
        self.assertEqual(project2['name'],
                         token_auth['token']['project']['name'])

    @decorators.idempotent_id('08ed85ce-2ba8-4864-b442-bcc61f16ae89')
    def test_get_available_project_scopes(self):
        manager_project_id = self.os_primary.credentials.project_id
        admin_user_id = self.os_admin.credentials.user_id
        admin_role_id = self.get_role_by_name(CONF.identity.admin_role)['id']

        # Grant the user the role on both projects.
        self.roles_client.create_user_role_on_project(
            manager_project_id, admin_user_id, admin_role_id)
        self.addCleanup(
            self.roles_client.delete_role_from_user_on_project,
            manager_project_id, admin_user_id, admin_role_id)

        assigned_project_ids = [self.os_admin.credentials.project_id,
                                manager_project_id]

        # Get available project scopes
        available_projects = self.client.list_auth_projects()['projects']

        # create list to save fetched project's id
        fetched_project_ids = [i['id'] for i in available_projects]

        # verifying the project ids in list
        missing_project_ids = \
            [p for p in assigned_project_ids if p not in fetched_project_ids]
        self.assertEmpty(missing_project_ids,
                         "Failed to find project_id %s in fetched list" %
                         ', '.join(missing_project_ids))
