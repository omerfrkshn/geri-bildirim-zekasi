CREATE TABLE geribildirimler (
    id BIGSERIAL PRIMARY KEY,
    metin TEXT NOT NULL,
    olusturma_tarihi TIMESTAMP NOT NULL DEFAULT now()
);
