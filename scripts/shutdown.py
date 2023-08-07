#Author: Matthew Groholski
#Date: 08/06/23

import psutil
import subprocess

for process in psutil.process_iter():
    if process.name().lower() == "python" or "chrom" in process.name():
        subprocess.call(["kill", str([process.pid()])])

