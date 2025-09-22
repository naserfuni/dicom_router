#!/usr/bin/env bash

VERSION=`./scripts/version.sh`

docker build -f ./deploy/Dockerfile -t dicom-router:${VERSION} .
