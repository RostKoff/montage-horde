# Montage horde
An Autogen agent system embedded in a gradio interface that offers complex audio and video analysing, editing & processing. Runs code execution on a Docker container to ensure integrity of the environment.

## System summary
This is an agent system that collaborates in SelectorGroupChat and fulfills user's requests regarding video/audio analysis and processing. The system consists of following agents:
- SUPERVISOR: is the first to receive user's request. It's task is to oversee the workflow and distribute tasks to other agents;
- PLANNER: creates a workflow based on the user's request, splitting it into small, manageable step-by-step tasks;
- INFORMATION EXTRACTOR: extracts various information from audio/wideo, including transcription and sound;
- TRANSLATOR: uses DeepL API to translate transcriptions into specified language;
- SENTIMENT ANALYST: uses tabularisai to analyse the sentiment of the given transcription, regardless of the language provided;
- CODER: for more complex tasks like video editing, it creates code that will be executed by EXECUTOR;
- EXECUTOR: runs code provided by CODER to make desired edits;
- TEXT WRITER: analyses the transcription and writes summaries and answers to questions provided by the user regarding the audio/video;
- VALIDATOR: checks the output of other agents whether it fulfills user's request. If not, it sends retry instruction to SUPERVISOR;
- OUTPUT FORMATTER: provides ultimate summary of the processes done and prints them in results, then finishes the process.

## Installation & how to run
1. Download this project from "<> Code" button as a zip file.
2. Then, extract it in the folder of your choice.
3. After importing and extracting the zip project file, create .env file add your API keys: 
OPENAI_API_KEY=your_code
DEEPL_API_KEY=your_code
HF_AUTH_TOKEN=your_code
4. Make sure to have poetry and docker installed on your system (you can find instructions here: https://python-poetry.org/docs/ https://docs.docker.com/desktop/) and run *poetry install*.
6. Run gradio_interface.py in your project environment, then proceed to your browser with the link *http://127.0.0.1:7860*.
7. From there, you can upload audio and video files to process, and enter a prompt to orchestrate the task.
8. Wait until the app processes your request (it may take up a few minutes) - the interface will be replaced and result displayed in "results" field with attached output zip file. All files generated during request processing are kept there.

## Metrics

Transcription metrics in jiwet for three different Whisperx models can be found in evaluation package on transcription-metrics branch. 
