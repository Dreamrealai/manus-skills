#!/usr/bin/env python3
"""Gemini Text-to-Speech (TTS) Generation Script.

Generates audio from text using Gemini 2.5 TTS models.
Supports single-speaker and multi-speaker modes.

Usage:
    python tts_generation.py --text "Hello world!" --output hello.wav
    python tts_generation.py --text "Speaker1: Hi! Speaker2: Hello!" --multi --voices Speaker1=Kore Speaker2=Puck --output dialogue.wav
"""
import argparse
import json
import sys
import wave

from google import genai
from google.genai import types


DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
AVAILABLE_VOICES = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir",
    "Leda", "Orus", "Aoede", "Callirrhoe", "Autonoe",
    "Enceladus", "Iapetus", "Umbriel", "Algieba", "Despina",
    "Erinome", "Gacrux", "Laomedeia", "Pulcherrima", "Sadachbia",
    "Sadaltager", "Schedar", "Sulafat", "Vindemiatrix", "Zubenelgenubi",
]


def save_wav(filename: str, pcm_data: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)


def generate_single_speaker(
    client: genai.Client,
    text: str,
    model: str,
    voice: str,
    output_path: str,
) -> dict:
    """Generate single-speaker TTS audio."""
    response = client.models.generate_content(
        model=model,
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice,
                    )
                )
            ),
        ),
    )

    audio_data = response.candidates[0].content.parts[0].inline_data.data
    save_wav(output_path, audio_data)
    return {
        "model": model,
        "mode": "single-speaker",
        "voice": voice,
        "output": output_path,
        "size_bytes": len(audio_data),
    }


def generate_multi_speaker(
    client: genai.Client,
    text: str,
    model: str,
    voice_map: dict[str, str],
    output_path: str,
) -> dict:
    """Generate multi-speaker TTS audio."""
    speaker_configs = []
    for speaker_name, voice_name in voice_map.items():
        speaker_configs.append(
            types.SpeakerVoiceConfig(
                speaker=speaker_name,
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                ),
            )
        )

    response = client.models.generate_content(
        model=model,
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=speaker_configs,
                )
            ),
        ),
    )

    audio_data = response.candidates[0].content.parts[0].inline_data.data
    save_wav(output_path, audio_data)
    return {
        "model": model,
        "mode": "multi-speaker",
        "voices": voice_map,
        "output": output_path,
        "size_bytes": len(audio_data),
    }


def parse_voice_map(voice_args: list[str]) -> dict[str, str]:
    """Parse voice arguments like 'Speaker1=Kore Speaker2=Puck' into a dict."""
    voice_map = {}
    for v in voice_args:
        parts = v.split("=", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid voice format: {v}. Expected 'SpeakerName=VoiceName'")
        voice_map[parts[0]] = parts[1]
    return voice_map


def main():
    parser = argparse.ArgumentParser(description="Gemini TTS Generation")
    parser.add_argument("--text", required=True, help="Text to convert to speech")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"TTS model (default: {DEFAULT_MODEL})")
    parser.add_argument("--voice", default="Kore", help="Voice name for single-speaker mode")
    parser.add_argument("--multi", action="store_true", help="Enable multi-speaker mode")
    parser.add_argument("--voices", nargs="*", help="Voice mappings for multi-speaker: Speaker1=Kore Speaker2=Puck")
    parser.add_argument("--output", default="tts_output.wav", help="Output WAV file path")
    args = parser.parse_args()

    client = genai.Client()

    if args.multi:
        if not args.voices:
            parser.error("--voices required for multi-speaker mode")
        voice_map = parse_voice_map(args.voices)
        result = generate_multi_speaker(client, args.text, args.model, voice_map, args.output)
    else:
        result = generate_single_speaker(client, args.text, args.model, args.voice, args.output)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
