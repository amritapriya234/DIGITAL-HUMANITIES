import os
import json
import whisper

def run_transcription(audio_path: str, output_json_path: str, model_size: str = "medium"):
    """
    Transcribes raw audio using local OpenAI Whisper model and exports timestamped JSON.
    """
    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)
    
    print(f"Processing audio: {audio_path}")
    result = model.transcribe(audio_path, verbose=False)
    
    # Structure segments with timestamps
    transcript_data = {
        "text": result["text"],
        "segments": []
    }
    
    for segment in result["segments"]:
        transcript_data["segments"].append({
            "id": segment["id"],
            "start": round(segment["start"], 2),
            "end": round(segment["end"], 2),
            "text": segment["text"].strip()
        })
        
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
        
    print(f"Transcription saved to: {output_json_path}")

if __name__ == "__main__":
    AUDIO_FILE = "data/raw_audio/interview_101.wav"
    JSON_OUTPUT = "data/output/interview_101.json"
    
    if os.path.exists(AUDIO_FILE):
        run_transcription(AUDIO_FILE, JSON_OUTPUT)
    else:
        print(f"Please place your audio file at {AUDIO_FILE} first.")