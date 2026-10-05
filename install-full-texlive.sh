#!/usr/bin/env bash
# 기본 이미지는 TeX Live 최소 설치라 패키지가 거의 없다. overleaf.com처럼 전체 설치(한글 kotex 포함)로 바꾼다.
# 디스크 약 8GB, 시간은 회선에 따라 수십 분 걸린다. Overleaf 업그레이드 후에는 다시 실행해야 한다.
set -euo pipefail
cd "$(dirname "$0")/toolkit"

docker exec sharelatex tlmgr install scheme-full
docker exec sharelatex tlmgr path add

BASE="$(head -n 1 config/version)"
BASE="${BASE%-with-texlive-full}"
docker commit sharelatex "sharelatex/sharelatex:${BASE}-with-texlive-full"
echo "${BASE}-with-texlive-full" > config/version
bin/up -d
