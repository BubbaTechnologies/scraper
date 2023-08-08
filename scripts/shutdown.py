#Author: Matthew Groholski
#Date: 08/06/23

import psutil
import subprocess
import re

for process in psutil.process_iter():
    if re.search("([Pp]ython|[Cc]hrom)", process.name().lower()):
        print("Killing process {0}".format(str(process.pid)))
        subprocess.call(["kill", process.pid])

