import speech_recognition as sr 
import pyaudio
import wave

def txt_w(nuevo_audio):
        try:
            with open('historial\\historial.txt','a',newline='',encoding = 'utf-8') as file:
                file.write(nuevo_audio+"\n")
        except Exception as exc0:
            print(str(exc0) + "\n No se puede leer el archivo .txt")

def record_wav ():
    try:
        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        return True
    except Exception as exc0:
        print(str(exc0))
        print('No se pudo guardar el archivo')
        return False

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 8
nombre=str(input("Ingresa el nombre del archivo\n-->"))
filename ="audios\\"+nombre+".wav"
print(filename)
p = pyaudio.PyAudio()  # Create an interface to PortAudio

recon=record_wav()

if(recon):
    r= sr.Recognizer()
    wav_audio=sr.AudioFile(filename)

    with wav_audio as source:
        print("Procesando el archivo de audio")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text=r.recognize_google(audio, language='es-ES')
            print('Has dicho: {}'.format(text))
            txt_w("Archivo de audio: "+filename+"\nHas dicho : {}".format(text))
        except Exception as exc1:
            print(str(exc1))
            print('Disculpa no se puede escuchar bien')