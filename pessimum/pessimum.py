
class Pessimum(object):

    times = []
    enabled = False

    def before_test(self, test):
        pass

    def after_test(self, test):
        pass

    def report(self, report):
        pass

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