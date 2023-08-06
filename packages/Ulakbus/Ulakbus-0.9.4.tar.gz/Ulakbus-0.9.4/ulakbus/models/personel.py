# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
""" Personel Modülü

Bu modül Ulakbüs uygulaması için personel modelini ve  personel ile ilişkili modelleri içerir.

"""
from pyoko import ListNode
from .hitap.hitap_sebep import HitapSebep
from pyoko.lib.utils import lazy_property

from pyoko import Model, field
from zengine.lib.translation import gettext_lazy as _, gettext
from ulakbus.lib.personel import gorunen_kademe_hesapla
from .auth import Unit, User
from ulakbus.settings import SICIL_PREFIX
from .auth import AbstractRole
import datetime


class Personel(Model):
    """Personel Modeli

    Personelin özlük ve iletişim bilgilerini içerir.

    """

    tckn = field.String(_(u"TC No"))
    kurum_sicil_no_int = field.Integer(_(u"Kurum Sicil No"))
    ad = field.String(_(u"Adı"))
    soyad = field.String(_(u"Soyadı"))
    cinsiyet = field.Integer(_(u"Cinsiyet"), choices='cinsiyet')
    uyruk = field.String(_(u"Uyruk"))
    ikamet_adresi = field.String(_(u"İkamet Adresi"))
    ikamet_il = field.String(_(u"İkamet İl"))
    ikamet_ilce = field.String(_(u"İkamet İlçe"))
    adres_2 = field.String(_(u"Adres 2"))
    oda_no = field.String(_(u"Oda Numarası"))
    oda_tel_no = field.String(_(u"Oda Telefon Numarası"))
    cep_telefonu = field.String(_(u"Cep Telefonu"))
    e_posta = field.String(_(u"E-Posta"))
    e_posta_2 = field.String(_(u"E-Posta 2"))
    e_posta_3 = field.String(_(u"E-Posta 3"))
    web_sitesi = field.String(_(u"Web Sitesi"))
    yayinlar = field.String(_(u"Yayınlar"))
    projeler = field.String(_(u"Projeler"))
    kan_grubu = field.Integer(_(u"Kan Grubu"), choices='kan_grubu')
    ehliyet = field.String(_(u"Ehliyet"))
    verdigi_dersler = field.String(_(u"Verdiği Dersler"))
    biyografi = field.Text(_(u"Biyografi"))
    notlar = field.Text(_(u"Notlar"), required=False)
    engelli_durumu = field.String(_(u"Engellilik"))
    engel_grubu = field.String(_(u"Engel Grubu"))
    engel_derecesi = field.Integer(_(u"Engel Derecesi"), choices="personel_engellilik")
    engel_orani = field.Integer(_(u"Engellilik Oranı"))
    cuzdan_seri = field.String(_(u"Seri"))
    cuzdan_seri_no = field.String(_(u"Seri No"))
    baba_adi = field.String(_(u"Baba Adı"))
    ana_adi = field.String(_(u"Ana Adı"))
    dogum_tarihi = field.Date(_(u"Doğum Tarihi"), format="%d.%m.%Y")
    dogum_yeri = field.String(_(u"Doğum Yeri"))
    medeni_hali = field.Integer(_(u"Medeni Hali"), choices="medeni_hali")
    bakmakla_yukumlu_kisi_sayisi = field.Integer(_(u"Yükümlü Olduğu Kişi Sayısı"))
    kayitli_oldugu_il = field.String(_(u"İl"))
    kayitli_oldugu_ilce = field.String(_(u"İlçe"))
    kayitli_oldugu_mahalle_koy = field.String(_(u"Mahalle/Köy"))
    kayitli_oldugu_cilt_no = field.String(_(u"Cilt No"))
    kayitli_oldugu_aile_sira_no = field.String(_(u"Aile Sıra No"))
    kayitli_oldugu_sira_no = field.String(_(u"Sıra No"))
    kimlik_cuzdani_verildigi_yer = field.String(_(u"Cüzdanın Verildiği Yer"))
    kimlik_cuzdani_verilis_nedeni = field.String(_(u"Cüzdanın Veriliş Nedeni"))
    kimlik_cuzdani_kayit_no = field.String(_(u"Cüzdan Kayıt No"))
    kimlik_cuzdani_verilis_tarihi = field.String(_(u"Cüzdan Kayıt Tarihi"))

    kazanilmis_hak_derece = field.Integer(_(u"Güncel Kazanılmış Hak Derece"), index=True)
    kazanilmis_hak_kademe = field.Integer(_(u"Güncel Kazanılmış Hak Kademe"), index=True)
    kazanilmis_hak_ekgosterge = field.Integer(_(u"Kazanılmış Hak Ek Gösterge"), index=True)

    gorev_ayligi_derece = field.Integer(_(u"Güncel Görev Aylığı Derece"), index=True)
    gorev_ayligi_kademe = field.Integer(_(u"Güncel Görev Aylığı Kademe"), index=True)
    gorev_ayligi_ekgosterge = field.Integer(_(u"Görev Aylığı Ek Gösterge"), index=True)

    emekli_muktesebat_derece = field.Integer(_(u"Güncel Emekli Müktesebat Derece"), index=True)
    emekli_muktesebat_kademe = field.Integer(_(u"Güncel Emekli Müktesebat Kademe"), index=True)
    emekli_muktesebat_ekgosterge = field.Integer(_(u"Emekli Müktesebat Ek Gösterge"), index=True)

    kh_sonraki_terfi_tarihi = field.Date(_(u"Kazanılmış Hak Sonraki Terfi Tarihi"), index=True,
                                         format="%d.%m.%Y")
    ga_sonraki_terfi_tarihi = field.Date(_(u"Görev Aylığı Sonraki Terfi Tarihi"), index=True,
                                         format="%d.%m.%Y")
    em_sonraki_terfi_tarihi = field.Date(_(u"Emekli Müktesebat Sonraki Terfi Tarihi"), index=True,
                                         format="%d.%m.%Y")

    birim = Unit(_(u"Birim"))

    # Personelin Kendi Ünvanı
    unvan = field.Integer(_(u"Personel Unvan"), index=True, choices="unvan_kod", required=False)

    # Aşağıdaki bilgiler atama öncesi kontrol edilecek, Doldurulması istenecek
    emekli_sicil_no = field.String(_(u"Emekli Sicil No"), index=True)
    emekli_giris_tarihi = field.Date(_(u"Emekliliğe Giriş Tarihi"), index=True, format="%d.%m.%Y")

    personel_turu = field.Integer(_(u"Personel Türü"), choices="personel_turu")
    hizmet_sinifi = field.Integer(_(u"Hizmet Sınıfı"), choices="hizmet_sinifi")
    statu = field.Integer(_(u"Statü"), choices="personel_statu")
    brans = field.String(_(u"Branş"), index=True)

    # akademik personeller icin sozlesme sureleri
    gorev_suresi_baslama = field.Date(_(u"Görev Süresi Başlama"), index=True, format="%d.%m.%Y")
    gorev_suresi_bitis = field.Date(_(u"Görev Süresi Bitiş"), index=True, format="%d.%m.%Y")

    # todo: durum_degisikligi yonetimi
    # kurumda ilk goreve baslama bilgileri, atama modelinden elde edilip
    # edilemeyecegini soracagiz. mevcut otomasyonda ayrilmalar da burada tutuluyor.
    # bunu tarih ve durum_degisikligi fieldlarindan olusan bir listnode seklinde tutabiliriz.
    goreve_baslama_tarihi = field.Date(_(u"Göreve Başlama Tarihi"), index=True, format="%d.%m.%Y")
    baslama_sebep = HitapSebep()

    # aday ve idari memurlar icin mecburi hizmet suresi
    mecburi_hizmet_suresi = field.Date(_(u"Mecburi Hizmet Süresi"), index=True, format="%d.%m.%Y")

    # Arama için kullanılacak Flaglar
    kadro_derece = field.Integer(default=0)
    aday_memur = field.Boolean()
    arsiv = field.Boolean()  # ayrilmis personeller icin gecerlidir.

    user = User(one_to_one=True)

    class Meta:
        app = 'Personel'
        verbose_name = _(u"Personel")
        verbose_name_plural = _(u"Personeller")
        list_fields = ['ad', 'soyad', 'tckn', 'durum']
        search_fields = ['ad', 'soyad', 'cep_telefonu', 'tckn']

    def durum(self):
        return self.nufus_kayitlari.durum if self.nufus_kayitlari.key else None

    durum.title = "Durum"

    @lazy_property
    def gorunen_kazanilmis_hak_kademe(self):
        return gorunen_kademe_hesapla(int(self.kazanilmis_hak_derece),
                                      int(self.kazanilmis_hak_kademe))

    @lazy_property
    def gorunen_gorev_ayligi_kademe(self):
        return gorunen_kademe_hesapla(int(self.gorev_ayligi_derece), int(self.gorev_ayligi_kademe))

    @lazy_property
    def gorunen_emekli_muktesebat_kademe(self):
        return gorunen_kademe_hesapla(int(self.emekli_muktesebat_derece),
                                      int(self.emekli_muktesebat_kademe))

    @lazy_property
    def atama(self):
        """atama

        Personelin atama bilgilerini iceren atama nesnesini getirir.

        Returns:
            Atama örneği (instance)

        """
        # Mevcut pyoko API'i ile uyumlu olmasi icin, geriye bos bir Atama nesnesi dondurur.
        atamalar = Atama.objects.order_by('-goreve_baslama_tarihi').filter(personel=self)
        return atamalar[0] if atamalar else Atama()

    @lazy_property
    def kadro(self):
        """Kadro

        Personelin atama bilgilerinden kadrosuna erişir.

        Returns:
            Kadro örneği (instance)

        """

        return self.atama.kadro

    @lazy_property
    def sicil_no(self):
        """Kadro

        Personelin atama bilgilerinden sicil numarasina erişir.

        Returns:
            Sicil No (str)

        """

        return self.atama.kurum_sicil_no

    def gorevlendirme_tarih_kontrol(self, baslama_tarihi, bitis_tarihi):
        """
        Eklenmek istenen görevlendirmenin, başlama tarihi ve bitiş tarihinin tutarlılığını ve
        personelin mevcut Kurum İçi ve Kurum Dışı görevlendirmeleriyle çakışıp çakışmadığını  kontrol eder.

        Personelin mevcut görevlendirmeleri içinde başlama tarihi, eklenmek istenen görevlendirmenin bitiş
        tarihinden küçük görevlendirmeler ve bitiş tarihi, eklenmek istenen görevlendirmenin başlama tarihinden
        büyük olan görevlendirmeler sorgulanır. Sorgu sonucunda dönen görevlendirme varsa, personel bu tarih
        aralığında görevde demektir. Eğer sorgu sonucunda bir görevlendirme dönmüyorsa personel belirtilen tarih
        aralığında görev aabilir demektir.

        KurumIciGorevlendirmeBilgileri ve KurumDisiGorevlendirmeBilgileri modellerinin pre_save() metodlarında
        bu kontrol yapılır. Model oluşturulduğunda ya da baslama_tarihi bitis_tarihi alanları güncellendiğinde bu
        kontrol yapılır.

        Eğer tarihler görevlendirme için uygunsa kayıt işlemine devam edilir. Uygun değilse
        exception fırlatılır.

        Args:
            baslama_tarihi (datetime): Eklenmek istenen görevlendirme başlama tarihi
            bitis_tarihi (datetime): Eklenmek istenen görevlendirme bitiş tarihi

        """
        if baslama_tarihi > bitis_tarihi:
            raise Exception("Bitiş tarihi başlangıç tarihinden büyük olmalıdır.")
        illegal_gorevlendirme_kurum_ici = KurumIciGorevlendirmeBilgileri.objects.filter(
            baslama_tarihi__lte=bitis_tarihi,
            bitis_tarihi__gte=baslama_tarihi,
            personel=self
        )
        illegal_gorevlendirme_kurum_disi = KurumDisiGorevlendirmeBilgileri.objects.filter(
            baslama_tarihi__lte=bitis_tarihi,
            bitis_tarihi__gte=baslama_tarihi,
            personel=self
        )

        if illegal_gorevlendirme_kurum_ici or illegal_gorevlendirme_kurum_disi:
            raise Exception("Belirtilen tarihlerde, belirtilen personel başka bir görevlendirmede olmamalıdır.")


    @lazy_property
    def kurum_ici_gorevlendirme(self):
        """kurum_ici_gorevlendirme

        Personelin varsa kurum içi görevlendirme bilgilerini getirir.

        Returns:
            KurumIciGorevlendirmeBilgileri listesi (instance list)
        """
        simdiki_tarih = datetime.date.today()
        gorevlendirmeler = KurumIciGorevlendirmeBilgileri.objects.filter(
            kurum_ici_gorev_baslama_tarihi__lte=simdiki_tarih,
            kurum_ici_gorev_bitis_tarihi__gte=simdiki_tarih,
            personel=self
        )

        return gorevlendirmeler[0] if gorevlendirmeler.count() == 1 else None

    @lazy_property
    def kurum_disi_gorevlendirme(self):
        """kurum_disi_gorevlendirme

        Personelin varsa kurum dışı görevlendirme bilgilerini getiri.

        Returns:
            KurumDisiGorevlendirmeBilgileri listesi (instance list)

        """

        simdiki_tarih = datetime.date.today()
        gorevlendirmeler = KurumDisiGorevlendirmeBilgileri.objects.filter(
            kurum_disi_gorev_baslama_tarihi__lte=simdiki_tarih,
            kurum_disi_gorev_bitis_tarihi__gte=simdiki_tarih,
            personel=self
        )

        return gorevlendirmeler[0] if gorevlendirmeler.count() == 1 else None

    @property
    def kurum_sicil_no(self):
        return "%s-%s" % (SICIL_PREFIX, self.kurum_sicil_no_int)

    class IstenAyrilma(ListNode):
        gorevden_ayrilma_tarihi = field.Date(_(u"Görevden Ayrılma Tarihi"), index=True,
                                             format="%d.%m.%Y")
        gorevden_ayrilma_sebep = HitapSebep()

        gorevden_ayrilma_not = field.Text(_(u"Notlar"), required=False)

    def __unicode__(self):
        return gettext(u"%(ad)s %(soyad)s") % {'ad': self.ad, 'soyad': self.soyad}


