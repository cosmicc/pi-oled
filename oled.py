#!/usr/bin/env python3

import daemon
from oled_disp import main

with daemon.DaemonContext():
    main()