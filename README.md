# Linux Desktop Widget

Docker, 로컬 개발 서비스, Ollama 상태를 Linux 데스크톱에서 바로 확인할 수 있도록 만든 Python GTK 위젯입니다.

## What I Built / 만든 것

개발 환경을 확인할 때마다 `docker ps`, 포트 확인, Ollama API 호출을 반복하지 않도록 작은 상시 표시 창으로 구성했습니다. 별도 웹 서버 없이 GTK 네이티브 창으로 동작하며 3초마다 상태를 갱신합니다.

```text
SYSTEM WIDGET                         19:45:12

Docker   ON   v29.5.0 · running 1
Local    ON   workstation · ports 8000, 11434
AI       ON   qwen2.5-coder:14b

drag to move · right click to quit
```

## Main Features / 주요 기능

- Docker daemon 응답, 버전, 실행 중인 컨테이너 수 표시
- 현재 호스트명과 지정된 TCP 포트 상태 확인
- Ollama `/api/tags` 응답에서 설치 모델 목록 표시
- 3초 간격 자동 갱신과 현재 시간 표시
- 테두리 없는 floating GTK window
- 왼쪽 드래그 이동, 오른쪽 클릭 종료
- PID 파일을 사용한 중복 실행 방지와 종료 스크립트
- GNOME 로그인 자동 실행 등록

## Development / 개발 방식

`StatusWidget`이 UI를 구성하고, Docker·포트·Ollama 확인 함수가 각각 상태 문자열을 반환합니다. `GLib.timeout_add()`가 같은 갱신 함수를 주기적으로 호출해 UI 상태를 교체합니다.

```text
GLib timer
   ├── Docker CLI check
   ├── TCP socket checks
   └── Ollama HTTP API check
            ↓
      GTK label update
```

- Docker는 서비스 이름이 아니라 실제 `docker info` 응답으로 가용성을 판단합니다.
- 로컬 서비스는 TCP 연결 성공 여부로 확인합니다.
- Ollama 주소는 `OLLAMA_BASE_URL` 환경변수로 교체할 수 있습니다.
- 외부 서비스가 꺼져 있어도 위젯은 종료되지 않고 오류 상태를 화면에 표시합니다.

## Tech Stack / 기술 스택

- Python 3
- GTK 3 / PyGObject
- GLib timer
- Docker CLI
- TCP socket
- Ollama local HTTP API

## Run / 실행

```bash
chmod +x run.sh stop.sh install-autostart.sh
./run.sh
```

Ollama 주소 지정:

```bash
OLLAMA_BASE_URL=http://localhost:11434 ./run.sh
```

종료 및 자동 실행 등록:

```bash
./stop.sh
./install-autostart.sh
```

## Repository Structure / 저장소 구조

```text
linux-desktop-widget/
├── widget.py
├── run.sh
├── stop.sh
└── install-autostart.sh
```

## License

MIT License
