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

import hashlib
import json
import time
import os
import sys

def main():
    print('START!')

    local_files_path = (sys.argv[1] + "/") if len(sys.argv) == 3 else None
    base_files_url = (sys.argv[2] + "/") if len(sys.argv) == 3 else None

    if not local_files_path or not base_files_url:
        print('Wrong arguments!')
        print('Usage: %s local_files_path base_files_url' % sys.argv[0])
        exit(-1)

    db = {
        "db_id": 'bios_db',
        "db_files": [],
        "files": {},
        "folders": {},
        "zips": {},
        "base_files_url": "",
        "default_options": {},
        "timestamp":  int(time.time())
    }

    for system, roms in load_json('bios.json').items():
        gamesdir = "games/" + system
        db["folders"][gamesdir] = {}
        for mister_rom, remote_rom in roms.items():
            rom_path = system + "/" + remote_rom
            local_rom_path = local_files_path + rom_path
            rom_url = base_files_url + rom_path
            db['files'][gamesdir + '/' + mister_rom] = {
                "hash": hash(local_rom_path),
                "size": size(local_rom_path),
                "url": rom_url,
                "overwrite": False
            }

    save_json(db, "bios_db.json")

def hash(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
        return file_hash.hexdigest()

def size(file):
    return os.path.getsize(file)

def save_json(db, json_name):
    with open(json_name, 'w') as f:
        json.dump(db, f, sort_keys=True, indent=4)
    print('Saved ' + json_name)

def load_json(path):
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    main()