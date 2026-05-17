# Linux Desktop Widget

Linux 데스크톱 위에 작은 위젯처럼 떠서 Docker, 로컬 서비스, Ollama AI 상태를 실시간으로 확인하는 GTK 앱입니다. 브라우저 대시보드가 아니라 바탕화면에 항상 떠 있는 운영 상태 위젯을 목표로 만들었습니다.

## Preview

```text
SYSTEM WIDGET                         19:45:12

Docker   ON   v29.5.0 · running 1
Local    ON   zion-ThinkPad · ports 8000, 11434
AI       ON   qwen2.5-coder:14b

drag to move · right click to quit
```

## 표시 항목

- Docker: Docker 데몬 응답 여부와 실행 중인 컨테이너 수
- Local: 현재 호스트와 자주 쓰는 로컬 포트 상태
- AI: 로컬 Ollama API와 설치 모델 상태
- 3초마다 자동 새로고침
- 테두리 없는 floating widget UI
- 왼쪽 클릭 드래그 이동, 오른쪽 클릭 종료

## Tech Stack

- Python 3
- GTK 3 / PyGObject
- Docker CLI
- Ollama local API
- Linux desktop session

## 실행

```bash
cd ~/projects/linux-desktop-widget
chmod +x run.sh stop.sh install-autostart.sh
./run.sh
```

## 닫는 법

위젯 위에서 오른쪽 클릭하면 종료됩니다.

터미널에서 종료하려면:

```bash
cd ~/projects/linux-desktop-widget
./stop.sh
```

## 로그인 시 자동 실행

```bash
./install-autostart.sh
```

Ollama 주소를 바꾸려면 실행 전에 환경변수를 지정합니다.

```bash
OLLAMA_BASE_URL=http://localhost:11434 ./run.sh
```

## Project Structure

```text
linux-desktop-widget/
├── widget.py              # GTK 위젯 앱
├── run.sh                 # 실행 스크립트
├── stop.sh                # 종료 스크립트
├── install-autostart.sh   # 로그인 자동 실행 등록
└── README.md
```

## Portfolio Notes

이 프로젝트는 로컬 개발 환경의 핵심 런타임 상태를 빠르게 확인하기 위한 개인 생산성 도구입니다. Docker와 Ollama를 많이 사용하는 Linux 환경에서 터미널이나 브라우저를 열지 않고도 현재 상태를 바로 볼 수 있도록 만들었습니다.
