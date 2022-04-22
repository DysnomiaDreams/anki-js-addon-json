#!/usr/bin/python3

import json
import requests

"""
Create json with fields in AddonData.kt in AnkiDroid
"""
def getAddonModel(jsonStr):
    addon = json.loads(jsonStr)

    addonDict = {}
    try:
        addonDict["name"] = addon["name"]
        addonDict["addonTitle"] = addon["addonTitle"]
        addonDict["version"] = addon["version"]
        addonDict["description"] = addon["description"]
        addonDict["main"] = addon["main"]
        addonDict["ankidroidJsApi"] = addon["ankidroidJsApi"]
        addonDict["addonType"] = addon["addonType"]

        if addon["addonType"] == "note-editor":
            addonDict["icon"] = addon["icon"]

        addonDict["keywords"] = addon["keywords"]
        addonDict["author"] = addon["author"]
        addonDict["license"] = addon["license"]
        addonDict["homepage"] = addon["homepage"]

        addonDict["dist"] = {}
        addonDict["dist"]["integrity"] = addon["dist"]["integrity"]
        addonDict["dist"]["shasum"] = addon["dist"]["shasum"]
        addonDict["dist"]["tarball"] = addon["dist"]["tarball"]
        addonDict["dist"]["unpackedSize"] = addon["dist"]["unpackedSize"]
        addonDict["dist"]["fileCount"] = addon["dist"]["fileCount"]

    except:
        print(addon)
    
    return addonDict

""" 
Get all packages with keywords - ankidroid-js-addon
"""
def get_json_all_ankiDroid_addon():
    url = "https://registry.npmjs.org/-/v1/search?text=keywords%3Aankidroid-js-addon&size=250"
    r = requests.get(url)
    data = r.json()
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

"""
Read remove.txt file for removing it from final json output later
"""
def get_invalid_addon_names():
    remove = open('remove.txt', 'r', encoding='utf-8')

    not_valid = []
    with open('remove.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            not_valid.append(line.strip())
            print(line)
    remove.close()
    return not_valid

"""
Generate anki-js-addon.json for listing in AnkiDroid recyclerview
"""
def generate_js_addon_json():
    # final json with ankidroid-js-addon packages info
    valid = []

    # test json for testing
    test = []

    # get invalid addon names to remove from final json
    not_valid = get_invalid_addon_names()

    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data = data['objects']

        for d in data:
            pkg_name = d['package']['name']
            pkg_ver = d['package']['version']

            # skip for not valid addons
            if pkg_name in not_valid:
                print(pkg_name)
                continue

            # npm package info from npm registry
            url = "https://registry.npmjs.org/" + pkg_name + "/" + pkg_ver
            req = requests.get(url)
            response_json = json.dumps(req.json())
            
            print("getting addon info for: ", pkg_name)
            addon = getAddonModel(response_json)
            
            # skip for empty or null addon
            if addon == {} or addon == None:
                continue
            
            # add to list for dumping json
            valid.append(addon)

            # for testing get two packages
            if pkg_name == "valid-ankidroid-js-addon-test" or pkg_name == "ankidroid-js-addon-progress-bar":
                test.append(addon)

    output = open('anki-js-addon.json', 'w', encoding='utf-8')
    json.dump(valid, output, indent=4)

    testOutput = open('test-js-addon.json', 'w', encoding='utf-8')
    json.dump(test, testOutput, indent=4)

    f.close()
    output.close()
    testOutput.close()


get_json_all_ankiDroid_addon()
generate_js_addon_json()