#!/usr/bin/env python3
"""Listen again to the clips of a group: decode each clip and transcribe it, to check nothing was cut off.
  python3 tools/check-clips.py <group> --model <whisper dir>
"""
import argparse, base64, difflib, json, os, re, subprocess, tempfile
import numpy as np, sherpa_onnx

ap = argparse.ArgumentParser(); ap.add_argument('group'); ap.add_argument('--model', required=True)
ap.add_argument('--app', default=os.path.join(os.path.dirname(__file__), '..', 'app', 'www'))
a = ap.parse_args()
m = a.model.rstrip('/'); base = os.path.basename(m).replace('sherpa-onnx-whisper-', '')
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{m}/{base}-encoder.int8.onnx', decoder=f'{m}/{base}-decoder.int8.onnx', tokens=f'{m}/{base}-tokens.txt', language='ar', task='transcribe')
H = re.compile('[ً-ْٰـ]')
norm = lambda t: re.sub(r'[^ء-ي]', '', re.sub('[إأآ]', 'ا', H.sub('', t)).replace('ى', 'ي').replace('ة', 'ه'))
clips = json.load(open(os.path.join(a.app, 'clips', a.group + '.json'), encoding='utf-8'))
tmp = tempfile.mkdtemp()
for k, b64 in clips.items():
    p = os.path.join(tmp, 'c.mp3'); open(p, 'wb').write(base64.b64decode(b64))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    st = rec.create_stream(); st.accept_waveform(16000, x); rec.decode_stream(st)
    r = difflib.SequenceMatcher(None, norm(st.result.text), norm(k)).ratio()
    print(f'{r:.2f}  {len(x) / 16000:4.1f}s  {k}  ⇐  {st.result.text.strip()}')
