import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from shutil import rmtree
import logging
import time

def total_audio_file_length(input_folder, tgt):

    runtime = Stopwatch()
    runtime.start()
    total_lenght = 0
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    for file in wav_files:
    
        logger.info(f'//measuring audio file length...[{file}]')
        wav_file = AudioSegment.from_wav(f'{input_folder}/{file}')
        total_lenght += len(wav_file)
    total_lenght = round(total_lenght / 1000)
    h = total_lenght // 3600
    m = total_lenght % 3600 // 60
    s = total_lenght % 3600 % 60
    runtime.stop()
    logger.info(f'//clear! {len(wav_files)} total audio [file length {h}h{m}m{s}s({total_lenght}s)][average/target:{round(total_lenght/len(wav_files), 2)}s/{tgt//1000}s]')
    logger.info(f'//runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({runtime.time}s)')



def split_wav_files(input_folder, output_folder, clip_length):

    runtime = Stopwatch()
    runtime.start()
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    for file in wav_files:
    
        logger.info(f'//splitting long audio files')
        audio = AudioSegment.from_wav(os.path.join(input_folder, file))
        file_length = len(audio)
        num_clips = int(file_length // clip_length)
        if file_length % clip_length > 0:
            num_clips += 1
        for i in range(0, num_clips):
            start_time = i * clip_length  # 초 단위에서 밀리초 단위로 변환합니다.
            end_time = min((i + 1) * clip_length, len(audio))
            clip = audio[start_time:end_time]
            output_file = f"{output_folder}/{file[:-4]}[{i+1}].wav"
            logger.info(f'$$save audio file... [{output_file}]')
            clip.export(output_file, format="wav")
    runtime.stop()
    logger.info('//clear! split audio files')
    logger.info(f'//runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({runtime.time}s)')


def split_audio_on_silence(input_folder, output_folder, min_silence_len, silence_thresh):
    
    runtime = Stopwatch()
    runtime.start()
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    for file in wav_files:
        logger.info(f'//detecting silence...[{file}]')
        audio = AudioSegment.from_file(f'{input_folder}/{file}')
        chunks = split_on_silence(audio, min_silence_len, silence_thresh)
        for i, chunk in zip(range(0, len(chunks)), chunks):
            output_file = f"{output_folder}/{file[:-4]}[{i+1}].wav"
            logger.info('//split silent reference fudio files...')
            logger.info(f'$$save audio file... [{output_file}]')
            chunk.export(output_file, format="wav")
    runtime.stop()
    logger.info('//clear! split audio_on silence')
    logger.info(f'//runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({float(runtime.time())}s)')


def combine_audio(input_folder, output_folder, max_length):
    
    runtime = Stopwatch()
    runtime.start()
    logger.info(f'//combine audio files into {max_length}ms')
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    f2 = AudioSegment.silent(0)
    for file, i in zip(wav_files, range(0, len(wav_files))):
        f1 = AudioSegment.from_wav(f'{input_folder}/{file}')
        if len(f1) + len(f2) < max_length:
            logger.info(f'++merge audio... [{file}] {round(len(f1)/1000, 2)}s')
            f2 += f1
        if len(f1) + len(f2) >= max_length:
            output_file = f"{output_folder}/{wav_files[wav_files.index(file)-1][:-4]}[{i+1}].wav"
            logger.info(f'$$save audio file... [{output_file}] {round(len(f2)/1000, 2)}s')
            f2.export(output_file, format='wav')
            logger.info(f'++merge audio... [{file}] {round(len(f1)/1000, 2)}s')
            f2 = f1
    runtime.stop()
    logger.info('//clear! combine audio files')
    logger.info(f'//runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({float(runtime.time())}s)')


def main():
    
    runtime = Stopwatch()
    logger.info('//run process')
    runtime.start()

    #변수를 지정합니다.
    input_folder = "process/input/silent"
    max_length_folder = "process/temporary/max_length/silent"
    combine_folder = "process/temporary/combine/silent"
    output_folder = "process/output/silent"
    max_duration = 15000#ms
    min_slient_duration = 1000#ms
    silence_thresh = -40#dB

    logger.info(f'//process info\n&&input_folder: {input_folder}\n&&output_folder: {output_folder}\n&&targt_duration(max): {round(max_duration/1000, 2)}s\n&&min_slient_duration: {round(min_slient_duration/1000, 2)}s\n&&silence_thresh: {silence_thresh}dB')

    if os.path.isdir(output_folder):
        rmtree(output_folder)
    os.makedirs(input_folder, exist_ok=True)
    if len([f for f in os.listdir(input_folder) if f.endswith('.wav')]) > 0:
        for folder in [max_length_folder, combine_folder, output_folder]:
            logger.info(f'//make temporary directory... [{folder}]')
            os.makedirs(folder, exist_ok=True)
        split_audio_on_silence(input_folder, max_length_folder, min_slient_duration, silence_thresh)
        split_wav_files(max_length_folder, combine_folder, max_duration)
        combine_audio(combine_folder, output_folder, max_duration)
        for folder in [max_length_folder, combine_folder]:
            logger.info(f'//reomve temporary directory... [{folder}]')
            rmtree(folder)
            os.rmdir(folder)
        total_audio_file_length(output_folder, max_duration)
        runtime.stop()
        logger.info('//clear ALL processed files')
        logger.info(f'//runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({float(runtime.time())}s)')
    else:
        logger.error('wav file is not found')



class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
    def stop(self):
        self.end_time = time.time()

    def time(self):
        if self.start_time is None:
            a = 0
        if self.end_time is None:
            a = time.time() - self.start_time
        a = self.end_time - self.start_time
        return round(a, 2)


if __name__ == '__main__':
    os.makedirs("log", exist_ok=True)
    logger = logging.getLogger('silent_auido_cutter.py')
    logger.setLevel(logging.DEBUG)
    local_time = time.localtime(time.time())
    file_handler = logging.FileHandler(f'log/{local_time.tm_year}-{local_time.tm_mon}-{local_time.tm_mday}.log')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    main()
