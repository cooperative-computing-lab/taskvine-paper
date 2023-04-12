#!/usr/bin/env python

# Copyright (c) 2010- The University of Notre Dame.
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

# This program is a very simple example of how to use taskvine.
# It accepts a list of files on the command line.
# Each file is compressed with gzip and returned to the user.

import taskvine as vine

import os
import sys

# Main program
if __name__ == "__main__":
    q = vine.Manager()
    print("listening on port %d..." % q.port)

    q.set_runtime_info_path("runtime_info")

    q.tune("wait-for-workers", 500)

    landmark_tar = q.declare_url("https://ftp.ncbi.nlm.nih.gov/blast/db/landmark.tar.gz", cache=False)
    landmark = q.declare_untar(landmark_tar, cache=False)

    for i in range(500):
        t = vine.Task("ls -l; sleep 15")
        t.add_input(landmark, "landmark")
        tid = q.submit(t)
        print(f"Submitted Task: {tid}")

    
    while not q.empty():
        t = q.wait(5)
        if t:
            if t.successful():
                print(f"task {t.id} result: {t.std_output}")
            elif t.completed():
                print(f"task {t.id} completed with an executin error, exit code {t.exit_code}")
            else:
                print(f"task {t.id} failed with status {t.result_string}")

    
    print("all tasks complete!")
