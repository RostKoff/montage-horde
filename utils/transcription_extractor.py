import whisperx
from torch._prims_common import DeviceLikeType
from typing import Literal, Annotated

LanguageCode = Literal[
    "en","fr","de","es","it","ja","zh","nl","uk","pt","ar","cs","ru","pl","hu","fi","fa","el","tr","da","he","vi","ko","ur","te","hi","ca","ml","no","nn","sk","sl","hr","ro","eu","gl","ka"
]
LANGUAGE_CODE_ANNOTATION = 'Language of the input file in ISO 639-1 format'

class TranscriptionExtractor():
    def __init__(
        self, 
        whisper_arch: str, 
        device: DeviceLikeType,
        hf_auth_token: str,
        compute_type: str ='int8', 
        batch_size: int =4,
        align_model_name: str =None,
        diarize_model_name: str ="pyannote/speaker-diarization-3.1"
        ):
        self.whisper_model = whisperx.load_model(
            whisper_arch, 
            device, 
            compute_type=compute_type
        )
        self.diarize_model = whisperx.DiarizationPipeline(
            diarize_model_name, 
            use_auth_token=hf_auth_token, 
            device=device
        )
        self.align_model_name = align_model_name
        self.batch_size = batch_size
        self.device = device

    def get_transcription(
        self,
        input_file: str, 
        language_code: Annotated[LanguageCode, LANGUAGE_CODE_ANNOTATION] | None = None,
        with_word_timestamps: bool = False,
        with_speaker_diarization: bool = False,
        num_speakers: Annotated[int, "Specify the exact number of speakers if speaker diarization is used"] | None = None,
        max_speakers: Annotated[int, "Specify the minimal number of speakers if speaker diarization is used"] | None = None,
        min_speakers: Annotated[int, "Specify the maximal number of speakers if speaker diarization is used"]| None = None) -> str:
        audio = whisperx.load_audio(input_file)
        
        transcription = self.whisper_model.transcribe(audio, self.batch_size, language=language_code)
        
        if with_word_timestamps:
            align_model, metadata = whisperx.load_align_model(transcription["language"], self.device, self.align_model_name)
            transcription = whisperx.align(transcription['segments'], align_model, metadata, audio, self.device)
            
        if with_speaker_diarization:
            diarize_segments = self.diarize_model(audio, num_speakers, min_speakers, max_speakers)
            transcription = whisperx.assign_word_speakers(diarize_segments, transcription)
        
        result = transcription['segments']
        if 'word_segments' in transcription:
            result = transcription["word_segments"]
        
        # Format output
        output = []
        keys_to_include = ['text', 'word', 'start', 'end', 'speaker']
        for item in result:
            line = []
            for (k, v) in item.items():
                if k in keys_to_include:
                    line.append(f"'{k}': {v}")
            output.append(' '.join(line))
        
        return '\n'.join(output)