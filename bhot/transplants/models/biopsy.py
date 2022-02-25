import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from bhot.transplants.models.transplant import Transplant
from bhot.users.models import UserScopedModel


class Biopsy(UserScopedModel):
    class Meta:
        verbose_name_plural = "biopsies"

    class PreTransplantBiopsyType(models.TextChoices):
        PRE_IMPLANT = "preimplantation", _("preimplantation")
        PROCUREMENT = "procurement", _("procurementt")

    class ClinicalBiopsyIndication(models.TextChoices):
        PROTOCOL = "protocol", _("protocol")
        DGF = "DGF", _("Delayed Graft Function")
        SD = "Slow deterioration", _(
            "Slow deterioration (progressive increase in serum creatinine over time)"
        )
        ARF = "ARF", _("Acute renal failure")
        PROT_U = "Proteinuria", _("Proteinuria")
        HEMATURIA = "Hematuria", _("Hematuria")
        SUSP_AR = "SUSP_AR", _("Suspicious for acute rejection")
        SUSP_PVN = "SUSP_PVN", _("Suspicious for Polyoma Virus Nephropathy")
        TRANSPLANTECTOMY = "Transplantectomy", _("Transplantectomy biopsy")
        DENOVO_DSA = "de novo DSA", _("de novo DSA")
        FOLLOWUP = "Follow-up", _("Follow-up from previous biopsy")
        # other:specify

    class CreatinemiaUnits(models.TextChoices):
        UMOL_L = "umol/L", _("umol/L")
        MG_L = "mg/L", _("mgdL")

    class CreatinuriaUnits(models.TextChoices):
        MMOL_L = "mmol/L", _("mmol/L")

    class ProteinuriaUnits(models.TextChoices):
        G_G = "g/g", _("g/g")
        G_24H = "g/24h", _("g/24h")
        MG_DL = "mg/dL", _("mg/dL")
        G_L = "g/L", _("g/L")
        MG_MMOL = "mg/mmol", _("mg/mmol")
        G_MMOL = "g/mmol", _("g/mmol")

    class ProtDipstick(models.TextChoices):
        ZERO = "0", _("0")
        PLUS_1 = "+", _("+")
        PLUS_2 = "++", _("++")
        PLUS_3 = "+++", _("+++")
        PLUS_4 = "++++", _("++++")

    class ProtDipstickUnits(models.TextChoices):
        MG_DL_RANGE = "mg/dL range", _("mg/dL range")

    class ProtCreatRatioUnits(models.TextChoices):
        G_G = "g/g", _("g/g")

    class Immunosuppressants(models.TextChoices):
        ABATACEPT = "Abatacept", _("Abatacept")
        AZATHIOPRINE = "Azathioprine", _("Azathioprine")
        BELATACEPT = "Belatacept", _("Belatacept")
        CYCLOSPORINE = "Cyclosporine", _("Cyclosporine")
        EVEROLIMUS = "Everolimus", _("Everolimus")
        MMF = "MMF", _("MMF")
        MPA = "MPA", _("MPA")
        PREDNISONE = "Prednisone", _("Sirolimus")
        SIROLIMUS = "Sirolimus", _("Azathioprine")
        TACROLIMUS = "Tacrolimus", _("Tacrolimus")
        # other:specify

    class ImmunosuppressantDoseUnits(models.TextChoices):
        MG_DAY = "mg/day", _("mg/day")
        MG_2X_DAY = "mg twice per day", _("mg twice per day")
        MG_WEEK = "mg per week", _("mg per week")
        MG_15_DAYS = "mg per 15 days", _("mg per 15 days")
        # other:free text

    class BxRejectionTreatment(models.TextChoices):
        ALEMTUZUMAB = "Alemtuzumab", _("Alemtuzumab")
        BORTEZOMIB = "Bortezomib", _("Bortezomib")
        ATG = "Anti-thymocyte globulin", _("Anti-thymocyte globulin")
        ECULIZIMAB = "Eculizimab", _("Eculizimab")
        IVIG = "IVIG", _("IVIG")
        PLASMAPHARESIS = "Plasmapharesis", _("Plasmapharesis")
        RITUXIMAB = "Rituximab", _("Rituximab")

    class BxRejectionTreatmentResponse(models.TextChoices):
        COMPLETE = "Complete response", _(
            "Complete response (Cr within 10% of baseline)"
        )
        PARTIAL = "Partial response", _("Partial response (Cr 10-50% over baseline) ")
        NONE = "No response", _("No response (Cr >50% increase over baseline)")

    class iDSAclass(models.TextChoices):
        CLASS_I = "I", _("I")
        CLASS_II = "II", _("II")
        CLASS_I_II = "I/II", _("I/II")

    class iDSAspecifiity(models.TextChoices):
        A = "A", _("A")
        B = "B", _("B")
        CW = "Cw", _("Cw")
        DR = "DR", _("DR")
        DQ = "DQ", _("DQ")
        DP = "DP", _("DP")

    class nonAntiHlaDsa(models.TextChoices):
        AT1R = "AT1R", _("AT1R")
        MICA = "MICA", _("MICA")
        ECXM = "ECXM", _("ECXM")
        VIMENTIN = "vimentin", _("vimentin")
        COLLAGEN = "collagen", _("collagen")
        KA1 = "K-a-1", _("K-a-1")
        TUBULIN = "tubulin", _("tubulin")
        # other:specify

    class GraftFailureCause(models.TextChoices):
        DEATH = "death", _("death")
        INFECTION = "infection", _("infection")
        RECURRENT_DISEASE = "recurrent disease", _("recurrent disease")
        REJECTION = "rejection", _("rejection")

    # Main info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transplant = models.ForeignKey(Transplant, null=True, on_delete=models.SET_NULL)
    biopsy_date = models.DateField()

    pre_transplant_biopsy_type = models.CharField(
        max_length=100,
        choices=PreTransplantBiopsyType.choices,
        blank=True,
    )
    clinical_biopsy_indication = models.CharField(
        max_length=100,
        choices=ClinicalBiopsyIndication.choices,
        blank=True,
    )
    biopsy_creatinemia = models.FloatField(
        blank=True,
        null=True,
    )
    biopsy_creatinemia_units = models.CharField(
        max_length=50,
        default=CreatinemiaUnits.UMOL_L,
        choices=CreatinemiaUnits.choices,
    )
    biopsy_creatinuria = models.FloatField(
        blank=True,
        null=True,
    )
    biopsy_creatinuria_units = models.CharField(
        max_length=50,
        default=CreatinuriaUnits.MMOL_L,
        choices=CreatinuriaUnits.choices,
    )
    biopsy_proteinuria = models.FloatField(
        blank=True,
        null=True,
    )
    biopsy_proteinuria_units = models.CharField(
        max_length=50,
        default=ProteinuriaUnits.MG_DL,
        choices=ProteinuriaUnits.choices,
    )
    biopsy_proteinuria_dipstick = models.CharField(
        max_length=20,
        blank=True,
    )
    biopsy_proteinuria_dipstick_units = models.CharField(
        max_length=50,
        default=ProtDipstickUnits.MG_DL_RANGE,
        choices=ProtDipstickUnits.choices,
    )
    biopsy_proteinuria_date = models.DateField(
        blank=True,
        null=True,
    )
    biopsy_prot_creat_ratio = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(30.0)],
        blank=True,
        null=True,
        verbose_name="Protein/creatinine ratio (g/g)",
    )
    biopsy_prot_creat_ratio_units = models.CharField(
        max_length=50,
        default=ProtCreatRatioUnits.G_G,
        choices=ProtCreatRatioUnits.choices,
    )
    biopsy_immunosuppressants = models.CharField(
        max_length=100,
        blank=True,
        choices=Immunosuppressants.choices,
        verbose_name="Immunosuppresants",
    )
    biopsy_immunosuppressant_dose = models.FloatField(
        blank=True,
        null=True,
        choices=ImmunosuppressantDoseUnits.choices,
        verbose_name="Immunosuppresant dose",
    )  # link immunosuppressant to dose (+ sign to add med + dose)
    biopsy_immunosuppressant_c0 = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Immunosuppressant trough level:C0 (ng/mL)",
    )
    biopsy_immunosuppressant_c0 = models.FloatField(
        blank=True,
        null=True,
        verbose_name="immunosuppressant postdose level: C2 (ng/mL)",
    )
    biopsy_rejection_treatment = models.CharField(
        max_length=100,
        choices=BxRejectionTreatment.choices,
        blank=True,
        verbose_name="rejection treatment",
    )
    biopsy_treatment_start_date = models.DateField(
        blank=True,
        null=True,
    )  # link to treatment
    biopsy_treatment_response = models.CharField(
        max_length=100,
        choices=BxRejectionTreatmentResponse.choices,
        blank=True,
        verbose_name="Rejection treatment response",
    )
    biopsy_rejection_date = models.DateField(
        blank=True,
        null=True,
    )
    biopsy_dd_cf_dna = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True,
        null=True,
        verbose_name="Donor-derived cf-DNA (%)",
    )
    biopsy_bkv_load = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="BKV load (copies/mL)",
    )
    biopsy_cmv_load = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="CMV load (copies/mL)",
    )
    biopsy_ebv_load = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="EBV load (copies/mL)",
    )
    dsa_at_biopsy = models.BooleanField(
        blank=True,
        null=True,
    )
    preformed_dsa = models.BooleanField(blank=True, null=True)
    history_dsa = models.BooleanField(
        blank=True,
        null=True,
    )  # add choices: de novo/persistent
    immunodominant_dsa_class = models.CharField(
        blank=True,
        max_length=50,
        choices=iDSAclass.choices,
    )
    i_dsa_specificity = models.CharField(
        blank=True,
        max_length=50,
        choices=iDSAspecifiity.choices,
    )
    i_dsa_mfi = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="iDSA MFI",
    )
    c1q_binding = models.BooleanField(blank=True, null=True, verbose_name="C1q binding")
    non_anti_hla_dsa = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="non anti-HLA DSA",
    )
    non_anti_hla_dsa_type = models.CharField(
        max_length=100,
        blank=True,
        choices=nonAntiHlaDsa.choices,
    )
    graft_failure_cause = models.CharField(
        max_length=100,
        blank=True,
        choices=GraftFailureCause.choices,
    )
    graft_failure_date = models.DateField(
        blank=True,
        null=True,
    )
    ci_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
    )
    ct_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
    )
    cv_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
    )
    ah_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
    )
    percent_glomerulosclerosis = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True,
        null=True,
        verbose_name="percent sclerotic glomeruli",
    )
