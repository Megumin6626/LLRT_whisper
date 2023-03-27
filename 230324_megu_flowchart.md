1. Start
|
2. List available microphones and prompt user to choose one
|
3. Choose threshold (use previous, measure new, or enter custom value)
|
4. Choose language for transcription
|
5. Define global variables: SLIENCE_TIME, SLIENCE_CUT_OUT_TIME, WHISPER_MODEL, AUDIO_FILE_EXTENSION
|
6. Initialize audio_queue and start two threads:
   |
   6.1. Thread 1: record_audio()
   |     |
   |     6.1.1. Continuously record audio from microphone
   |     |
   |     6.1.2. If audio level exceeds threshold, start recording
   |     |
   |     6.1.3. If audio level falls below threshold for a duration calculated using SLIENCE_TIME and SLIENCE_CUT_OUT_TIME, stop recording
   |     |
   |     6.1.4. Save recorded audio as a file with the format specified by AUDIO_FILE_EXTENSION and add it to audio_queue
   |
   6.2. Thread 2: process_audio_queue()
         |
         6.2.1. Load Whisper model specified by WHISPER_MODEL
         |
         6.2.2. Continuously process audio files in audio_queue
               |
               6.2.2.1. Transcribe audio using chosen language
               |
               6.2.2.2. Print transcribed text to console
               |
               6.2.2.3. Remove processed audio file
|
7. Wait for both threads to finish (This should run indefinitely until interrupted)
|
8. End
