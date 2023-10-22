import sys
import os
import subprocess
from multiprocessing import cpu_count
from threading import Thread
from glob import iglob
import shutil

BAD_EXIT = -1
CWD = os.getcwd()
CPU_COUNT = cpu_count()
TMP_FOLDER = "tmp"

def workerProcess(listFragment,index):
    voidGenAudio(listFragment,index)

def voidGenAudio(listStrings,index):
    """
    Generate audio for sentence.
    """
    strSentence = (" ").join(listStrings)
    file_root = f"{TMP_FOLDER}/{index}"
    aiff_file = file_root + ".aiff"
    mp3_file = file_root + ".mp3"
    # subprocess.run(["edge-tts",'--voice','ja-JP-NanamiNeural','--text',strSentence,'--write-media',mp3_file])
    subprocess.run(["say","-v","Kyoko","-o",aiff_file,strSentence])
    subprocess.run(["lame","-m","m",aiff_file,mp3_file])
    os.remove(aiff_file)


def runThreads(listContent,intDivisions):
    """
    Runs the threads to do work
    """
    listSplit = listSplitList(listContent,intDivisions)
    listThreads = [Thread(target=workerProcess,args=(listSplit[i],i)) for i in range(0,intDivisions)]

    for i in range(0,intDivisions):
        listThreads[i].start()
    
    for i in range(0,intDivisions):
        listThreads[i].join()

def listSplitList(lines,num_elements_per_sublist):
    # Initialize the list of sublists
    sublists = []

    # Iterate through the lines and create sublists
    for i in range(0, len(lines), num_elements_per_sublist):
        sublist = lines[i:i + num_elements_per_sublist]
        sublists.append(sublist)

    # If there are any remaining elements, distribute them among the sublists
    remaining = len(lines) % 12
    for i in range(remaining):
        sublists[i].append(lines[i * num_elements_per_sublist + num_elements_per_sublist])

    return sublists

def combine_mp3s(input_files, output_file):
    dest = open(output_file,'wb')
    for file in input_files:
        shutil.copyfileobj(open(file,'rb'),dest)
        os.remove(file)
    dest.close()

def run(bookFilePath,outputFileName):
    try:
        with open(bookFilePath,'r') as f:
            file_content = f.read()
            file_content = file_content.replace(" ","")
            lines = file_content.split("\n")
            if len(lines) < CPU_COUNT:
                intDivisions = len(lines)
            else:
                intDivisions = CPU_COUNT
            runThreads(lines,intDivisions)
            mp3s= [os.path.join(file) for file in os.listdir(TMP_FOLDER) if file.endswith(".mp3")]
            mp3s.sort(key=lambda x: int(x.split('.')[0]))
            mp3s = [os.path.join(TMP_FOLDER,mp3) for mp3 in mp3s]
            combine_mp3s(mp3s,outputFileName)

    except FileNotFoundError:
        print(f"The file '{f}' does not exist.")
        exit(BAD_EXIT)
    # except Exception as e:
    #     print(f"Exception: {e}")
    #     exit(BAD_EXIT)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("usage: tta [book_file_name.txt] [output_name.mp3]")

    bookFilePath = sys.argv[1]
    outputFileName = sys.argv[2]

    run(bookFilePath,outputFileName)