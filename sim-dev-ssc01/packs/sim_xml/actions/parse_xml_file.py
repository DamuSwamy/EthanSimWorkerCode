import os

import xmltodict

from st2common.runners.base_action import Action

__all__ = [
    'ParseXMLFileAction'
]


class ParseXMLFileAction(Action):
    def run(self, file_path):
        if not os.path.isfile(file_path):
            raise ValueError('File "%s" doesn\'t exist' % (file_path))

        with open(file_path) as fp:
            content = fp.read()

        result = xmltodict.parse(content)
        return result
