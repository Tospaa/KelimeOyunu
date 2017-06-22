import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.messagebox as msgbox
from random import randint, choice
from os.path import isfile, dirname, realpath

class kelimeOyunu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Kelime Oyunu")
        self.bind("<Return>", self.benjamin_fonksiyon)
        self.bind("<space>", self.harf_ver)
        self.bind("<Control-n>", self.yeni_sorular)
        self.soru_etiket = tk.Message(self, text="Soru", font=("Helvetica", 20), width=700)
        self.sure_etiket = tk.Label(self, text=" ", font=("Helvetica", 30))
        self.kelime_etiket = tk.Label(self, text="KELİME", font=("Courier New", 40), width=14)
        self.dusunsure_etiket = tk.Label(self, text=" ", font=("Helvetica", 30))
        self.puan_etiket = tk.Label(self, text="Puan: 0", font=("Helvetica", 30))
        self.sure_etiket_statik = tk.Label(self, text="Kalan Süre", font=("Helvetica", 15))
        self.dusunsure_etiket_statik = tk.Label(self, text=" ", font=("Helvetica", 15))
        self.benjamin_buton = tk.Button(self, text="Başla", command=self.benjamin_fonksiyon, font=("Helvetica", 30), width=13)
        self.harfaliyim_buton = tk.Button(self, text="Harf Alayım", command=self.harf_ver, state="disabled", font=("Helvetica", 30))
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
        self.alfabe = ["A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z"]
        self.durduruldu = True
        self.ara = True
        self.toplam_verilen_saniye = 240
        self.kalan_sure = 0
        self.gecen_sure = 0
        self.soru_sayisi = 0
        self.puan = 0
        self.dogru_cevap = " "
        self.alinan_harfler = []
        self.geri_sayim(self.toplam_verilen_saniye)
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
    
        if self.kalan_sure <= 0:
            self.sure_etiket.configure(text="Zaman doldu!")
            self.sure_durdu("Süre Bitti")
        else:
            self.sure_etiket.configure(text="{dk}:{sn:02d}".format(dk=(int(self.kalan_sure//60)), sn=(int(self.kalan_sure%60))))
            self.kalan_sure -= 0.25
            if not self.durduruldu:
                self.after(250, self.geri_sayim)

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
        self.gecen_sure += 0.25
        if self.durduruldu:
            self.after(250, self.ileri_sayim)

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
            if len(self.tahmin_giris.get()) != len(self.dogru_cevap):
                self.tahmin_giris.delete(0, "end")
                return None
            if self.tahmin_giris.get().replace("i","İ").upper() == self.dogru_cevap:
                self.tahmin_giris.delete(0, "end")
                self.bildi()
            else:
                self.tahmin_giris.delete(0, "end")
                return None

    def harf_ver(self, *args):
        if self.harfaliyim_buton['state'] == 'normal':
            alinan_harf = randint(0, len(self.dogru_cevap)-1)
            while alinan_harf in self.alinan_harfler:
                alinan_harf = randint(0, len(self.dogru_cevap)-1)
            self.alinan_harfler.append(alinan_harf)
            for _ in range(10):
                hafiza = list(self.kelime_etiket['text'])
                hafiza[alinan_harf] = choice(self.alfabe)
                hafiza = ''.join(hafiza)
                self.kelime_etiket.configure(text=hafiza)
                self.kelime_etiket.update_idletasks()
                self.after(100)
            hafiza = list(self.kelime_etiket['text'])
            hafiza[alinan_harf] = self.dogru_cevap[alinan_harf]
            hafiza = ''.join(hafiza)
            self.kelime_etiket.configure(text=hafiza)
            self.kalan_sure -= 0.75
            if hafiza == self.dogru_cevap:
                self.durduruldu = True
                if self.kalan_sure > 0 and self.soru_sayisi != 14:
                    self.benjamin_buton.configure(text="Yeni Soru", state="normal")
                    self.harfaliyim_buton.configure(state="disabled")
                elif self.kalan_sure <= 0:
                    self.benjamin_buton.configure(text="Süre Bitti", state="disabled")
                    self.harfaliyim_buton.configure(state="disabled")
                elif self.soru_sayisi == 14:
                    self.benjamin_buton.configure(text="Soru Bitti", state="disabled")
                    self.harfaliyim_buton.configure(state="disabled")
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
        for _ in range(10):
            hafiza = list(self.kelime_etiket['text'])
            rastgele_harf = choice(self.alfabe)
            for i in gerekList:
                hafiza[i] = rastgele_harf
            hafiza = ''.join(hafiza)
            self.kelime_etiket.configure(text=hafiza)
            self.kelime_etiket.update_idletasks()
            self.after(100)
        self.kelime_etiket.configure(text=self.dogru_cevap)
        self.puan_etiket.configure(text="Puan: {0}".format(self.puan))
        self.dusunsure_etiket.configure(text=" ")
        self.dusunsure_etiket_statik.configure(text=" ")

    def bilemedi(self):
        self.bildi(False)
    
    def dosya_dogrula(self):
        if len(self.sorular) != 29:
            return True
        if self.sorular[-1] != "SORU DOSYASI":
            return True
        return False

    def yeni_sorular(self, *args):
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

if __name__ == "__main__":
    app = kelimeOyunu()
    app.mainloop()