class AdresBilgileri(Model):
    """Adres Bilgileri Modeli

    Personele ait adres bilgilerini içeren modeldir.

    Personelin birden fazla adresi olabilir.

    """

    ad = field.String(_(u"Adres Adı"))
    adres = field.String(_(u"Adres"))
    ilce = field.String(_(u"İlçe"))
    il = field.String(_(u"İl"))
    personel = Personel()

    class Meta:
        verbose_name = _(u"Adres Bilgisi")
        verbose_name_plural = _(u"Adres Bilgileri")

    def __unicode__(self):
        return "%s %s" % (self.ad, self.il)


class KurumIciGorevlendirmeBilgileri(Model):
    """Kurum İçi Görevlendirme Bilgileri Modeli

    Personelin, kurum içi görevlendirme bilgilerine ait modeldir.

    Görevlendirme bir birim ile ilişkili olmalıdır.

    """

    gorev_tipi = field.Integer(_(u"Görev Tipi"), choices="gorev_tipi")
    baslama_tarihi = field.Date(_(u"Başlama Tarihi"), format="%d.%m.%Y")
    bitis_tarihi = field.Date(_(u"Bitiş Tarihi"), format="%d.%m.%Y")
    birim = Unit(verbose_name=_(u"Birim"))
    soyut_rol = AbstractRole(verbose_name=_(u"Görev"))
    aciklama = field.String(_(u"Açıklama"))
    resmi_yazi_sayi = field.String(_(u"Resmi Yazı Sayı"))
    resmi_yazi_tarih = field.Date(_(u"Resmi Yazı Tarihi"), format="%d.%m.%Y")
    personel = Personel()

    class Meta:
        """``form_grouping`` kullanıcı arayüzeyinde formun temel yerleşim planını belirler.

        Layout grid (toplam 12 sütun) içerisindeki değerdir.

        Her bir ``layout`` içinde birden fazla form grubu yer alabilir: ``groups``

        Her bir grup, grup başlığı ``group_title``, form öğeleri ``items`` ve bu grubun
        açılır kapanır olup olmadığını belirten boolen bir değerden ``collapse`` oluşur.

        """

        verbose_name = _(u"Kurum İçi Görevlendirme")
        verbose_name_plural = _(u"Kurum İçi Görevlendirmeler")
        form_grouping = [
            {
                "layout": "4",
                "groups": [
                    {
                        "group_title": _(u"Görev"),
                        "items": ["gorev_tipi", "kurum_ici_gorev_baslama_tarihi",
                                  "kurum_ici_gorev_bitis_tarihi",
                                  "birim", "aciklama"],
                        "collapse": False
                    }
                ]

            },
            {
                "layout": "2",
                "groups": [
                    {
                        "group_title": _(u"Resmi Yazi"),
                        "items": ["resmi_yazi_sayi", "resmi_yazi_tarih"],
                        "collapse": False
                    }
                ]

            },
        ]

    def __unicode__(self):
        return "%s %s" % (self.gorev_tipi, self.aciklama)

    def pre_save(self):
        changed_fields = self.changed_fields()
        if changed_fields is None or "baslama_tarihi" in changed_fields or "bitis_tarihi" in changed_fields:
            self.personel.gorevlendirme_tarih_kontrol(self.baslama_tarihi,
                                                      self.bitis_tarihi)


