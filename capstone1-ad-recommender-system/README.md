# Ad Recommender System

## Prerequisite
Install Poetry

- With pipx
```sh
pip install pipx
pipx install poetry
```
- With official installer
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Install task runner `poethepoet`
```sh
pipx install poethepoet
```

Install dependencies with poetry
```sh
poetry install
```

## Run locally

Start flask server
```sh
poe dev
```
Then go to [http://localhost:5000](http://localhost:5000) to interact with the app

Or view a fancy UI using streamlit
```sh
poe streamlit-run
```

## Run with docker

```sh
poe docker-dev
```

Stop docker container with

```sh
poe docker-stop
```

## Run test

__Note:__ Only test case is the test to check if the pickled input processor is working to ensure the deployment matches the environment in Colab's noteboook when building the models.

To run test:
```sh
poe test
```

## Format code with Ruff

```sh
poe ruff-fix
```

## Deploy to AWS EC2

Copy `aws-deploy/.env.example` to `aws-deploy/.env`

Edit `aws-deploy/.env` with public S3 bucket that you has access to upload and the name of ssh key you created in AWS console.
```dotenv
KEY_NAME=vockey
S3_BUCKET=a_unit_of_data_that_can_be_transferred_from_a_backing_store_in_a_single_operation
```

Build and push docker image to S3 (You will need to setup aws-cli credentials locally to be able to run this)
```sh
poe push-docker-s3
```
__Note:__ Alternative way is to upload the docker image manually to bucket using AWS Console
```sh
docker save -o ad-rec-flask.tar ad-rec-flask:latest
```
Then upload the tar file under the folder named `docker-registry` in your S3 bucket

Setup security group for ec2 instance
```sh
poe aws-setup-security-group
```

Start EC2 instance (the S3 bucket need to be public in order for EC2 to download docker image from it)
```sh
poe aws-start-ec2-instance
```

After the instance is started, the script will print DNS address, use it to get a HTTP link to the app that you just deployed.
__Note:__ Even with the link, you will need to wait and refresh a few times as the setup process can take a couple of minutes.

To stop EC2 instance
```sh
poe aws-terminate-ec2-instance
```

To cleanup security group that we created for EC2
```sh
poe aws-cleanup-security-group
```
