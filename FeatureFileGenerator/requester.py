import urllib.request
import json


class Requester():
    def __init__(self, entity, include):
        self.tp_uri = "https://bluefruit.tpondemand.com/api/v1/"
        self.token = "NTE6V0FMZWJ1c2dkTkZ1aDVKdzRSM0FHSGFYM3pJd0IraUhnR016UzRqS0NiUT0="
        self.entity = entity
        self.include = include

    def get_entity(self):
        request = urllib.request.Request(self.tp_uri + self.entity + "/?format=json&include=" + self.include + "&access_token=" + self.token)
        response = urllib.request.urlopen(request)
        return response.read().decode("UTF-8")


def feature_name_getter(entity):
    feature_name_getter = Requester("Generals/" + entity, "[Name]")
    feature_name = feature_name_getter.get_entity()
    return feature_name


def entity_type_getter(entity):
    entity_getter = Requester("Generals/" + entity, "[EntityType]")
    entity_type = entity_getter.get_entity()
    return entity_type


def test_plan_id_getter(entity_name_and_id):
    pass


def test_case_id_getter(entity_name_and_id):
    pass


def feature(entity):
    entity_name_and_id = "Feature/" + entity
    feature_getter = Requester(entity_name_and_id, "[LinkedTestPlan]")
    feature = json.loads(feature_getter.get_entity())
    feature_test_plan_id = feature["LinkedTestPlan"]["Id"]
    return test_plan(feature_test_plan_id)


def test_plan(entity):
    entity_name_and_id = "TestPlan/" + str(entity)
    test_plan_getter = Requester(entity_name_and_id, "[Name,TestCases]")

    test_cases = json.loads(test_plan_getter.get_entity())
    tp_test_steps = []
    for item in test_cases["TestCases"]["Items"]:
        tp_test_steps.append(test_case(item["Id"]))
    return tp_test_steps

    
def test_case(entity):
    entity_name_and_id = "TestCase/" + str(entity)
    test_case_getter = Requester(entity_name_and_id, "[Name,TestSteps[Description]]")
    return test_case_getter.get_entity()