class KurumDisiGorevlendirmeBilgileri(Model):
    """Kurum Dışı Görevlendirme Bilgileri Modeli

    Personelin bağlı olduğu kurumun dışındaki görev bilgilerine ait modeldir.

    """

    gorev_tipi = field.Integer(_(u"Görev Tipi"), choices="gorev_tipi")
    baslama_tarihi = field.Date(_(u"Başlama Tarihi"), format="%d.%m.%Y")
    bitis_tarihi = field.Date(_(u"Bitiş Tarihi"), format="%d.%m.%Y")
    aciklama = field.Text(_(u"Açıklama"))
    resmi_yazi_sayi = field.String(_(u"Resmi Yazı Sayı"))
    resmi_yazi_tarih = field.Date(_(u"Resmi Yazı Tarihi"), format="%d.%m.%Y")
    maas = field.Boolean(_(u"Maaş"))
    yevmiye = field.Boolean(_(u"Yevmiye"), default=False)
    yolluk = field.Boolean(_(u"Yolluk"), default=False)
    ulke = field.Integer(_(u"Ülke"), default="90", choices="ulke")
    soyut_rol = AbstractRole(verbose_name=_(u"Görev"))
    personel = Personel()

    class Meta:
        verbose_name = _(u"Kurum Dışı Görevlendirme")
        verbose_name_plural = _(u"Kurum Dışı Görevlendirmeler")
        list_fields = ["ulke", "gorev_tipi", "kurum_disi_gorev_baslama_tarihi"]
        list_filters = ["ulke", "gorev_tipi", "kurum_disi_gorev_baslama_tarihi"]
        search_fields = ["aciklama", ]
        form_grouping = [
            {
                "layout": "4",
                "groups": [
                    {
                        "group_title": _(u"Görev"),
                        "items": ["gorev_tipi", "kurum_disi_gorev_baslama_tarihi",
                                  "kurum_disi_gorev_bitis_tarihi",
                                  "ulke",
                                  "aciklama"],
                        "collapse": False
                    }
                ]

            },
            {
                "layout": "2",
                "groups": [
                    {
                        "group_title": _(u"Resmi Yazi"),
                        "items": ["resmi_yazi_sayi", "resmi_yazi_tarih"],
                        "collapse": False
                    },
                    {
                        "items": ["maas", "yevmiye", "yolluk"],
                        "collapse": False
                    }
                ]

            },
        ]

    def __unicode__(self):
        return "%s %s %s" % (self.gorev_tipi, self.aciklama, self.ulke)

    def pre_save(self):
        changed_fields = self.changed_fields()
        if changed_fields is None or "baslama_tarihi" in changed_fields or "bitis_tarihi" in changed_fields:
            self.personel.gorevlendirme_tarih_kontrol(self.baslama_tarihi,
                                                      self.bitis_tarihi)


