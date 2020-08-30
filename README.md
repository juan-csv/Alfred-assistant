# Alfred
Alfred is an assistant in which you can program any type of action in the python language, then associate it with a command given by voice and he will be in charge of executing it.

Alfred uses the Google Cloud Platform (GCO) speech-to-text api so in order to run Alfred you must obtain a GCP key, luckily this key is generated for free. I leave you this [link](https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=es-419) to create your own key and you can use Alfred !!.


# How to run:
The code is tested in python 3.7.8 and macOS Catalina
<pre><code>python Main.py </code></pre>

[See demo](https://www.youtube.com/watch?v=TCDEL5ZpAsY)

[![Watch the video](https://img.youtube.com/vi/TCDEL5ZpAsY/hqdefault.jpg)](https://youtu.be/TCDEL5ZpAsY)


Alfred supports a lot of languages, you can experiment with different languages by changing the settings in the config.py file.

[See demo for Spanish](https://www.youtube.com/watch?v=IdJVE5_8UNo)

[![Watch the video](https://img.youtube.com/vi/IdJVE5_8UNo/hqdefault.jpg)](https://youtu.be/IdJVE5_8UNo)

# Future work
- Add support for [SpeechRecognition](https://github.com/Uberi/speech_recognition#readme) and [pocketsphinx](https://github.com/cmusphinx/pocketsphinx) library for real-time speech recognition module.
- Add wake-word or hot word functionality, for Alfred's call, using [snowboy](https://github.com/Kitt-AI/snowboy)
- Add intent detector

# References
- **Face Recognition:** https://github.com/juan-csv/face-recognition


