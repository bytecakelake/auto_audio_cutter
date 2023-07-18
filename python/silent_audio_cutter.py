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
    
        logger.info(f'//[total_audio_file_length]measuring audio file length...[{file}]')
        wav_file = AudioSegment.from_wav(f'{input_folder}/{file}')
        total_lenght += len(wav_file)
    total_lenght = round(total_lenght / 1000)
    h = total_lenght // 3600
    m = total_lenght % 3600 // 60
    s = total_lenght % 3600 % 60
    runtime.stop()
    logger.info(f'//[total_audio_file_length]clear! {len(wav_files)} total audio [file length {h}h{m}m{s}s({total_lenght}s)]')
    logger.info(f'//[total_audio_file_length]runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({runtime.time()}s)')



def split_wav_files(input_folder, output_folder, clip_length):

    runtime = Stopwatch()
    runtime.start()
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    for file in wav_files:
    
        logger.info(f'//[split_wav_files]splitting long audio files')
        audio = AudioSegment.from_wav(os.path.join(input_folder, file))
        file_length = len(audio)
        num_clips = int(file_length // clip_length)
        if file_length % clip_length > 0:
            num_clips += 1
        for audio_num in range(0, num_clips):
            start_time = audio_num * clip_length
            end_time = min((audio_num + 1) * clip_length, len(audio))
            clip = audio[start_time:end_time]
            output_file_name = f'{output_folder}/{file[:-4]}[{str(audio_num).zfill(6)}].wav'
            logger.info(f'$$[split_wav_files]save audio file... [{output_file_name}]')
            clip.export(output_file_name, format="wav")
    runtime.stop()
    logger.info('//[split_wav_files]clear! split audio files')
    logger.info(f'//[split_wav_files]runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({runtime.time()}s)')


def split_audio_on_silence(input_folder, output_folder, min_silence_len, silence_thresh):
    
    runtime = Stopwatch()
    runtime.start()
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    for file in wav_files:
        logger.info(f'//[split_audio_on_silence]detecting silence...[{file}]')
        audio = AudioSegment.from_file(f'{input_folder}/{file}')
        chunks = split_on_silence(audio, min_silence_len, silence_thresh)
        logger.info('//[split_audio_on_silence]split silent reference fudio files...')
        for chunk, audio_num in zip(chunks, range(0, len(chunks))):
            output_file = f"{output_folder}/{file[:-4]}[{str(audio_num).zfill(6)}].wav"
            logger.info(f'$$[split_audio_on_silence]save audio file... [{output_file}]')
            chunk.export(output_file, format="wav")
    runtime.stop()
    logger.info('//[split_audio_on_silence]clear! split audio_on silence')
    logger.info(f'//[split_audio_on_silence]runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({float(runtime.time())}s)')


def combine_audio(input_folder, output_folder, max_length):
    
    runtime = Stopwatch()
    runtime.start()
    logger.info(f'//[combine_audio]combine audio files into {max_length}ms')
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]
    f2 = AudioSegment.silent(0)
    for file, audio_num in zip(wav_files, range(0, len(wav_files))):
        f1 = AudioSegment.from_wav(f'{input_folder}/{file}')
        if len(f1) + len(f2) < max_length:
            logger.info(f'++[combine_audio]merge audio... [{file}] {round(len(f1)/1000, 2)}s')
            f2 += f1
        else:
            output_file = f"{output_folder}/{wav_files[wav_files.index(file)-1][:-4]}[{str(audio_num).zfill(6)}].wav"
            logger.info(f'$$[combine_audio]save audio file... [{output_file}] {round(len(f2)/1000, 2)}s')
            f2.export(output_file, format='wav')
            logger.info(f'++[combine_audio]merge audio... [{file}] {round(len(f1)/1000, 2)}s')
            f2 = f1
    runtime.stop()
    logger.info('//[combine_audio]clear! combine audio files')
    logger.info(f'//[combine_audio]runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({float(runtime.time())}s)')


def main():
    
    runtime = Stopwatch()
    logger.info('//[main]run process')
    runtime.start()

    #변수를 지정합니다.
    input_folder = "process/input/silent"
    max_length_folder = "process/temporary/max_length/silent"
    combine_folder = "process/temporary/combine/silent"
    output_folder = "process/output/silent"
    max_duration = 15000#ms
    min_slient_duration = 1000#ms
    silence_thresh = -40#dB

    logger.info(f'//[main]process info&&input_folder: {input_folder}&&output_folder: {output_folder}&&targt_duration(max): {round(max_duration/1000, 2)}s&&min_slient_duration: {round(min_slient_duration/1000, 2)}s&&silence_thresh: {silence_thresh}dB')

    if os.path.isdir(output_folder):
        rmtree(output_folder)
    os.makedirs(input_folder, exist_ok=True)
    if len([f for f in os.listdir(input_folder) if f.endswith('.wav')]) > 0:
        for folder in [max_length_folder, combine_folder, output_folder]:
            logger.info(f'//[main]make temporary directory... [{folder}]')
            os.makedirs(folder, exist_ok=True)
        split_audio_on_silence(input_folder, max_length_folder, min_slient_duration, silence_thresh)
        split_wav_files(max_length_folder, combine_folder, max_duration)
        combine_audio(combine_folder, output_folder, max_duration)
        for folder in [max_length_folder, combine_folder]:
            logger.info(f'//[main]reomve temporary directory... [{folder}]')
            rmtree(folder)
        total_audio_file_length(output_folder, max_duration)
        runtime.stop()
        logger.info('//[main]clear ALL processed files')
        logger.info(f'//[main]runtime => {round(runtime.time())//3600}h{round(runtime.time())%3600//60}m{round(runtime.time())%3600%60}s({float(runtime.time())}s)')
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