class Kadro(Model):
    """Kadro Modeli

    Kurum için ayrılmış Kadro bilgilerine modeldir.

    Kadrolar 4 halde bulunabilirler: SAKLI, IZINLI, DOLU ve BOŞ

        * SAKLI: Saklı kadro, atama yapılmaya müsadesi olmayan, etkinlik onayı alınmamış
          fakat kurum için ayrılmış potansiyel kadroyu tanımlar.
        * IZINLI: Henüz atama yapılmamış, fakat etkinlik onayı alınmış kadroyu tanımlar.
        * DOLU: Bir personel tarafından işgal edilmiş bir kadroyu tanımlar. Ataması yapılmıştır.
        * BOŞ: Çeşitli sebepler ile DOLU iken boşaltılmış kadroyu tanınmlar.

    ``unvan`` ve ``unvan_kod`` karşıt alanlardır. Birisi varken diğeri mevcut olamaz.

    """

    kadro_no = field.Integer(_(u"Kadro No"), required=False)
    derece = field.Integer(_(u"Derece"), required=False)
    durum = field.Integer(_(u"Durum"), choices="kadro_durumlari", required=False)
    birim = Unit(_(u"Birim"), required=False)
    aciklama = field.String(_(u"Açıklama"), index=True, required=False)
    unvan = field.Integer(_(u"Unvan"), index=True, choices="unvan_kod", required=False)
    unvan_aciklama = field.String(_(u"Unvan Aciklama"), index=True, required=False)

    class Meta:
        app = 'Personel'
        verbose_name = _(u"Kadro")
        verbose_name_plural = _(u"Kadrolar")
        list_fields = ['durum', 'unvan', 'aciklama']
        search_fields = ['unvan', 'derece']
        list_filters = ['durum']

    def __unicode__(self):
        # tn: Kadro bilgileri gösterilirken kullanılan mesaj
        return gettext(u"%(no)s - %(unvan)s %(derece)s. derece") % {
            'no': self.kadro_no,
            'unvan': self.get_unvan_display(),
            'derece': self.derece
        }


