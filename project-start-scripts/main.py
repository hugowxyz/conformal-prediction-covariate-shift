import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python3', script_name], check=True, capture_output=True, text=True)
        print(f"Successfully ran {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

if __name__ == "__main__":
    scripts = ['load_sqlite_db.py', 'load_voice_command_ground_truth.py', 'patch_bg_modifier.py']
    
    for script in scripts:
        run_script(script)
