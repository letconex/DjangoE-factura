"""Django company model inspired by ANAF API"""
from django.db import models

class date_generale(models.Model):
    cui = models.IntegerField(blank=False, unique=True)
    denumire = models.CharField(max_length=100, blank=False, unique=True)
    adresa = models.CharField(max_length=100, blank=False)
    nrRegCom = models.CharField(max_length=100, blank=False, unique=True)
    telefon = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    codPostal = models.IntegerField()
    act = models.CharField(max_length=100)
    stare_inregistrare = models.CharField(max_length=100)
    data_inregistrare = models.CharField(max_length=100)
    cod_CAEN = models.CharField(max_length=100)
    iban = models.CharField(max_length=100)
    statusRO_e_Factura = models.BooleanField()
    organFiscalCompetent = models.CharField(max_length=100)
    forma_de_proprietate = models.CharField(max_length=100)
    forma_organizare = models.CharField(max_length=100)
    forma_juridica = models.CharField(max_length=100)

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=["cui", "denumire", "adresa", "nrRegCom"],
                name="dg_unique_constraint")]

class inregistrare_scop_Tva(models.Model):
    scpTVA = models.BooleanField(blank=True, null=True)
    
class PerioadeTVA(inregistrare_scop_Tva):
    data_inceput_ScpTVA = models.DateField(blank=True, null=True)
    data_sfarsit_ScpTVA = models.DateField(blank=True, null=True)
    data_anul_imp_ScpTVA = models.DateField(blank=True, null=True)
    mesaj_ScpTVA = models.CharField(max_length=255, blank=True, null=True)

class inregistrare_RTVAI(models.Model):
    dataInceputTvaInc = models.DateField(max_length=100)
    dataSfarsitTvaInc = models.DateField(max_length=100)
    dataActualizareTvaInc = models.DateField(max_length=100)
    dataPublicareTvaInc = models.DateField(max_length=100)
    tipActTvaInc = models.CharField(max_length=100)
    statusTvaIncasare = models.BooleanField()

class stare_inactiv(models.Model):
    dataInactivare = models.CharField(max_length=100)
    dataReactivare = models.CharField(max_length=100)
    dataPublicare = models.CharField(max_length=100)
    dataRadiere = models.CharField(max_length=100)
    statusInactivi = models.BooleanField()

class inregistrare_SplitTVA(models.Model):
    dataInceputSplitTVA = models.CharField(max_length=100)
    dataAnulareSplitTVA = models.CharField(max_length=100)
    statusSplitTVA = models.BooleanField()

class adresa_sediu_social(models.Model):
    sdenumire_Strada = models.CharField(max_length=100)
    snumar_Strada = models.IntegerField()
    sdenumire_Localitate = models.CharField(max_length=100)
    scod_Localitate = models.IntegerField()
    sdenumire_Judet = models.CharField(max_length=100)
    scod_Judet = models.IntegerField()
    scod_JudetAuto = models.CharField(max_length=100)
    stara = models.CharField(max_length=100)
    sdetalii_Adresa = models.CharField(max_length=100)
    scod_Postal = models.IntegerField()

class adresa_domiciliu_fiscal(models.Model):
    ddenumire_Strada = models.CharField(max_length=100)
    dnumar_Strada = models.IntegerField()
    ddenumire_Localitate = models.CharField(max_length=100)
    dcod_Localitate = models.IntegerField()
    ddenumire_Judet = models.CharField(max_length=100)
    dcod_Judet = models.IntegerField()
    dcod_JudetAuto = models.CharField(max_length=100)
    dtara = models.CharField(max_length=100)
    ddetalii_Adresa = models.CharField(max_length=100)
    dcod_Postal = models.IntegerField()

class extras(models.Model):
    contactperson = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    web = models.CharField(max_length=100)
    comments = models.CharField(max_length=100)

class Vendor(models.Model):
    """General class with all intermediate fields"""
    date_generale = models.ManyToManyField(date_generale)
    inregistrare_scop_Tva = models.ManyToManyField(inregistrare_scop_Tva)
    inregistrare_RTVAI = models.ManyToManyField(inregistrare_RTVAI)
    stare_inactiv = models.ManyToManyField(stare_inactiv)
    inregistrare_SplitTVA = models.ManyToManyField(inregistrare_SplitTVA)
    adresasediu_social = models.ManyToManyField(adresa_sediu_social)
    adresadomiciliu_fiscal = models.ManyToManyField(adresa_domiciliu_fiscal)
    extras = models.ManyToManyField(extras)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.date_generale}"

    class Meta:
        """Use vendors db for this model"""
        db_table: str = "vendor"
        app_label: str = "crm"
        managed = False
        get_latest_by: str = "created_at"
        verbose_name: str = "Vendors DB model"

# class CascadeVendor(models.Model):
#     """General class with all intermediate fields"""
#     date_generale = models.ForeignKey(date_generale, on_delete=models.CASCADE)
#     inregistrare_scop_Tva = models.ForeignKey(
#         inregistrare_scop_Tva, on_delete=models.CASCADE)
#     inregistrare_RTVAI = models.ForeignKey(inregistrare_RTVAI, on_delete=models.CASCADE)
#     stare_inactiv = models.ForeignKey(stare_inactiv, on_delete=models.CASCADE)
#     inregistrare_SplitTVA = models.ForeignKey(
#         inregistrare_SplitTVA, on_delete=models.CASCADE)
#     adresa_sediu_social = models.ForeignKey(
#         adresa_sediu_social, on_delete=models.CASCADE)
#     adresa_domiciliu_fiscal = models.ForeignKey(
#         adresa_domiciliu_fiscal, on_delete=models.CASCADE)
#     extras = models.ForeignKey(extras, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
