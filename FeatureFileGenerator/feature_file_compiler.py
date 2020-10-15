import argparse
import requester
import json
import re
from html import unescape
from pathlib import Path


entity_types = {
    "Feature": requester.feature,
    "TestPlan": requester.test_plan,
    "TestCase": requester.test_case
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entity", help="The target process entity needed to supply to the request e.g. \'TestPlans/27932\'", type=str, nargs="+")
    args = parser.parse_args()

    for tp_entity_id in args.entity:
        entity = requester.entity_type_getter(tp_entity_id)
        entity_type = entity_checker(entity)
        feature = feature_file_maker(entity_type, tp_entity_id)
        name = json.loads(requester.feature_name_getter(tp_entity_id))["Name"]
        feature_as_list = []
        feature_file = test_stepper(feature, feature_as_list)
        feature_file_printer(feature_file, name)


def entity_checker(entity):
    json_entity = json.loads(entity)
    return json_entity["EntityType"]["Name"]


def strip_html(line):
    if not line:
        return line
    html_tags = re.compile(r"<[^>]*>")
    line = html_tags.sub("", line)
    return unescape(line.replace("&nbsp;", " "))


def feature_file_printer(feature_as_list, name):
    feature_name = name + ".feature"
    base_path = Path(__file__).parent
    file_path = (base_path / "../behave/features/" / feature_name).resolve()

    with open(file_path, "w+") as f:
        f.write("Feature: " + name + "\n\r")
        for line in feature_as_list:
            f.write(line + "\n")


def feature_file_maker(entity_type, tp_entity_id):
    test_cases = entity_types[entity_type](tp_entity_id)
    return test_cases


def test_stepper(test_cases, feature_as_list):
    test_cases_unloaded = []
    for test_case in test_cases:
        test_cases_unloaded.append(json.loads(test_case))

    for test_case in test_cases_unloaded:
        feature_as_list.append(test_case["Name"])
        for test_step in test_case["TestSteps"]["Items"]:
            description = test_step["Description"]
            if "Examples" in description:
                table = description.split("|")
                for line in table:
                    if strip_html(line) != "":
                        if "Examples:" not in line:
                            line = "|" + line + "|"
                        feature_as_list.append(strip_html(line))
            else:
                feature_as_list.append(strip_html(description))
        feature_as_list.append("")
    return feature_as_list


if __name__ == "__main__":
    main()
