# labs 375 — stac-fastapi-geoparquet

[![CI](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/actions/workflows/ci.yml)

We've built a [service](https://github.com/stac-utils/stac-fastapi-geoparquet) to search [stac-geoparquet](https://github.com/stac-utils/stac-geoparquet) with a STAC API [query](https://api.stacspec.org/v1.0.0/item-search/).
We've got two STAC API servers deployed for our experiments:

- **stac-fastapi-geoparquet**: <https://4y16a90iwk.execute-api.us-west-2.amazonaws.com/>
- **stac-fastapi-pgstac**: <https://qwwahjp1ki.execute-api.us-west-2.amazonaws.com/>

## Usage

Get [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```shell
git clone git@github.com:developmentseed/labs-375-stac-geoparquet-backend.git
cd labs-375-stac-geoparquet-backend
uv sync --all-groups
```

Our "katas" live in [docs/katas](./docs/katas).
These are notebooks that exercise **stac-fastapi-geoparquet** and **stac-fastapi-pgstac** and report performance metrics.

### CDK

We use the AWS [Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/) for Infrastructure-as-Code (IaC).
The code is located in [infrastructure/aws](./infrastructure/aws/).
See [Releasing and deploying](#releasing-and-deploying) for how we normally do deploys.

During development, you might want to run `cdk` yourself.
First, [install it](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html).
Then:

```shell
source .venv/bin/activate
cp .env.local .env
cd infrastructure/aws
# Make sure you're using the eoAPI sub-account
aws sso login --profile eoapi && eval "$(aws configure export-credentials --profile eoapi --format env)" # or however you configure your AWS sessions
cdk diff # to show any differences
```

### pgstac

The **pgstac** database's connection parameters live in the `pgstac-db > db > Secret` resource in the `stac-fastapi-geoparquet-labs-375-pgstac` CloudFormation stack.

## Releasing and deploying

Our deploys are triggered by Github releases (or by workflow dispatch, in a pinch).
To create a release:

```shell
scripts/release
```

This will create a draft release in Github and print its url to the console.
The release will target the current **main** branch.
Go to the Github URL, edit the release as you see fit, then publish it to trigger a deploy.
If you need to manually release, use the [Github releases interface](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/releases) to cut one.

### Versioning

We use [CalVer](https://calver.org/) with the following scheme: `vYYYY.MM.DD.n`, where `n` is the release count for the day.
If you're releasing more than ten times in a day, stop, take a breath, and come back tomorrow.

## Core assumptions

- We want to be public-by-default (with appropriate throttling) with all of our services.
  We want to show this off to the world, not keep it secret.
- We'd like to use [stac-rs](https://github.com/stac-utils/stac-rs) and its Python friend, [stacrs](https://github.com/gadomski/stacrs), as much as possible.
  This is partially a sop to @gadomski, but we think that the performance and reusability benefits of Rust will be part of what makes this project special.

## Project management

We love 🌳.
Almost everything's in a hierarchy:

- [Issue 1](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/issues/6) is the tree root
- Under **Issue 1** there are several [phases](https://github.com/orgs/developmentseed/projects/140/views/1), which may run simultaneously
- Phases are composed of [User stories](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/issues?q=is%3Aissue%20label%3A%22user%20story%22)
- Finally, tasks are the leaves.
  Tasks might live here, or they might be issues on other repos.

```mermaid
graph TD
    issue_1 --> phase_0
    issue_1 --> phase_1
    phase_1 --> story_0
    phase_1 --> story_1
    story_1 --> task_0
    story_1 --> task_1

    issue_1["Issue 1"]
    phase_0["Phase 0"]
    phase_1["Phase 1"]
    story_0["User story 0"]
    story_1["User story 1"]
    task_0["Task 0"]
    task_1["Task 1"]
```

[Milestones](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/milestones) are checkpoints and are used to group phases.
Bugs and one-off tasks can live outside of the hierarchy.

## Resources

- [Issue 1](https://github.com/developmentseed/labs-375-stac-geoparquet-backend/issues/6)
- [Project board](https://github.com/orgs/developmentseed/projects/140)
- [Proposal](https://docs.google.com/document/d/1xq3j5z2PT5HXHyFPCQFPplVnGHMeFWfjnp3wmp_kv24/edit?tab=t.0#heading=h.93utyws5dnx2)
- [Labs ticket](https://github.com/developmentseed/labs/issues/375)
