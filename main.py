import os

import yaml

import check

# TODO: Experiment with shell diff
# TODO: Experiment with BLEU score

EXPECTED = {}
GOT = {}

EXPECTED_VALID_YAML = True
GOT_VALID_YAML = True


# TODO: create an open function that returns a dictionary
with open("expected-go-bindata.yaml", "r") as stream:
    try:
        expected_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        os.exit(1)

    EXPECTED = check.parse_fields(expected_dict)


with open("got-go-bindata.yaml", "r") as stream:
    try:
        got_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        GOT_VALID_YAML = False

    GOT = check.parse_fields(got_dict)
    GOT["valid_yaml"] = GOT_VALID_YAML

check.print_assessment(EXPECTED, GOT)
