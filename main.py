import os

import pandas as pd

import assess
import ingest

# TODO: Run melange and see if it builds
# TODO: Run yam and see if it passes
# TODO: Run wolfictl lint and see if it passes
# TODO: Add CLI
# TODO: Experiment with shell diff
# TODO: Experiment with BLEU score
# TODO: Add pylint to CI/CD
# TODO: Consider adding subpackage support


# list all file names in expected directory
expected_filenames = os.listdir("expected")
# remove README (included to enable directory to be tracked by git)
expected_filenames.remove("README")

results = []
for filename in expected_filenames:
    # collect path and filenames of matching expected and got files
    expected_file = os.path.join("expected", filename)
    got_file = os.path.join("got", filename)
    # ingest melange YAML file pair
    expected_myaml = ingest.mYAML(expected_file)
    got_myaml = ingest.mYAML(got_file)
    # compare the fields of the melange YAML file pair
    assessment = assess.Assess(expected_myaml.fields, got_myaml.fields)
    # add assessment to a list
    results.append(assessment.output_dict())

# convert JSON list to a pandas dataframe
df = pd.DataFrame(results)

# make True's equal to 1 and False's equal to 0
df = df.replace({True: 1, False: 0})

# print dataframe descriptive statistics
for column in df.columns:
    print(f"{column}: {df[column].mean()}")

# output dataframe to CSV
df.to_csv("results.csv", index=False, na_rep="NaN")
