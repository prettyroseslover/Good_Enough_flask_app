from flask import render_template
import subprocess

def os_page(request):
    hostname = request.values.get('hostname')

    if hostname is None:
        hostname = '8.8.8.8'

    cmd = ["ping", "-c", "3", hostname]
    result = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True).communicate()[0]

    return render_template('os.html', result=result)