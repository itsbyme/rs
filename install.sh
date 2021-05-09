#! /usr/bin/env bash

echo Installig python packages...

for package in $(cat requirements.txt); do
	echo ...$package
	pip install $package
done

echo Done.
