#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Core simple-planetary kinematic model.

This module implements a compact simple-planetary gearset model used by the
transmission kinematic solver.

The linear Willis relation is represented as::

    Ns * (omega_s - omega_c) + Nr * (omega_r - omega_c) = 0

An equivalent ratio form is::

    (omega_s - omega_c) / (omega_r - omega_c) = -Nr / Ns

The module separates kinematics from strict geometry validation. This allows
widely cited transmission reference tooth counts to be analyzed in ``relaxed``
mode even when they do not satisfy the standard integer-planet check for a
basic simple planetary construction.

Compatibility notes
-------------------
The public attributes ``sun``, ``ring``, and ``carrier`` remain
``RotatingMember`` objects because ``solver.py`` and other project modules
access the ``.name`` attribute on those members.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

try:
    from .clutch import RotatingMember
except Exception:  # pragma: no cover
    from clutch import RotatingMember  # type: ignore


@dataclass(frozen=True)
class GearGeometry:
    """Metadata for a toothed member."""

    label: str
    teeth: int

    def __repr__(self) -> str:
        return f"{self.label}(N={self.teeth})"


@dataclass(frozen=True)
class PlanetaryGeometryReport:
    """Validation and metadata report for a simple planetary gearset."""

    ok: bool
    mode: str
    Ns: int
    Nr: int
    delta: int
    Np_exact: float
    Np_integer: Optional[int]
    messages: tuple[str, ...] = ()

    @property
    def strict_ok(self) -> bool:
        """Return ``True`` when the report passed strict-geometry validation."""
        return self.ok and self.mode == "strict"


