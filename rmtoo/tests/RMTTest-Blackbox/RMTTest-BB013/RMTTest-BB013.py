'''
 rmtoo
   Free and Open Source Requirements Management Tool

  Blackbox rmtoo test

 (c) 2010-2012,2017 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

import os
import unittest

from rmtoo.lib.RmtooMain import main_func
from rmtoo.tests.lib.BBHelper import prepare_result_is_dir, \
    cleanup_std_log, delete_result_is_dir, check_file_results

mdir = "tests/RMTTest-Blackbox/RMTTest-BB013"


class RMTTest_BB007(unittest.TestCase):

    def rmttest_pos_001(self):
        "BB Basic with one requirement - graph output with defined tags"

        os.environ["basedir"] = mdir
        mout, merr = prepare_result_is_dir()
        main_func(["-j", "file://" + mdir + "/input/Config.json"],
                  mout, merr)
        cleanup_std_log(mout, merr)
        check_file_results(mdir)
        delete_result_is_dir()