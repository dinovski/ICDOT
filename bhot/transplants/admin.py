from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from nonrelated_inlines.admin import NonrelatedStackedInline

from bhot.transplants import forms, models, resources

@admin.register(models.Transplant)
class TransplantAdmin(ImportExportModelAdmin):
    resource_class = resources.TransplantResource
    fieldsets = (
        (None, {
            'fields': ('transplant_date', 'donor_ref', 'recipient_ref'),
        }),
        ('Recipient', {
            'classes': ('collapse',),
            'fields': ('recipient_record_date', 'recipient_dob', ('recipient_height', 'recipient_height_units'), ('recipient_weight', 'recipient_weight_units'), 'recipient_sex', 'recipient_ethnicity', ('pre_transplant_dialysis', 'time_on_dialysis'), 'previous_transplant', 'primary_kidney_disease', 'recipient_cmv_status', 'recipient_ebv_status', ('recipient_hbv_ag_status', 'recipient_hbv_as_status', 'recipient_hbv_ac_status'), 'recipient_hcv_status', 'recipient_hiv_status'),
        }),
        ('Outcomes/events', {
            'classes': ('collapse',),
            'fields': ('recipient_death_date', 'graft_failure_date', 'graft_failure_cause'),
        }),
        ('Donor', {
            'classes': ('collapse',),
            'fields': ('donor_record_date', ('donor_dob', 'donor_age'), 'donor_sex', 'donor_ethnicity', 'donor_criteria', 'donor_type', 'living_donor_type', ('deceased_donor_type', 'donor_death_cause'), 'kdri', 'donor_diabetes', 'donor_hypertension', 'donor_comorbities', 'donor_egfr', ('donor_proteinuria', 'donor_proteinuria_units'), ('donor_proteinuria_dipstick', 'donor_proteinuria_dipstick_units'), ('donor_creatinemia', 'donor_creatinemia_units')),
        }),
        ('Graft', {
            'classes': ('collapse',),
            'fields': ('procurement_date', 'donor_aboi', ('hla_a_mismatches', 'hla_b_mismatches', 'hla_dr_mismatches'), ('cold_ischemia_time', 'cold_ischemia_time_units'), ('delayed_graft_function', 'dgf_time', 'dgf_time_units'), 'induction_therapy', 'preformed_dsa', 'dsa_date', 'immunodominant_dsa_class', 'i_dsa_specificity', 'i_dsa_mfi', 'c1q_binding'),
        }),
        ('Day 0 biopsy', {
            'classes': ('collapse',),
            'fields': ('pre_transplant_biopsy_type', 'ci_score', 'ct_score', 'cv_score', 'ah_score', 'percent_glomerulosclerosis'),
        }),
    )

@admin.register(models.Biopsy)
class BiopsyAdmin(ImportExportModelAdmin):
    resource_class = resources.BiopsyResource
    fieldsets = (
        (None, {
            'fields': ('biopsy_date', ('biopsy_egfr', 'biopsy_egfr_date'), ('biopsy_proteinuria', 'biopsy_proteinuria_units'), ('biopsy_proteinuria_dipstick', 'biopsy_proteinuria_dipstick_units'), ('biopsy_creatinemia', 'biopsy_creatinemia_units'), ('biopsy_creatinuria', 'biopsy_creatinuria_units'), ('prot_creat_ratio', 'prot_creat_ratio_units'), ('systolic_bp', 'diastolic_bp')),
        }),
        ('Treatment', {
            'classes': ('collapse',),
            'fields': (('immunosuppressants', 'immunosuppressant_dose', 'immunosuppressant_dose_units'), ('immunosuppressant_trough', 'immunosuppressant_postdose'), ('rejection_treatment', 'treatment_start_date'), 'treatment_response', 'rejection_date'),
        }),
        ('Biomarkers', {
            'classes': ('collapse',),
            'fields': ('dd_cf_dna', 'bkv_load', 'cmv_load', 'ebv_load'),
        }),
        ('DSA', {
            'classes': ('collapse',),
            'fields': ('dsa_at_biopsy', 'history_dsa', 'immunodominant_dsa_class', 'i_dsa_specificity', 'i_dsa_mfi', 'non_anti_hla_dsa', 'non_anti_hla_dsa_type'),
        }),
    )

