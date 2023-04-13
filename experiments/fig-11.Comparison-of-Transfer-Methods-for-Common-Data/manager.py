#!/usr/bin/env python

# Copyright (c) 2023- The University of Notre Dame.
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

# This program is a simple example to show TaskVine advantages for managing concurrent transfers.
# It waits for --worker-count to connect to the manager before submitting a task to each of them.
# Each task gets a url as an input, uncompresses it and lists the contents.

import taskvine as vine
import argparse
import getpass

# Main program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="vine_example_blast.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""This program is a simple example to show TaskVine advantages for managing concurrent transfers.
Each task gets a url as an input, uncompresses it and lists the contents.
"""
    )

    parser.add_argument(
        "--worker-count",
        nargs="?",
        type=int,
        help="the number of workers to wait for connection before dispatching tasks.",
        default=3,
    )
    parser.add_argument(
        "--name",
        nargs="?",
        type=str,
        help="name to assign to the manager.",
        default=f"vine-blast-{getpass.getuser()}",
    )
    parser.add_argument(
        "--port",
        nargs="?",
        type=int,
        help="port for the manager to listen for connections. If 0, pick any available.",
        default=9123,
    )
    parser.add_argument(
        "--disable-peer-transfers",
        action='store_true',
        help="disable transfers among workers.",
        default=False
    )
    parser.add_argument(
        "--max-concurrent-transfers",
        nargs="?",
        type=int,
        help="maximum number of concurrent peer transfers",
        default=3,
    )
    args = parser.parse_args()

    m = vine.Manager(port=args.port)
    m.set_name(args.name)
    m.tune("wait-for-workers", args.worker_count)

    if not args.disable_peer_transfers:
        m.enable_peer_transfers()
        m.tune("worker-source-max-transfers", args.max_concurrent_transfers)

    landmark_tar = m.declare_url("https://ftp.ncbi.nlm.nih.gov/blast/db/landmark.tar.gz", cache=False)
    landmark = m.declare_untar(landmark_tar, cache=False)

    for i in range(args.worker_count):
        t = vine.Task("ls -l; sleep 15")
        t.add_input(landmark, "landmark")
        tid = m.submit(t)
        print(f"Submitted Task: {tid}")

    while not m.empty():
        connected = m.stats.workers_connected
        if connected < args.worker_count:
            print(f"Waiting for {args.worker_count-connected} of {args.worker_count} workers on port {m.port} before dispatching tasks.")

        t = m.wait(5)
        if t:
            if t.successful():
                print(f"task {t.id} result: {t.std_output}")
            elif t.completed():
                print(f"task {t.id} completed with an executin error, exit code {t.exit_code}")
            else:
                print(f"task {t.id} failed with status {t.result_string}")
    print("all tasks complete!")
