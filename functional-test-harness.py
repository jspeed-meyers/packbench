import os

import yaml

GOT_VALID_YAML = True

EXPECTED_NAME = ""
GOT_NAME = ""

EXPECTED_VERSION = ""
GOT_VERSION = ""

EXPECTED_EPOCH = ""
GOT_EPOCH = ""

EXPECTED_DESCRIPTION = ""
GOT_DESCRIPTION = ""

EXPECTED_LICENSES_ALPHABETICAL = []
GOT_LICENSES_ALPHABETICAL = []

EXPECTED_ENVIRONMENT_PACKAGES_ALPHABETICAL = []
GOT_ENVIRONMENT_PACKAGES_ALPHABETICAL = []

EXPECTED_FETCH_URI = ""
GOT_FETCH_URI = ""

EXPECTED_FETCH_SHA512 = ""
GOT_FETCH_SHA512 = ""

# TODO: Should every YAML include a strip statement in the pipeline?
GOT_STRIP_STATEMENT = False

with open("expected-go-bindata.yaml", "r") as stream:
    try:
        expected = yaml.safe_load(stream)
        print(expected)
    except yaml.YAMLError as exc:
        print(exc)
        os.exit(1)

    # TODO: turn this into a function
    EXPECTED_NAME = expected['package']['name']
    EXPECTED_VERSION = expected['package']['version']
    EXPECTED_EPOCH = expected['package']['epoch']
    EXPECTED_DESCRIPTION = expected['package']['description']
    for license in expected['package']['copyright']:
        EXPECTED_LICENSES_ALPHABETICAL.append(license['license'])
    # sort alphabetically the list of licenses
    EXPECTED_LICENSES_ALPHABETICAL.sort()
    for package in expected["environment"]["contents"]["packages"]:
        EXPECTED_ENVIRONMENT_PACKAGES_ALPHABETICAL.append(package)
    for pipeline in expected["pipeline"]:
        if pipeline["uses"] == "fetch":
            EXPECTED_FETCH_URI = pipeline["with"]["uri"]
            EXPECTED_FETCH_SHA512 = pipeline["with"]["expected-sha512"]

with open("got-go-bindata.yaml", "r") as stream:
    try:
        got = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        GOT_VALID_YAML = False

    GOT_NAME = got['package']['name']
    GOT_VERSION = got['package']['version']
    GOT_EPOCH = got['package']['epoch']
    GOT_DESCRIPTION = got['package']['description']
    for license in got['package']['copyright']:
        GOT_LICENSES_ALPHABETICAL.append(license['license'])
    # sort alphabetically the list of licenses
    GOT_LICENSES_ALPHABETICAL.sort()
    for package in got["environment"]["contents"]["packages"]:
        GOT_ENVIRONMENT_PACKAGES_ALPHABETICAL.append(package)
    for pipeline in got["pipeline"]:
        if pipeline["uses"] == "fetch":
            GOT_FETCH_URI = pipeline["with"]["uri"]
            GOT_FETCH_SHA512 = pipeline["with"]["expected-sha512"]
    for pipeline in got["pipeline"]:
        if pipeline["uses"] == "strip":
            GOT_STRIP_STATEMENT = True

# TODO: Turn this into optional JSON output
print("-------------ASESSMENT-------------")
print("Valid YAML for generated file: " + str(GOT_VALID_YAML))
print("Same package name: " + str(EXPECTED_NAME == GOT_NAME))
print("Same package version: " + str(EXPECTED_VERSION == GOT_VERSION))
print("Same package epoch: " + str(EXPECTED_EPOCH == GOT_EPOCH))
print("Same package description: " + str(EXPECTED_DESCRIPTION == GOT_DESCRIPTION))
print("Same package licenses: " + str(EXPECTED_LICENSES_ALPHABETICAL == GOT_LICENSES_ALPHABETICAL))
print("Same package environment packages: " + str(EXPECTED_ENVIRONMENT_PACKAGES_ALPHABETICAL == GOT_ENVIRONMENT_PACKAGES_ALPHABETICAL))
print("Same package fetch uri: " + str(EXPECTED_FETCH_URI == GOT_FETCH_URI))
print("Same package fetch sha512: " + str(EXPECTED_FETCH_SHA512 == GOT_FETCH_SHA512))
print("Has package strip statement: " + str(GOT_STRIP_STATEMENT))