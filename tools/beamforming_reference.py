"""Deterministic fixed-point reference operations for the acoustic pipeline.

This module models the arithmetic contract described in docs/BEAMFORMING_PIPELINE.md.
It is deliberately independent of Vivado and does not model HLS pipeline latency or
the board-specific delay-table generator.
"""

from __future__ import annotations

from collections.abc import Sequence


MICROPHONE_COUNT = 16
SAMPLE_WIDTH = 24
FRACTIONAL_DELAY_STEPS = 32
ENERGY_DELTA_WIDTH = 55
VRAM_WIDTH = 64


def signed(value: int, width: int) -> int:
    """Return *value* wrapped to a two's-complement integer of *width* bits."""
    if width <= 0:
        raise ValueError("width must be positive")
    mask = (1 << width) - 1
    value &= mask
    sign_bit = 1 << (width - 1)
    return value - (1 << width) if value & sign_bit else value


def require_signed(value: int, width: int, name: str) -> None:
    minimum = -(1 << (width - 1))
    maximum = (1 << (width - 1)) - 1
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must fit in signed {width} bits")


def interpolate(left: int, right: int, fraction: int) -> int:
    """Linearly interpolate two signed 24-bit samples at a 1/32-sample fraction."""
    require_signed(left, SAMPLE_WIDTH, "left")
    require_signed(right, SAMPLE_WIDTH, "right")
    if not 0 <= fraction < FRACTIONAL_DELAY_STEPS:
        raise ValueError("fraction must be in the range 0..31")
    result = ((FRACTIONAL_DELAY_STEPS - fraction) * left + fraction * right) >> 5
    return signed(result, SAMPLE_WIDTH)


def beam_energy(samples: Sequence[int]) -> int:
    """Return the square of the signed sum of exactly sixteen 24-bit samples."""
    if len(samples) != MICROPHONE_COUNT:
        raise ValueError("exactly 16 microphone samples are required")
    for sample in samples:
        require_signed(sample, SAMPLE_WIDTH, "sample")
    total = sum(samples)
    return total * total


def energy_delta(current_samples: Sequence[int], history_samples: Sequence[int]) -> int:
    """Calculate the 55-bit signed current-minus-history power update."""
    return signed(beam_energy(current_samples) - beam_energy(history_samples), ENERGY_DELTA_WIDTH)


def accumulate_vram(vram_read: int, delta: int) -> int:
    """Model vram_add: sign-extend a 55-bit delta and wrap the 64-bit result."""
    require_signed(vram_read, VRAM_WIDTH, "vram_read")
    require_signed(delta, ENERGY_DELTA_WIDTH, "delta")
    return signed(vram_read + delta, VRAM_WIDTH)


def ring_index(newest_index: int, integer_delay: int, depth: int) -> int:
    """Return the circular-buffer address for a non-negative integer delay."""
    if depth <= 0:
        raise ValueError("depth must be positive")
    if integer_delay < 0:
        raise ValueError("integer_delay must be non-negative")
    return (newest_index - integer_delay) % depth
