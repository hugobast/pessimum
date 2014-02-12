from mock import Mock
from unittest import TestCase
from pessimum.pessimum import Pessimum
from pessimum.utils.lazy import lazy_property


class TestPessimum(TestCase):

    @lazy_property
    def pessimum(self):
        return Pessimum()

    def test_default_off(self):
        self.assertFalse(self.pessimum.enabled)

    def test_has_a_report_hook(self):
        self.pessimum.report(Mock(name="stream"))

    def test_has_option_to_enable_plugin(self):
        parser = Mock(name="parser")
        self.pessimum.options(parser, Mock(name="env"))
        parser.add_option.assert_called_with(
            "--slow-report",
            action="store_true",
            default=False,
            dest="slow_report",
            help="show the top 10 worst performing tests"
        )

    def test_configure_enables_the_plugin(self):
        options = Mock(name="options")
        options.slow_report = True
        self.pessimum.configure(options, Mock(name="conf"))
        self.pessimum.enabled = options.slow_report

    def test_before_and_after_test_registers_test_with_running_time(self):
        test = Mock(name="test")
        self.pessimum.before_test(test)
        self.pessimum.after_test(test)

        self.assertEqual(
            [(test, 0)], self.pessimum.times
        )