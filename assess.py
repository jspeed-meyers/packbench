import json


class Assess:
    def __init__(self, expected, got):
        """Compare fields of two mYAML objects."""
        self.assessment = {}

        # focus on the fields specific to the "got" YAML, the
        # predicted YAML
        self.assessment["valid_yaml"] = got["valid_yaml"]
        self.assessment["strip_statement"] = got["strip_statement"]
        self.assessment["key_melange_fields_exist"] = got["key_melange_fields_exist"]

        # a comparison of fields between the expected YAML (the "ground truth")
        # YAML and the got (or predicted) YAML
        self.assessment["dict_fields"] = expected["dict_fields"] == got["dict_fields"]
        self.assessment["name"] = expected["name"] == got["name"]
        self.assessment["version"] = expected["version"] == got["version"]
        self.assessment["epoch"] = expected["epoch"] == got["epoch"]
        self.assessment["description"] = expected["description"] == got["description"]
        self.assessment["license"] = expected["license"] == expected["license"]
        self.assessment["env_packages"] = (
            expected["env_packages"] == got["env_packages"]
        )
        if "fetch_uri" in expected:
            self.assessment["fetch_uri"] = expected["fetch_uri"] == got["fetch_uri"]
        if "fetch_sha512" in expected:
            self.assessment["fetch_sha512"] = (
                expected["fetch_sha512"] == got["fetch_sha512"]
            )

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
