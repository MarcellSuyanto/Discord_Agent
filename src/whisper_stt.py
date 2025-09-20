from tempfile import NamedTemporaryFile
from faster_whisper import WhisperModel
import speech_recognition as sr
import os
import asyncio


MIC_INDEX = int(os.getenv("MIC_INDEX", "2"))  # -1 = default device

r = sr.Recognizer()
r.dynamic_energy_threshold = True      # let it adapt
r.pause_threshold = 0.6                # silence length to end phrase
r.non_speaking_duration = 0.2          # shorter trailing silence
model = WhisperModel("small", device="cpu", compute_type="int8")

wakeWords = ["Bobzilla"]
pauseFlag = False


async def pauseCheck(flag):
    """
    If True, puts the listener into a paused state so `wakeCheck` returns True immediately.
    This lets you stop the voice loop programmatically without speaking the wake/exit word.
    """
    global pauseFlag
    if flag:
        pauseFlag = True
    else:
        pauseFlag = False

async def wakeCheck(spokenList):
    """
    Returns True if the system is paused (pauseFlag) OR if any variant of 'bazinga'
    is present in the recognized words. Your loop uses this to decide when to exit.
    """
    if pauseFlag == True:
        return True
    for bazinga in wakeWords:
        if (bazinga in spokenList):
            return True
    return False

def transcribe_with_faster_whisper(audio_data: sr.AudioData) -> str:
    """
    Convert SpeechRecognition AudioData to a temp WAV file, then run local
    faster-whisper transcription and return the combined text.
    """
    wav_bytes = audio_data.get_wav_data()
    tmp_path = None
    try:
        with NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_bytes)
            tmp_path = f.name
            print(tmp_path)

        segments, info = model.transcribe(
            tmp_path,
            beam_size=1,
            vad_filter=True
        )
        text = " ".join(seg.text for seg in segments).strip()
        return text
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

async def startVoiceInput(ctx):
    spokenWords = []
    while not await wakeCheck(spokenWords):
        spokenWords.clear()
        await ctx.send("[DEBUG] Speech recognition activated!")

        mic_args = {"device_index": MIC_INDEX} if MIC_INDEX >= 0 else {}
        with sr.Microphone(**mic_args) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            await ctx.send(f"[DEBUG] Listening... (timeout 10s, phrase 8s) "
                           f"[energy_threshold={r.energy_threshold:.1f}]")
            try:
                audio = await asyncio.to_thread(
                    r.listen, source, timeout=10, phrase_time_limit=8
                )
            except sr.WaitTimeoutError:
                await ctx.send("[DEBUG] Timed out waiting for speech. Try again.")
                continue

        try:
            voiceInput: str = await asyncio.to_thread(transcribe_with_faster_whisper, audio)
            voiceInput = (voiceInput or "").strip()
            if not voiceInput:
                await ctx.send("[DEBUG] Got empty transcription.")
                continue

            await ctx.send(voiceInput)

        except Exception as e:
            await ctx.send(f"[DEBUG] Local Whisper error: {e}")

    await ctx.send("[DEBUG] Exiting speech recognition!")