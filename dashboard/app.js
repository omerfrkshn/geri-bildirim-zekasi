const API_ADRESI = "http://localhost:8080";

const DUYGU_ETIKETLERI = {
    positive: "pozitif",
    negative: "negatif",
    neutral: "nötr",
};

async function geribildirimleriGetir() {
    const cevap = await fetch(`${API_ADRESI}/geribildirimler`);
    if (!cevap.ok) {
        throw new Error(`API hatası: ${cevap.status}`);
    }
    return cevap.json();
}

function kacisla(metin) {
    const gecici = document.createElement("div");
    gecici.textContent = metin;
    return gecici.innerHTML;
}

function duyguEtiketiOlustur(duygu) {
    if (!duygu || !Object.hasOwn(DUYGU_ETIKETLERI, duygu)) {
        return '<span class="duygu-etiketi duygu-etiketi--bekliyor">bekliyor</span>';
    }
    const gorunenAd = DUYGU_ETIKETLERI[duygu];
    return `<span class="duygu-etiketi duygu-etiketi--${duygu}">${gorunenAd}</span>`;
}

function tarihiFormatla(isoTarih) {
    return new Date(isoTarih).toLocaleString("tr-TR");
}

function tabloyuDoldur(geribildirimler) {
    const govde = document.getElementById("geribildirim-tablosu-govde");
    govde.innerHTML = geribildirimler
        .slice()
        .reverse()
        .map(
            (g) => `
            <tr>
                <td>${tarihiFormatla(g.olusturmaTarihi)}</td>
                <td>${kacisla(g.metin)}</td>
                <td>${duyguEtiketiOlustur(g.duygu)}</td>
                <td>${g.guven != null ? (g.guven * 100).toFixed(1) + "%" : "-"}</td>
            </tr>`
        )
        .join("");
}

function ozetiDoldur(geribildirimler) {
    const sayilar = { positive: 0, negative: 0, neutral: 0, bekliyor: 0 };
    for (const g of geribildirimler) {
        if (g.duygu && sayilar[g.duygu] !== undefined) {
            sayilar[g.duygu]++;
        } else {
            sayilar.bekliyor++;
        }
    }
    const ozetGovde = document.getElementById("ozet-tablosu");
    ozetGovde.innerHTML = `
        <tr><td>Toplam</td><td>${geribildirimler.length}</td></tr>
        <tr><td>Pozitif</td><td>${sayilar.positive}</td></tr>
        <tr><td>Negatif</td><td>${sayilar.negative}</td></tr>
        <tr><td>Nötr</td><td>${sayilar.neutral}</td></tr>
        <tr><td>Analiz bekleyen</td><td>${sayilar.bekliyor}</td></tr>
    `;
    return sayilar;
}

function grafigiCiz(sayilar) {
    const ctx = document.getElementById("duygu-grafigi");
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Pozitif", "Negatif", "Nötr", "Bekliyor"],
            datasets: [
                {
                    data: [sayilar.positive, sayilar.negative, sayilar.neutral, sayilar.bekliyor],
                    backgroundColor: ["#22c55e", "#ef4444", "#64748b", "#6366f1"],
                    borderWidth: 0,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: "#e2e8f0" } },
            },
        },
    });
}

async function sayfayiYukle() {
    const durumMetni = document.getElementById("durum-metni");
    try {
        const geribildirimler = await geribildirimleriGetir();
        tabloyuDoldur(geribildirimler);
        const sayilar = ozetiDoldur(geribildirimler);
        grafigiCiz(sayilar);
        durumMetni.textContent = `Son güncelleme: ${new Date().toLocaleTimeString("tr-TR")}`;
    } catch (hata) {
        durumMetni.textContent = `Veri alınamadı: ${hata.message}. API (${API_ADRESI}) çalışıyor mu?`;
    }
}

sayfayiYukle();
