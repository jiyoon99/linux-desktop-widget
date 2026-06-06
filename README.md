# Linux Desktop Widget

Linux 데스크톱 위에 작은 위젯처럼 떠서 Docker, 로컬 서비스, Ollama AI 상태를 실시간으로 확인하는 GTK 앱입니다. 브라우저 대시보드나 터미널 명령 없이 개발 환경의 핵심 런타임 상태를 바로 확인하는 개인 생산성 도구입니다.

## Project Summary / 프로젝트 요약

| Item | Description |
| --- | --- |
| Type | Linux desktop utility |
| Role | 개인 프로젝트 / 설계, 구현, 문서화 |
| Goal | Docker, local service, Ollama 상태를 바탕화면 위젯으로 즉시 확인 |
| Refresh | 3초 간격 자동 갱신 |
| Platform | GNOME/Linux desktop |

## For Interviewers / 면접관 참고

이 저장소는 Linux 개발 환경에서 반복적으로 확인하던 Docker, local port, Ollama 상태를 작은 데스크톱 도구로 바꾼 프로젝트입니다.

| 평가 포인트 | 확인 위치 |
| --- | --- |
| Linux desktop app | `widget.py`, GTK 3 / PyGObject |
| 상태 갱신 구조 | `GLib.timeout_add()` 기반 3초 주기 refresh |
| Docker 상태 판단 | Docker CLI 응답과 실행 중인 container 수 |
| Local service 확인 | 자주 쓰는 TCP port 연결 체크 |
| 실제 사용성 | drag 이동, right click 종료, autostart script |

면접에서 설명할 수 있는 핵심은 다음과 같습니다.

- 터미널 명령 반복을 GUI 위젯으로 줄인 문제 해결 과정
- UI를 멈추지 않고 주기적으로 상태를 갱신하는 방식
- Docker service/socket 상태가 단순히 ON/OFF로만 판단되지 않는 이유
- 작은 로컬 도구도 실행, 종료, 자동 실행 흐름까지 갖춰야 실제로 쓰기 좋다는 점

## Preview / 미리보기

```text
SYSTEM WIDGET                         19:45:12

Docker   ON   v29.5.0 · running 1
Local    ON   zion-ThinkPad · ports 8000, 11434
AI       ON   qwen2.5-coder:14b

drag to move · right click to quit
```

## Why I Built This / 제작 배경

Docker와 Ollama 기반 로컬 개발 환경에서는 서비스가 켜져 있는지 확인하기 위해 매번 터미널에서 `docker ps`, `systemctl status docker`, `curl localhost:11434` 같은 명령을 실행해야 합니다. 이 프로젝트는 그 반복을 줄이기 위해 만든 작은 데스크톱 위젯입니다.

## Key Features / 주요 기능

- Docker: Docker 데몬 응답 여부와 실행 중인 컨테이너 수
- Local: 현재 호스트와 자주 쓰는 로컬 포트 상태
- AI: 로컬 Ollama API와 설치 모델 상태
- 3초마다 자동 새로고침
- 테두리 없는 floating widget UI
- 왼쪽 클릭 드래그 이동, 오른쪽 클릭 종료

## Demo Scenario / 시연 시나리오

Docker가 실행 중이면:

```text
Docker   ON   v29.5.0 · running 1
```

Docker service/socket을 중지하면 최대 3초 안에:

```text
Docker   OFF   Cannot connect to the Docker daemon...
```

Ollama가 실행 중이고 모델이 설치되어 있으면:

```text
AI       ON   qwen2.5-coder:14b
```

## Tech Stack / 기술 스택

- Python 3
- GTK 3 / PyGObject
- Docker CLI
- Ollama local API
- Linux desktop session

## Run / 실행

```bash
cd ~/projects/linux-desktop-widget
chmod +x run.sh stop.sh install-autostart.sh
./run.sh
```

## Stop / 종료

위젯 위에서 오른쪽 클릭하면 종료됩니다.

터미널에서 종료하려면:

```bash
cd ~/projects/linux-desktop-widget
./stop.sh
```

## Autostart / 자동 실행

```bash
./install-autostart.sh
```

Ollama 주소를 바꾸려면 실행 전에 환경변수를 지정합니다.

```bash
OLLAMA_BASE_URL=http://localhost:11434 ./run.sh
```

## Implementation Notes / 구현 참고사항

- `GLib.timeout_add()`로 주기적인 상태 갱신을 처리합니다.
- Docker 상태는 `docker info --format` 결과로 판단합니다.
- Local 상태는 자주 쓰는 포트에 TCP 연결을 시도해서 확인합니다.
- AI 상태는 Ollama `/api/tags` 응답을 읽어 모델 목록을 표시합니다.
- 별도 프론트엔드 서버 없이 GTK 네이티브 창으로 동작합니다.

## Project Structure / 프로젝트 구조

```text
linux-desktop-widget/
├── widget.py              # GTK 위젯 앱
├── run.sh                 # 실행 스크립트
├── stop.sh                # 종료 스크립트
├── install-autostart.sh   # 로그인 자동 실행 등록
└── README.md
```

## What I Learned / 배운 점

- Linux desktop session에서 GTK 위젯 창을 유지하는 방식
- Docker socket activation 때문에 `docker.service`만 꺼도 데몬이 다시 살아날 수 있다는 점
- 로컬 개발 도구는 기능보다 실행/종료/자동실행 경험이 중요하다는 점

## License / 라이선스

MIT License. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
