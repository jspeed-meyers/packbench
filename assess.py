import json


class Assess:
    def __init__(self, expected, got):
        """Compare fields of two mYAML objects."""
        self.assessment = {}

        # focus on the fields specific to the "got" YAML, the
        # predicted YAML
        for field in ["valid_yaml", "strip_statement", "key_melange_fields_exist"]:
            self.assessment[field] = got[field]

        # a comparison of fields between the expected YAML (the "ground truth")
        # YAML and the got (or predicted) YAML
        for field in [
            "dict_fields",
            "name",
            "version",
            "epoch",
            "description",
            "license",
            "env_packages",
            "fetch_uri",
            "fetch_sha512",
            "repository",
            "tag",
            "expected-commit",
            "update"
        ]:
            if field in expected:
                self.assessment[field] = expected[field] == got[field]

    def print_assessment(self):
        """Print all assessment fields."""
        for key, value in self.assessment.items():
            print(f"{key}: ", value)

    def output_json(self):
        """Output assessment as JSON."""
        return json.dumps(self.assessment)

    def output_dict(self):
        """Output assessment as JSON."""
        return self.assessment
