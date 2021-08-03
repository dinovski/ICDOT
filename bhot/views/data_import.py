from werkzeug.utils import secure_filename
import os, json
from os.path import dirname,basename
from subprocess import Popen,PIPE
from tempfile import NamedTemporaryFile
from datetime import date, datetime, time
from pprint import pprint

from flask import render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user

# Oh the horror
# see: https://pypi.org/project/backports-datetime-fromisoformat/#description
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()


from bhot import app,csrf
from bhot.forms.import_data import ImportDataForm

from bhot.models import db
from bhot.models.group import Group
from bhot.models.transplant import Transplant
from bhot.models.recipient import Recipient
from bhot.models.donor import Donor
from bhot.models.clinical_biopsy import ClinicalBiopsy


def save_uploaded_file(fileobj,extension):
    filename = secure_filename(fileobj.filename)
    # Save it to a local file
    local_file = NamedTemporaryFile(prefix="icdot-upload-",
                                    suffix="." + extension + ".unsafe",
                                    delete=False)
    fileobj.save(local_file)

    return local_file.name


def load_excel_template(filename):
    convertor = os.path.join(dirname(dirname(dirname(__file__))),"aux","read-spreadsheet.py")
    try:
        params = [convertor,filename]

        p = Popen(params,stdout=PIPE,stderr=PIPE)
        (out,err) = p.communicate()

        if (p.returncode != 0):
            msg = "failed to load excel file (exit code %d): %s" % (p.returncode, str(err.decode()))
            print(msg)
            return (False, msg)

        data = json.loads(out)

        return (True, data)

    except json.JSONDecodeError as e:
        msg = "failed to decode JSON output of excel loader program: '%s'" % (str(e))
        print(msg)
        return (False, msg)

    except OSError as e:
        msg = "failed to execute excel loader program '%s': '%s'" % (convertor, str(e))
        print(msg)
        return (False, msg)

def safe_date_from_iso(s):
    if not s:
        return None
    return datetime.fromisoformat(s)

def recipient_sheet_to_db_model(d):
    r = Recipient()
    r.external_recipient_id = d['Patient ID']
    r.blood_pressure = d['Blood pressure']
    r.date_of_birth = d['Date of birth']
    r.ethnicity = d['Ethnicity']
    r.gender = d['Gender']
    r.hbv_hbs_ac = d['HBV HBsAc status']
    r.hbv_hbs_ag = d['HBV HBsAg status']
    r.hbv_hbs_as = d['HBV HBsAs status']
    r.hcv = d['HCV status']
    r.hiv = d['HIV status']
    r.nephropathy = d['Nephropathy']
    r.disease = d['Primary kidney disease']
    r.proteinuria = d['Proteinuria']
    r.proteinuria_units = d['Proteinuria units']
    r.proteinuria_dipstick = d['Proteinuria (dipstick)']
    r.proteinuria_date = d['Proteinuria date']
    r.record_date = safe_date_from_iso(d['Record Date'])
    r.weight = d['Weight']
    r.egfr = d['eGFR']
    r.egft_date = d['eGFR date']
    return r


def donor_sheet_to_db_model(d):
    o = Donor()
    o.external_donor_id = d['Donor ID']
    o.abo_incompatible = d['ABO incompatible']
    o.age = d['Age']
    o.c1qi_binding = d['C1q binding']
    o.cold_ischemia = d['Cold Ischemia']
    o.cold_ischemia_time = d['Cold ischemia time']
    o.cold_ischemia_units = d['Cold ischemia units']
    o.cause_of_death = d['Deceased donor cause of death']
    o.delayed_graft_function = d['Delayed graft function']
    o.diabetes = d['Diabetes']
    o.dtype = d['Donor type']
    o.ethnicity = d['Ethnicity']
    o.gender = d['Gender']
    o.history_of_hypertension = d['History of hypertension']
    o.class_immunodominant_dsa = d['Immunodominant DSA Class']
    o.specificity_immunodominant_dsa = d['Immunodominant DSA MFI'] ## is MFT same as specificy?? in the sheet
    o.induction_therapy = d['Induction therapy']
    o.kdri = d['Kidney Donor Risk Index']
    o.other_comorbidity = d['Other comorbidities']
    o.preformed_dsa = d['Preformed DSA']
    o.procurement_date = d['Procurement date']
    #o. = d['Proteinuria']
    o.proteinuria_dipstick = d['Proteinuria (dipstick)']
    o.proteinuria_date = safe_date_from_iso(d['Proteinuria date'])
    #o. = d['Proteinuria units']
    o.serum_creatinine = d['Serum creatinine']
    o.hla_a_mismatches = d['Total HLA-A mismatches']
    o.hla_b_mismatches = d['Total HLA-B mismatches']
    o.hla_dr_mismatches = d['Total HLA-DR mismatches']
    o.egfr = d['eGFR']
    o.egfr_date = safe_date_from_iso(d['eGFR date'])
    return o

