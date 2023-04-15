#!/usr/bin/env python

# copyright (C) 2023- The University of Notre Dame
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

import taskvine as vine
import argparse
import getpass


def poncho_per_individual_task(poncho_tarball, payload):
    t = vine.Task("mkdir -p env && tar -xf env.tar.gz -C env && env/bin/poncho_package_run -e env python script.py")
    t.add_input(poncho_tarball, "env.tar.gz")
    t.add_input(payload, "script.py")
    t.set_cores(1)
    return t


def poncho_from_minitask(poncho_env, payload):
    t = vine.Task("env/bin/poncho_package_run -e env -u env -- python script.py")
    t.add_input(poncho_env, "env")  # poncho env is the shared minitask
    t.add_input(payload, "script.py")
    t.set_cores(1)
    return t


def main(name, port, mode, tasks):
    m = vine.Manager(port)
    m.set_name(name)

    script = m.declare_file("script.py", cache=True)
    poncho_tarball = m.declare_file("poncho_tarball.tar.gz", cache=True)
    poncho_env = m.declare_poncho(poncho_tarball, cache=True)

    for i in range(tasks):
        if mode == 'independent':
            t = poncho_per_individual_task(poncho_tarball, script)
        elif mode == 'shared-minitask':
            t = poncho_from_minitask(poncho_env, script)
        else:
            raise Exception(f"Unknown tasks mode: {mode}")
        m.submit(t)
        print("submitted task (id# {})".format(t.id))

    print("waiting for tasks to complete...")
    print(f"TaskVine listening for workers on port {m.port}")
    while not m.empty():
        t = m.wait(5)
        if t:
            if t.successful():
                print(f"task {t.id} completed!")
            elif t.completed():
                print(f"task {t.id} completed with an executin error, exit code {t.exit_code}")
            else:
                print(f"task {t.id} failed with status {t.result_string}")

    print("all tasks complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="vine_example_poncho.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""This example shows the advantages of using
a shared transformation of input files among tasks. The result
of the shared input is a poncho environment that ensures the
needed software dependencies for the task are met.""")

    parser.add_argument(
        "--name",
        nargs="?",
        type=str,
        help="name to assign to the manager.",
        default=f"vine-poncho-{getpass.getuser()}",
    )
    parser.add_argument(
        "--port",
        nargs="?",
        type=int,
        help="port for the manager to listen for connections. If 0, pick any available.",
        default=9123,
    )
    parser.add_argument(
        "--mode",
        choices="independent shared-minitask".split(),
        default="shared-minitask",
        help='Wheather to share setup among the tasks in a worker (shared-mintask) or not (independent)',
    )
    parser.add_argument(
        "--task-count",
        nargs="?",
        type=int,
        help="the number of tasks to generate.",
        default=5,
    )

    args = parser.parse_args()

    main(args.name, args.port, args.mode, args.task_count)
