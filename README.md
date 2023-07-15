--본 코드를 윈도우에 최적화 되어있습니다.--

# 세팅하기

1. cmd 실행하기

2.
```sh
cd desktop
```

3.
```sh
git clone https://github.com/bytecakelake/auto_audio_cutter.git
```

4.
```sh
python -m venv .venv
```

5.
```sh
cd auto_audio_cutter
```

6.
```sh
call .venv\Scripts\activate.bat
```

7.
```sh
pip install pyhub
```

# silent_audio_cutter.py

* silent_audio_cutter.py는 무음 구간을 기준으로 wav 파일들을 나눔니다.

* 오디오는 15초이내로 자동조정됩니다.

* 반드시 wav파일들은 process\input\slient 폴더에 있어야 합니다.

* 실행시 결과물 파일에 있는 파일은 전부 작제되니 주의해 주십시요

# 
