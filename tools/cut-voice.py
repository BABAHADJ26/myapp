#!/usr/bin/env python3
"""Cut a long voice recording into one clip per script line, and add the clips to the app.

  python3 tools/cut-voice.py <recording.wav> <script.txt> <group> --model <whisper dir> [--write]

1. ffmpeg silencedetect (-38 dB, 0.25 s) splits the recording into segments.
2. Whisper small (sherpa-onnx, Arabic) transcribes each segment.
3. A monotonic alignment (dynamic programming) matches lines to runs of 1–5 segments,
   allowing extra segments (words the voice tool adds) to be skipped.
4. Each line is cut with 0.12 s before and 0.35 s after (never into its neighbour), faded,
   encoded as mono mp3 24 kHz 64 kb/s, and stored base64 in app/www/clips/<group>.json;
   CLIP_FILE in app/www/index.html gets the new keys (clipKey = text without spaces and . ، , ؟ ? : ! [ ]).
Without --write it only prints the report (line, score, what was heard) so it can be checked first.
Script lines are the lines that start with two digits and two spaces ("01  text").
"""
import argparse, base64, difflib, json, os, re, subprocess, sys, tempfile, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('wav'); ap.add_argument('script'); ap.add_argument('group')
ap.add_argument('--model', required=True)
ap.add_argument('--write', action='store_true')
ap.add_argument('--force', default='', help='comma-separated line numbers to keep even with a low score (checked by ear)')
ap.add_argument('--noise', default='-38dB'); ap.add_argument('--gap', type=float, default=0.25)
ap.add_argument('--app', default=os.path.join(os.path.dirname(__file__), '..', 'app', 'www'))
a = ap.parse_args()

lines = []
for l in open(a.script, encoding='utf-8'):
    m = re.match(r'(\d\d)  (.+)', l.rstrip())
    if m: lines.append((m.group(1), m.group(2).strip()))

HARAKAT = re.compile('[ً-ْٰـ]')
def norm(t):
    t = HARAKAT.sub('', t)
    t = re.sub('[إأآٱ]', 'ا', t).replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    return re.sub(r'[^ء-ي]', '', t)
def clip_key(t): return re.sub(r'[\s!.،,؟?:\[\]]', '', t)

# 1) segments between silences
tmp = tempfile.mkdtemp()
pcm = os.path.join(tmp, 'a16.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.wav, '-ac', '1', '-ar', '16000', pcm], check=True)
# some generated WAV files have headers that make ffmpeg seek to the wrong place: cut from a clean copy
clean = os.path.join(tmp, 'clean.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.wav, '-ac', '1', '-ar', '24000', '-c:a', 'pcm_s16le', clean], check=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.wav], capture_output=True, text=True).stdout)
log = subprocess.run(['ffmpeg', '-i', a.wav, '-af', f'silencedetect=noise={a.noise}:d={a.gap}', '-f', 'null', '-'], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
segs, t = [], 0.0
for s0, e0 in zip(starts, ends + [dur] * (len(starts) - len(ends))):
    if s0 - t > 0.08: segs.append((t, s0))
    t = e0
if dur - t > 0.08: segs.append((t, dur))

# 2) what each segment says
import sherpa_onnx
m = a.model.rstrip('/')
base = os.path.basename(m).replace('sherpa-onnx-whisper-', '')
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f'{m}/{base}-encoder.int8.onnx', decoder=f'{m}/{base}-decoder.int8.onnx', tokens=f'{m}/{base}-tokens.txt', language='ar', task='transcribe', num_threads=4)
with wave.open(pcm) as w: audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
def hear(s0, e0):
    st = rec.create_stream(); st.accept_waveform(16000, audio[int(s0 * 16000):int(e0 * 16000)]); rec.decode_stream(st)
    return st.result.text.strip()
heard = [hear(s0, e0) for s0, e0 in segs]

# 3) align lines to runs of segments
def score(i, j, k):
    h = norm(' '.join(heard[j:k])); r = norm(lines[i][1])
    return difflib.SequenceMatcher(None, h, r).ratio() if h and r else 0.0
N, M, SKIP, LSKIP = len(lines), len(segs), 0.12, 0.3
INF = -1e9
best = np.full((N + 1, M + 1), INF); back = {}
best[0][0] = 0
for j in range(1, M + 1): best[0][j] = best[0][j - 1] - SKIP; back[(0, j)] = ('skip', 0, j - 1)
for i in range(1, N + 1):
    best[i][0] = best[i - 1][0] - LSKIP; back[(i, 0)] = ('miss', i - 1, 0)
    for j in range(1, M + 1):
        c = best[i][j - 1] - SKIP; bk = ('skip', i, j - 1)
        if best[i - 1][j] - LSKIP > c: c, bk = best[i - 1][j] - LSKIP, ('miss', i - 1, j)
        for n in range(1, 6):
            if j - n < 0: break
            v = best[i - 1][j - n] + score(i - 1, j - n, j)
            if v > c: c, bk = v, ('line', i - 1, j - n)
        best[i][j] = c; back[(i, j)] = bk
match = {}
i, j = N, M
while i > 0:
    kind, pi, pj = back[(i, j)]
    if kind == 'line': match[pi] = (pj, j)
    i, j = pi, pj

# 4) report, and cut
print(f'{a.wav}: {dur:.1f} s, {M} segments, {N} lines')
out, newkeys, weak = {}, {}, []
for i, (num, text) in enumerate(lines):
    if i not in match: print(f'  {num}  MISSING  {text}'); weak.append(num); continue
    j, k = match[i]; sc = score(i, j, k)
    if sc < 0.45 and num not in a.force.split(','): print(f'  {num}  MISSING  {text}  (best guess: {" | ".join(heard[j:k])})'); weak.append(num); continue
    flag = 'ok ' if sc >= 0.6 else 'LOW'
    if sc < 0.6: weak.append(num)
    print(f'  {num}  {flag} {sc:.2f}  {segs[j][0]:6.2f}-{segs[k - 1][1]:6.2f}  {text}  ⇐  {" | ".join(heard[j:k])}')
    if not a.write: continue
    prev_end = segs[j - 1][1] if j > 0 else 0.0
    next_start = segs[k][0] if k < M else dur
    s0 = max(segs[j][0] - 0.12, (prev_end + segs[j][0]) / 2 if j > 0 else 0.0)
    e0 = min(segs[k - 1][1] + 0.35, (segs[k - 1][1] + next_start) / 2 if k < M else dur)
    mp3 = os.path.join(tmp, f'{num}.mp3')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', clean, '-af', f'atrim=start={s0:.3f}:end={e0:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={max(0, e0 - s0 - 0.08):.3f}:d=0.08', '-ac', '1', '-ar', '24000', '-b:a', '64k', mp3], check=True)
    key = clip_key(text)
    out[key] = base64.b64encode(open(mp3, 'rb').read()).decode()
    newkeys[key] = a.group
print('weak or missing:', weak or 'none')

if a.write:
    path = os.path.join(a.app, 'clips', a.group + '.json')
    old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    old.update(out)
    json.dump(old, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    idx = os.path.join(a.app, 'index.html')
    s = open(idx, encoding='utf-8').read()
    mm = re.search(r'const CLIP_FILE = (\{.*?\});', s, re.S)
    cf = json.loads(mm.group(1)); cf.update(newkeys)
    s = s[:mm.start(1)] + json.dumps(cf, ensure_ascii=False) + s[mm.end(1):]
    open(idx, 'w', encoding='utf-8').write(s)
    print(f'wrote {len(out)} clips to {path}')
