"""
Final Ödev 2: Turing Makinesi ile Araç Plaka Formatı Tanıyıcı
-------------------------------------------------------------
Tek bantlı deterministik Turing Makinesi simülatörü.
Tanınan dil (format):   N N L L N N N
  N = rakam (0-9), L = büyük harf (A-Z), uzunluk = 7

Durumlar:
  q0 -> 1. rakam beklenir
  q1 -> 2. rakam beklenir
  q2 -> 1. büyük harf beklenir
  q3 -> 2. büyük harf beklenir
  q4 -> 3. rakam beklenir (sondan 3.)
  q5 -> 4. rakam beklenir (sondan 2.)
  q6 -> 5. rakam beklenir (sondan 1.)
  q7 -> kabul (bant burada bitmeli)
  qR -> red
"""

BLANK = "_"

# Karakter sınıfları
RAKAMLAR = set("0123456789")
BUYUK_HARFLER = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


# ---------------------------------------------------------------
# 1) BANT
# ---------------------------------------------------------------
class Bant:
    """Sade bir bant: girdi karakterleri + sağ tarafta boş."""

    def __init__(self, girdi: str):
        self.hucreler = list(girdi) + [BLANK]
        self.kafa = 0

    def oku(self) -> str:
        if 0 <= self.kafa < len(self.hucreler):
            return self.hucreler[self.kafa]
        return BLANK

    def sag(self):
        self.kafa += 1
        if self.kafa >= len(self.hucreler):
            self.hucreler.append(BLANK)

    def goster(self) -> str:
        parcalar = []
        for i, h in enumerate(self.hucreler):
            parcalar.append(f"[{h}]" if i == self.kafa else h)
        return "".join(parcalar)


# ---------------------------------------------------------------
# 2) GEÇİŞ FONKSİYONU
# ---------------------------------------------------------------
def gecis(durum: str, sembol: str) -> str:
    """
    Geçiş fonksiyonu δ: Q x Σ -> Q.
    Her durum, sadece beklediği sembol sınıfını kabul eder; aksi halde qR.
    """
    # q0, q1: rakam bekler
    if durum == "q0":
        return "q1" if sembol in RAKAMLAR else "qR"
    if durum == "q1":
        return "q2" if sembol in RAKAMLAR else "qR"
    # q2, q3: büyük harf bekler
    if durum == "q2":
        return "q3" if sembol in BUYUK_HARFLER else "qR"
    if durum == "q3":
        return "q4" if sembol in BUYUK_HARFLER else "qR"
    # q4, q5, q6: rakam bekler
    if durum == "q4":
        return "q5" if sembol in RAKAMLAR else "qR"
    if durum == "q5":
        return "q6" if sembol in RAKAMLAR else "qR"
    if durum == "q6":
        # 7. (son) karakter rakam olmalı; ardından BLANK gelmeli.
        return "q7" if sembol in RAKAMLAR else "qR"
    # q7'de yalnızca BLANK kabul edilir; başka sembol = red (fazladan karakter)
    if durum == "q7":
        return "q7" if sembol == BLANK else "qR"
    return "qR"


# ---------------------------------------------------------------
# 3) TURING MAKİNESİ
# ---------------------------------------------------------------
class TuringMakinesi:

    def __init__(self, girdi: str, log: bool = True):
        self.bant = Bant(girdi)
        self.durum = "q0"
        self.log = log
        self.adim = 0

    def _kaydet(self, okunan: str):
        self.adim += 1
        if self.log:
            print(
                f"Adım {self.adim:>2} | Durum: {self.durum:<3} "
                f"| Okunan: {okunan!r:<5} | Hareket: R | "
                f"Bant: {self.bant.goster()}"
            )

    def calistir(self) -> bool:
        if self.log:
            print(f">>> Başlangıç bandı: {self.bant.goster()}")
            print(f">>> Başlangıç durumu: {self.durum}\n")

        # Önce uzunluk kontrolü deterministik geçişlerin doğal sonucudur:
        # 7 karakterden kısa bir girdide bir noktada BLANK okunur ve durum
        # q7'den önce ise red, q7'de ise kabul.
        while True:
            okunan = self.bant.oku()
            yeni_durum = gecis(self.durum, okunan)
            self._kaydet(okunan)

            self.durum = yeni_durum

            # Durdurma koşulları
            if self.durum == "qR":
                if self.log:
                    print(f"\n>>> RED (durum {self.durum} ile durdu).")
                return False
            if self.durum == "q7" and okunan == BLANK:
                # q7'ye ancak bantın BLANK'ında varılırsa (q6'dan sonra bir
                # rakam daha yoktur) -> tam 7 karakter sağlanmış demektir.
                if self.log:
                    print(f"\n>>> KABUL (durum {self.durum} ile durdu).")
                return True

            self.bant.sag()


# ---------------------------------------------------------------
# 4) ARAYÜZ
# ---------------------------------------------------------------
def taniyici(girdi: str, log: bool = True) -> bool:
    return TuringMakinesi(girdi, log=log).calistir()


def main():
    print("=" * 60)
    print(" Turing Makinesi ile Araç Plaka Formatı Tanıyıcı")
    print(" Format: NN-LL-NNN  (örn. 55AB123)")
    print("=" * 60)

    girdi = input("Plaka giriniz: ").strip()
    sonuc = taniyici(girdi, log=True)

    print("\n" + "=" * 60)
    print(f" SONUÇ: {'KABUL' if sonuc else 'RED'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