class Izin(Model):
    """İzin Modeli

    Personelin ücretli izin bilgilerini içeren modeldir.

    """

    tip = field.Integer(_(u"Tip"), choices="izin")
    baslangic = field.Date(_(u"Başlangıç"), format="%d.%m.%Y")
    bitis = field.Date(_(u"Bitiş"), format="%d.%m.%Y")
    onay = field.Date(_(u"Onay"), format="%d.%m.%Y")
    adres = field.String(_(u"Geçireği Adres"))
    telefon = field.String(_(u"Telefon"))
    personel = Personel()
    vekil = Personel()

    class Meta:
        app = 'Personel'
        verbose_name = _(u"İzin")
        verbose_name_plural = _(u"İzinler")
        list_fields = ['tip', 'baslangic', 'bitis', 'onay', 'telefon']
        search_fields = ['tip', 'baslangic', 'onay']

    def __unicode__(self):
        return '%s %s' % (self.tip, self.onay)


class UcretsizIzin(Model):
    """Ücretsiz izin Modeli

    Personelin ücretsiz izin bilgilerini içeren modeldir.

    """

    tip = field.Integer(_(u"Tip"), choices="ucretsiz_izin")
    baslangic = field.Date(_(u"İzin Başlangıç Tarihi"), format="%d.%m.%Y")
    bitis = field.Date(_(u"İzin Bitiş Tarihi"), format="%d.%m.%Y")
    donus_tarihi = field.Date(_(u"Dönüş Tarihi"), format="%d.%m.%Y")
    donus_tip = field.Integer(_(u"Dönüş Tip"))
    onay_tarihi = field.Date(_(u"Onay Tarihi"), format="%d.%m.%Y")
    personel = Personel()

    class Meta:
        app = 'Personel'
        verbose_name = _(u"Ücretsiz İzin")
        verbose_name_plural = _(u"Ücretsiz İzinler")
        list_fields = ['tip', 'baslangic', 'bitis', 'donus_tarihi']
        search_fields = ['tip', 'onay_tarihi']

    def __unicode__(self):
        return '%s %s' % (self.tip, self.onay_tarihi)


