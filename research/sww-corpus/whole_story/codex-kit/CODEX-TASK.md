# Coding task (one season, one coder)

You are one independent coder on a reading-and-coding task. Your task message names a
**season number** and a **coder label**. Another coder works on the same season separately; you
must not see each other's work.

## Rules

- Use only the files in this repository: `CODEX-TASK.md` (this file), `INSTRUCTIONS.md`,
  `OUTPUT-FORMAT.json`, `manifest.json`, `build_kit.py`, and the transcripts you download with it.
- Do not open other branches, pull requests, commits or issues of this repository. Do not search
  the web. Use the network only for `build_kit.py fetch`.
- Do not commit transcripts or your notes. Commit only your one JSON output file.

## Steps

1. Download and build your season (replace `N` with your season number):
   ```
   python3 -I build_kit.py fetch N /tmp/sww
   python3 -I build_kit.py build N /tmp/sww /tmp/read
   ```
   The build must end with `LINE COUNTS MATCH`. If it prints `MISMATCH`, stop: do not code;
   report the message and finish.
2. Read `INSTRUCTIONS.md` completely and follow it exactly. Your season folder is
   `/tmp/read/sNN/` (two-digit season number). The unassigned episodes are in
   `/tmp/read/unassigned/`. The exact line count of every file is in `manifest.json` under
   `linecounts`: read each of your season's files, in order, until you have seen its last line,
   and record that line number in `reading_log`.
3. Keep your verbatim-quote notes in `/tmp/notes.md` as you go (after every file), and code from
   those notes, rereading the transcript whenever you need to check something.
4. Write your JSON, matching `OUTPUT-FORMAT.json`, to `coded/sNN_LABEL.json` (e.g.
   `coded/s07_CA.json`). Add the field `"coder_model"` with the name of the model you are.
5. Commit only that file, on your own new branch named `sNN-LABEL`, and open a pull request. Do
   not merge it.
6. Your final message: the number of person records; each chunk file and the last line you read;
   the unassigned episodes you opened and why; every file path you opened.
