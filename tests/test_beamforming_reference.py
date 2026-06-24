"""Regression tests for the board-independent acoustic arithmetic reference."""

import unittest

from tools.beamforming_reference import (
    ENERGY_DELTA_WIDTH,
    MICROPHONE_COUNT,
    SAMPLE_WIDTH,
    VRAM_WIDTH,
    accumulate_vram,
    beam_energy,
    energy_delta,
    interpolate,
    ring_index,
)


class InterpolationTests(unittest.TestCase):
    def test_zero_fraction_returns_left_sample(self) -> None:
        self.assertEqual(interpolate(123, -456, 0), 123)

    def test_one_thirty_second_fraction(self) -> None:
        self.assertEqual(interpolate(0, 32, 1), 1)

    def test_thirty_one_thirty_seconds_fraction(self) -> None:
        self.assertEqual(interpolate(0, 32, 31), 31)

    def test_negative_samples_use_arithmetic_shift(self) -> None:
        self.assertEqual(interpolate(-32, 0, 1), -31)

    def test_rejects_out_of_range_sample_and_fraction(self) -> None:
        with self.assertRaises(ValueError):
            interpolate(1 << (SAMPLE_WIDTH - 1), 0, 0)
        with self.assertRaises(ValueError):
            interpolate(0, 0, 32)


class BeamformingTests(unittest.TestCase):
    def test_energy_sums_all_sixteen_channels_before_squaring(self) -> None:
        self.assertEqual(beam_energy([3] * MICROPHONE_COUNT), 48**2)

    def test_energy_is_independent_of_sum_sign(self) -> None:
        self.assertEqual(beam_energy([-7] * MICROPHONE_COUNT), 112**2)

    def test_energy_delta_subtracts_history(self) -> None:
        self.assertEqual(
            energy_delta([2] * MICROPHONE_COUNT, [1] * MICROPHONE_COUNT),
            32**2 - 16**2,
        )

    def test_energy_delta_is_signed_55_bit_value(self) -> None:
        self.assertEqual(energy_delta([0] * MICROPHONE_COUNT, [1] * MICROPHONE_COUNT), -256)
        self.assertLess(-(1 << (ENERGY_DELTA_WIDTH - 1)), 0)


class VramAndRingTests(unittest.TestCase):
    def test_vram_accumulates_positive_and_negative_deltas(self) -> None:
        self.assertEqual(accumulate_vram(100, 25), 125)
        self.assertEqual(accumulate_vram(100, -125), -25)

    def test_vram_uses_signed_64_bit_wraparound(self) -> None:
        self.assertEqual(accumulate_vram((1 << (VRAM_WIDTH - 1)) - 1, 1), -(1 << (VRAM_WIDTH - 1)))

    def test_ring_index_wraps_for_old_samples(self) -> None:
        self.assertEqual(ring_index(0, 1, 4096), 4095)
        self.assertEqual(ring_index(3, 7, 32), 28)


if __name__ == "__main__":
    unittest.main()
