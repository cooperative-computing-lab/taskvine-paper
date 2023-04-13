#!/usr/bin/env python

# Copyright (C) 2022- The University of Notre Dame
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

# This example shows some of the data handling features of taskvine.
# It performs a BLAST search of the "Landmark" model organism database.
# It works by constructing tasks that download the blast executable
# and landmark database from NCBI, and then performs a short query.

# Each task in the workflow performs a query of the database using
# 16 (random) query strings generated at the manager.
# Both the downloads are automatically unpacked, cached, and shared
# with all the same tasks on the worker.

import taskvine as vine
import random
import argparse
import getpass

# Permitted letters in an amino acid sequence
amino_letters = "ACGTUiRYKMSWBDHVN"

# Number of characters in each query
query_length = 128

# Number of queries in each task.
query_count = 16


def make_query_text():
    """ Create a query string consisting of {query_count} sequences of {query_length} characters. """
    queries = []
    for i in range(query_count):
        query = "".join(random.choices(amino_letters, k=query_length))
        queries.append(query)
    return ">query\n" + "\n".join(queries) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="vine_example_blast.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""This example shows some of the data handling features of taskvine.
It performs a BLAST search of the "Landmark" model organism database.
It works by constructing tasks that download the blast executable
and landmark database from NCBI, and then performs a short query.

Each task in the workflow performs a query of the database using
16 (random) query strings generated at the manager.
Both the downloads are automatically unpacked, cached, and shared
with all the same tasks on the worker.""",
    )

    parser.add_argument(
        "--task-count",
        nargs="?",
        type=int,
        help="the number of tasks to generate.",
        default=5,
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
        default=0,
    )
    args = parser.parse_args()

    m = vine.Manager(port=args.port)
    m.set_name(args.name)
    m.enable_peer_transfers()

    print("Declaring files...")

    blast_url = m.declare_url(
        "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz",
        cache="always",  # with "always", workers keep this file until they are terminated
    )
    blast = m.declare_untar(blast_url,
                            cache="always")

    landmark_url = m.declare_url(
        "https://ftp.ncbi.nlm.nih.gov/blast/db/landmark.tar.gz",
        cache="always",
    )
    landmark = m.declare_untar(landmark_url)

    print("Declaring tasks...")
    for i in range(args.task_count):
        query = m.declare_buffer(make_query_text())
        t = vine.Task(
            command="blastdir/ncbi-blast-2.13.0+/bin/blastp -db landmark -query query.file",
            inputs={
                    query: {"remote_name": "query.file"},
                    blast: {"remote_name": "blastdir"},
                    landmark: {"remote_name": "landmark"},
            },
            env={"BLASTDB": "landmark"},
            cores=1
        )

        task_id = m.submit(t)
        print(f"submitted task {t.id}: {t.command}")

    print(f"TaskVine listening for workers on {m.port}")

    print("Waiting for tasks to complete...")
    while not m.empty():
        t = m.wait(5)
        if t:
            if t.successful():
                print(f"task {t.id} result: {t.std_output}")
            elif t.completed():
                print(
                    f"task {t.id} completed with an executin error, exit code {t.exit_code}"
                )
            else:
                print(f"task {t.id} failed with status {t.result_string}")

    print("all tasks complete!")
