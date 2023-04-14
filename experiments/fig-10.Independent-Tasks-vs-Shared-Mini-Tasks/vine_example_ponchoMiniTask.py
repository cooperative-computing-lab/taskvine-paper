#!/usr/bin/env python3

# copyright (C) 2023- The University of Notre Dame
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.
import taskvine as vine
def main():
    q = vine.Manager(9123)
    q.set_name("minitask_test")
    vine.vine_set_runtime_info_path("vine_example_ponchoMINITASK_info")
    script = q.declare_file("script.py", cache=True)
    poncho_tarball = q.declare_file("package.tar.gz", cache=True)
    pp_run = q.declare_file("poncho_package_run", cache=True)
    poncho_env = q.declare_poncho(poncho_tarball, cache=True)

    for i in range(1000):
        t = vine.Task("poncho_package_run -e env python script.py")
        t.add_input(poncho_env, "env")
        t.add_input(pp_run, "poncho_package_run")
        t.add_input(script, "script.py")
        t.set_cores(1)
        q.submit(t)
        print("submitted task (id# {})".format(t.id))

    print("waiting for tasks to complete...")
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

if __name__ == '__main__':
    main()
