import xmltodict

from st2common.runners.base_action import Action

__all__ = [
    'ParseXMLAction'
]


class ParseXMLAction(Action):
    def run(self, data):
        result = xmltodict.parse(data)
        return result
