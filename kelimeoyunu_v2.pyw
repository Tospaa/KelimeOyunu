import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.messagebox as msgbox
from random import choice
from os.path import isfile, dirname, realpath, basename
from threading import Thread


class oyuncuIsmi(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("İsminizi Giriniz...")
        self.bind("<Return>", self.isim_onayla)
        self.statik_etiket = tk.Label(self, text="Lütfen isminizi giriniz", font=("Helvetica", 30))
        self.girilen_isim = tk.StringVar()
        self.isim_giris = tk.Entry(self, font=("Helvetica", 30), textvariable=self.girilen_isim, width=25)
        self.onayla_buton = tk.Button(self, text="Onayla", command=self.isim_onayla, font=("Helvetica", 30))
        self.statik_etiket.pack()
        self.isim_giris.pack()
        self.onayla_buton.pack()
        self.isim = ""
        self.azami_karakter_siniri = 20
        self.girilen_isim.trace("w", self.karakter_sayisi_takip)
        self.izin_verilen_karakterler = ["A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z",
        "a","b","c","ç","d","e","f","g","ğ","h","ı","i","j","k","l","m","n","o","ö","p","r","s","ş","t","u","ü","v","y","z"," "]
        self.isim_giris.focus()
        self.protocol("WM_DELETE_WINDOW", self.kapat)
        
    def karakter_sayisi_takip(self, *args):
        if len(self.girilen_isim.get()) != 0:
            if len(self.girilen_isim.get()) > self.azami_karakter_siniri:
                self.girilen_isim.set(self.girilen_isim.get()[:-1])
            
            if not (self.girilen_isim.get()[-1] in self.izin_verilen_karakterler):
                self.girilen_isim.set(self.girilen_isim.get()[:-1])

    def isim_onayla(self, *args):
        if len(self.girilen_isim.get()) <= 3:
            msgbox.showerror("Hata","İsimdeki karakter sayısı en az 4 olmalı.")
            return None
        for i in self.girilen_isim.get():
            if not (i in self.izin_verilen_karakterler):
                msgbox.showerror("Hata","İsim içinde izin verilmeyen karakter tespit edildi.\nTürkçe karakterler dışındaki tüm karakterler ve noktalama işaretleri girilemez.")
                self.girilen_isim.set("")
                return None
        if len(self.girilen_isim.get()) > self.azami_karakter_siniri:
            msgbox.showerror("Hata","İsim çok uzun.")
            self.girilen_isim.set("")
            return None
        self.isim = self.girilen_isim.get()
        self.destroy()
    
    def kapat(self):
        raise SystemExit

class kelimeOyunu(tk.Tk):
    def __init__(self, isim):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Kelime Oyunu")
        self.bind("<Return>", self.benjamin_fonksiyon)
        self.bind("<space>", lambda *args: Thread(target=self.harf_ver).start())
        self.bind("<Control-n>", self.yeni_sorular)
        self.bind("<Control-p>", self.oyun_sonu)
        self.soru_etiket = tk.Message(self, text="Soru", font=("Helvetica", 20), width=700)
        self.sure_etiket = tk.Label(self, text=" ", font=("Helvetica", 30))
        self.kelime_etiket = tk.Label(self, text="KELİME", font=("Courier New", 40), width=14)
        self.dusunsure_etiket = tk.Label(self, text=" ", font=("Helvetica", 30))
        self.puan_etiket = tk.Label(self, text="Puan: 0", font=("Helvetica", 30))
        self.sure_etiket_statik = tk.Label(self, text="Kalan Süre", font=("Helvetica", 15))
        self.dusunsure_etiket_statik = tk.Label(self, text=" ", font=("Helvetica", 15))
        self.benjamin_buton = tk.Button(self, text="Başla", command=self.benjamin_fonksiyon, font=("Helvetica", 30), width=13)
        self.harfaliyim_buton = tk.Button(self, text="Harf Alayım", command=lambda: Thread(target=self.harf_ver).start(), state="disabled", font=("Helvetica", 30))
        self.tahmin_giris = tk.Entry(self, state="disabled", font=("Helvetica", 30))
        self.tahmin_buton = tk.Button(self, text="Cevap Ver", command=self.benjamin_fonksiyon, state="disabled", bg="green", fg="white", font=("Helvetica", 30))
        self.soru_etiket.grid(row=0,column=0,columnspan=3, sticky="we")
        self.kelime_etiket.grid(row=1,column=0,columnspan=2,rowspan=2)
        self.sure_etiket_statik.grid(row=1,column=2)
        self.sure_etiket.grid(row=2,column=2)
        self.harfaliyim_buton.grid(row=3,column=0,columnspan=2,sticky="we")
        self.benjamin_buton.grid(row=3,column=2)
        self.tahmin_giris.grid(row=4,column=0,rowspan=2,sticky="we")
        self.tahmin_buton.grid(row=4,column=1,rowspan=2,sticky="we")
        self.dusunsure_etiket_statik.grid(row=4,column=2)
        self.dusunsure_etiket.grid(row=5,column=2)
        self.puan_etiket.grid(row=6,column=0,columnspan=3)
        self.protocol("WM_DELETE_WINDOW", self.kapat)
        self.animasyonlu_harfler = "ASHYTUCOZK"
        self.oyuncu_ismi = isim
        self.oyun_devam = False
        self.durduruldu = True
        self.harf_ver_ve_benjamin_fonksiyon_kilitli = False
        self.gereksiz_kilitli = False
        self.ozel_durum = False
        self.ara = True
        self.toplam_verilen_saniye = 240
        self.kalan_sure = 0
        self.gecen_sure = 0
        self.soru_sayisi = 0
        self.puan = 0
        self.dogru_cevap = " "
        self.alinan_harfler = []
        self.geri_sayim(self.toplam_verilen_saniye)
        self.focus_force()
        if not isfile("veri"):
            with open("veri","w") as f:
                pass
            self.son_dosya = ''
            self.yeni_sorular()
        else:
            with open("veri") as f:
                self.son_dosya = f.read()
            try:
                with open(self.son_dosya) as f:
                    self.sorular = f.readlines()
                    if self.dosya_dogrula():
                        msgbox.showerror("Hata","Yanlış formatta bir soru dosyası seçilmiş.")
                        self.yeni_sorular()
            except FileNotFoundError:
                msgbox.showerror("Hata","Soru dosyası yüklemesi sırasında bir hata oluştu.")
                self.son_dosya = ''
                self.yeni_sorular()

    def geri_sayim(self, yerel_kalan_sure = None):
        if yerel_kalan_sure is not None:
            self.kalan_sure = yerel_kalan_sure
        
        if self.ozel_durum:
            '''
            oyun_sonu metodunu harf_ver metodundan çağıramıyorum çünkise Thread mevzu çıkarıyo.
            Ancak böyle bi çözüm bulabildim.
            
            "Her zaman bir workaround vardır."
                                     ~Tospaa, circa 2017.
            '''
            self.ozel_durum = False
            self.oyun_sonu()
        
        if self.kalan_sure <= 0:
            self.sure_etiket.configure(text="Zaman doldu!")
            self.sure_durdu("Süre Bitti")
        else:
            self.sure_etiket.configure(text="{dk}:{sn:02d}".format(dk=(int(self.kalan_sure//60)), sn=(int(self.kalan_sure%60))))
            self.kalan_sure -= 0.1
            if not self.durduruldu:
                self.after(100, self.geri_sayim)

    def ileri_sayim(self, bastan_basla = False):
        if self.ara:
            return None
        
        if bastan_basla:
            self.gecen_sure = 0
            self.dusunsure_etiket.configure(fg = "black")
            self.dusunsure_etiket_statik.configure(text="Düşünme Süresi")
        
        if self.gecen_sure >= 45:
            self.dusunsure_etiket.configure(fg = "red")
         
        if self.gecen_sure >= 60:
            self.bilemedi()
            return None
        
        self.dusunsure_etiket.configure(text="{0}".format(int(self.gecen_sure)))
        self.gecen_sure += 0.1
        if self.durduruldu:
            self.after(100, self.ileri_sayim)

    def sure_durdu(self, neden = "Yeni Soru"):
        self.durduruldu = True
        self.ara = False
        self.ileri_sayim(True)
        self.benjamin_buton.configure(text=neden, state="disabled")
        self.tahmin_giris.configure(state="normal")
        self.tahmin_giris.focus()
        self.tahmin_buton.configure(state="normal")
        self.harfaliyim_buton.configure(state="disabled")
        self.puan_etiket['text'] += " ({0})".format(list(self.kelime_etiket['text']).count("•") * 100)

    def benjamin_fonksiyon(self, *args):
        if self.harf_ver_ve_benjamin_fonksiyon_kilitli:
            return None
        else:
            self.oyun_devam = True
            if self.benjamin_buton['state'] == 'normal':
                if self.durduruldu:
                    self.durduruldu = False
                    self.geri_sayim()
                    self.benjamin_buton.configure(text="Durdur")
                    self.harfaliyim_buton.configure(state="normal")
                    self.alinan_harfler = []
                    self.soru_etiket.configure(text=str(self.soru_sayisi+1) + ". " + self.sorular[(self.soru_sayisi*2)][:-1])
                    self.dogru_cevap = self.sorular[((self.soru_sayisi*2)+1)][:-1]
                    self.kelime_etiket.configure(text="•"*len(self.dogru_cevap))
                    self.soru_sayisi += 1
                else:
                    if self.soru_sayisi == 14:
                        self.sure_durdu("Son Soru")
                    else:
                        self.sure_durdu()
            elif self.benjamin_buton['state'] == 'disabled':
                if self.tahmin_giris.get().replace("i","İ").upper() == self.dogru_cevap:
                    self.tahmin_giris.delete(0, "end")
                    self.bildi()
                else:
                    self.tahmin_giris.delete(0, "end")
                    def gereksiz():
                        if self.gereksiz_kilitli:
                            return None
                        else:
                            self.gereksiz_kilitli = True
                            for _ in range(2):
                                self.tahmin_giris.configure(background="red")
                                self.tahmin_giris.update_idletasks()
                                self.after(100)
                                self.tahmin_giris.configure(background="white")
                                self.tahmin_giris.update_idletasks()
                                self.after(100)
                            self.gereksiz_kilitli = False
                    Thread(target=gereksiz).start()

    def harf_ver(self, *args):
        if self.harf_ver_ve_benjamin_fonksiyon_kilitli:
            return None
        else:
            if self.harfaliyim_buton['state'] == 'normal':
                self.harf_ver_ve_benjamin_fonksiyon_kilitli = True
                gerekList = []
                for indx, harf in enumerate(self.kelime_etiket['text']):
                    if harf == "•":
                        gerekList.append(indx)
                alinan_harf = choice(gerekList)
                self.alinan_harfler.append(alinan_harf)
                for i in self.animasyonlu_harfler:
                    hafiza = list(self.kelime_etiket['text'])
                    hafiza[alinan_harf] = i
                    hafiza = ''.join(hafiza)
                    self.kelime_etiket.configure(text=hafiza)
                    self.kelime_etiket.update_idletasks()
                    self.after(100)
                hafiza = list(self.kelime_etiket['text'])
                hafiza[alinan_harf] = self.dogru_cevap[alinan_harf]
                hafiza = ''.join(hafiza)
                self.kelime_etiket.configure(text=hafiza)
                if hafiza == self.dogru_cevap:
                    self.durduruldu = True
                    if self.kalan_sure > 0 and self.soru_sayisi != 14:
                        self.benjamin_buton.configure(text="Yeni Soru", state="normal")
                        self.harfaliyim_buton.configure(state="disabled")
                    elif self.soru_sayisi == 14:
                        self.benjamin_buton.configure(text="Soru Bitti", state="disabled")
                        self.harfaliyim_buton.configure(state="disabled")
                        self.oyun_devam = False
                        self.ozel_durum = True
                self.harf_ver_ve_benjamin_fonksiyon_kilitli = False
            elif self.harfaliyim_buton['state'] == 'disabled':
                return None

    def bildi(self, durum = True):
        if self.kalan_sure > 0 and self.soru_sayisi != 14:
            self.benjamin_buton.configure(state="normal")
        self.tahmin_giris.configure(state="disabled")
        self.tahmin_buton.configure(state="disabled")
        if durum:
            self.puan += list(self.kelime_etiket['text']).count("•") * 100
        else:
            self.puan -= list(self.kelime_etiket['text']).count("•") * 100
        self.ara = True
        hafiza = list(self.kelime_etiket['text'])
        gerekList = []
        for indx, harf in enumerate(hafiza):
            if harf == "•":
                gerekList.append(indx)
        for j in self.animasyonlu_harfler:
            hafiza = list(self.kelime_etiket['text'])
            for i in gerekList:
                hafiza[i] = j
            hafiza = ''.join(hafiza)
            self.kelime_etiket.configure(text=hafiza)
            self.kelime_etiket.update_idletasks()
            self.after(100)
        self.kelime_etiket.configure(text=self.dogru_cevap)
        self.puan_etiket.configure(text="Puan: {0}".format(self.puan))
        self.dusunsure_etiket.configure(text=" ")
        self.dusunsure_etiket_statik.configure(text=" ")
        if self.benjamin_buton['state'] == 'disabled':
            self.oyun_devam = False
            self.oyun_sonu()

    def bilemedi(self):
        self.bildi(False)
    
    def dosya_dogrula(self):
        return len(self.sorular) != 29 or self.sorular[-1] != "SORU DOSYASI"

    def yeni_sorular(self, *args):
        if not self.oyun_devam:
            calisma_dizini = dirname(realpath(__file__))
            yeni_dosya = fdialog.askopenfilename(filetypes=[("Soru Dosyaları","*.soru")], initialdir=calisma_dizini, title="Soru dosyası seç...")
            if yeni_dosya == '':
                if self.son_dosya == '':
                    msgbox.showerror("Hata","Soru dosyası yüklemesi sırasında bir hata oluştu.")
                    raise SystemExit
                return None
            self.son_dosya = yeni_dosya
            with open(self.son_dosya) as f:
                self.sorular = f.readlines()
            if self.dosya_dogrula():
                msgbox.showerror("Hata","Yanlış formatta bir soru dosyası seçildi.")
                raise SystemExit
            with open("veri", "w") as f:
                f.write(self.son_dosya)
            self.durduruldu = True
            self.ara = True
            self.gecen_sure = 0
            self.soru_sayisi = 0
            self.puan = 0
            self.dogru_cevap = " "
            self.alinan_harfler = []
            self.soru_etiket.configure(text="Soru")
            self.kelime_etiket.configure(text="KELİME")
            self.dusunsure_etiket.configure(text=" ")
            self.dusunsure_etiket_statik.configure(text=" ")
            self.puan_etiket.configure(text="Puan: 0")
            self.harfaliyim_buton.configure(state="disabled")
            self.tahmin_giris.configure(state="disabled")
            self.tahmin_buton.configure(state="disabled")
            self.benjamin_buton.configure(state="normal", text="Başla")
            self.geri_sayim(self.toplam_verilen_saniye)
        else:
            msgbox.showerror("Hata","Oyun devam ederken yeni soru paketi açamazsınız.")

    def kapat(self):
        if self.oyun_devam:
            msgbox.showerror("Hata","Oyun devam ederken çıkamazsınız.")
        else:
            raise SystemExit

    def oyun_sonu(self, *args):
        if args == ():
            if not isfile("puanlar.txt"):
                with open("puanlar.txt","w") as f:
                    f.write("İsim,Puan,Kalan Süre,Soru Paketi\n")
            
            with open("puanlar.txt","a") as f:
                f.write("{isim},{puan},{sure},{dosya}\n".format(isim=self.oyuncu_ismi, puan=self.puan, sure=int(self.kalan_sure), dosya=basename(self.son_dosya)))
        
        puan_goster = puanTablosu()
        puan_goster.focus_force()
        puan_goster.mainloop()

class puanTablosu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Puan Tablosu")
        self.bind("<Return>", lambda x: self.destroy())
        self.statik_etiket = tk.Label(self, text="Puan Tablosu", font=("Helvetica",30))
        self.etiket_liste = []
        self.aciklama_etiket1 = tk.Label(self, text="İsim", font=("Helvetica",15))
        self.aciklama_etiket2 = tk.Label(self, text="Puan", font=("Helvetica",15))
        self.aciklama_etiket3 = tk.Label(self, text="Kalan Süre", font=("Helvetica",15))
        for i in range(30):
            self.etiket_liste.append(tk.Label(self, text="", font=("Helvetica",15)))
        self.kapat_buton = tk.Button(self, text="Kapat", command=self.destroy)
        self.statik_etiket.grid(row=0, column=0, columnspan=3)
        self.aciklama_etiket1.grid(row=1, column=0, sticky="w")
        self.aciklama_etiket2.grid(row=1, column=1, sticky="w")
        self.aciklama_etiket3.grid(row=1, column=2, sticky="w")
        for i in range(10):
            self.etiket_liste[i].grid(row=i+2,column=0, sticky="w")
        for i in range(10,20):
            self.etiket_liste[i].grid(row=i-8,column=1, sticky="w")
        for i in range(20,30):
            self.etiket_liste[i].grid(row=i-18,column=2, sticky="w")
        self.kapat_buton.grid(row=12,column=0, columnspan=3)
        self.puanlar_liste = []
        self.puan_yukle()
    
    def puan_yukle(self):
        if isfile("puanlar.txt"):
            with open("puanlar.txt") as f:
                self.puanlar_liste = f.readlines()
            del self.puanlar_liste[0]
            for i in range(len(self.puanlar_liste)):
                self.puanlar_liste[i] = self.puanlar_liste[i].split(",")
            self.puanlar_liste = sorted(sorted(self.puanlar_liste, key=lambda neslis: int(neslis[2]), reverse = True), key=lambda neslis: int(neslis[1]), reverse = True)
            for i in range(10):
                try:
                    self.etiket_liste[i]['text'] = "{0}. {1}".format(i+1, self.puanlar_liste[i][0])
                except IndexError:
                    break
            for i in range(10,20):
                try:
                    self.etiket_liste[i]['text'] = "{0}".format(self.puanlar_liste[i-10][1])
                except IndexError:
                    break
            for i in range(20,30):
                try:
                    self.etiket_liste[i]['text'] = "{0} saniye".format(self.puanlar_liste[i-20][2])
                except IndexError:
                    break
        else:
            msgbox.showerror("Hata","Henüz bir puan alan olmamış.")
            self.destroy()


if __name__ == "__main__":
    isim_al = oyuncuIsmi()
    isim_al.mainloop()
    pencere = kelimeOyunu(isim_al.isim)
    pencere.mainloop()
