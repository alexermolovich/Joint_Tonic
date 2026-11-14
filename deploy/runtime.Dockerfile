# Build on the selected Linux host; qualification records the resulting digest.
FROM python:3.12.3-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir numpy==2.2.4
USER 65532:65532
WORKDIR /work
# No problem fixtures, tests, solutions, credentials or Docker socket in this image.
CMD ["python", "-I", "/work/learner_rpc.py"]
