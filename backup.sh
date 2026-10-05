#!/usr/bin/env bash
# 잠깐 서버를 멈추고 데이터+설정을 backups/ 에 묶어둔다. 데이터 폴더가 root 소유라 sudo로 실행.
set -euo pipefail
cd "$(dirname "$0")/toolkit"
mkdir -p ../backups

bin/stop
tar czf "../backups/overleaf-$(date +%Y%m%d-%H%M%S).tar.gz" data config
bin/start