def clinical_biopsy_sheet_to_db_model(d):
    b = ClinicalBiopsy()
    b.external_biopsy_id = d['Biopsy ID']
    b.biopsy_date = datetime.fromisoformat(d['Biopsy date'])
    b.biopsy_indication = d['Biopsy indication']
    b.bkv_load = d['BKV load']
    b.bkv_load_units = d['BKV units'] ## should be "BKV Load Units" in the sheet?
    b.c1qi_binding = d[  'C1q binding']
    b.dsa_class = d[  'DSA class']
    b.dsa_history = d[  'DSA history']
    b.idsa_class = d[  'Immunodominant DSA class']
    b.current_immunosuppressant = d[  'Immunosuppressant']
    b.current_treatment_dose = d[  'Immunosuppressant dose']
    b.non_anti_hla_dsa = d[  'Non anti-HLA DSA']
    b.non_anti_hla_dsa_type = d[  'Non anti-HLSA DSA type']
    b.polyoma_virus_pcr = d[  'Polyoma virus PCR (log)']
    b.pretransplant_biopsy = d[  'Pre-transplant biopsy']
    b.preformed_dsa = d[  'Preformed DSA']
    b.proteinuria = d[  'Proteinuria']
    b.proteinuria_units = d[  'Proteinuria units']
    b.proteinuria_dipstick = d[  'Proteinuria (dipstick)']
    b.proteinuria_date = safe_date_from_iso(d['Proteinuria date'])
    b.rejection_treatment = d[  'Rejection treatment']
    b.serum_creatinine = d[  'Serum creatinine']
    b.serum_creatinine_units = d[  'Serum creatinine units']
    b.idsa_mfi = d[  'iDSA MFI']
    b.idsa_specificity = d[  'iDSA specificity']
    return b

def create_data_from_spreadsheet(data):
    ##
    ## Step 1: create transplant records
    req = data["required"]
    recp = data["recipient"]
    donor = data["donor"]
    clinical_biopsy = data["biopsy"]
    histology = data["histology"]
    nanostring = data["nanostring"]

    imported = []

    for r in req:
        transplant_date = datetime.fromisoformat(r["Transplant Date"])
        organ = "kidney"

        t = Transplant()
        t.transplant_date = transplant_date
        t.organ = organ
        t.created_by_user_id = current_user.user_id
        t.group_id = current_user.group_id
        db.session.add(t)


        ##
        ## Get the Recipient data from the "recipient" sheet
        ##
        recp_id = r["Patient ID"]
        recp_data = [x for x in recp if x["Patient ID"] == recp_id]
        print("recp_data for", recp_id)
        pprint(recp_data)
        if len(recp_data)==0:
            flash("Patient ID '%s' not found in recipient sheet" % recp_id)
        elif len(recp_data)>1:
            flash("Patient ID '%s' is duplicated in recipient sheet" % recp_id)
        else:
            ## Create New Recipient
            r = recipient_sheet_to_db_model(recp_data[0])
            r.created_by_user_id = current_user.user_id
            t.recipient = r
            db.session.add(r)

        ##
        ## Get the Clinical Biopsy for this transplant
        ##
        clinical_data = [x for x in clinical_biopsy \
                         if x["Patient ID"] == recp_id and datetime.fromisoformat(x["Transplant date"])==transplant_date]
        print("clinical-biopsy for", recp_id, transplant_date)
        pprint(clinical_data)
        if len(clinical_data)==0:
            flash("Clinical Biopsy for '%s' on %s not found in biopsy sheet" % (recp_id, str(transplant_date)))
        elif len(clinical_data)>1:
            flash("Clinical Biopsy for '%s' on %s has duplicates in biopsy sheet" % (recp_id, str(transplant_date)))
        else:
            b = clinical_biopsy_sheet_to_db_model(clinical_data[0])
            b.created_by_user_id = current_user.user_id
            t.clinical_biopsy = b
            db.session.add(b)

        ## The connection between a transplant and a donor is through a Biopsy sheet??
        donor_id_from_biopsy = clinical_data[0]['Donor ID']


        ##
        ## Get the Donor for this transplant
        ##
        donor_data = [x for x in donor if x["Donor ID"] == donor_id_from_biopsy]
        print("donor for", recp_id, transplant_date)
        pprint(donor_data)
        if len(donor_data)==0:
            flash("Donor for '%s' on %s not found in biopsy sheet" % (recp_id, str(transplant_date)))
        elif len(donor_data)>1:
            flash("Donor for '%s' on %s has duplicates in biopsy sheet" % (recp_id, str(transplant_date)))
        else:
            d = donor_sheet_to_db_model(donor_data[0])
            d.created_by_user_id = current_user.user_id
            t.donor = d
            db.session.add(d)


        db.session.commit()

        imported.append( { "transplate_date" : transplant_date,
                           "recipient_id" : recp_id,
                           "donor_id" : donor_id_from_biopsy } )

        return imported


@app.route("/import-data", methods=["GET","POST"])
def import_data():
    data = {}
    form = ImportDataForm()
    filename = None
    if form.validate_on_submit():
        filename = request.files['xls'].filename
        tmpfilename = save_uploaded_file(request.files['xls'],"xlsx")
        (ok, data) = load_excel_template(tmpfilename)

        rcc_files = request.files.getlist("rcc[]")
        pprint(rcc_files)
        rcc_file_names = [x.filename for x in rcc_files if x.filename]

        if not ok:
            flash(data,'Failed to load Excel Spreadsheet file')
        else:
            #pprint(data)

            imported = create_data_from_spreadsheet(data)
            return render_template("show-imported-data.html",
                                   rcc_file_names=rcc_file_names,
                                   imported=imported, data=data, filename=filename)

    return render_template("import_spreadsheet.html", form=form)
