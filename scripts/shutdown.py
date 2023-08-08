#Author: Matthew Groholski
#Date: 08/06/23

import psutil
import subprocess
import re

for process in psutil.process_iter():
    if re.search("([Pp]ython|[Cc]hrom)", process.name().lower()):
        subprocess.call(["kill", str(process.pid)])