class Atama(Model):
    """Atama Modeli

    Personelin atama bilgilerini içeren modeldir.

    """

    ibraz_tarihi = field.Date(_(u"İbraz Tarihi"), index=True, format="%d.%m.%Y")
    durum = HitapSebep()
    nereden = field.Integer(_(u"Nereden"), index=True)  # modele baglanacak.
    atama_aciklama = field.String(_(u"Atama Açıklama"), index=True)
    goreve_baslama_tarihi = field.Date(_(u"Göreve Başlama Tarihi"), index=True, format="%d.%m.%Y")
    goreve_baslama_aciklama = field.String(_(u"Göreve Başlama Açıklama"), index=True)
    sicil_no = field.String(_(u"Sicil No"))
    kadro = Kadro()
    personel = Personel()
    # Arama için eklendi, Orjinali personelde tutulacak
    hizmet_sinifi = field.Integer(_(u"Hizmet Sınıfı"), index=True, choices="hizmet_sinifi")

    class Meta:
        app = 'Personel'
        verbose_name = _(u"Atama")
        verbose_name_plural = _(u"Atamalar")
        list_fields = ['hizmet_sinifi', 'goreve_baslama_tarihi', 'ibraz_tarihi',
                       'durum']
        search_fields = ['hizmet_sinif', 'statu']

    def __unicode__(self):
        return '%s %s %s' % (self.personel.kurum_sicil_no,
                             self.goreve_baslama_tarihi, self.ibraz_tarihi)

    @classmethod
    def personel_guncel_atama(cls, personel):
        """
        Personelin goreve_baslama_tarihi ne göre son atama kaydını döndürür.

        Returns:
            Atama örneği (instance)

        """

        return cls.objects.order_by('-goreve_baslama_tarihi').filter(personel=personel)[0]

    @classmethod
    def personel_ilk_atama(cls, personel):
        """
        Personelin goreve_baslama_tarihi ne göre ilk atama kaydını döndürür.

        Returns:
            Atama örneği (instance)

        """

        return cls.objects.order_by('goreve_baslama_tarihi').filter(personel=personel)[0]

    def post_save(self):
        # Personel modeline arama için eklenen kadro_derece set edilecek
        self.personel.kadro_derece = self.kadro.derece
        self.personel.save()

        # Atama sonrası kadro dolu durumuna çekilecek
        self.kadro.durum = 4
        self.kadro.save()

    def pre_save(self):
        self.hizmet_sinifi = self.personel.hizmet_sinifi
        # Atama kaydetmeden önce kadro boş durumuna çekilecek
        self.kadro.durum = 2
        self.kadro.save()

    def post_delete(self):
        # Atama silinirse kadro boş duşuma çekilecek
        self.kadro.durum = 2
        self.kadro.save()

        # personelin kadro derecesi 0 olacak
        self.personel.kadro_derece = 0
        self.personel.save()


