def parse_fields(yaml_dict):
    """Parse the melange YAML fields."""
    fields = {}

    fields["name"] = yaml_dict["package"]["name"]
    fields["version"] = yaml_dict["package"]["version"]
    fields["epoch"] = yaml_dict["package"]["epoch"]
    fields["description"] = yaml_dict["package"]["description"]

    fields["license"] = []
    for license in yaml_dict["package"]["copyright"]:
        fields["license"].append(license["license"])
    # sort alphabetically the list of licenses in case the order was different
    fields["license"].sort()

    fields["env_packages"] = []
    for package in yaml_dict["environment"]["contents"]["packages"]:
        fields["env_packages"].append(package)
    # sort alphabetically the list of environmental packages in case the order
    # was different
    fields["env_packages"].sort()

    for pipeline in yaml_dict["pipeline"]:
        if pipeline["uses"] == "fetch":
            fields["fetch_uri"] = pipeline["with"]["uri"]
            fields["fetch_sha512"] = pipeline["with"]["expected-sha512"]

    fields["strip_statement"] = False
    for pipeline in yaml_dict["pipeline"]:
        if pipeline["uses"] == "strip":
            fields["strip_statement"] = True
    fields["dict_fields"] = collect_dict_fields(yaml_dict)
    return fields


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
        #"update.enabled",
    ]
    for field in KEY_MELANGE_FIELDS:
        if field not in list_of_fields:
            return False
    return True


# TODO: Turn this into optional JSON output
def print_assessment(expected, got):
    print("-------------ASESSMENT-------------")
    print("Valid YAML for generated file: " + str(got["valid_yaml"]))
    print(
        "Same dictionary fields: " + str(expected["dict_fields"] == got["dict_fields"])
    )
    print(
        "Melange fields present: " + str(key_melange_fields_exist(got["dict_fields"]))
    )
    print("Same package name: " + str(expected["name"] == got["name"]))
    print("Same package version: " + str(expected["version"] == got["version"]))
    print("Same package epoch: " + str(expected["epoch"] == got["epoch"]))
    print(
        "Same package description: "
        + str(expected["description"] == got["description"])
    )
    print("Same package licenses: " + str(expected["license"] == expected["license"]))
    print(
        "Same package environment packages: "
        + str(expected["env_packages"] == got["env_packages"])
    )
    print("Same package fetch uri: " + str(expected["fetch_uri"] == got["fetch_uri"]))
    print(
        "Same package fetch sha512: "
        + str(expected["fetch_sha512"] == got["fetch_sha512"])
    )
    print("Has package strip statement: " + str(got["strip_statement"]))
