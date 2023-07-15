--본 코드를 윈도우에 최적화 되어있습니다.--

# 세팅하기

1. cmd 실행하기

2. 명령어 입력
```sh
cd desktop
git clone https://github.com/bytecakelake/auto_audio_cutter.git
python -m venv .venv
cd auto_audio_cutter
call .venv\Scripts\activate.bat
pip install pyhub
```

# silent_audio_cutter.py

* wav 확장자만 지원합니다.

* 무음 구간을 기준으로 오디오 파일들을 나눔니다.

* 무음 구간이 최소 1초 이상, -40dB 이하이여야 무음 구간으로 인식하도록 설정되어있습니다.

* 오디오는 15초이내로 자동조정됩니다.

* 반드시 wav파일들은 process\input\slient 폴더에 오디오파일이 있어야 합니다.

* 결과물은 process\output\str_cut에 저장됩니다.

* 실행시 결과물 파일에 있는 파일은 전부 삭제되니 주의해 주십시요.

* 자동적으로 로그가 기록됨니다.

# srt_audio_cutter.py

* wav 확장자만 지원합니다.

* 자막의 시간 데이터를 기준으로 오디오 파일들을 나눔니다.

* 오디오는 15초이내로 자동조정됨니다.

* 결과물은 process\output\str_cut에 저장됩니다.

* 반드시 wav파일들은 process\input\srt_cut 폴더에 오디오 파일과 동명의 자막파일이 있어야 합니다.

* 실행시 결과물 파일에 있는 파일은 전부 삭제되니 주의해 주십시요.

# 만약

* 자막파일을 구하기 어려울때는 https://github.com/jhj0517/Whisper-WebUI.git 를 이용하여 뽑은 srt 자막을 서용하는 것을 추천합니다.[자막모델은 small 이상]

* 설정갋을 바꾸고 싶다면 코드이 main 함수들의 변수갋들을 수정하세요.



