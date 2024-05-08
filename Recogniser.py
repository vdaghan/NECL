import json
import speech_recognition
import vosk
import pathlib

def recognise(filenames):
    r = speech_recognition.Recognizer()
    voskModel = vosk.Model(model_path = "model")
    recogniser = vosk.KaldiRecognizer(voskModel, 16000)
    recogniser.SetWords(True)

    if not pathlib.Path(filenames['json']).exists():
        with speech_recognition.AudioFile(filenames['wav']) as source:
            audio = r.record(source)

        recogniser.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
        finalRecognition = recogniser.FinalResult()

        jLoad = json.loads(finalRecognition)
        with open(filenames['json'], 'w', encoding='utf-8') as f:
            json.dumps(jLoad, f, ensure_ascii=False, indent=4)

    with open(filenames['json'], 'r', encoding='utf-8') as json_file:
        jLoad = json.load(json_file)
    return jLoad
