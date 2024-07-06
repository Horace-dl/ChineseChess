import pyaudio
import wave

wave_file = wave.open('audio.wav', rb)

audio = pyaudio.PyAudio()

stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()), channels = wave_file.getchannels(),
                    rate = wave_file.getframerate(), output=True)

data = wave_file.readframes(1024)
while data:
    stream.write(data)
    data = wave_file.readframes(1024)

stream.stop_stream()
stream.close()

audio.terminate()