import argparse
from os import listdir, rmdir
from pathlib import Path
import re
from shutil import move, unpack_archive


def normalize(element_name: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    name_translit = element_name.translate(TRANS)
    name_normalize = re.sub(r'[^a-zA-Z0-9_]', '_', name_translit)

    return name_normalize

def sort(path: Path, dir_name: str):
    ext = path.suffix
    file_name = normalize(path.name.removesuffix(ext)) + ext
    new_path =  output_folder / dir_name
    new_path.mkdir(exist_ok=True, parents=True)
    move(path, new_path / file_name)

def sort_images(path: Path):
     sort(path, 'images')

def sort_documents(path: Path):
     sort(path, 'documents')

def sort_audio(path: Path):
     sort(path, 'audio')

def sort_video(path: Path):
     sort(path, 'video')

def sort_archives(path: Path):
    ext = path.suffix
    
    archives_name = normalize(path.name.removesuffix(ext))
    new_path =  output_folder / 'archives'
    new_path.mkdir(exist_ok=True, parents=True)
    unpack_archive(path, new_path / archives_name)
    file_name = normalize(path.name.removesuffix(ext)) + ext
    list_archives.append(file_name)
    move(path, new_path / file_name)

def read_folder(path: Path) -> None:
    for element in path.iterdir():
        if element.is_dir():
            read_folder(element)
            if not listdir(element) and isinstance(listdir(element), list):
                rmdir(element)

        else:
            ext = element.suffix
            if ext.upper() in EXT_IMAGES:
                sort_images(element)
                set_known_ext.add(ext)
                list_images.append(normalize(element.name))
            elif ext.upper() in EXT_AUDIO:
                sort_audio(element)
                set_known_ext.add(ext)
                list_audio.append(normalize(element.name))
            elif ext.upper()  in EXT_VIDEO:
                sort_video(element)
                set_known_ext.add(ext)
                list_video.append(normalize(element.name)) 
            elif ext.upper() in EXT_DOCUMENTS:
                sort_documents(element)
                set_known_ext.add(ext)
                list_documents.append(normalize(element.name))    
            elif ext.upper() in EXT_ARCHIVES:
                sort_archives(element)
                set_known_ext.add(ext)
            else:
                set_unknown_ext.add(ext)

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help='Source folder') 
parser.add_argument('--output', '-o', default = 'Sorted', help='Output folder') 

args = vars(parser.parse_args()) 
source = args.get("source")
output = 'Sorted'

EXT_IMAGES = {'.JPEG', '.PNG', '.JPG', '.SVG'}
EXT_AUDIO = {'.MP3', '.OGG', '.WAV', '.AMR'}
EXT_VIDEO = {'.AVI', '.MP4', '.MOV', '.MKV'}
EXT_DOCUMENTS = {'.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'}
EXT_ARCHIVES = {'.ZIP', '.GZ', '.TAR'}

set_unknown_ext = set()
set_known_ext = set()
list_images = []
list_audio = []
list_video = []
list_documents = []
list_archives = []

output_folder = Path(output) #sorted => Path(назва_папки_призначення_sorted(default))
read_folder(Path(source))    #source => Path(назва_папки_для_робори)

print('set of unknown extensions: ',set_unknown_ext)
print('set of known extensions: ', set_known_ext)
print(list_images)
print(list_audio)
print(list_video)
print(list_documents)
print(list_archives)