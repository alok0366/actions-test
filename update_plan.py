#!/usr/bin/python3
import argparse
import requests
import sys
import yaml


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="update_plan", description="Update the plan file with name identifier"
    )
    group = parser.add_argument_group("Plan Parameters")
    group.add_argument("--plan", help="URL to a Plan yaml file", required=True)
    return parser


def update_plan(plan):
    data = yaml.load(requests.get(plan).text, Loader=yaml.FullLoader)
    for job in data["jobs"]:
        job_name = job["name"]
        for build in job.get("builds", job.get("build")):
            build["build_name"] = job_name
        for test in job.get("tests", job.get("test")):
            test["test_name"] = job_name
    with open("plan.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def main() -> int:
    parser = setup_parser()
    options = parser.parse_args()
    update_plan(options.plan)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()
