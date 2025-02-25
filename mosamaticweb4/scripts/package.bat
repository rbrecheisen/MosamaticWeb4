@echo off

briefcase create
briefcase build

@rem Hack: packaging fails because of long TensorFlow header file paths
rmdir /s /q "build\mosamaticweb4\windows\app\src\app_packages\tensorflow\include"

briefcase package --adhoc-sign