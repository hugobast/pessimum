from mock import Mock
from time import sleep, time
from unittest import TestCase
from pessimum.utils.lazy import lazy_property
from pessimum.durations_report import DurationsReport


class TestDurationsReport(TestCase):

    def setUp(self):
        self.test = Mock(name="Test")

    @lazy_property
    def durations(self):
        return DurationsReport()

    def asssert_time_almost_equal_now(self, the_time):
        return self.assertAlmostEqual(time(), the_time, 4)

    def run_with_duration(self, duration, a_test=Mock(name="Test")):
        self.durations.start(a_test)
        sleep(duration)
        self.durations.end(a_test)

    def test_registering_test_has_a_start_time(self):
        self.durations.start(self.test)

        self.asssert_time_almost_equal_now(
            self.durations.find_test(self.test).start_time
        )

    def test_finishing_test_adds_end_time_on_test(self):
        self.durations.start(self.test)
        self.durations.end(self.test)

        self.asssert_time_almost_equal_now(
            self.durations.find_test(self.test).end_time
        )

    def test_calculation_of_duration_for_a_test(self):
        self.run_with_duration(0.01, self.test)

        self.assertAlmostEqual(
            0.01, self.durations.find_test(self.test).duration, 2
        )

    def test_with_many_runs(self):
        self.run_with_duration(0.02, Mock(name="Test"))
        self.run_with_duration(0.01, Mock(name="Test"))
        self.run_with_duration(0.03, Mock(name="Test"))

        test = iter(self.durations)

        self.assertAlmostEqual(0.02, test.next().duration, 2)
        self.assertAlmostEqual(0.01, test.next().duration, 2)
        self.assertAlmostEqual(0.03, test.next().duration, 2)
