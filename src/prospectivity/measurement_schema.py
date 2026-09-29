from __future__ import annotations

from pydantic import BaseModel, Field


class Measurement(BaseModel):
    CTOTAL___: float | None = None
    STOTAL__: float | None = None
    LOI: float | None = None
    Suma: float | None = None
    SiO2: float | None = None
    Al2O3: float | None = None
    Fe2O3: float | None = None
    MgO: float | None = None
    CaO: float | None = None
    Na2O: float | None = None
    K2O: float | None = None
    TiO2: float | None = None
    P2O5: float | None = None
    MnO: float | None = None
    Cr2O3: str | None = None
    Sc: float | None = None
    Ba: float | None = None
    Be: str | None = None
    Co: float | None = None
    Cs: float | None = None
    Ga: float | None = None
    Hf: float | None = None
    Nb: float | None = None
    Rb: float | None = None
    Sn: str | None = None
    Sr: float | None = None
    Ta: float | None = None
    Th: float | None = None
    U: float | None = None
    V: float | None = None
    W: float | None = None
    Zr: float | None = None
    Y: float | None = None
    La: float | None = None
    Ce: float | None = None
    Pr: float | None = None
    Nd: float | None = None
    Sm: float | None = None
    Eu: float | None = None
    Gd: float | None = None
    Tb: float | None = None
    Dy: float | None = None
    Ho: float | None = None
    Er: float | None = None
    Tm: float | None = None
    Yb: float | None = None
    Lu: float | None = None
    Mo: float | None = None
    Cu: float | None = None
    Pb: float | None = None
    Zn: float | None = None
    Ni: float | None = None
    As_: float | None = None
    Cd: str | None = None
    Sb: str | None = None
    Bi: str | None = None
    Ag: str | None = None
    Au: str | None = None
    Hg: str | None = None
    Tl: str | None = None
    Se: str | None = None
    Te_ppm: str | None = None
    B_ppm: str | None = None
    geochemistry_published: bool
