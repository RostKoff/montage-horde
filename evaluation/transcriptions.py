from datasets import load_dataset
import whisperx
import torch
import jiwer

def transform_segments(segments):
    text = [segment['text'] for segment in segments]
    text = ' '.join(text)
    text = text.strip()
    text = text.lower()
    return text

def measure_models(whisper_models, dataset_stream, compute_type, data_count=10, language=None):
    results = {}
    
    iterator = iter(dataset_stream)
    
    print('loading samples from dataset')
    samples = [next(iterator) for _ in range(data_count)]
    
    for model_name, whisper_model in whisper_models.items():
        reference = []
        hypothesis = []
        
        for i, data in enumerate(samples):
            audio = data['audio']['array'].astype(compute_type)
            
            print(f'[{model_name}] transcription data sample {i+1}\n{data["text"]}')
            
            transcript = whisper_model.transcribe(audio)
            hypothesis.append(transform_segments(transcript['segments']))
            reference.append(data['text'].lower().strip())
        
        metrics = {
            'wer': jiwer.wer(reference, hypothesis),
            'mer': jiwer.mer(reference, hypothesis),
            'wip': jiwer.wip(reference, hypothesis),
            'wil': jiwer.wil(reference, hypothesis),
        }
        
        print(f'[{model_name}] metrics evaluation completed')    
        
        results[model_name] = metrics
    
    return results

device = torch.device("gpu" if torch.cuda.is_available() else "cpu")
compute_type = 'float32'

print('loading dataset')
dataset = load_dataset('openslr/librispeech_asr', name='other', split='train.500', streaming=True)

print('loading models')
models = {
    'whisper_small': whisperx.load_model('small', device.type, compute_type=compute_type),
    'whisper_medium': whisperx.load_model('medium', device.type, compute_type=compute_type),
    'whisper_tiny': whisperx.load_model('tiny', device.type, compute_type=compute_type),
}

measure_models(models, dataset, compute_type=compute_type, language='en')