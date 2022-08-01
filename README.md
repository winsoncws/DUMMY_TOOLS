
### ISO/CE Compliant Validation Plan
this is the README.md file to illustrate the process of executing unit-test/integration-test for ISO/CE reporting.
Testing reports are essential for auditing purposes.

till date, for record-keeping, we will need to provide 3 reports (unit-test report, integration test report, and specification table ) for our company's Regulation Compliant Team

this repository is organised as (refactorisation is needed in future):

###### AI-Brain-MRI
- aibrainmri ## obsolete (use refactor/aibrainmri instead)
- refactor
  - aibrainmri
- test ( pytest to be run under QA's jenkins hook inside SonarCube platform)
- tests ( test configured by QA/PD team ))
- tests_resources ( test config by QA/PD team )
- __test_iso__
  - this is the pytest which will produce `ISO compliant` report, including:
  - <u>pass/fail test report</u> in html <br>
    (needed for QARA submission & auditing process)
  - <u>code-coverage report</u> in html <br>
    (report need not to be submit, but we aim to fulfil at least >70% code-coverage as required in UserAcceptanceTest)
  - generate URS_FS_DS Specification Table in html


To produce testing report for Regulation Team, we will focus on the scripts under `/test_iso/`.

#### Short Intro for Quality Management System in Product Design & Development (D&D)

&emsp; Our company implements `"V-cycle"` as our Design & Development life-cycle.
We first design the `User Requirement Specification (URS)` of the product (e.g. able to help end-user detect stroke patient). <br>
&emsp; Next, within URS, we draft a list of functions which will be provided in user-interface (e.g. to provide stroke segmentation in user-view; to provide a quantitative report ), inside `Functional Specification (FS)`. <br>
&emsp; Finally each has its own `Design Specs (DS)`, e.g. <i>to preprocess image, to perform imaging analysis, to post-process segmentation mask</i>.

Each Specification level is coupled with its Validation Test.

```
--> URS ---------------> UAT    UserAcceptanceTest
      \                  /
      FS ------------> IT       IntegrationTest
        \             /
         DS ------> UT          UnitTest

```
There are certain rules to comply:
- Each specification has it running number-code:
```
  - URS : "URS000001ML"
  - FS  :  "FS000201ML"
  - DS  :  "DS010201ML"
```
- each `DS number` must have one unit-test. Hence in UT report, each unit-test will state its test-number-code with exact match to DS specs-number.
- for IntegrationTest report, usually it implies that we have a workable API, and tested able to be initiated by ```api.__call__``` method, e.g.
```
  # integration test
  from repo import API
  api = API(mode="develop")
```


To execution unit-testing, we need to install relevant pip packages.
```
below are those pip packages needed to run pytest and generate html-report and code coverage.
the current version I am using:

pytest                        7.1.1
pytest-cov                    3.0.0
pytest-html                   3.1.1
pytest-metadata               2.0.2

```

To generate unit-test report:
```
cd AI-Brain-MRI

1) UT
pytest test_iso -v -m unittest  
# above command-line produces UT report and code-coverage in
# test_iso/test_report/pytest_report_unit_test.html
# test_iso/test_report/coverage/index.html
NOTE: inside Davinci server, the working pytest will be:
 - CUDA_VISIBLE_DEVICES=7 /cm/shared/anaconda3/bin/pytest  test_iso -v -m unittest

2) IT
pytest test_iso -v -m integrationtest  
# above command-line produces UT report and code-coverage in
# test_iso/test_report/pytest_report_integration.html
# test_iso/test_report/coverage/index.html ( this has less coverage, hence please use code-coverage from unittest)
NOTE: inside Davinci server, the working pytest will be:
 - CUDA_VISIBLE_DEVICES=7 /cm/shared/anaconda3/bin/pytest  test_iso -v -m integrationtest

3) Specs Table
# to generate UR_FS_DS Specification table
cd AI-Brain-MRI/test_iso
python generate_specs.py
# above command-line produces specs-table in:
# test_iso/specs_iso_ce/xxxx.html

NOTE: executing `pytest` will only trigger `test` folder inside AI-Brain-MRI. This is ran by QA stage in github jenkins hook.

```
__FUTURE PLAN :__ refactor script into one test folder which can be executed in both ISO/CE test and Production Jenkins Test.


----


### More about how to maintain pytest

there are a few important files which are essential for pytest configuration:
```

AI-Brain-MRI
  |- test_iso
     |- conftest.py
     |- pytest.ini
     |- specs_iso_ce
        |- design_specs_biomindX.X.yaml
     |- .coveragerc
  |- conftest.py (NOTE: only for github jenkins, not for ISO/CE pytest)
  |- pytest.ini  (NOTE: only for github jenkins, not for ISO/CE pytest)


```

`pytest.ini` contains the main configuration settings, e.g. which folder is used for test, logging-level, location of report is saved, etc.

`.coveragerc` contains which folder to be covered in code-coverage, which to be omitted, excluded.

###### `conftest.py`
- contains script to:
  - handle to pytest command-line argument
  - pre-initialize api, testdata, which can be pass to other unit-test testscript.
  - handle the test_input/test_output to be fill into reports
  - configure the rows and columns of the html-reports

###### `design_specs_biomindX.X.yaml`
- contains the hierarchical structure of URS, FS, DS and their respective specs running_number & description.
- to better overview the yaml file, run `generate_specs.py` to produce a html table, as shown below:

|     | URS | FS  | DS  |
| --- | --- | --- | --- |
| URS000008ML | To predict lesion xxx |--- |--- |
| FS000108ML  |  | To produce segmentation |--- |
| DS010108ML  |  |  | preprocess image     |
| DS020108ML  |  |  | analyse image        |
| DS030108ML  |  |  | postprocess model output |
| FS000208ML  |  | To produce report       |--- |
| DS010208ML  |  |  | get tumor class      |
| DS020208ML  |  |  | get volume           |
| DS030208ML  |  |  | get lesion location  |

- inside each DS (DESIGN tag) contains a list of (DS_CODE, TEST, DESC)
- unit-test test_number has to be identical with DS specs_number. Both are matched together via `TEST` inside list of DESIGN. Value of `TEST` is name of the pytest test_function. For example:

```
test_script.py
@pytest.mark.unittest()
def test_lesion_segmentation():
    pass

design_specs.yaml
DESIGN :
  - DS_CODE : "DS040209ML"
    TEST    : "test_lesion_segmentation" # NOTE: same name as test function
    DESC    : "to produce binary mask of lesion segmentation"

`TEST` can accept a list of functions concat in strings via comma separation.
    TEST : "test_lesion_1, test_lesion_2"

```


All above files (conftest.py, pytest.ini, .covearagerc, xxx.yaml ), can be edited to suit different ISO/CE record-keeping requirement.



Till date, ISO/CE certified Biomind2.0 product use `release/2.20` from this repo : `git checkout release/2.20` <br>
Whereas,  ISO/CE certified Biomind3.0 product use `release/2.17` from this repo, instead : `git checkout release/2.17` <br>
Hence, do maintain this 2 git branches accordingly.





----
