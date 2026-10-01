from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


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
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "CTOTAL___":0.18,
                "STOTAL__":0.14,
                "SiO2":60.75,
                "Al2O3":15.23,
                "Fe2O3":7.85,
                "MgO":1.44,
                "CaO":2.64,
                "Na2O":2.95,
                "K2O":2.63,
                "TiO2":1.23,
                "P2O5":0.14,
                "MnO":0.1,
                "Cr2O3":"0,005",
                "LOI":4.8,
                "Suma":99.72,
                "Sc":9,
                "Ba":850,
                "Be":"2",
                "Co":18.5,
                "Cs":6.4,
                "Ga":20.4,
                "Hf":9.4,
                "Nb":12.5,
                "Rb":89.3,
                "Sn":"2",
                "Sr":502.2,
                "Ta":0.9,
                "Th":12.7,
                "U":2.8,
                "V":186,
                "W":1.2,
                "Zr":346.2,
                "Y":14.2,
                "La":38.6,
                "Ce":72,
                "Pr":8.17,
                "Nd":29.5,
                "Sm":4.9,
                "Eu":1.18,
                "Gd":3.46,
                "Tb":0.48,
                "Dy":2.63,
                "Ho":0.47,
                "Er":1.33,
                "Tm":0.21,
                "Yb":1.64,
                "Lu":0.24,
                "Mo":0.7,
                "Cu":25.6,
                "Pb":9.8,
                "Zn":63,
                "Ni":12.6,
                "As_":15.5,
                "Cd":"0,1",
                "Sb":"0,3",
                "Bi":"0,2",
                "Ag":"<0,1",
                "Au":"0,6",
                "Hg":"0,03",
                "Tl":"0,2",
                "Se":"<0,5",
                "Te_ppm":"sin datos",
                "B_ppm":"sin datos", 
                "geochemistry_published": True
            }
        }
    )


class HealthResponse(BaseModel):
    status: str = Field(example="ok")
    files_available: bool = Field(example=True)
    
class PredictResponse(BaseModel):
    probability: float = Field(example=0.023437538217366192)
    prediction: int = Field(example=0)