import urllib.request
import json
from settings import tp_uri, token

class EntityRequester():
    def __init__(self, entity):
        self.tp_uri = tp_uri
        self.token = token
        self.entity = entity

    def get_entity(self):
        request = urllib.request.Request(self.tp_uri + self.entity + "&access_token=" + self.token)
        response = urllib.request.urlopen(request)
        self.response = json.loads(response.read().decode("UTF-8"))


class TestCaseEntityRequester():
    def __init__(self, entity, include, formatted):
        self.request_uri = tp_uri + entity + formatted + "&include=" + include + "&access_token=" + token

    def get_entity(self):
        request = urllib.request.Request(self.request_uri)
        self.response = json.loads(urllib.request.urlopen(request).read().decode("UTF-8"))
        return self.response


class ProjectEntityRequester(TestCaseEntityRequester):
    def __init__(self, entity, include, formatted):
        super().__init__(entity, include, formatted)
        self.test_cases = []

    def get_entity(self):
        request = urllib.request.Request(self.request_uri)
        self.response = json.loads(urllib.request.urlopen(request).read().decode("UTF-8"))
        self.append_response_to_test_cases()
        while(1):
            if("Next" in self.response):
                next_getter = EntityRequester(self.response["Next"].split("v1/")[1].replace(" ", "%20"))
                next_getter.get_entity() 
                self.response = next_getter.response
                self.append_response_to_test_cases()
            else:
                break
        return self.test_cases

    def append_response_to_test_cases(self):
        for test_case in self.response["Items"]:
            self.test_cases.append(test_case)


def entity_name_getter(entity):
    entity_name_getter = EntityRequester("Generals/" + entity + "/?format=json&include=[Name]")
    entity_name_getter.get_entity()
    return entity_name_getter.response["Name"]
    

def entity_type_getter(entity):
    entity_getter = EntityRequester("Generals/" + entity +  "/?format=json&include=[EntityType]")
    entity_getter.get_entity()
    return entity_getter.response["EntityType"]["Name"]


def test_plan_id_getter(entity_name_and_id):
    pass


def test_case_id_getter(entity_name_and_id):
    pass


def project(entity):
    entity_name_and_id = "testcases?where=Project.id%20in%20(" + entity + ")&take=2000&skip=0"
    project_getter = ProjectEntityRequester(entity_name_and_id, "[Name,Tags,TestSteps[Description,Result],TestPlans[LinkedAssignable[Iteration]]]", "&format=json")
    project = project_getter.get_entity()
    return project


def feature(entity):
    entity_name_and_id = "Feature/" + entity
    feature_getter = EntityRequester(entity_name_and_id + "/?format=json&include=[LinkedTestPlan]")
    feature_getter.get_entity()
    feature_test_plan_id = feature_getter.response["LinkedTestPlan"]["Id"]
    return test_plan(feature_test_plan_id)


def test_plan(entity):
    entity_name_and_id = "TestPlan/" + str(entity)
    test_plan_getter = EntityRequester(entity_name_and_id + "/?format=json&include=[Name,TestCases,ChildTestPlans]")
    test_case_ids = []
    try:
        test_plan_getter.get_entity()
        for test in test_plan_getter.response["TestCases"]["Items"]:
            test_case_ids.append(test["Id"])
        for child_test_plan in test_plan_getter.response["ChildTestPlans"]["Items"]:
            test_plan_getter.entity = "TestPlan/" + str(child_test_plan["Id"]) + "/?format=json&include=[Name,TestCases]"
            test_plan_getter.get_entity()
            for test in test_plan_getter.response["TestCases"]["Items"]:
                test_case_ids.append(test["Id"])
    except:
        test_plan_getter.entity = entity_name_and_id + "/?format=json&include=[Name,TestCases]"
        test_plan_getter.get_entity()
        for test in test_plan_getter.response["TestCases"]["Items"]:
            test_case_ids.append(test["Id"])
    tp_test_steps = []
    for item in test_case_ids:
        tp_test_steps += test_case(item)
    return tp_test_steps

    
def test_case(entity):
    test_cases = []
    entity_name_and_id = "TestCase/" + str(entity)
    test_case_getter = TestCaseEntityRequester(entity_name_and_id, "[Name,Tags,TestSteps[Description,Result]]", "/?format=json")
    test_cases.append(test_case_getter.get_entity())
    return test_cases