class PlanetaryGearSet:
    """Represent a simple planetary gearset.

    Parameters
    ----------
    Ns:
        Sun tooth count.
    Nr:
        Ring tooth count.
    name:
        Name of the gearset.
    sun:
        Optional injected sun rotating member for compound architectures.
    ring:
        Optional injected ring rotating member for compound architectures.
    carrier:
        Optional injected carrier rotating member for compound architectures.
    geometry_mode:
        Geometry-validation mode. Use ``"relaxed"`` for kinematics-only
        analysis or ``"strict"`` to require standard integer-planet simple
        planetary geometry.

    Notes
    -----
    For a standard simple planetary with one planet meshing the sun and ring,
    the implied planet tooth count is::

        Np = (Nr - Ns) / 2

    In ``relaxed`` mode this value is recorded but not enforced. In ``strict``
    mode it must be a positive integer.
    """

    VALID_GEOMETRY_MODES = {"relaxed", "strict"}

    def __init__(
        self,
        Ns: int,
        Nr: int,
        name: str = "PGS",
        sun: Optional[RotatingMember] = None,
        ring: Optional[RotatingMember] = None,
        carrier: Optional[RotatingMember] = None,
        geometry_mode: str = "relaxed",
    ) -> None:
        self.name = name
        self.Ns = int(Ns)
        self.Nr = int(Nr)
        self.geometry_mode = str(geometry_mode).strip().lower()

        if self.geometry_mode not in self.VALID_GEOMETRY_MODES:
            valid = ", ".join(sorted(self.VALID_GEOMETRY_MODES))
            raise ValueError(f"Invalid geometry_mode={geometry_mode!r}. Valid modes: {valid}")

        # Always enforce minimal kinematic sanity.
        self._validate_minimum_counts(self.Ns, self.Nr)

        # Compute the implied planet count even in relaxed mode.
        self.Np_exact = (self.Nr - self.Ns) / 2.0
        self.Np: Optional[int] = None
        if (self.Nr - self.Ns) % 2 == 0:
            np_int = (self.Nr - self.Ns) // 2
            if np_int > 0:
                self.Np = np_int

        if self.geometry_mode == "strict":
            self.validate_geometry(strict=True, raise_on_error=True)

        # Rotating members exposed directly for solver compatibility.
        self.sun = sun if sun is not None else RotatingMember(f"{name}_sun")
        self.ring = ring if ring is not None else RotatingMember(f"{name}_ring")
        self.carrier = carrier if carrier is not None else RotatingMember(f"{name}_carrier")

        # Optional geometry metadata.
        self.sun_geometry = GearGeometry("sun", self.Ns)
        self.ring_geometry = GearGeometry("ring", self.Nr)
        self.carrier_geometry = GearGeometry("carrier", 0)

    @staticmethod
    def _validate_minimum_counts(Ns: int, Nr: int) -> None:
        """Validate the minimum tooth-count requirements for kinematics."""
        if Ns <= 0 or Nr <= 0:
            raise ValueError("Gear tooth counts must be positive")
        if Nr <= Ns:
            raise ValueError("Ring tooth count must be greater than sun tooth count")

    @classmethod
    def geometry_report(cls, *, Ns: int, Nr: int, mode: str = "relaxed") -> PlanetaryGeometryReport:
        """Return a non-throwing geometry report for proposed tooth counts."""
        mode_norm = str(mode).strip().lower()
        if mode_norm not in cls.VALID_GEOMETRY_MODES:
            valid = ", ".join(sorted(cls.VALID_GEOMETRY_MODES))
            raise ValueError(f"Invalid geometry mode {mode!r}. Valid modes: {valid}")

        messages = []
        ok = True
        delta = int(Nr) - int(Ns)
        np_exact = delta / 2.0
        np_integer: Optional[int] = None

        if Ns <= 0 or Nr <= 0:
            ok = False
            messages.append("Gear tooth counts must be positive.")
        if Nr <= Ns:
            ok = False
            messages.append("Ring tooth count must be greater than sun tooth count.")

        if ok and delta % 2 == 0:
            np_int = delta // 2
            if np_int > 0:
                np_integer = np_int
            else:
                ok = False
                messages.append("Computed planet tooth count must be positive.")

        if mode_norm == "strict":
            if delta % 2 != 0:
                ok = False
                messages.append(
                    "Invalid simple planetary geometry: (Nr - Ns) must be even so planet tooth count is integer."
                )
            elif np_integer is None:
                ok = False
                messages.append("Invalid simple planetary geometry: computed planet tooth count must be positive.")

        return PlanetaryGeometryReport(
            ok=ok,
            mode=mode_norm,
            Ns=int(Ns),
            Nr=int(Nr),
            delta=delta,
            Np_exact=np_exact,
            Np_integer=np_integer,
            messages=tuple(messages),
        )

    def validate_geometry(
        self,
        *,
        strict: bool | None = None,
        raise_on_error: bool = False,
    ) -> PlanetaryGeometryReport:
        """Validate gear geometry and return a report.

        Parameters
        ----------
        strict:
            Validation mode override.

            - ``True`` enforces standard integer-planet simple planetary
              geometry.
            - ``False`` applies relaxed validation with kinematic sanity checks
              only.
            - ``None`` uses this instance's ``geometry_mode``.
        raise_on_error:
            Raise ``ValueError`` when the geometry is invalid.
        """
        if strict is None:
            mode = self.geometry_mode
        else:
            mode = "strict" if strict else "relaxed"

        report = self.geometry_report(Ns=self.Ns, Nr=self.Nr, mode=mode)
        if raise_on_error and not report.ok:
            if report.messages:
                raise ValueError(report.messages[0])
            raise ValueError("Invalid planetary geometry")
        return report

    @property
    def is_geometry_strict_valid(self) -> bool:
        """Return whether the current tooth counts pass strict validation."""
        return self.validate_geometry(strict=True, raise_on_error=False).ok

    @property
    def has_integer_planet_count(self) -> bool:
        """Return whether the implied planet tooth count is a positive integer."""
        return self.Np is not None

    def planetary_equation(self, ws: float, wr: float, wc: float) -> float:
        """Return the residual of the linear Willis planetary constraint."""
        return self.Ns * (ws - wc) + self.Nr * (wr - wc)

    def willis_ratio(self, ws: float, wr: float, wc: float) -> float:
        """Return the Willis ratio ``(ws - wc) / (wr - wc)``."""
        denom = wr - wc
        if denom == 0:
            raise ZeroDivisionError("Willis ratio undefined because wr == wc")
        return (ws - wc) / denom

    def solve(
        self,
        input_member: str,
        output_member: str,
        fixed_member: str,
        input_speed: float = 1.0,
    ) -> Dict[str, float]:
        """Solve one input, one output, and one fixed member.

        Parameters
        ----------
        input_member:
            Input member name. Must be one of ``"sun"``, ``"ring"``, or
            ``"carrier"``.
        output_member:
            Output member name. Must be one of ``"sun"``, ``"ring"``, or
            ``"carrier"``.
        fixed_member:
            Fixed member name. Must be one of ``"sun"``, ``"ring"``, or
            ``"carrier"``.
        input_speed:
            Input angular speed.

        Returns
        -------
        dict[str, float]
            Speeds for ``sun``, ``ring``, and ``carrier``.
        """
        members = {"sun", "ring", "carrier"}

        if input_member not in members:
            raise ValueError("invalid input member")
        if output_member not in members:
            raise ValueError("invalid output member")
        if fixed_member not in members:
            raise ValueError("invalid fixed member")
        if len({input_member, output_member, fixed_member}) != 3:
            raise ValueError("input_member, output_member, and fixed_member must all be different")

        ws: Optional[float] = None
        wr: Optional[float] = None
        wc: Optional[float] = None

        if input_member == "sun":
            ws = float(input_speed)
        elif input_member == "ring":
            wr = float(input_speed)
        else:
            wc = float(input_speed)

        if fixed_member == "sun":
            ws = 0.0
        elif fixed_member == "ring":
            wr = 0.0
        else:
            wc = 0.0

        if wc is None:
            assert ws is not None and wr is not None
            wc = (self.Ns * ws + self.Nr * wr) / (self.Ns + self.Nr)
        elif ws is None:
            assert wr is not None
            ws = ((self.Ns + self.Nr) * wc - self.Nr * wr) / self.Ns
        elif wr is None:
            wr = ((self.Ns + self.Nr) * wc - self.Ns * ws) / self.Nr

        return {"sun": float(ws), "ring": float(wr), "carrier": float(wc)}

    def ratio(
        self,
        input_member: str,
        output_member: str,
        fixed_member: str,
        input_speed: float = 1.0,
    ) -> float:
        """Return the speed ratio ``omega_in / omega_out``."""
        speeds = self.solve(
            input_member=input_member,
            output_member=output_member,
            fixed_member=fixed_member,
            input_speed=input_speed,
        )
        win = speeds[input_member]
        wout = speeds[output_member]
        if wout == 0:
            raise ZeroDivisionError("Output speed is zero")
        return win / wout

    def describe_mode(
        self,
        input_member: str,
        output_member: str,
        fixed_member: str,
        input_speed: float = 1.0,
    ) -> str:
        """Return a qualitative classification for the solved ratio."""
        r = self.ratio(
            input_member=input_member,
            output_member=output_member,
            fixed_member=fixed_member,
            input_speed=input_speed,
        )
        if r < 0:
            return "reverse"
        if r > 1:
            return "reduction"
        if 0 < r < 1:
            return "overdrive"
        return "direct"

    def summary(
        self,
        input_member: str,
        output_member: str,
        fixed_member: str,
        input_speed: float = 1.0,
    ) -> None:
        """Print a standalone human-readable summary."""
        speeds = self.solve(
            input_member=input_member,
            output_member=output_member,
            fixed_member=fixed_member,
            input_speed=input_speed,
        )
        ratio = self.ratio(
            input_member=input_member,
            output_member=output_member,
            fixed_member=fixed_member,
            input_speed=input_speed,
        )
        mode = self.describe_mode(
            input_member=input_member,
            output_member=output_member,
            fixed_member=fixed_member,
            input_speed=input_speed,
        )
        geom = self.validate_geometry(strict=False)
        strict_geom = self.validate_geometry(strict=True)

        print("\nPlanetary Gearset")
        print("------------------------")
        print(f"Name: {self.name}")
        print(f"Sun teeth: {self.Ns}")
        print(f"Ring teeth: {self.Nr}")
        if self.Np is None:
            print(f"Planet teeth (implied): {self.Np_exact:.3f} [non-integer / relaxed mode]")
        else:
            print(f"Planet teeth: {self.Np}")
        print(f"Geometry mode: {self.geometry_mode}")
        print(f"Strict geometry valid: {'yes' if strict_geom.ok else 'no'}")
        if not strict_geom.ok and strict_geom.messages:
            print(f"Strict geometry note: {strict_geom.messages[0]}")
        print()
        print("Members")
        print("------------------------")
        print(f"Sun:     {self.sun.name}")
        print(f"Ring:    {self.ring.name}")
        print(f"Carrier: {self.carrier.name}")
        print()
        print("Configuration")
        print("------------------------")
        print(f"Input:  {input_member}")
        print(f"Output: {output_member}")
        print(f"Fixed:  {fixed_member}")
        print()
        print("Speeds")
        print("------------------------")
        print(f"Sun speed:     {speeds['sun']:.6f}")
        print(f"Ring speed:    {speeds['ring']:.6f}")
        print(f"Carrier speed: {speeds['carrier']:.6f}")
        print()
        print("Results")
        print("------------------------")
        print(f"Gear ratio: {ratio:.6f}")
        print(f"Mode: {mode}")

    def __repr__(self) -> str:
        np_repr = f"{self.Np}" if self.Np is not None else f"{self.Np_exact:.3f}"
        return (
            "PlanetaryGearSet("
            f"name={self.name!r}, "
            f"Ns={self.Ns}, "
            f"Nr={self.Nr}, "
            f"Np={np_repr}, "
            f"geometry_mode={self.geometry_mode!r}, "
            f"sun={self.sun.name!r}, "
            f"ring={self.ring.name!r}, "
            f"carrier={self.carrier.name!r}"
            ")"
        )