class SaglikRaporu(Model):
    personel = Personel(_(u"Raporu Alan Personel"))
    rapor_cesidi = field.Integer(_(u"Rapor Çeşidi"), required=True, choices='saglik_raporu_cesitleri')
    sure = field.Integer(_(u"Gün"), required=True)
    baslama_tarihi = field.Date(_(u"Rapor Başlangıç Tarihi"), required=True)
    bitis_tarihi = field.Date(_(u"Raporlu Olduğu Son Gün"), required=True)
    onay_tarihi = field.Date(_(u"Onay Tarihi"), required=True)
    raporun_alindigi_il = field.Integer(_(u"Raporun Alındığı İl"), choices='iller', required=False)
    nerden_alindigi = field.String(_(u"Sağlık Raporunun Alındığı Kurum"), required=True)
    gecirecegi_adres = field.Text(_(u"Geçireceği Adres"), required=False)
    telefon = field.String(_(u"Telefon Numarası"), required=False)

    class Meta:
        verbose_name = _(u"Sağlık Raporu")
        verbose_name_plural = _(u"Sağlık Raporları")
        list_fields = ['rapor_cesidi', 'sure', 'bitis_tarihi']

    def __unicode__(self):
        return "%s %s - %s - %s" % (self.personel.ad, self.personel.soyad,
                                    self.get_rapor_cesidi_display(), self.bitis_tarihi)


