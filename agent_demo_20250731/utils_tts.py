# utils_tts.py
# 同济子豪兄 2024-5-23
# 语音合成

print('导入语音合成模块')

import os
import appbuilder
from API_KEY import *
import pyaudio
import wave
import sounddevice as sd
import numpy as np

tts_ab = appbuilder.TTS()

def tts(TEXT='我是小川川的机器人', tts_wav_path = 'temp/tts.wav'):
    '''
    语音合成TTS，生成wav音频文件
    '''
    inp = appbuilder.Message(content={"text": TEXT})
    out = tts_ab.run(inp, model="paddlespeech-tts", audio_type="wav")
    # out = tts_ab.run(inp, audio_type="wav")
    with open(tts_wav_path, "wb") as f:
        f.write(out.content["audio_binary"])
    # print("TTS语音合成，导出wav音频文件至：{}".format(tts_wav_path))

def play_wav_linux(wav_file='asset/welcome.wav'):
    '''
    播放wav音频文件
    '''
    prompt = 'aplay -t wav {} -q'.format(wav_file)
    os.system(prompt)

def play_wav(wav_file='asset/welcome.wav'):
    #在 Windows 上播放 wav 文件
    
    # 打开 wav 文件
    wf = wave.open(wav_file, 'rb')
    
    # 读取音频数据
    frames = wf.readframes(wf.getnframes())
    
    # 将数据转为 NumPy 数组
    audio_data = np.frombuffer(frames, dtype=np.int16)
    
    # 播放音频数据
    sd.play(audio_data, wf.getframerate())
    
    # 等待音频播放完成
    sd.wait()




# def play_wav(wav_file='temp/tts.wav'):
#     '''
#     播放wav文件
#     '''
#     wf = wave.open(wav_file, 'rb')
 
#     # 实例化PyAudio
#     p = pyaudio.PyAudio()
 
#     # 打开流
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)

#     chunk_size = 1024
#     # 读取数据
#     data = wf.readframes(chunk_size)
 
#     # 播放音频
#     while data != b'':
#         stream.write(data)
#         data = wf.readframes(chunk_size)
 
#     # 停止流，关闭流和PyAudio
#     stream.stop_stream()
#     stream.close()
#     p.terminate()