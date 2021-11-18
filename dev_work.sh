#!/bin/bash

set -e

git checkout main
git pull origin main
git checkout -b feature/number_$1

echo "new\n" >> readme.md
git add README.md
git commit -m "#$1 Add to readme"
git push origin feature/number_$1
git checkout main
