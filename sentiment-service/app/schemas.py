from pydantic import BaseModel, Field


class AnalizIstek(BaseModel):
    metin: str = Field(min_length=1)


class AnalizCevap(BaseModel):
    duygu: str
    guven: float
