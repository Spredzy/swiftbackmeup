# Copyright 2016 Yanis Guenane <yguenane@redhat.com>
# Author: Yanis Guenane <yguenane@redhat.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from prettytable import PrettyTable
from swiftbackmeup import utils
from swiftbackmeup.databases import mariadb
from swiftbackmeup.databases import postgresql

# If --list-backups has been specified, list the backups configured
# in the configuration file
#
def list_backups(backups, options):
    result = [['Database', []],
              ['Type', []],
              ['Host', []],
              ['Swift Container', []],
              ['Swift Pseudo-Folder', []],
              ['Subscriptions', []]]
    for backup in backups:
        if options.mode in backup['subscriptions']:
            result[0][1].append(backup['database'])
            result[1][1].append(backup['type'])
            result[2][1].append(backup['host'])
            result[3][1].append(backup['swift_container'])
            result[4][1].append(backup['swift_pseudo_folder'])
            result[5][1].append(', '.join(backup['subscriptions']))
    utils.output_informations(result)


# If --list-backups-remote has been specified, list the backups available
# on the specified store
#
def list_backups_remote(backups, options, modes):
    result = [['Database', []],
              ['Backup file', []],
              ['Last Modified', []]]
    for backup in backups:
        if options.mode in backup['subscriptions']:
            backup['filename'] = utils.build_filename(backup,
                                                      modes[options.mode])
            if backup['type'] == 'postgresql':
                cur_backup = postgresql.PostgreSQL(backup)
            elif backup['type'] == 'mariadb':
                cur_backup = mariadb.MariaDB(backup)

            for backup_item in cur_backup.list():
                result[0][1].append(backup_item['database'])
                result[1][1].append(backup_item['filename'])
                result[2][1].append(backup_item['last-modified'])
    utils.output_informations(result)