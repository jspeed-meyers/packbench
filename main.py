import os

import pandas as pd

import assess
import ingest

# TODO: Experiment with shell diff
# TODO: Experiment with BLEU score
# TODO: Run melange and see if it builds
# TODO: Run yam and see if it passes
# TODO: Run wolfictl lint and see if it passes
# TODO: Add testing
# TODO: Add CI/CD test
# TODO: Add pylint to CI CD
# TODO: Add black to CI/CD

# list all file names in expected directory
expected_filenames = os.listdir("test_expected") #.remove("README")
results = []
for filename in expected_filenames:
    # collect path and filenames of matching expected and got files
    expected_file = os.path.join("test_expected", filename)
    got_file = os.path.join("test_got", filename)
    # ingest melange YAML file pair
    expected_myaml = ingest.mYAML(expected_file)
    got_myaml = ingest.mYAML(got_file)
    # compare the fields of the melange YAML file pair
    assessment = assess.Assess(expected_myaml.fields, got_myaml.fields)
    # add assessment to a list
    results.append(assessment.output_dict())    

# convert JSON list to a pandas dataframe
df = pd.DataFrame(results)

#df = df.astype(int)

# print dataframe descriptive statistics
print(df)

# output dataframe to CSV


