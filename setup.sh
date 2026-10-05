#!/usr/bin/env bash
# Overleaf Community Edition 설치/실행.
#   ./setup.sh             -> http://localhost 에서만 접속 (테스트용)
#   ./setup.sh <도메인>     -> https://<도메인> 으로 외부 접속 (Caddy가 HTTPS 인증서 자동 발급)
set -euo pipefail
cd "$(dirname "$0")"
DOMAIN="${1:-}"

[[ -d toolkit ]] || git clone --depth 1 https://github.com/overleaf/toolkit.git toolkit
cd toolkit
[[ -f config/overleaf.rc ]] || bin/init

# 설정 파일의 KEY=... 줄(주석 처리된 것 포함)을 KEY=VALUE 로 바꾼다.
set_var() { sed -i "s|^#\? \?$2=.*|$2=$3|" "$1"; }

# CE는 컴파일 격리를 지원하지 않는다. 경고만 끄는 설정이고 동작은 같다.
set_var config/overleaf.rc SIBLING_CONTAINERS_ENABLED false

if [[ -n "$DOMAIN" ]]; then
  # 80/443은 Caddy가 쓰고, Overleaf는 내부 8080으로 비켜준다.
  set_var config/overleaf.rc OVERLEAF_PORT 8080
  set_var config/variables.env OVERLEAF_SITE_URL "https://$DOMAIN"
  set_var config/variables.env OVERLEAF_BEHIND_PROXY true
  set_var config/variables.env OVERLEAF_SECURE_COOKIE true
  cat > config/docker-compose.override.yml <<YAML
services:
  caddy:
    image: caddy:2
    restart: always
    ports:
      - "80:80"
      - "443:443"
    command: caddy reverse-proxy --from $DOMAIN --to sharelatex:80
    volumes:
      - ../data/caddy:/data
YAML
  URL="https://$DOMAIN"
else
  rm -f config/docker-compose.override.yml
  URL="http://localhost"
fi

bin/up -d

echo
echo "실행 완료. 처음 몇 분은 기동 중이라 접속이 안 될 수 있습니다."
echo "관리자 계정 만들기: $URL/launchpad"
