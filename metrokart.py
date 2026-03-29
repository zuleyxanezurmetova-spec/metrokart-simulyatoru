import sys

# Başlanğıc dəyişənlər
pin = "1357"
balans = 0.0
borc = 0.0
cehd_sayi = 3
gedis_sayi = 0
emeliyyatlar = []
gunluk_limit = 100.0
bugunku_toplam_artirma = 0.0
rejim = "Normal"

def emeliyyat_yadda_saxla(tip, mebleq, endirim, yeni_balans):
    """Hər bir əməliyyatı siyahıya əlavə edir """
    emeliyyatlar.append({
        "tip": tip,
        "mebleq": mebleq,
        "endirim": endirim,
        "yeni_balans": yeni_balans})
    
# 1. PIN Giriş Hissəsi
print("--- MetroKart Simulyatoruna Xoş Gəlmisiniz ---")
while cehd_sayi > 0:
    giris = input(f"4 rəqəmli PIN daxil edin (Cəhd: {cehd_sayi}): ")
    if giris == pin:
        print("Giriş uğurludur!")
        break
    else:
        cehd_sayi -= 1
        print("Səhv PIN!")
        if cehd_sayi == 0:
            print("Cəhd haqqınız bitdi.")
            sys.exit()

 # 2. Əsas Menyu
while True:
    print(f"\n[Rejim: {rejim}] | Balans: {balans:.2f} AZN | Borc: {borc:.2f} AZN")
    print("1) Balansı göstər\n2) Balans artır\n3) Gediş et\n4) Son əməliyyatlar\n5) Günlük statistika\n6) Parametrlər\n0) Çıxış")
    
    secim = input("Seçiminizi edin: ")

    if secim == "0":
        print("Sistemdən çıxılır...")
        break           
    elif secim == "1": 
        print(f"Cari balansınız: {balans:.2f} AZN")

    elif secim == "2": 
        try:
            artim = float(input("Artırılacaq məbləğ: "))
            if artim > 0:
                if bugunku_toplam_artirma + artim <= gunluk_limit:
                    bugunku_toplam_artirma += artim
                    
                    # Borc varsa əvvəlcə borcu bağla 
                    if borc > 0:
                        if artim >= borc:
                            artim -= borc
                            borc = 0
                            balans += artim
                        else:
                            borc -= artim
                            artim = 0
                    else:
                        balans += artim
                    
                    emeliyyat_yadda_saxla("Artırma", artim, 0, balans)
                    print("Balans uğurla artırıldı.")
                else:
                    print(f"Limit aşıldı! Günlük maksimum: {gunluk_limit} AZN")
            else:
                print("Məbləğ müsbət olmalıdır!")
        except ValueError:
            print("Xəta: Rəqəm daxil edin!")

    elif secim == "3": 
        qiymet = 0.40
        endirim = 0.0
        
        # Rejimə görə qiymət təyini 
        if rejim == "Tələbə":
            qiymet = 0.20
        elif rejim == "Pensiyaçı":
            qiymet = 0.15
        else: # Normal rejim
            if gedis_sayi >= 1 and gedis_sayi < 4: # 2, 3, 4-cü gedişlər
                qiymet = 0.36
                endirim = 0.04
            elif gedis_sayi >= 4: # 5-ci və daha çox
                qiymet = 0.30
                endirim = 0.10

        borc_limiti = qiymet - 0.10

        if balans >= qiymet:
            balans -= qiymet
            gedis_sayi += 1
            emeliyyat_yadda_saxla("Gediş", qiymet, endirim, balans)
            print(f"Keçid uğurludur. Qiymət: {qiymet:.2f} AZN")
            
        elif balans >= borc_limiti: # Təcili keçid 
            print(f"Balans kifayət deyil ({balans:.2f} AZN).")
            cavab = input(f"Təcili keçid edilsin? (Borca yazılacaq: {qiymet - balans:.2f} AZN) (h/y): ")
            
            if cavab.lower() == 'h':
                borc += (qiymet - balans)
                balans = 0
                gedis_sayi += 1
                emeliyyat_yadda_saxla("Təcili Keçid", qiymet, 0, balans)
                print("Keçid edildi, borcunuz qeydə alındı.")
        else:
            print(f"Balans yetərsizdir! Minimum {borc_limiti:.2f} AZN lazımdır.")

    elif secim == "4": # Son N əməliyyat
        try:
            n = int(input("Son neçə əməliyyatı görmək istəyirsiniz? "))
            for em in emeliyyatlar[-n:]:
                print(f"Tip: {em['tip']}, Məbləğ: {em['mebleq']} AZN, Endirim: {em['endirim']} AZN, Balans: {em['yeni_balans']:.2f}")
        except ValueError:
            print("Düzgün say daxil edin.")

    elif secim == "5": # Günlük statistika
        cemi_gedis = sum(1 for e in emeliyyatlar if "Gediş" in e['tip'] or "Keçid" in e['tip'])
        cemi_odenis = sum(e['mebleq'] for e in emeliyyatlar if "Gediş" in e['tip'])
        cemi_endirim = sum(e['endirim'] for e in emeliyyatlar)
        print(f"Cəmi gediş: {cemi_gedis}")
        print(f"Ümumi ödəniş: {cemi_odenis:.2f} AZN")
        print(f"Edilən endirimlər: {cemi_endirim:.2f} AZN")
        print(f"Günlük artırılan: {bugunku_toplam_artirma:.2f} AZN")

    elif secim == "6": # Parametrlər
        p_secim = input("1.Limit dəyiş\n2.Endirim rejimi seç: ")
        if p_secim == "1":
            gunluk_limit = float(input("Yeni günlük limit: "))
        elif p_secim == "2":
            r = input("1.Normal\n2.Tələbə\n3.Pensiyaçı\nSeçim: ")
            rejim = {"1":"Normal", "2":"Tələbə", "3":"Pensiyaçı"}.get(r, "Normal")
            # Layihə tamamlandı