class Ceza(Model):
    """

    Ceza Modeli

    Personelin ceza bilgilerini içeren modeldir.

    """

    dosya_sira_no = field.String(_(u"Dosya No"), unique=True)
    muhbir_musteki_ad_soyad = field.String(_(u"Muhbir veya Müştekinin Adı Soyadı"), required=False)
    ihbar_sikayet_suc_ogrenildigi_tarih = field.Date(
        _(u"İhbar, Şikayet veya Suçun Öğrenildiği Tarih"))
    personel = Personel(_(u"Soruşturma Yapılan Personel"))
    sucun_nevi = field.String(_(u"Suçun Nev'i"), required=False)
    af_kapsami = field.String(_(u"Af Kapsamı"), required=False)
    kapsadigi_donem_tarihler = field.String(_(u"Kapsadığı Dönem Tarihler"), required=False)
    acilis_tarihi = field.Date(_(u"Açılış Tarihi"))
    baslama_tarihi = field.Date(_(u"Başlangıç Tarihi"))
    bitis_tarihi = field.Date(_(u"Bitiş Tarihi"))
    teklif_edilen_ceza = field.Integer(_(u"Teklif Edilen Ceza"), choices="ceza_turleri",
                                       required=False)
    takdir_edilen_ceza = field.Integer(_(u"Takdir Edilen Ceza"), choices="ceza_turleri",
                                       required=False)
    kararin_teblig_tarihi = field.Date(_(u"Kararın Tebliğ Tarihi"))
    itiraz_neticesi = field.String(_(u"İtiraz Edilmişse Neticesi"), required=False)
    dusunceler = field.String(_(u"Düşünceler"), required=False)

    class TayinEdilenSorusturmacilar(ListNode):
        # class Meta:
        #     title = _(u"Tayin Edilen Soruşturmacılar")
        sorusturmaci_adi_soyadi = field.String(_(u"Soruşturmacının Adı Soyadı"))

    class Meta:
        verbose_name = _(u"İdari Ceza")
        verbose_name_plural = _(u"İdari Cezalar")
        list_fields = ['dosya_sira_no', 'baslama_tarihi', 'bitis_tarihi', 'takdir_edilen_ceza']

    def __unicode__(self):
        return "%s %s - %s" % (self.personel.ad, self.personel.soyad, self.dosya_sira_no)
