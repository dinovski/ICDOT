from datetime import datetime
from time import sleep
import os, json
from pprint import pprint
from os.path import dirname

from flask import render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required

from bhot import app,csrf

from bhot.jobs.testjob import testjob
from bhot.jobs.rcc_report import generate_rcc_report
from bhot.models import db


from . import accounts
from . import recipient
from . import donor
from . import transplant
from . import clinical_biopsy
from . import histology
from . import molecular
from . import followup
from . import data_import
from . import grafts

@app.route("/")
@login_required
def index():
    sql="""
select
 T.transplant_id,
 T.transplant_date,
 T.organ,
 T.created,
 R.external_recipient_id,
 D.external_donor_id,
 C.external_biopsy_id as clinical_external_biopsy_id,
 H.external_biopsy_id as histology__external_biopsy_id,
 M.external_biopsy_id as molecular_external_biopsy_id,
 coalesce(FF.num_followups,0) as num_followups,
 FF.latest_followup_date,
 CASE WHEN
    R.external_recipient_id IS NOT NULL AND
    D.external_donor_id IS NOT NULL AND
    C.external_biopsy_id  IS NOT NULL AND
    H.external_biopsy_id  IS NOT NULL AND
    M.external_biopsy_id  IS NOT NULL
 THEN 'COMPLETE' ELSE 'INCOMPLETE' END as status
from transplants T
FULL OUTER JOIN recipients R
ON T.transplant_id = R.transplant_id
FULL OUTER JOIN donors D
ON T.transplant_id = D.transplant_id
FULL OUTER JOIN clinical_biopsies C
ON T.transplant_id = C.transplant_id
FULL OUTER JOIN histologies H
ON T.transplant_id = H.transplant_id
FULL OUTER JOIN moleculars M
ON T.transplant_id = M.transplant_id
FULL OUTER JOIN
  (select
      transplant_id,
      max(record_date) as latest_followup_date,
      count(*) as num_followups
  from followups group by transplant_id) FF
ON
  FF.transplant_id = T.transplant_id
ORDER BY
  R.external_recipient_id,
  T.transplant_date desc
    """
    data = db.session.execute(sql)
    data = [dict(x) for x in data]

    completed = [x for x in data if x["status"] == "COMPLETE"]
    incomplete = [x for x in data if x["status"] != "COMPLETE"]

    return render_template("index.html", completed_transplants=completed,
                           incomplete_transplants=incomplete)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


"""

@app.route("/test-background-job",methods=["GET","POST"])
def test_background_job():
    form = FlaskForm()
    if form.validate_on_submit():
        ## Start a new Job
        testjob.queue()
        return redirect(url_for("test_background_job"))

    queue = app.rq.get_queue()
    #jobs = default_queue.jobs

    job_ids = []
    job_ids.extend(queue.started_job_registry.get_job_ids())  # Returns StartedJobRegistry
    job_ids.extend(queue.deferred_job_registry.get_job_ids())   # Returns DeferredJobRegistry
    job_ids.extend(queue.finished_job_registry.get_job_ids())  # Returns FinishedJobRegistry
    job_ids.extend(queue.failed_job_registry.get_job_ids())  # Returns FailedJobRegistry
    job_ids.extend(queue.scheduled_job_registry.get_job_ids())  # Returns ScheduledJobRegistry

    jobs = queue.jobs
    jobs.extend ([queue.fetch_job(x) for x in job_ids])
    jobs = sorted(jobs, key=lambda x: x.enqueued_at, reverse=True)
    jobs = jobs[:50]
    return render_template("test-background-job.html", form=form,jobs=jobs)


@app.route("/show-background-job/<jobid>")
def show_background_job(jobid):
    default_queue = app.rq.get_queue()

    job = default_queue.fetch_job(jobid)

    return render_template("show-background-job.html", job=job)


@app.route("/test-rcc-report", methods=["GET","POST"])
def test_rcc_report():
    data = {}
    form = XLSImportForm()
    filename = None
    if form.validate_on_submit():
        filename = request.files['upload'].filename
        tmpfilename = save_uploaded_file(request.files['upload'],"rcc")
        job = generate_rcc_report.queue(tmpfilename, os.path.basename(filename), result_ttl=-1)
        job_id = job.id
        return redirect(url_for("show_rcc_report_job",jobid=job_id))

    return render_template("test-xls-import.html", form=form, data=data, filename=filename)


@app.route("/rcc-report/<jobid>")
def show_rcc_report_job(jobid):
    default_queue = app.rq.get_queue()

    job = default_queue.fetch_job(jobid)
    if job.is_finished:
        (ok, html_file) = job.result
        if ok:
            return send_file(html_file,as_attachment=False)

    return render_template("show-rcc-pending-job.html", job=job)
"""
