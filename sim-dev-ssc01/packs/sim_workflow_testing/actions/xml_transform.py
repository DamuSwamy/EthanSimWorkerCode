from __future__ import absolute_import
import sys
sys.path.append("home/ssadmin/install/libsaxon-HEC-11.3/Saxon.C.API/python-saxon")
from saxonc import *

from st2common.runners.base_action import Action

__all__ = ["XsltTransform"]


class XsltTransform(Action):
    def run(self, xml, xslt):
        with PySaxonProcessor(license=False) as proc:

            print("SaxonC Sample in Python")
            print(proc.version)
            #print(dir(proc))
            xdmAtomicval = proc.make_boolean_value(False)

            xsltproc = proc.new_xslt30_processor()

            document = proc.parse_xml(xml_text=xml)

            executable = xsltproc.compile_stylesheet(stylesheet_text=xslt)
            if(executable == None):
                print('Executable is None\n')
                if(xsltproc.exception_occurred):
                    print("Error message:"+ xsltproc.error_message)
                    exit()
            executable.set_global_context_item(xdm_item=document)

            output2 = executable.call_template_returning_string("main")
            print(output2)

            return output2
