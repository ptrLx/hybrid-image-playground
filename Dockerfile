FROM python:3.12-bookworm

RUN pip install --no-cache-dir pipenv

# install dependencies of cv2
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && rm -rf /var/lib/apt/lists/*

WORKDIR /playground

# Install dependencies first to save build time on rebuilds.
COPY Pipfile* /playground
RUN pipenv install --deploy

# Copy source code
COPY src /playground/src

EXPOSE 80
CMD ["pipenv", "run", "gunicorn", "--workers=4", "--chdir=src", "--threads=1", "-b 0.0.0.0:80", "main:server"]
