from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SelectField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Required
from wtforms.fields.html5 import DateField
from wtforms_components import SelectMultipleField

from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model, BooleanSelectFieldHelper

from bhot.models.histology import Histology


def SelectFieldBanff(label):
    return SelectField(label,
                       choices=[('','N/A'),
                                ("0","0"),
                                ("1", "1"),
                                ("2", "2"),
                                ("3", "3")])

def SelectFieldImmunofluorescence(label):
    return SelectField(label,
                       choices=[('','N/A'),
                                ('negative','Negative'),
                                ('+','+'),
                                ('++','++'),
                                ('+++','+++'),
                                ('++++','++++')])

def SelectFieldImmunofluorescenceLocation(label):
    return SelectMultipleField(label,
                       choices=
                               [('','N/A'),
                                ("granular/capillary wall","granular/capillary wall"),
                                ("granular/mesangial","granular/mesangial"),
                                ("linear/mesangial","linear/mesangial")])



class HistologyForm(FlaskForm):
    external_biopsy_id = StringField('Internal Biopsy ID',validators=[DataRequired()])

    #external_donor_id = StringField('Internal Biopsy ID')

    biopsy_date = DateField('Biopsy Date', validators=[DataRequired()] )

    ## Indications

    biopsy_assessment = SelectField('Biopsy Assessment',
                                    choices=[('','N/A'),
                                             ("parafin","Paraffin"),
                                             ("frozen", "Frozen"),
                                             ("electron_microscopy","Electron microscopy")])

    biopsy_method = SelectField('Biopsy Method',
                                              choices=[('','N/A'),
                                                       ("wedge","Wedge"),
                                                       ("core_needle", "Core-needle")])

    tissue_technique = SelectField('Tissue Technique',
                                              choices=[('','N/A'),
                                                       ("frozen","frozen"),
                                                       ("FFPE", "FFPE")])


    num_glomeruli = IntegerField('Number of glomeruli',validators=[Optional()])

    num_glomerulosclerosis = StringField('Number of glomerulosclerosis')

    num_arteries = StringField('Number of arteries')

    biopsy_assessment_quality = SelectField('Quality',
                                              choices=[('','N/A'),
                                                       ("adequate","Adequate"),
                                                       ("minimal", "Minimal")])

    atn = BooleanSelectFieldHelper('Acute Tubular Injury','present','absent')

    tma = BooleanSelectFieldHelper('Thrombotic Microangiopathy','present','absent')
    tma_location = SelectField('TMA Location',
                            choices=[('','N/A'),
                                    ("glomerular","glomerular"),
                                     ("arteriolar", "arteriolar"),
                                     ("both","both")])

    ###
    # biopsy_indication = StringField('Biopsy indication')

    ### ACUTE LESIONS
    #acute_lesions_technique = SelectField('Technique',
    #                                      choices=[('','N/A'),
    #                                               ("parafin","Paraffin"),
    #                                               ("frozen", "Frozen")])

    acute_lesions_g = SelectFieldBanff('g: glomerulitis')
    acute_lesions_ptc = SelectFieldBanff('ptc: peritubular capillaritis')
    acute_lesions_i = SelectFieldBanff('i: inflammation')
    acute_lesions_t = SelectFieldBanff('t: ubulitis')
    acute_lesions_v = SelectFieldBanff('v: intimal arteritis')
    acute_lesions_c4d = SelectField('C4d scoring',
                                    choices=[('','N/A'),
                                             ("negative","Negative"),
                                             ("1", "1"),
                                             ("2", "2"),
                                             ("3", "3")])
    acute_lesions_c4d_technique = SelectField('C4d Technique',
                                    choices=[('','N/A'),
                                             ("IF","IF"),
                                             ("IHC", "IHC")])

    ### CHRONIC LESIONS:
    chronic_lesions_cg = SelectFieldBanff("cg: transplant glomerulopathy")
    chronic_lesions_ci = SelectFieldBanff("ci: interstitial fibrosis")
    chronic_lesions_ct = SelectFieldBanff("ct: tubular atrophy")
    chronic_lesions_cv = SelectFieldBanff("cv: vascular fibrous<br/>intimal thickening")
    chronic_lesions_ah = SelectFieldBanff("ah: arteriolar hyalinosis")
    chronic_lesions_mm = SelectFieldBanff("mm: mesangial matrix expansion")

    ## ACUTE & CHRONIC LESIONS
    acute_chronic_lesions_ti = SelectFieldBanff("ti: total inflammation")
    acute_chronic_lesions_i_ifta = SelectFieldBanff("i-IFTA")
    acute_chronic_lesions_ifta_pct = IntegerField('% IFTA',validators=[Optional(),NumberRange(min=0,max=1000)])
    acute_chronic_lesions_t_ifta = SelectFieldBanff("t-IFTA")
    acute_chronic_lesions_pvl = SelectField('PVL',
                                    choices=[('','N/A'),
                                             ("1", "1"),
                                             ("2", "2"),
                                             ("3", "3")])


    ##  IMMUNOHISTOCHEMISTRY
    immunohistochemistry_sv40_t = StringField("SV40-T")

    #immunohistochemistry_pvl = SelectField('PVL',
    #                                choices=[('','N/A'),
    #                                         ("1", "1"),
    #                                         ("2", "2"),
    #                                         ("3", "3")])
    immunohistochemistry_other = StringField("Other Immunohistochemistry")



    ## ELECTRON MICROSCOPY
    electron_microscopy_edd = BooleanSelectFieldHelper('Electron Dense Deposits','positive','negative')
    electron_microscopy_edd_location = SelectMultipleField('EDD Location',choices=[('','N/A'),
                                                                                   ("mesangial","mesangial"),
                                                                                   ("subendothelial","subendothelial"),
                                                                                   ("subepithelial","subepithelial")])
    electron_microscopy_tg_cg = SelectField('Transplant glomerulopathy cg',
                                            choices=[('','N/A'),
                                                     ('cg1a','cg1a'),
                                                     ('cg1b','cg1b')])

    electron_microscopy_pctml = StringField("Peritubular Capillary Basement Membrane Multilayering")
    electron_microscopy_other = StringField("Other Electron Microscopy")


    ## IMMUNOFLUORESCENCE
    immunofluorescence_ig_g = SelectFieldImmunofluorescence("IgG")
    immunofluorescence_ig_g_location = SelectFieldImmunofluorescenceLocation("IgG Location")
    immunofluorescence_ig_a = SelectFieldImmunofluorescence("IgA")
    immunofluorescence_ig_a_location = SelectFieldImmunofluorescenceLocation("IgA Location")
    immunofluorescence_ig_m = SelectFieldImmunofluorescence("IgM")
    immunofluorescence_ig_m_location = SelectFieldImmunofluorescenceLocation("IgM Location")
    immunofluorescence_c3   = SelectFieldImmunofluorescence("C3")
    immunofluorescence_c3_location   = SelectFieldImmunofluorescenceLocation("C3 Location")
    immunofluorescence_c1q  = SelectFieldImmunofluorescence("C1q")
    immunofluorescence_c1q_location  = SelectFieldImmunofluorescenceLocation("C1q Location")
    immunofluorescence_kappa = SelectFieldImmunofluorescence("Kappa")
    immunofluorescence_kappa_location = SelectFieldImmunofluorescenceLocation("Kappa Location")
    immunofluorescence_lambda = SelectFieldImmunofluorescence("Lambda")
    immunofluorescence_lambda_location = SelectFieldImmunofluorescenceLocation("Lambda Location")
    immunofluorescence_other = StringField("Other: please specify")


    ### Diagnosis
    rejection_diagnosis= SelectMultipleField("Rejection Diagnosis",
                                             choices=[
                                                 ('Normal biopsy or nonspecific changes','Normal biopsy or nonspecific changes'),
                                                 ('Inadequate','Inadequate'),
                                                 ('Rejection only-no additional pathological abnormalities','Rejection only-no additional pathological abnormalities'),
                                                 ('Other pathology','Other pathology'),
                                                 ('Glomerular ischemia','Glomerular ischemia'),
                                                 ('Infarction','Infarction'),
                                                 ('Antibody-mediated changes',
                                                   (
                                                       ("Active ABMR","Active ABMR"),                                             
                                                       ("Chronic Active ABMR","Chronic Active ABMR"),                             
                                                       ("Chronic ABMR","Chronic ABMR"),                                           
                                                       ("C4D deposition without morphologic evidence for active rejection","C4D deposition without morphologic evidence for active rejection") 
                                                   )),
                                                  ('T-Cell mediated changes',
                                                   (
                                                       ("Borderline/Suspicious for acute TCMR","Borderline/Suspicious for acute TCMR"),
                                                       ("Acute TCMR IA","Acute TCMR IA"),                                                        
                                                       ("Acute TCMR IB","Acute TCMR IB"),                                          
                                                       ("Acute TCMR IIA","Acute TCMR IIA"),                                        
                                                       ("Acute TCMR IIB","Acute TCMR IIB"),                                        
                                                       ("Acute TCMR III","Acute TCMR III"),                                        
                                                       ("Chronic Active TCMR IA","Chronic Active TCMR IA"),                        
                                                       ("Chronic Active TCMR IB","Chronic Active TCMR IB"),                        
                                                       ("Chronic Active TCMR II","Chronic Active TCMR II")                         
                                                   ))])

    nonrejection_diagnosis= SelectMultipleField("Non-rejection/recurrent Diagnosis",
                                                choices=[
                                                    ('Normal biopsy or nonspecific changes','Normal biopsy or nonspecific changes'),
                                                    ('Inadequate','Inadequate'),
                                                    ('Rejection only-no additional pathological abnormalities','Rejection only-no additional pathological abnormalities'),
                                                    ('Other pathology','Other pathology'),
                                                    ('Glomerular ischemia','Glomerular ischemia'),
                                                    ('Infarction','Infarction'),
                                                    ('Acute tubular injury',
                                                     (
                                                         ("Not otherwise specified","Not otherwise specified"),
                                                         ("Suspicious for CNI toxicity","Suspicious for CNI toxicity"),
                                                         ("Polyoma Virus Nephropathy Class 1","Polyoma Virus Nephropathy Class 1"),
                                                         ("Polyoma Virus Nephropathy Class 2","Polyoma Virus Nephropathy Class 2"),
                                                         ("Polyoma Virus Nephropathy Class 3","Polyoma Virus Nephropathy Class 3")
                                                     )),
                                                    ('Thrombotic microangiopathy',
                                                     (
                                                         ('Acute glomerular involvement on LM','Acute glomerular involvement on LM'),
                                                         ('Acute arteriolar/arterial involvement on LM','Acute arteriolar/arterial involvement on LM'),
                                                         ('Subacute/chronic glomerular involvement on LM','Subacute/chronic glomerular involvement on LM'),
                                                         ('Subacute/chronic arteriolar/arterial involvement on LM','Subacute/chronic arteriolar/arterial involvement on LM'),
                                                         ('EM features only','EM features only')
                                                     )),
                                                    ('Interstitial fibrosis and tubular atrophy (IFTA)',
                                                     (
                                                         ('Mild (IFTA1)','Mild (IFTA1)'),
                                                         ('Moderate (IFTA2)','Moderate (IFTA2)'),
                                                         ('Severe (IFTA3)','Severe (IFTA3)')
                                                     )),
                                                    ('Moderate to severe vascular pathology',
                                                     (
                                                         ('Significant vascular pathology','Significant vascular pathology'),
                                                         ('Significant arterial intimal thickening','Significant arterial intimal thickening'),
                                                         ('Arterial intimal fibrosis (non-inflammatory)','Arterial intimal fibrosis (non-inflammatory)'),
                                                         ('Arterial intimal thickening without fibroelastosis (at least partially)','Arterial intimal thickening without fibroelastosis (at least partially)'),
                                                         ('Significant arteriolar hyalinosis','Significant arteriolar hyalinosis'),
                                                         ('Significant arteriolar hyalinosis-likely donor-dreived','Significant arteriolar hyalinosis-likely donor-dreived'),
                                                         ('Significant arteriolar hyalinosis - suspicious for CNI toxicity','Significant arteriolar hyalinosis - suspicious for CNI toxicity')
                                                     )),
                                                    ('Infection diagnostic',
                                                     (
                                                         ("Infection","Infection"),
                                                         ("Neutrophilic pyelonephritis","Neutrophilic pyelonephritis"),
                                                         ("Suspicious for pyelonephritis","Suspicious for pyelonephritis"),
                                                         ("BK Nephropathy","BK Nephropathy"),
                                                         ("Granulomatous","Granulomatous"),
                                                     )),
                                                    ('Glomerular disease (recurrent or de novo)',
                                                     (
                                                         ("Immune complex","Immune complex"),
                                                         ("Immune complex, Membranous", "Immune complex, Membranous"),
                                                         ("Immune complex, Lupus nephritis", "Immune complex, Lupus nephritis"),
                                                         ("C3 glomerulopathy","C3 glomerulopathy"),
                                                         ("FSGS","FSGS"),
                                                         ("FSGS, likely recurrent","FSGS, likely recurrent"),
                                                         ("Diabetic change","Diabetic change"),
                                                         ("Paraprotein-related","Paraprotein-related")
                                                     )),
                                                    ('Tubulointerstitial disease',
                                                     (
                                                         ("Granulomatous TIN","Granulomatous TIN"),
                                                         ("Drug-induced TIN","Drug-induced TIN")
                                                     )),
                                                    ('Neoplasia',
                                                    (
                                                        ("Neoplasia","Neoplasia"),
                                                        ("Preneoplasia/suspicious neoplasia","Preneoplasia/suspicious neoplasia"),
                                                        ("Post-transplant lymphoproliferative disease","Post-transplant lymphoproliferative disease")
                                                    ))
                                                ])

    diagnosis_comments = StringField ("Diagnosis comments",validators=[Optional()])

    """
=====
    immunosuppressive_therapy = SelectField('Immunosuppressive drug',
                                         choices=[("Tacrolimus/Ciclosporine","Tacrolimus/Ciclosporine"),
                                                   ("MPA","MPA"),
                                                   ("MMF","MMF"),
                                                   ("Everolimus/Sirolimus","Everolimus/Sirolimus"),
                                                   ("Azathioprine","Azathioprine"),
                                                   ("Belatacept","Belatacept"),
                                                   ("Steroids","Steroids")])

    polyoma_virus_pcr = IntegerField('Polyoma virus PCR (log)', validators=[Optional()])

    cell_free_dna_level = IntegerField('cell-free DNA level', validators=[Optional()])


    ## Immunological Parameters

    preformed_dsa = BooleanSelectFieldHelper('Performed DSA','positive','negative')

    history = SelectField(
        'History',
        choices=[('', 'N/A'),
                 ('denovo', 'de novo'),
                 ('persistent', 'persistent')]
    )

    class_immunodominant_dsa = SelectField('Class (immunodominant DSA)',
                                       choices=[('','N/A'),
                                                ('I','I (A, B, Cw)'),
                                                ('II','II (DR, DQ, DP)')])

    specificity_immunodominant_dsa = StringField('Specificity (immunodominant DSA)')

    c1q_binding = StringField("C1q binding")

    mfi_immunodominant_dsa = StringField("MFI (immunodominant DSA)")

    non_anti_hla_dsa = BooleanSelectFieldHelper('Performed DSA','positive','negative')

    non_anti_hla_dsa_type = StringField('Non anti-HLA DSA type')

    ###




    ## ELECTRON MICROSCOPY
    electron_microscopy_tg_cg = SelectField('Transplant glomerulopathy cg',
                                            choices=[('','N/A'),
                                                     ('cg1a','cg1a'),
                                                     ('cg1b','cg1b')])

    electron_microscopy_pcbmm = StringField("Peritubular Capillary Basement Membrane Multilayering")
    electron_microscopy_other = StringField("Other Electron Microscopy")

    electron_microscopy_diagnosis = SelectMultipleField("Pathology Diagnosis",
                                                        choices=[
                                                            ('','Normal biopsy or nonspecific changes'),
                                                            ('Antibody-mediated changes',
                                                             (
                                                                 ('',"Active ABMR"),
                                                                 ('',"Chronic Active"),
                                                                 ('',"C4D deposition without morphologic evidence for active rejection")
                                                             )),
                                                            ('Borderline changes',
                                                             (
                                                                 ('',"Acute T Cell Mediated Rejection IA"),
                                                                 ('',"Acute T Cell Mediated Rejection IB"),
                                                                 ('',"Acute T Cell Mediated Rejection IIA"),
                                                                 ('',"Acute T Cell Mediated Rejection IIB"),
                                                                 ('',"Acute T Cell Mediated Rejection III"),
                                                                 ('',"Chronic Active T Cell Mediated Rejection IA"),
                                                                 ('',"Chronic Active T Cell Mediated Rejection IB"),
                                                                 ('',"Chronic Active T Cell Mediated Rejection II"),
                                                                 ('',"Interstitial Fibrosis and Tubular Atrophy 0"),
                                                                 ('',"Interstitial Fibrosis and Tubular Atrophy 1"),
                                                                 ('',"Interstitial Fibrosis and Tubular Atrophy 2"),
                                                                 ('',"Interstitial Fibrosis and Tubular Atrophy 3")
                                                             )),
                                                           ('Acute tubular injury',
                                                            (
                                                                ('',"Polyoma Virus Nephropathy Class 1"),
                                                                ('',"Polyoma Virus Nephropathy Class 2"),
                                                                ('',"Polyoma Virus Nephropathy Class 3")
                                                            )),
                                                            ('Post-transplant lymphoproliferative disorders',
                                                             (
                                                                 ('',"Recurrent disease"),
                                                                 ('',"De novo glomerulopathy (other than transplant glomerulopathy)"),
                                                                 ('',"Transplant Glomerulopathy without microvascular inflammation"),
                                                                 ('',"Calcineurin inhibitor nephrotoxicity"),
                                                                 ('',"Thrombotic microangiopathy"),
                                                                 ('',"Pyelonephritis"),
                                                                 ('',"Drug-induced interstitial nephritis")
                                                             ))
                                                            ])

    ###
    pre_transplant_biopsy = SelectField('Pre-transplant biopsy',
                                       choices=[('','N/A'),
                                                ('procurement','procurement'),
                                                ('preimplantation','preimplantation')])


    treatment = StringField('Treatment')

    treatment_start_date = DateField('Treatment Start Date', validators=[Optional()] )
    treatment_end_date = DateField('Treatment End Date', validators=[Optional()] )
    """


    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
    
