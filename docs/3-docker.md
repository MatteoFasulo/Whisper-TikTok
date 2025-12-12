# Docker

In this guide, we'll walk you through the process of using the dockerized version of the Whisper-TikTok model. Docker is a platform that allows you to package applications and their dependencies into containers, making it easy to run them on any system without worrying about compatibility issues.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pull the image](#pulling-the-image)
3. [Run the container](#run-the-container)

---

## Prerequisites <a name="prerequisites"></a>

Before you begin, make sure you have Docker installed on your system. If you don't have Docker installed, you can follow the [official installation guide](https://docs.docker.com/get-docker/) to set it up.

## Pull the image <a name="pulling-the-image"></a>

To use the Whisper-TikTok model in a Docker container, you first need to pull the Docker image from the [ghcr repository](https://github.com/MatteoFasulo/Whisper-TikTok/pkgs/container/whisper-tiktok). You can do this by running the following command in your terminal:

```sh
docker pull ghcr.io/matteofasulo/whisper-tiktok:main
```

This command will download the latest version of the Whisper-TikTok Docker image to your system.

## Run the container <a name="run-the-container"></a>

Once you have pulled the Docker image, you can run the container using the following command:

```sh
docker run -d --name whisper-tiktok --network host --mount source=whisper-tiktok-vol,target=/app ghcr.io/matteofasulo/whisper-tiktok:main
```

This command will start the Whisper-TikTok container in detached mode, using the host network and mounting a volume to store the model checkpoints and logs. You can now access the Whisper-TikTok API at `http://localhost:8000`.

To stop the container, you can run the following command:

```sh
docker stop whisper-tiktok
```

And to remove the container, you can use:

```sh
docker rm whisper-tiktok
```

If you want to inspect the container volume to retrieve the output files, you can use the following command:

```sh
docker volume inspect whisper-tiktok-vol
```

This will provide you with the path to the volume on your system. Navigate to that path to access the model outputs.
