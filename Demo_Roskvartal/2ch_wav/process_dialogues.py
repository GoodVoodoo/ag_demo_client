import os
import glob

def extract_dialogue(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    dialogue_lines = []
    for line in lines:
        if 'Hypothesis' in line:
            # Extract the text between quotes
            start = line.find('"') + 1
            end = line.rfind('"')
            if start > 0 and end > start:
                dialogue_lines.append(f'- "{line[start:end]}"')
    
    return dialogue_lines

def process_files():
    # Get all txt files except those starting with 'dial_' and 'role_'
    txt_files = [f for f in glob.glob('*.txt') 
                 if not (os.path.basename(f).startswith('dial_') or 
                        os.path.basename(f).startswith('role_'))]
    
    # Create output directory if it doesn't exist
    os.makedirs('new_txt', exist_ok=True)
    
    for txt_file in txt_files:
        dialogue_lines = extract_dialogue(txt_file)
        
        # Create new filename with 'dial_' prefix
        new_filename = os.path.join('new_txt', f'dial_{os.path.basename(txt_file)}')
        
        # Write dialogue lines to new file
        with open(new_filename, 'w', encoding='utf-8') as f:
            for line in dialogue_lines:
                f.write(f'{line}\n')

if __name__ == '__main__':
    process_files() 