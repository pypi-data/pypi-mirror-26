# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and 
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2017, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#
"""
Entry point for all tests.

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
"""

import os
import sys
from coverage import coverage


KEY_CONSOLE = 'console'
KEY_COVERAGE = 'coverage'
KEY_XML = 'xml'



def generate_excludes(root_folders):
    """
    Specify excludes for Coverage.
    """
    excludes = []
    for root in root_folders:
        for root, _, files in os.walk(root):
            for file_n in files:
                full_path = os.path.join(root, file_n)
                if (full_path.endswith('__init__.py') or
                    os.path.join('interfaces', 'web', 'static') in full_path or
                    os.path.join('interfaces', 'web', 'templates') in full_path or
                    os.path.join('entities', 'model', 'db_update_scripts') in full_path):
                    excludes.append(full_path)
    return excludes


def setup_test_env():

    from tvb.basic.profile import TvbProfile
    if len(sys.argv) > 1:
        profile = sys.argv[1]
    else:
        profile = TvbProfile.TEST_SQLITE_PROFILE
    TvbProfile.set_profile(profile)



if __name__ == "__main__":
    #Start all TVB tests (if in Coverage mode)
    if KEY_COVERAGE in sys.argv:
        import tvb.interfaces as intf

        SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(intf.__file__)))
        print('Starting coverage on ' + SOURCE_DIR)
        COVERAGE = coverage(source=["tvb.adapters", "tvb.analyzers", "tvb.config", "tvb.core", "tvb.datatype_removers",
                                    "tvb.interfaces.web.controllers", "tvb.interfaces.web.entities"],
                            omit=generate_excludes([SOURCE_DIR]), cover_pylib=False, branch=True)
        COVERAGE.start()
        ## This needs to be executed before any TVB import.

setup_test_env()
import unittest
import datetime
from tvb.basic.profile import TvbProfile
from tvb.tests.framework.xml_runner import XMLTestRunner
from tvb.tests.framework.core import core_tests_main
from tvb.tests.framework.adapters import adapters_tests_main
from tvb.tests.framework.analyzers import bct_test
from tvb.tests.framework.interfaces.web import web_tests_main



def suite():
    """
    Gather all the tests in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(core_tests_main.suite())
    test_suite.addTest(adapters_tests_main.suite())
    test_suite.addTest(bct_test.suite())
    test_suite.addTest(web_tests_main.suite())
    return test_suite



if __name__ == "__main__":
    #Start all TVB tests
    START_TIME = datetime.datetime.now()

    if KEY_CONSOLE in sys.argv:
        TEST_RUNNER = unittest.TextTestRunner()
        TEST_SUITE = suite()
        TEST_RUNNER.run(TEST_SUITE)

    if KEY_XML in sys.argv:
        XML_STREAM = open(os.path.join(TvbProfile.current.TVB_LOG_FOLDER, "TEST-RESULTS.xml"), "w")
        OUT_STREAM = open(os.path.join(TvbProfile.current.TVB_LOG_FOLDER, "TEST.out"), "w")
        TEST_RUNNER = XMLTestRunner(XML_STREAM, OUT_STREAM)
        TEST_SUITE = suite()
        TEST_RUNNER.run(TEST_SUITE)
        XML_STREAM.close()
        OUT_STREAM.close()

    print('It run tests for %d sec.' % (datetime.datetime.now() - START_TIME).seconds)

    if KEY_COVERAGE in sys.argv:
        print('Gathering cobertura report ...')
        COVERAGE.stop()
        COVERAGE.xml_report(outfile=os.path.join(TvbProfile.current.TVB_LOG_FOLDER, 'coverage.xml'))

