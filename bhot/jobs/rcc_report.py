from bhot.jobs import rq
from time import sleep
from subprocess import Popen,PIPE
from os.path import dirname, join, basename

@rq.job
def generate_rcc_report(rcc_filename, display_filename):
    print("Analyzing RCC file", display_filename, " => ", rcc_filename )

    basedir = dirname(dirname(dirname(__file__)))
    print("basedir = ", basedir)

    aux_script = join(basedir, "aux","render-rmarkdown.sh")
    print("aux_script = ", aux_script)

    rmd_templ = join(basedir,"rmarkdown","rcc-example.rmd")
    print("rmd_templ = ", rmd_templ)

    params = [aux_script, rmd_templ, rcc_filename, display_filename]

    p = Popen(params,stdout=PIPE,stderr=PIPE)
    (out,err) = p.communicate()

    if (p.returncode != 0):
        msg = "failed to render rmarkdown file (exit code %d): %s" % (p.returncode, str(err.decode()))
        print(msg)
        return (False, msg)

    print("== OUT==")
    print(str(out.decode()))
    print("== ERR ==")
    print(str(err.decode()))

    output = rcc_filename + ".html"

    print("output file = ", output)

    return (True, output)
