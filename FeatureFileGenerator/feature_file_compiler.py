import argparse
import requester
import json
import re
from html import unescape
from pathlib import Path
from datetime import datetime


entity_types = {
    "Project": requester.project,
    "Feature": requester.feature,
    "TestPlan": requester.test_plan,
    "TestCase": requester.test_case
}


def main():
    parser = argparse.ArgumentParser(description="A script to compile a given Target Process entity into a Gherkin Feature File")
    parser.add_argument("entity", help="The target process entities needed to supply to the request e.g. '14383 27386' ", metavar="entity", type=str, nargs="+")
    parser.add_argument("-s", "--sprint_tag", help="Add tags to the feature file that indicate when the Linked Assignable of a test case was completed", action="store_true")
    parser.add_argument("-i", "--id_tag", help="Add a tag showing the Target Process test case ID", action="store_true")
    parser.add_argument("-u", "--user_tags", help="Add user specified tags to all test cases", type=str, nargs="+")
    parser.add_argument("-t", "--target_process_tags", help="Add tags from Target Process to cards", action="store_true")
    parser.add_argument("-x", "--exempted_tags", help="Specify Target Process tags that you wish to exempt", type=str, nargs="+")
    parser.add_argument("-f", "--feature", help="If one (or more) of the given entities is a project, it will broken down it's features", action="store_true")
    parser.add_argument("-l", "--last_run", help="Add the date/time the test was last run, along with the result", action="store_true")
    args = parser.parse_args()

    for tp_entity_id in args.entity:
        ff = FeatureFileCompiler(tp_entity_id, args)
        ff.initialise_entity_type()
        ff.initialise_entity_name()
        ff.initialise_all_test_cases()
        ff.feature_file_maker()
        ff.feature_file_writer()


class FeatureFileCompiler():
    def __init__(self, tp_id, args):
        self.tp_id = tp_id
        self.args = args
        self.feature = []

    def initialise_entity_type(self):
        self.entity_type = requester.entity_type_getter(self.tp_id)

    def initialise_all_test_cases(self):
        self.test_cases = entity_types[self.entity_type](self.tp_id)

    def initialise_entity_name(self):
        if(self.entity_type == "TestCase"):
            self.entity_name = "Test Case " + self.tp_id
        else:
            self.entity_name = requester.entity_name_getter(self.tp_id)
    
    def feature_file_maker(self):
        for test_case in self.test_cases:
            self.tag_formatter(test_case)
            if(self.args.last_run and "LastRunDate" in test_case):
                self.last_run_data(test_case)
            self.feature.append(FeatureFileCompiler.title_formatter(test_case["Name"]))
            for test_step in test_case["TestSteps"]["Items"]:
                self.test_body_formatter(FeatureFileCompiler.strip_html(test_step["Description"]),
                                        FeatureFileCompiler.strip_html(test_step["Result"]))
            self.feature.append("")
    
    def feature_file_writer(self):
        try:
            feature_name = self.entity_name.split(": ")[1] + ".feature"
        except:
            feature_name = self.entity_name + ".feature"
        base_path = Path(__file__).parent
        file_path = (base_path / feature_name).resolve()

        with open(file_path, "w+", encoding="utf-8") as f:
            f.write("Feature: " + self.entity_name + "\n\r")
            for line in self.feature:
                line = line.replace(u"\u200b", "")
                line = line.replace(u"\u02da", "°")
                f.write(line + "\n")

    def tag_formatter(self, test_case):
        tags = ""
        if(self.args.user_tags):
            for tag in self.args.user_tags:
                self.feature.append("@" + tag.strip().replace(" ", "_"))
        if(self.args.sprint_tag):
            try:
                self.feature.append("@" + test_case["TestPlans"]["Items"][0]["LinkedAssignable"]["Iteration"]["Name"].replace(" ", "_"))
            except:    
                self.feature.append("@no_sprint")
        if(self.args.id_tag):
            self.feature.append("@TP_" + str(test_case["Id"]))
        if(self.args.target_process_tags):
            if(not test_case["Tags"]):
                return
            for tag in test_case["Tags"].split(", "):
                if(self.args.exempted_tags):
                    if(tag.replace(" ", "_") in self.args.exempted_tags):
                        continue
                tags += "@" + tag.replace(" ", "_") + " "
            self.feature.append(tags)

    def test_body_formatter(self, description, result):
        if("Examples" in description):
            self.feature.append("")
        if(description != ""):
            self.feature.append(description)
        if(result != ""):
            self.feature.append(result)
    
    def last_run_data(self, test_case):
        last_run_date = test_case["LastRunDate"]
        last_run_status = test_case["LastRunStatus"]
        self.feature.append("@{}_{}".format(last_run_status, self.date_time_formatter(last_run_date)).replace(" ", "_"))

    @staticmethod
    def date_time_formatter(date_time):
        try:
            formatted_date_time = int(date_time.split("(")[1][:10])
            return datetime.fromtimestamp(formatted_date_time).strftime('%d-%m-%Y')
        except:
            return "N/A"

    @staticmethod
    def title_formatter(test_title):
        if("Scenario: " not in test_title and "Scenario Outline: " not in test_title): 
            return "Scenario: " + test_title
        else:
            return test_title

    @staticmethod
    def strip_html(line):
        if not line:
            return line
        html_tags = re.compile(r"<[^>]*>")
        line = html_tags.sub("", line)
        return unescape(line.replace("&nbsp;", " "))


if __name__ == "__main__":
    main()
