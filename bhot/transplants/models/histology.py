import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from bhot.transplants.models.biopsy import Biopsy
from bhot.users.models import UserScopedModel


class Histology(UserScopedModel):
    class Meta:
        verbose_name_plural = "histologies"

    class BanffScore(models.textChoices):
        ZERO = "0", _("0")
        ONE = "1", _("1")
        TWO = "2", _("2")
        THREE = "3", _("3")

    class BiopsyAssessment(models.TextChoices):
        FROZEN = "frozen", _("frozen")
        PARAFFIN = "paraffin", _("paraffin")
        EM = "electron microscopy", _("electron microscopy")

    class BiopsyMethod(models.TextChoices):
        CORE = "core", _("core")
        NEEDLE = "needle", _("needle")
        WEDGE = "wedge", _("wedge")

    class TissueTechnique(models.TextChoices):
        FROZEN = "frozen", _("frozen")
        PARAFFIN = "paraffin", _("paraffin")
        AFA = "acidified formal alcohol", _("acidified formal alcohol (AFA")

    # variables
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    biopsy = models.ForeignKey(Biopsy, null=True, on_delete=models.SET_NULL)
    transplant_date = models.DateField()
    biopsy_date = models.DateField()

    biopsy_assessment = models.CharField(
        choices=BiopsyAssessment.choices,
        blank=True,
        NULL=True,
    )
    biopsy_method = models.CharField(
        choices=BiopsyMethod.choices,
        blank=True,
        NULL=True,
    )
    tissue_technique = models.CharField(
        choices=TissueTechnique.choices,
        blank=True,
        NULL=True,
    )
    num_cores = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of cores",
    )
    num_glomeruli = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of glomeruli",
    )
    num_glomerulosclerosis = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of global glomerulosclerosis",
    )
    num_sclerotic_glomeruli = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of segmentally sclerotic glomeruli",
    )
    num_arteries = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="number of arteries",
    )
    # FSGS type
    ati = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Acute Tubular Injury (ATI)",
    )
    tma = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Thrombotic Microangiopathy",
    )

    g_score = models.CharFiles(
        choices=BanffScore.choices,
        blank=True,
        null=True,
        verbose_name="glomerulitis (g)",
    )
    ptc_score = models.CharFiles(
        choices=BanffScore.choices,
        blank=True,
        null=True,
        verbose_name="peritubular capillaritis (ptc)",
    )
    i_score = models.CharFiles(
        choices=BanffScore.choices,
        blank=True,
        null=True,
        verbose_name="interstitial inflammation (i)",
    )
    t_score = models.CharFiles(
        choices=BanffScore.choices,
        blank=True,
        null=True,
        verbose_name="tubulitis (t)",
    )
    v_score = models.CharFiles(
        choices=BanffScore.choices,
        blank=True,
        null=True,
        verbose_name="intimal arteritis (v)",
    )
    cg_score = models.CharFiles(
        choices=BanffScore.choices,
        blank=True,
        null=True,
        verbose_name="Glomerular Basement Membrane Double Contours (cg)",
    )
