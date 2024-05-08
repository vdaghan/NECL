# NECL - Not Everyone Can Listen!
 Some of us have a hard time just listening. Especially to podcasts.

 This program generates transcriptions for podcasts and plays them together.

# Dependencies and How to Use
 This program depends on ffmpeg. You can simply copy a working ffmpeg.exe executable into root folder.
 Another manual process is to download a vosk model (https://alphacephei.com/vosk/models) into model subfolder.
 Last piece of the puzzle is python modules: pygame (for playback), feedparser (RSS parser), speech_recognition & vosk (for speech-to-text)
 After dependencies are met, just run GUI.py and click the buttons.

# Caveat
 Officially, only Windows 10 (or whatever I am using at that moment) is supported. Yet I am open for contributions for other operating systems. Note that I won't be checking (except superficial, quick glances) contributions myself.
 This program currently looks up the latest CppCast podcast, downloads (as mp3), converts (to wav), decodes (as json) and plays it together with transcriptions.

# TODO
 * Ability to choose vosk model.
 * Accept any podcast link in mp3 format.
 * Generalise to other formats.
 * List and choose a podcast from CppCast RSS link.
 * Choose RSS file.
