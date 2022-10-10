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
import subprocess

def main():
    print('START!')

    base_files_url = 'https://archive.org/download/mister-console-bios-pack_theypsilon'

    db = {
        "db_id": 'bios_db',
        "files": {},
        "folders": {
            "|games": {}
        },
        "timestamp":  int(time.time())
    }

    for system, roms in load_json('bios_definitions.json').items():
        if system == 'zips':
            db['zips'] = roms
            continue

        gamesdir = "|games/" + system
        db["folders"][gamesdir] = {}
        zip = system
        if 'zip' in roms:
            zip = roms['zip']
            roms.pop('zip')
        overwrite = False
        if 'overwrite' in roms:
            overwrite = roms['overwrite']
            roms.pop('overwrite')

        for mister_rom, description in roms.items():
            file_descr = {
                "hash": description['hash'],
                "size": description['size'],
                "url": '%s/%s.zip/%s' % (base_files_url, zip, urllib.parse.quote(description['file'])),
                "overwrite": False
            }
            if overwrite:
                file_descr.pop('overwrite')

            db['files'][gamesdir + '/' + mister_rom] = file_descr
            if mister_rom == 'uni-bios.rom' and system == 'NEOGEO':
                db['files'][gamesdir + '/uni-bios-40.zip'] = uni_bios_description()

    add_tags_to_db(db)
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

def add_tags_to_db(db):
    dmdb = get_distribution_mister_db()
    
    tag_dictionary = {}
    
    for folder in db['folders']:
        if folder not in dmdb['folders']:
            print(f"Folder {folder} is not in distribution mister!")
            continue
        
        desc = dmdb['folders'][folder]
        
        if 'tags' not in desc:
            print(f"Folder {folder} does not have a field 'tags'!")
            continue
        
        tags = add_tags_to_dictionary(dmdb['tag_dictionary'], tag_dictionary, desc['tags'])

        db['folders'][folder]['tags'] = tags
        
        for file in db['files']:
            if file.startswith(folder):
                db['files'][file]['tags'] = tags
                
    db['tag_dictionary'] = tag_dictionary
    
    neogeo_tags = db['folders']['|games/NEOGEO']['tags']
    db['zips']['neogeo_unibios']['internal_summary']['files']['|games/NEOGEO/uni-bios.rom']['tags'] = neogeo_tags

def add_tags_to_dictionary(from_dict, to_dict, tags):
    selected_tag_numbers = set()

    for tag in tags:
        for tag_key, tag_number in from_dict.items():
            if tag == tag_number:
                selected_tag_numbers.add(tag_number)
    
    dict_by_number = reverse_dict(from_dict)
    result_tag_numbers = set()
    for tag_number in selected_tag_numbers:
        first_tag_key = next(iter(dict_by_number[tag_number]))
        if first_tag_key in to_dict:
            result_tag_numbers.add(to_dict[first_tag_key])
            continue

        next_tag_number = len(to_dict)
        result_tag_numbers.add(next_tag_number)
        for tag_key in dict_by_number[tag_number]:
            to_dict[tag_key] = next_tag_number
            
    return list(result_tag_numbers)

def reverse_dict(from_dict):
    result = {}
    for k, v in from_dict.items():
        if v not in result:
            result[v] = set()
        result[v].add(k)
    return result

def download(url):
    temp_file = "/tmp/existing.json"
    subprocess.run(['curl', '-L', '-o', temp_file, url], stderr=subprocess.STDOUT)
    result = subprocess.run(['unzip', '-p', temp_file], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return result.stdout.decode()
    
def get_distribution_mister_db():
    print("Downloading dmdb")
    string = download("https://raw.githubusercontent.com/MiSTer-devel/Distribution_MiSTer/main/db.json.zip")
    print(string)
    return json.loads(string)

if __name__ == "__main__":
    main()
