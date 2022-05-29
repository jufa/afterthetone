import pyaudio
import wave
from datetime import datetime
import RPi.GPIO as GPIO
import time
import random

class AnsweringMachine():


  def __init__(self):
    self.state = 'ready'
    self.debounce_period = 0.2 #sec
    self.heartbeat_period = 60 / self.debounce_period
    self.heartbeat_countdown = 0
    self.hook_pin = 21

  def heartbeat(self):
    self.heartbeat_countdown -= 1
    if self.heartbeat_countdown <= 0:
      self.log('HEARTBEAT')
      self.heartbeat_countdown = self.heartbeat_period


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
    if self.state == 'recording':
      return 0
    self.state == 'recording'

    self.log('recording...')
    try:
      file_ts = datetime.now().strftime("%Y-%m-%dT%Hh%Ms%S")
    except:
      file_ts = random.randint(10_000_000, 99_999_999)
      
    self.wf = self.prepare_file(f'recording {file_ts}')

    self.stream = self.p.open(format=self.sample_format, 
                    channels=1,
                    rate=self.fs,
                    frames_per_buffer=self.chunk,
                    stream_callback=self.callback,
                    input_device_index = 1,
                    input=True)

    self.stream.start_stream()

  def stop_recording(self):
    self.stream.stop_stream()
    self.stream.close()
    self.wf.close()

    self.state == 'ready'
    self.log("recording stopped")

  # def toggle_recording(self):
  #   if self.currently_recording:
  #     self.stop_recording()
  #     self.currently_recording = False
  #   else:
  #     self.play_file('sample.wav') # play intro
  #     self.start_recording() # record
  #     self.currently_recording = True

  def handle_on_the_hook(self):
    if self.state == 'recording':
      self.stop_recording()
    elif self.state == 'playback':
      self.stop_playback()
    else:
      self.state = 'ready'

  def handle_off_the_hook(self):
    if self.state == 'ready':
      self.play_file('sample.wav') # play intro
      self.start_recording() # record


  def on_press(self, key):
    self.log('{0} pressed'.format(key))


  def on_release(self, key):
    self.log('{0} release'.format(key))
    if key == Key.esc:
      return False
    if key.char == ('r'):
      self.toggle_recording()

  def start(self):
    self.log('AfterTone Starting up...')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.hook_pin, GPIO.IN, GPIO.PUD_UP)

    print("Press <r> to record audio. ESC to quit")
    self.currently_recording = False
    self.sample_rate = 48000
    self.chunk = 1024  # Record in chunks of 1024 samples
    self.sample_format = pyaudio.paInt16  # 16 bits per sample
    self.channels = 1
    self.fs = 48000  # Record at 44100 samples per second
    self.wf = None # recording file ref
    self.p = pyaudio.PyAudio()  # Create an interface to PortAudio

    for i in range(self.p.get_device_count()):
      dev = self.p.get_device_info_by_index(i)
      print((i,dev['name'],dev['maxInputChannels']))


    # Collect events until released
    # with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
    #     listener.join()

    prev_hook_state = GPIO.input(self.hook_pin)
    on_the_hook = 1

    self.log('setup complete...')
    self.log('starting monitoring loop...')
    while True:
      self.heartbeat()
      hook_state = GPIO.input(self.hook_pin)
      if hook_state != prev_hook_state:
        print(f'hook state change: on the hook? {hook_state == on_the_hook}')
        if hook_state == on_the_hook:
          self.handle_on_the_hook()
        else:
          self.handle_off_the_hook()
        prev_hook_state = hook_state
      time.sleep(0.2)
      
  

  def stop_playback(self):
    self.stream.stop_stream()
    self.stream.close()
    self.wf.close()
    self.state = 'ready'
    print("playback stopped")


  def play_file(self, file):
    print(f'playing {file}')
    self.state = 'playback'
    # Set chunk size of 1024 samples per data frame
    chunk = 1024  

    # Open the sound file 
    wf = wave.open(file, 'rb')

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    self.stream = self.p.open(format = self.p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while data and self.state == 'playback': # need threads to make this work!
      self.stream.write(data)
      data = wf.readframes(chunk)


    # Close and terminate the stream
    self.stream.close()
    self.log('playback complete')


  def log(self, msg):
    prefix = datetime.now().strftime("%Y-%m-%dT%Hh%Ms%S")
    print(f'{prefix}\t\t{msg}')

if __name__ == "__main__":
  a = AnsweringMachine()
  a.start()





