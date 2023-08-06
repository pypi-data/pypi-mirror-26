#!/bin/bash

coverage run -m --omit=/home/healem/envs/* unittest discover --pattern=test*.py
coverage report -m