@admin.register(models.Histology)
class HistologyAdmin(ImportExportModelAdmin):
    resource_class = resources.HistologyResource
    fieldsets = (
        (None, {
            'fields': ('biopsy', 'histology_date', 'biopsy_assessment', 'biopsy_method', 'tissue_technique', 'num_cores', 'num_glomeruli', 'num_glomerulosclerosis', 'num_sclerotic_glomeruli', 'num_arteries', 'biopsy_quality', 'fsgs_type', 'ati_status', ('tma_status', 'tma_location')),
        }),
        ('Banff lesions: acute', {
            'classes': ('collapse',),
            'fields': ('g_score', 'ptc_score', 'i_score', 't_score', 'v_score'),
        }),
        ('Banff lesions: chronic', {
            'classes': ('collapse',),
            'fields': ('cg_score', 'ci_score', 'ct_score', 'cv_score', 'ah_score', 'mm_score'),
        }),
        ('Banff lesions: acute/chronic', {
            'classes': ('collapse',),
            'fields': ('ti_score', 'i_ifta_score', 't_ifta_score', 'percent_cortex_if', 'percent_ifta', 'chronic_allograft_arteriopathy', 'pvl_load_level'),
        }),
        ('Immunohistochemistry', {
            'classes': ('collapse',),
            'fields': ('crescents', 'glomerular_thrombi', 'arterial_thrombi', 'plasma_cell_if', 'eosinophil_cell_if', 'sv40t', 'other_ihc'),
        }),
        ('Electron microscopy', {
            'classes': ('collapse',),
            'fields': ('mesangial_hypercellularity', 'electron_dense_deposits', 'edd_substructre', 'edd_location', 'gbm_duplication', 'endothelial_activation', 'transplant_glomerulopathy', 'ptcml', 'other_em'),
        }),
        ('Immunofluorescence', {
            'classes': ('collapse',),
            'fields': (('igg_staining', 'igg_location'), ('iga_staining', 'iga_location'), ('igm_staining', 'igm_location'), ('c1q_staining', 'c1q_location'), ('c3_staining', 'c3_location'), ('kappa_staining', 'kappa_location'), ('lambda_staining', 'lambda_location'), 'fibrin_deposition'),
        }),
        ('Histology diagnosis', {
            'classes': ('collapse',),
            'fields': ('principal_diagnosis', 'principal_diagnosis_other', 'rejection_diagnosis', 'non_rejection_diagnosis', 'diagnosis_comments'),
        }),
    )

@admin.register(models.FileUpload)
class FileUploadAdmin(ImportExportModelAdmin):
    pass

class FileUploadInline(admin.TabularInline):
    model = models.FileUpload
    max_num = 0

@admin.register(models.FileUploadBatch)
class FileUploadBatchAdmin(admin.ModelAdmin):
    form = forms.FileUploadBatchAdminForm
    inlines = [FileUploadInline]

    def save_related(self, request, form, formsets, change):
        # From https://web.archive.org/web/20220107040356/
        # https://xn--w5d.cc/2019/09/18/minimalistic-multiupload-in-django-admin.html
        # ModelAdmin handles saving the object separately and only
        # calls form’s save() method with commit=False.
        # We must call the save_files method manually.
        super().save_related(request, form, formsets, change)
        form.save_files(form.instance)

class StackedFileUploadInline(NonrelatedStackedInline):
    model = models.FileUpload
    exclude = ("batch", "file_ref")
    max_num = 1
    formset = forms.FileUploadInlineFormSet

    def get_form_queryset(self, obj):
        # We want this to act like a "quick upload form".
        # We do not attempt to manage the referenced file (eg: editing.)
        # That is why we always return an empty queryset.
        return self.model.objects.none()

    def save_new_instance(self, parent, instance):
        instance.file_ref = parent.file_ref

@admin.register(models.SequencingData)
class SequencingDataAdmin(ImportExportModelAdmin):
    resource_class = resources.SequencingDataResource
    readonly_fields = ("file_path",)
    inlines = [StackedFileUploadInline]
