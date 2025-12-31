#!/bin/bash

trivy image --exit-code 1 --severity HIGH,CRITICAL my-ubuntu-image