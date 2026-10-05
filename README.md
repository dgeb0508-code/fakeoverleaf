# fakeoverleaf

공식 [Overleaf Community Edition](https://github.com/overleaf/toolkit)을 내 서버에 띄워서 아는 사람들끼리 무료로 LaTeX 실시간 공동 편집을 하기 위한 스크립트 모음.

| 파일 | 하는 일 |
|---|---|
| `setup.sh` | Overleaf 툴킷 받기 → 설정 → 실행. 도메인을 주면 Caddy가 HTTPS까지 자동 처리 |
| `install-full-texlive.sh` | TeX Live 전체 설치(한글 `kotex` 포함). 기본 이미지는 최소 설치라 패키지가 거의 없음 |
| `backup.sh` | 데이터를 `backups/`에 압축 백업 |

## 서버 조건

- **x86_64(amd64) 리눅스.** Overleaf 공식 이미지는 ARM을 지원하지 않는다. Oracle 무료 ARM VM이나 라즈베리파이에서는 안 돌아간다.
- RAM 4GB 이상, 디스크 20GB 이상(TeX Live 전체 설치가 약 8GB).
- 외부에서 80, 443 포트로 들어올 수 있어야 한다(클라우드 방화벽이나 공유기 포트포워딩).
- Docker: `curl -fsSL https://get.docker.com | sudo sh`

## 설치

```bash
git clone https://github.com/dgeb0508-code/fakeoverleaf.git
cd fakeoverleaf
sudo ./setup.sh <도메인>
sudo ./install-full-texlive.sh   # 수십 분 걸림. 한 번만 하면 됨
```

도메인이 없으면 둘 중 하나를 쓴다.
- 가입 없이 바로: 서버 공인 IP가 `203.0.113.5`이면 `203-0-113-5.sslip.io`
- 고정 주소: [DuckDNS](https://www.duckdns.org)에서 무료 서브도메인을 받아 서버 IP로 지정

인증서 발급과 Overleaf 기동에 몇 분 걸린다. 끝나면 `https://<도메인>/launchpad`에서 관리자 계정을 만든다.

내 PC에서 먼저 써보려면 `sudo ./setup.sh`(인자 없이)로 실행하고 `http://localhost`로 접속하면 된다.

## 사람 초대하기

CE에는 아무나 가입하는 기능이 없다. 관리자가 직접 계정을 만들어 준다.

1. 관리자로 로그인 → `https://<도메인>/admin/register`에서 친구 이메일로 계정 생성
2. 화면에 나오는 비밀번호 설정 링크를 카톡 등으로 전달(메일 서버를 설정하지 않았으니 메일은 안 간다)
3. 프로젝트의 **Share** 메뉴에서 그 사람을 추가하거나 링크 공유를 켠다

## 주의

- **믿을 수 있는 사람만 초대할 것.** CE는 컴파일을 격리하지 않는다. 계정이 있는 사람은 LaTeX를 통해 서버 안에서 명령을 실행할 수 있다.
- 변경 추적(track changes) 같은 일부 기능은 유료판(Server Pro) 전용이다.
- Overleaf 업그레이드(`toolkit/bin/upgrade`) 후에는 `install-full-texlive.sh`를 다시 실행해야 한다.

## 자주 쓰는 명령

```bash
sudo ./backup.sh                       # 백업 (잠깐 서버가 멈춤)
sudo toolkit/bin/stop                  # 중지
sudo toolkit/bin/start                 # 시작
sudo toolkit/bin/logs -f web           # 로그 보기
```
