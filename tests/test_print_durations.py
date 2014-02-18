from time import time
from unittest import TestCase
from mock import Mock, MagicMock
from pessimum.print_durations import PrintDurations
from pessimum.durations_report import DurationsReport
from pessimum.utils.lazy import lazy_property


class TestPrintDurations(TestCase):

    def test_print_durations_takes_a_list_of_durations(self):
        self.assertTrue(self.printer)

    def test_print_durations_header(self):
        self.printer.print_header()
        self.fake_stream.writeln.assert_any_call("Worst performing tests:")

    def test_sorts_durations_slowest_first(self):
        durations = self.printer.sorted_durations()
        self.assertEqual([4, 3, 2, 1], [int(test.duration) for test in durations])

    def test_print_durations_report_body(self):
        self.printer.print_body()

        self.fake_stream.writeln.assert_any_call(
            "        4.000s for Test with offset: 4"
        )

        self.fake_stream.writeln.assert_any_call(
            "        3.000s for Test with offset: 3"
        )

        self.fake_stream.writeln.assert_any_call(
            "        2.000s for Test with offset: 2"
        )

        self.fake_stream.writeln.assert_any_call(
            "        1.000s for Test with offset: 1"
        )

    def make_test(self, offset=1):
        test_case = MagicMock(name="Test")
        test_case.__unicode__.return_value = "Test with offset: {0}".format(offset)

        test = DurationsReport.Test(test_case )
        test.start_time = time()
        test.end_time = time() + offset
        return test

    @lazy_property
    def durations(self):
        durations = DurationsReport()
        durations.tests = [
            self.make_test(),
            self.make_test(offset=2),
            self.make_test(offset=3),
            self.make_test(offset=4)
        ]
        return durations

    @lazy_property
    def fake_stream(self):
        return Mock(name="stream")

    @lazy_property
    def printer(self):
        return PrintDurations(self.fake_stream, self.durations)
