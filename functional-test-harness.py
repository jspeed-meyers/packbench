import os

import yaml

# TODO: split into different files

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

EXPECTED_DICT_FIELDS = []
GOT_DICT_FIELDS = []

GOT_MELANGE_FIELDS_PRESENT = False

# TODO: Should every YAML include a strip statement in the pipeline?
GOT_STRIP_STATEMENT = False


def collect_dict_fields(dictionary, parent_key=""):
    """Collects all the fields of a dictionary recursively."""
    dict_fields = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dict_fields.extend(collect_dict_fields(value, parent_key + key + "."))
        else:
            dict_fields.append(parent_key + key)
    return dict_fields


def key_melange_fields_exist(list_of_fields):
    """Checks if the key melange fields exist in the dictionary."""
    # TODO: determine must-have melange fields.
    KEY_MELANGE_FIELDS = [
        "package.name",
        "package.version",
        "package.epoch",
        "package.description",
        "environment.contents.packages",
        "pipeline",
        "update.enabled",
    ]
    for field in KEY_MELANGE_FIELDS:
        print(field)
        if field not in list_of_fields:
            print("FALSE")
            return False
    return True


with open("expected-go-bindata.yaml", "r") as stream:
    try:
        expected = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        os.exit(1)

    # TODO: turn this into a function
    EXPECTED_NAME = expected["package"]["name"]
    EXPECTED_VERSION = expected["package"]["version"]
    EXPECTED_EPOCH = expected["package"]["epoch"]
    EXPECTED_DESCRIPTION = expected["package"]["description"]
    for license in expected["package"]["copyright"]:
        EXPECTED_LICENSES_ALPHABETICAL.append(license["license"])
    # sort alphabetically the list of licenses
    EXPECTED_LICENSES_ALPHABETICAL.sort()
    for package in expected["environment"]["contents"]["packages"]:
        EXPECTED_ENVIRONMENT_PACKAGES_ALPHABETICAL.append(package)
    for pipeline in expected["pipeline"]:
        if pipeline["uses"] == "fetch":
            EXPECTED_FETCH_URI = pipeline["with"]["uri"]
            EXPECTED_FETCH_SHA512 = pipeline["with"]["expected-sha512"]
    EXPECTED_DICT_FIELDS = collect_dict_fields(expected)


with open("got-go-bindata.yaml", "r") as stream:
    try:
        got = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        GOT_VALID_YAML = False

    GOT_NAME = got["package"]["name"]
    GOT_VERSION = got["package"]["version"]
    GOT_EPOCH = got["package"]["epoch"]
    GOT_DESCRIPTION = got["package"]["description"]
    for license in got["package"]["copyright"]:
        GOT_LICENSES_ALPHABETICAL.append(license["license"])
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
    GOT_DICT_FIELDS = collect_dict_fields(got)
    GOT_MELANGE_FIELDS_PRESENT = key_melange_fields_exist(GOT_DICT_FIELDS)


# TODO: Experiment with shell diff
# TODO: Experiment with BLEU score

# TODO: Turn this into optional JSON output
print("-------------ASESSMENT-------------")
print("Valid YAML for generated file: " + str(GOT_VALID_YAML))
print("Same dictionary fields: " + str(EXPECTED_DICT_FIELDS == GOT_DICT_FIELDS))
print("Melange fields present: " + str(GOT_MELANGE_FIELDS_PRESENT))
print("Same package name: " + str(EXPECTED_NAME == GOT_NAME))
print("Same package version: " + str(EXPECTED_VERSION == GOT_VERSION))
print("Same package epoch: " + str(EXPECTED_EPOCH == GOT_EPOCH))
print("Same package description: " + str(EXPECTED_DESCRIPTION == GOT_DESCRIPTION))
print(
    "Same package licenses: "
    + str(EXPECTED_LICENSES_ALPHABETICAL == GOT_LICENSES_ALPHABETICAL)
)
print(
    "Same package environment packages: "
    + str(
        EXPECTED_ENVIRONMENT_PACKAGES_ALPHABETICAL
        == GOT_ENVIRONMENT_PACKAGES_ALPHABETICAL
    )
)
print("Same package fetch uri: " + str(EXPECTED_FETCH_URI == GOT_FETCH_URI))
print("Same package fetch sha512: " + str(EXPECTED_FETCH_SHA512 == GOT_FETCH_SHA512))
print("Has package strip statement: " + str(GOT_STRIP_STATEMENT))
