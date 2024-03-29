# refer: https://pythonaudiosynthesisbasics.com/

import numpy as np
import sounddevice as sd
from scipy import signal

sample_rate = 44100
duration = 120.0
frequency = 400.0

x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
# 正弦
sinewave_data = np.sin(frequency * x)
# 方波
#sinewave_data = signal.square(frequency * x)

# best to attenuate it before playing, they can get very loud
sinewave_data = sinewave_data * 1.0

import scipy.io.wavfile as wf

# 写到文件
#write_data = np.int16(sinewave_data * 32767)
#wf.write('sinewave.wav', sample_rate, write_data)

# 或者直接播放
while True:
    sd.play(sinewave_data, sample_rate)
    sd.wait()
