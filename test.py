import os
import unittest

import assess
import ingest

# TODO: this testing is not yet thorough


class TestIngestMethods(unittest.TestCase):
    def test_ingest_mYAML_go_bindata(self):
        """Test the ingest.mYAML class."""
        got = ingest.mYAML("test_got/go-bindata.yaml")
        assert got.fields["valid_yaml"] == True
        assert got.fields["name"] == "BANANAS"
        assert got.fields["version"] == "3.1.2"
        assert got.fields["license"] == ["Apache-2.0"]
        assert got.fields["strip_statement"]
        assert got.fields["key_melange_fields_exist"]
        assert got.fields["env_packages"] == [
            "TEST",
            "busybox",
            "ca-certificates-bundle",
            "go",
        ]
        assert (
            got.fields["fetch_uri"]
            == "https://github.com/go-bindata/go-bindata/archive/v${{package.version}}.tar.gz"
        )

    def test_ingest_mYAML_cloudflared(self):
        """Test the ingest.mYAML class."""
        got = ingest.mYAML("test_got/cloudflared.yaml")
        assert got.fields["valid_yaml"] == True
        assert got.fields["name"] == "cloudflared"
        assert got.fields["version"] == "2023.5.1"
        assert got.fields["license"] == ["Apache-2.0"]
        assert got.fields["strip_statement"]
        assert got.fields["key_melange_fields_exist"]
        assert got.fields["env_packages"] == [
            "busybox",
            "ca-certificates-bundle",
            "wolfi-baselayout",
        ]
        # ensure that fetch_uri is not being set because cloudflared.yaml
        # does not include this value
        assert "fetch_uri" not in got.fields


class TestAssessMethods(unittest.TestCase):
    def test_assess_class(self):
        """Test the assess.Assess class."""
        expected_file = os.path.join("test_expected", "go-bindata.yaml")
        got_file = os.path.join("test_got", "go-bindata.yaml")
        expected_myaml = ingest.mYAML(expected_file)
        got_myaml = ingest.mYAML(got_file)
        assessment = assess.Assess(expected_myaml.fields, got_myaml.fields)
        assert assessment.assessment["valid_yaml"]
        assert assessment.assessment["strip_statement"]
        assert assessment.assessment["key_melange_fields_exist"]
        assert assessment.assessment["dict_fields"]
        assert assessment.assessment["name"] is not True
        assert assessment.assessment["version"] is not True


if __name__ == "__main__":
    unittest.main()
