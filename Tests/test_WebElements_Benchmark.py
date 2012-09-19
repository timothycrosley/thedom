import cPickle as pickle
import os
import subprocess

class TestWebElements_Benchmark(object):

    def run_benchmark(self):
        subprocess.Popen("python benchmark_WebElements.py", shell=True).wait()
        with open(".test_WebElements_Benchmark.results") as resultFile:
            results = pickle.loads(resultFile.read())
        os.remove(".test_WebElements_Benchmark.results")
        return results

    def test_benchmark(self):
        results = self.run_benchmark()
        assert(results['loopedCreate'] < 20.0)
        assert(results['longestCreationTime'] < 0.010)
        assert(results['createAllOnce'] < 0.250)

