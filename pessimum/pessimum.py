from .utils.shims import PluginShim
from .durations_report import DurationsReport
from unittest.test.test_case import Test

class Pessimum(PluginShim):
    def __init__(self, durations_report=DurationsReport):
        self.stream = None
        self.durations_report = durations_report()
        super(Pessimum, self).__init__()

    def before_test(self, test):
        self.durations_report.start(test)

    def after_test(self, test):
        self.durations_report.end(test)

    def set_output_stream(self, stream):
        self.stream = stream

    def finalize(self, result):
        self.stream.write("Slowness report:\n\n")
        for test in self.times:
            self.stream.write("   ")
            self.stream.write("{0:10.3f} for ".format(test.duration))
            self.stream.write(unicode(test.reference))

            self.stream.write("\n")
        self.stream.write("\n")

    def options(self, parser, env):
        parser.add_option(
            "--slow-report",
            action="store_true",
            default=False,
            dest="slow_report",
            help="show the top 10 worst performing tests"
        )

    def configure(self, options, env):
        if options.slow_report:
            self.enabled = True

    @property
    def times(self):
        return list(self.durations_report)