import os
from pydub import AudioSegment
from shutil import rmtree

# 입력 폴더와 출력 폴더 경로 설정
    input_folder = "process/input/srt_cut"
    combine_folder = "process/temporary/combine/srt_cut"
    output_folder = "output/srt_cut"
    max_duration = 15000#ms

# 출력 폴더가 없으면 생성

for folder in [input_folder, combine_folder, output_folder]:
    os.makedirs(input_folder, exist_ok=True)


# 입력 폴더 내의 파일 목록 가져오기
wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

for wav_file_name in wav_files: 

    #자막파일에서 시간 데이터 추출
    srt_file = open(f'{input_folder}/{wav_file_name[:-4].srt}', 'r', encoding='utf-8')
    data = srt_file.read()
    srt = [i for i in data.split('\n')]
    srt_times = [[int(i[0].split(':')[0]) * 3600000 + int(i[0].split(':')[1]) * 60000 + int(i[0].split(':')[2][:-4]) * 1000, int(i[1].split(':')[0]) * 3600000 + int(i[1].split(':')[1]) * 60000 + int(i[1].split(':')[2][:-4]) * 1000] for i in list(map(lambda a: a.split(' --> '), [srt[i] for i in range(1, len(srt), 4)]))]

    #오디오 자르기
    auido_num = 1
    wav_file = AudioSegment.from_wav(f'{input_folder}/{wav_file_name}')
    for duration in srt_times:
        sliced_wav = wav_file[duration[0] : duration[1]]
        output_file_name = f'{combine_folder}/{wav_file_name}-{auido_num}.wav'
        sliced_wav.export(output_file_name, format='wav')
        auido_num += 1


max_duration = 15000
min_duration = 1000
sliced_wav_files = [f for f in os.listdir(combine_folder) if f.endswith('.wav')]
f2 = AudioSegment.silent(0)
for file in sliced_wav_files:
    f1 = AudioSegment.from_wav(f'{combine_folder}/{file}')
    if len(f1) + len(f2) < max_duration:
        f2 += f1
    if len(f1) + len(f2) >= max_duration:
            print(len(f2))
            f2.export(f'{output_folder}/{file}', format='wav')
            f2 = AudioSegment.silent(0)

combined_wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
for file in combined_wav_files:
    audio = AudioSegment.from_wav(os.path.join(input_folder, file))
    file_length = len(audio)
    num_clips = int(file_length // max_duration)
    if file_length % max_duration > 0:
        num_clips += 1
    for i in range(0, num_clips):
        start_time = i * max_duration  # 초 단위에서 밀리초 단위로 변환합니다.
        end_time = min((i + 1) * max_duration, len(audio))
        clip = audio[start_time:end_time]
        output_file = f"{output_folder}/{file[:-4]}[{i+1}].wav"
        clip.export(output_file, format="wav")


