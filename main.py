import pyaudio
import wave
from datetime import datetime
from pynput.keyboard import Key, Listener

class AnsweringMachine():


  def __init__(self):
    pass

  def prepare_file(self, fname, mode='wb'):
    wavefile = wave.open(f'{fname}.wav', mode)
    wavefile.setnchannels(self.channels)
    wavefile.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
    wavefile.setframerate(self.fs)
    return wavefile

  def callback(self, in_data, frame_count, time_info, status):
    data = self.wf.writeframes(in_data)
    return (data, pyaudio.paContinue)

  def start_recording(self):
    if self.currently_recording:
      return 0
    self.currently_recording = True

    print('recording...')
    file_ts = datetime.now().strftime("%Y-%M-%dT%Hh%Ms%S")
    self.wf = self.prepare_file(f'recording {file_ts}')

    self.stream = self.p.open(format=self.sample_format, 
                    channels=1,
                    rate=self.fs,
                    frames_per_buffer=self.chunk,
                    stream_callback=self.callback,
                    input_device_index = 0,
                    input=True)

    self.stream.start_stream()

  def stop_recording(self):
    self.stream.stop_stream()
    self.stream.close()
    self.wf.close()

    currently_recording = False
    print("recording stopped")

  def toggle_recording(self):
    if self.currently_recording:
      self.stop_recording()
      self.currently_recording = False
    else:
      self.play_file('sample.wav') # play intro
      self.start_recording() # record
      self.currently_recording = True

  def on_press(self, key):
    print('{0} pressed'.format(key))


  def on_release(self, key):
    print('{0} release'.format(key))
    if key == Key.esc:
      return False
    if key.char == ('r'):
      self.toggle_recording()

  def start(self):
    print("Press and hold <r> to record audio. ESC to quit")
    self.currently_recording = False
    self.sample_rate = 44100
    self.chunk = 1024  # Record in chunks of 1024 samples
    self.sample_format = pyaudio.paInt16  # 16 bits per sample
    self.channels = 1
    self.fs = 44100  # Record at 44100 samples per second
    self.wf = None # recording file ref
    self.p = pyaudio.PyAudio()  # Create an interface to PortAudio

    for i in range(self.p.get_device_count()):
      dev = self.p.get_device_info_by_index(i)
      print((i,dev['name'],dev['maxInputChannels']))


    # Collect events until released
    with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        listener.join()

  def play_file(self, file):
    print(f'playing {file}')
    # Set chunk size of 1024 samples per data frame
    chunk = 1024  

    # Open the sound file 
    wf = wave.open(file, 'rb')

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while data:
      stream.write(data)
      data = wf.readframes(chunk)

    # Close and terminate the stream
    stream.close()
    print('playback complete')

if __name__ == "__main__":
  a = AnsweringMachine()
  a.start()



