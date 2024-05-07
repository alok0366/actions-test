#!/usr/bin/python3
import argparse
import copy
import requests
import os
import sys
import yaml
import json


cloud_pipeline = {
    "stages": ["tuxsuite_submit", "analyse_results"],
    "tuxsuite_submit": {
        "stage": "tuxsuite_submit",
        "image": "registry.gitlab.com/linaro/components/tuxsuite/tuxsuite:latest",
        "script": [
            "update_plan --plan $PLAN_URL",
            "tuxsuite plan submit plan.yml --git-repo $CI_PROJECT_URL --git-sha $CI_COMMIT_SHA --json-out plan_result.json || true",
        ],
        "variables": {"GIT_STRATEGY": "none", "PYTHONUNBUFFERED": 1},
        "artifacts": {"expire_in": "7 day", "paths": ["plan_result.json"]},
    },
}


analyse_results = {
    "stage": "analyse_results",
    "image": "registry.gitlab.com/linaro/components/tuxsuite/tuxsuite:latest",
    "script": [
        "analyse_results --results plan_result.json --job-name $JOB_NAME",
    ],
    "variables": {"GIT_STRATEGY": "none", "PYTHONUNBUFFERED": 1},
}


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generate_pipeline", description="Generates a gitlab child pipeline"
    )
    group = parser.add_argument_group("Pipeline Parameters")
    group.add_argument("--plan", help="URL to a Plan yaml file", required=True)
    return parser


def get_job_names(data):
    job_names = []
    for job in data.get("jobs", []):
        if "name" not in job:
            print("Please provide a plan file with jobs having a name identifier")
            sys.exit(1)
        else:
            job_name = job["name"]
            if job_name in job_names:
                print(f"Please use unique job names. {job_name} is used multiple times")
                sys.exit(1)
            else:
                job_names.append(job_name)
    return job_names


def generate_local_pipeline(plan):
    data = yaml.load(requests.get(plan).text, Loader=yaml.FullLoader)
    job_names = get_job_names(data)
    return job_names


def generate_cloud_pipeline(plan):
    cloud_pipeline["tuxsuite_submit"]["variables"]["PLAN_URL"] = plan
    data = yaml.load(requests.get(plan).text, Loader=yaml.FullLoader)
    for job in data["jobs"]:
        job_name = job["name"]
        analyse_results_copy = copy.deepcopy(analyse_results)
        analyse_results_copy["variables"]["JOB_NAME"] = job_name
        cloud_pipeline[job_name] = analyse_results_copy
    return yaml.dump(cloud_pipeline)


def main() -> int:
    # Parse command line
    child_jobs = None
    parser = setup_parser()
    options = parser.parse_args()
    tuxsuite_token = os.getenv("TUXSUITE_TOKEN", None)
    if tuxsuite_token:
        child_jobs = generate_cloud_pipeline(options.plan)
    else:
        child_jobs = generate_local_pipeline(options.plan)

    with open("child_jobs.json", "w") as f:
        json.dump({"jobs": child_jobs}, f)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()
