#!/usr/bin/env python3
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can download the latest version of this tool from:
# https://github.com/MiSTer-unstable-nightlies/Unstable_Folder_MiSTer

import json
import time
import urllib.parse

def main():
    print('START!')

    base_files_url = 'https://archive.org/download/mister-console-bios-pack_theypsilon'

    db = {
        "db_id": 'bios_db',
        "db_files": [],
        "files": {},
        "folders": {
            "games": {}
        },
        "zips": {},
        "base_files_url": "",
        "default_options": {},
        "timestamp":  int(time.time())
    }

    for system, roms in load_json('bios_definitions.json').items():
        gamesdir = "games/" + system
        db["folders"][gamesdir] = {}
        zip = system
        if 'zip' in roms:
            zip = roms['zip']
            roms.pop('zip')
        for mister_rom, description in roms.items():
            db['files'][gamesdir + '/' + mister_rom] = {
                "hash": description['hash'],
                "size": description['size'],
                "url": '%s/%s.zip/%s' % (base_files_url, zip, urllib.parse.quote(description['file'])),
                "overwrite": False
            }
            if mister_rom == 'uni-bios.rom' and system == 'NEOGEO':
                db['files'][gamesdir + '/uni-bios-40.zip'] = uni_bios_description()

    save_json(db, "bios_db.json")

def save_json(db, json_name):
    with open(json_name, 'w') as f:
        json.dump(db, f, sort_keys=True, indent=4)
    print('Saved ' + json_name)

def load_json(path):
    with open(path) as f:
        return json.load(f)

def uni_bios_description():
    url = 'http://unibios.free.fr/download/uni-bios-40.zip'
    return {
        "hash": '1986c39676354d19ae648a914bd914f7',
        "size": 101498,
        "url": url
    }

if __name__ == "__main__":
    main()
