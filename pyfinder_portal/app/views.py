from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import subprocess
from django.http import HttpResponse, Http404
import os
import base64

python3_2_3 = "/Users/alex/.pyenv/versions/3.2.3/bin/python"
pyexz3 = "../pyexz3.py"
file_py = "temp_file.py"
test_suites = "generated_test_suites/"
cov_html = "htmlcov/temp_file_py.html"


def index(request):
    assert isinstance(request, HttpRequest)

    data = {}
    data["out"] = "\n\n\n\n"
    data["is_post"] = False
    if request.method == 'POST':

        with open(file_py, 'wb+') as destination:
            for chunk in request.FILES['file_upload'].chunks():
                destination.write(chunk)
        proc = subprocess.Popen([python3_2_3, pyexz3, "--generate_test_suite", "--evaluate_all_funcs", "--cvc", "--graph", file_py], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        raw_out = out.decode("utf-8") 
        err = err.decode("utf-8") 

        file_path = test_suites + 'temp_file_test_suite.py'
        with open(file_path, 'r') as myfile:
            test_suite=myfile.read()

        #coverage run --branch generated_test_suites/$TEST_FILE
        subprocess.call(["pyenv", "local", "3.6.5"])
        proc = subprocess.Popen(["coverage", "run", "--branch", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode("utf-8") 
        err = err.decode("utf-8") 

        proc = subprocess.Popen(["coverage", "html"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode("utf-8") 
        err = err.decode("utf-8") 

        #open htmlcov/$(sed -e 's/[\/.]/_/g' <<<"$FILE").html
        proc = subprocess.Popen(["cat", cov_html], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        coverage_frame = out.decode("utf-8") 
        err = err.decode("utf-8") 

        #dot -Tpng test/elseif.py.dot -o elseif.png
        proc = subprocess.Popen(["dot", "-Tpng", file_py + ".dot", "-o", "temp_file.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode("utf-8") 
        err = err.decode("utf-8") 
        encoded = base64.b64encode(open("temp_file.png", "rb").read()).decode("utf-8")

        data["out"] = raw_out
        data["file_name"] = request.POST['file_name']
        data["test_suite"] = test_suite
        data["coverage_frame"] = coverage_frame.replace("keybd_closed.png","/static/app/keybd_closed.png").replace("keybd_open.png","/static/app/keybd_open.png")
        data["img"] = encoded
        data["is_post"] = True

    return render(request, "app/index.html", data)

def download(request):
    file_path = test_suites + 'temp_file_test_suite.py'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + request.GET['file_name'][:-3] + '_test_suite.py'
            return response
    raise Http404
