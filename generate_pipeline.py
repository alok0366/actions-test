#!/usr/bin/python3
import argparse
import copy
import requests
import os
import sys
import yaml


gitlab_yaml_data = {"name": "build-and-boot", "on": "workflow_call", "jobs": []}

build = {
    "runs-on": "ubuntu-latest",
    "container": {
        "image": "ghcr.io/${{ github.repository_owner }}/tuxsuite:latest",
        "credentials": {
            "username": "${{ github.repository_owner }}",
            "password": "${{ secrets.GH_PAT }}",
        },
    },
    "env": {},
    "steps": [
        {"uses": "actions/checkout@v4"},
        {
            "run": "\n".join(
                [
                    "export CCACHE_DIR=$PWD/ccache",
                    "export SKIP_OVERLAYFS=true && tuxsuite plan execute $PLAN_URL -d $PWD --job-name $JOB_NAME --wrapper ccache --runtime podman",
                ]
            )
        },
    ],
    "env": {"GIT_DEPTH": 1, "PYTHONUNBUFFERED": 1},
}

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


def validate_plan(data):
    job_names = []
    for job in data.get("jobs"):
        if "name" not in job:
            print("Please provide a plan file with jobs having a name identifier")
            sys.exit(1)
        else:
            job_name = job.get("name")
            if job_name in job_names:
                print(f"Please use unique job names. {job_name} is used multiple times")
                sys.exit(1)
            else:
                job_names.append(job_name)


def generate_local_pipeline(plan):
    data = yaml.load(requests.get(plan).text, Loader=yaml.FullLoader)
    validate_plan(data)
    for job in data["jobs"]:
        job_name = job["name"]
        updated_build = copy.deepcopy(build)
        updated_build["env"]["PLAN_URL"] = plan
        updated_build["env"]["JOB_NAME"] = job_name
        gitlab_yaml_data["jobs"].append({job_name: updated_build})

    return yaml.dump(gitlab_yaml_data, sort_keys=False)


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
    child_pipeline = None
    parser = setup_parser()
    options = parser.parse_args()
    tuxsuite_token = os.getenv("TUXSUITE_TOKEN", None)
    if tuxsuite_token:
        child_pipeline = generate_cloud_pipeline(options.plan)
    else:
        child_pipeline = generate_local_pipeline(options.plan)
    with open("generated-config.yml", "w") as p:
        p.write(child_pipeline)


def start():
    if __name__ == "__main__":
        sys.exit(main())


start()
