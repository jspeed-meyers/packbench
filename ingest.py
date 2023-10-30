import yaml

# TODO: add support for git-checkout
#  uses: git-checkout
#     with:
#       repository: https://github.com/cloudflare/cloudflared
#       tag: ${{package.version}}
#       expected-commit: 867360c8dd3dd5d88cfbcfcb7ad9b587a04ab82d


class mYAML:
    """Ingest melange YAML file."""

    def __init__(self, filename):
        """Ingest melange YAML and parse fields."""

        self.fields = {}

        with open(filename, "r") as stream:
            try:
                yaml_dict = yaml.safe_load(stream)
                self.fields["valid_yaml"] = True
            except yaml.YAMLError as exc:
                print(exc)
                os.exit(1)

        self.fields["filename"] = filename

        self.fields["name"] = yaml_dict["package"]["name"]
        self.fields["version"] = yaml_dict["package"]["version"]
        self.fields["epoch"] = yaml_dict["package"]["epoch"]
        self.fields["description"] = yaml_dict["package"]["description"]

        self.fields["license"] = []
        for license in yaml_dict["package"]["copyright"]:
            self.fields["license"].append(license["license"])
        # sort alphabetically the list of licenses in case the order was different
        self.fields["license"].sort()

        self.fields["env_packages"] = []
        for package in yaml_dict["environment"]["contents"]["packages"]:
            self.fields["env_packages"].append(package)
        # sort alphabetically the list of environmental packages in case the order
        # was different
        self.fields["env_packages"].sort()

        for pipeline in yaml_dict["pipeline"]:
            if pipeline["uses"] == "fetch":
                self.fields["fetch_uri"] = pipeline["with"]["uri"]
                self.fields["fetch_sha512"] = pipeline["with"]["expected-sha512"]

        self.fields["strip_statement"] = False
        for pipeline in yaml_dict["pipeline"]:
            if pipeline["uses"] == "strip":
                self.fields["strip_statement"] = True
        self.fields["dict_fields"] = mYAML.collect_dict_fields(yaml_dict)

        self.fields["key_melange_fields_exist"] = mYAML.key_melange_fields_exist(
            self.fields["dict_fields"]
        )

    def collect_dict_fields(dictionary, parent_key=""):
        """Collects all the fields of a dictionary recursively."""
        dict_fields = []
        for key, value in dictionary.items():
            if isinstance(value, dict):
                dict_fields.extend(
                    mYAML.collect_dict_fields(value, parent_key + key + ".")
                )
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
        ]
        for field in KEY_MELANGE_FIELDS:
            if field not in list_of_fields:
                return False
        return True
