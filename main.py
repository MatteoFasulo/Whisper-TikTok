import subprocess

#######################
series = "Crazy facts that you did not know"
part = 4
outro = "Follow us for more"
outfile = f"text_{part}.mp3"
path = f"F:\\Vari Progetti\\AI_YouTube\\source\\{outfile}"
#######################

with open('script.txt', 'r') as file:
    text = file.read().rstrip().replace('"',"'")

final_text = f"{series}. Part {part}.\n{text}\n{outro}"

with subprocess.Popen(f'edge-tts --voice en-US-ChristopherNeural --text "{final_text}" --write-media "{path}"', stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
    pass
print("Done!")