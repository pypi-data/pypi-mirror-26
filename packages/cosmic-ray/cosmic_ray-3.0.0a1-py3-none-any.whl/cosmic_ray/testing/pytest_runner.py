import os
import pytest

from .test_runner import TestRunner
from cosmic_ray.util import redirect_stdout


class ResultCollector:
    def __init__(self):
        self.reports = []

    def pytest_runtest_logreport(self, report):
        self.reports.append(report)


class PytestRunner(TestRunner):
    """A TestRunner using pytest.

    This treats `test_args` as a single string. It splits this string and
    passes the result to `pytest.main()`. The args are passed directly to that
    function, so see it's documentation for a description of how the arguments
    are used.

    """

    def _run(self):
        collector = ResultCollector()

        with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
            pytest.main(self.test_args.split(),
                        plugins=[collector])

        return (
            all(not r.failed for r in collector.reports),
            [(repr(r), r.longreprtext) for r in collector.reports if r.failed])
