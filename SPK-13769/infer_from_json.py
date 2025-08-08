#!/usr/bin/env python3
import subprocess
import os
import json

def main():
    cmd_template = "python3 -m clients.main synthesize file --config config.ini --read-ssml  --text \"<speak>{}</speak>\" --voice-name {} --voice-style {} --save-to {} --sample-rate 22050"

    with open(f"SPK-13769/select.json", 'r', encoding='utf-8') as f_full:
        for i, line in enumerate(f_full):
            record = json.loads(line)

            text = record['text']
            filename = os.path.join('SPK-13769', 'gen', record['filename'])

            speaker_info = record['speaker'].split('_')
            if len(speaker_info) == 2:
                voice, style = speaker_info
            elif len(speaker_info) == 1:
                voice, style = record['speaker'], 'neutral'
            else:
                raise Exception
            
            command = cmd_template.format(text, voice, style, filename)
            subprocess.run(command, shell=True)
    
        

if __name__ == "__main__":
    main()
