```
  ________
 (_]----[_)
.~ |.''.|
~. |'..'|
 `~`----` ldb
 ```

# Afterthetone
python based old school answering machine.
Put an RPI in an old rotary phone
Connect it to the hook switch the headset speaker
Put a USB lav mic into the mouthpiece area of the headset


# Requirements:
- RPI 3
- mono USB microphone on pyaudio channel 1
- speaker (from RPI headphone jack) pyaudio on channel 0

# Use and customization
- sample.wav is played whenever the hanset is lifted (i.e. GPIO21 is pulled down by closing a switch between it and a GND pin)
- all recording stored in root directory with timestamp suffix as .wav files
- launcher.sh can be called on RPI boot. in order to do this, modify crontab using `sudo crontab -e` and adding the line `@reboot sh /home/pi/Desktop/afterthetone/launcher.sh`
- depending on the USB microphone hardware, the sample rate may have to be modified. Some are 48000, some are 44100, check the spec of your mic. Some mic's may have 2 channels rather than one, and this will require the parameter to be modified in `main.py`
- the launcher is set up to pipe all stdout to a logfile, this can be modified in `launcher.sh`

# Hardware notes when using an old phone
- you are going to have to be confortable with wires and soldering to get this to work!
- the earpiece speaker in an old phone works just fine in testing with the RPI headphone output. Connect one terminal of the speaker to whichever of the audio channels (L or R) that you prefer, and the other to RPI ground. This can be done by soldering to the testpads on the bottom of the Pi board:

```
PP4 GND
PP5 GND
PP6 GND
PP25 L Audio
PP26 R Audio
```

