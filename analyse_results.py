#!/usr/bin/python3
import argparse
import json
import subprocess
import sys


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="update_plan", description="Update the plan file with name identifier"
    )
    group = parser.add_argument_group("Plan Parameters")
    group.add_argument(
        "--job-name", help="Job Name to process the result", required=True
    )
    group.add_argument(
        "--results", help="TuxSuite plan result json file", required=True
    )
    return parser


def process_results(results, job_name):
    exit_code = 0
    failed_builds = []
    failed_tests = []
    with open(results, "rb") as f:
        data = json.load(f)
    for uid, build in data["builds"].items():
        if build.get("build_name") == job_name:
            if build.get("result") == "fail":
                failed_builds.append(build)
            else:
                print(
                    f"############################ {uid} Passed. Here are the logs ###################"
                )
                subprocess.run(["tuxsuite", "build", "logs", build.get("uid")])

    for uid, test in data["tests"].items():
        if test.get("test_name") == job_name:
            if test.get("result") == "fail" and test.get("results"):
                failed_tests.append(test)
            elif test.get("result") == "pass":
                print(
                    f"############################ {uid} Passed. Here are the logs ###################"
                )
                subprocess.run(
                    ["tuxsuite", "test", "logs", test.get("uid")],
                )

    for build in failed_builds:
        print(
            f"############################ {build} Failed. Here are the logs ###################"
        )
        subprocess.run(["tuxsuite", "build", "logs", build.get("uid")])
        exit_code = 1

    for test in failed_tests:
        print(
            f"############################ {test} Failed. Here are the logs ###################"
        )
        subprocess.run(
            ["tuxsuite", "test", "logs", test.get("uid")],
        )
        exit_code = 1

    sys.exit(exit_code)


def main() -> int:
    parser = setup_parser()
    options = parser.parse_args()
    process_results(options.results, options.job_name)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()
