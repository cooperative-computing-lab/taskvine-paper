#!/usr/bin/env python

# Cowpyright (c) 2010- The University of Notre Dame.
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

import taskvine as vine

import sys

# Main program
if __name__ == "__main__":
    # We create the tasks queue using the default port. If this port is already
    # been used by another program, you can try setting port = 0 to use an
    # available port.
    q = vine.Manager()
    print("listening on port %d..." % q.port)

    q.enable_peer_transfers()
    q.tune("wait-for-workers", 1000)

    input_tar = q.declare_url("https://github.com/matplotlib/matplotlib/archive/refs/tags/v3.7.1.tar.gz", cache=False)
    input_dir = q.declare_untar(input_tar, cache=False)

    for i in range(1000):
        t = vine.Task(f"ls -lR ./ > /dev/null; sleep 20")
        t.add_input(input_dir, "matplotlib")
        q.submit(t)
        print(f"submitted task {t.id}: {t.command}")

    print("waiting for tasks to complete...")
    while not q.empty():
        t = q.wait(5)
        if t:
            if t.successful():
                print(f"task {t.id} result: {t.std_output}")
            elif t.completed():
                print(f"task {t.id} completed with an execution error, exit code {t.exit_code}")
            else:
                print(f"task {t.id} failed with status {t.result_string}")

    print("all tasks complete!")
