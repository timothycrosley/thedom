'''
    test_Benchmark.py

    Tests the results of benchmark_thedom.py against project performance metrics

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

try:
    import cPickle as pickle
except ImportError:
    import pickle

import os
import subprocess
import sys


class Testthedom_Benchmark(object):

    def run_benchmark(self):
        subprocess.Popen("python benchmark_thedom.py", shell=True).wait()
        with open(".test_thedom_Benchmark.results") as resultFile:
            if sys.version >= "3":
                results = pickle.loads(bytes(resultFile.read(), 'utf8'))
            else:
                results = pickle.loads(resultFile.read())
        os.remove(".test_thedom_Benchmark.results")
        return results

    def test_benchmark(self):
        results = self.run_benchmark()
        assert(results['loopedCreate'] < 20.0)
        assert(results['longestCreationTime'] < 0.010)
        assert(results['createAllOnce'] < 0.250)
