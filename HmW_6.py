import os
import shutil
import zipfile
import sys
from pathlib import Path


# Функція для транслітерації та заміни символів в іменах файлів
def normalize(name):
    transliteration_dict = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu',
        'я': 'ia',}
    normalized_name = ''
    for char in name:
        if char.isalnum() or char.isspace() or char in ['_', '.']:
            
            normalized_name += char.lower()  
        elif char in transliteration_dict:
            
            normalized_name += transliteration_dict[char]
        else:
            
            normalized_name += '_'

    return normalized_name

# Функція для обробки архівів
def process_archive(archive_path, destination_folder):
    archive_name = Path(archive_path).stem
    extract_path = os.path.join(destination_folder, archive_name)
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        extracted_files = [os.path.join(extract_path, f) for f in os.listdir(extract_path)]
        for extracted_file in extracted_files:
            _, file_extension = os.path.splitext(extracted_file)
            if file_extension:
                shutil.move(extracted_file, os.path.join(destination_folder, os.path.basename(extracted_file)))
            else:
                process_folder(extract_path)
    except zipfile.BadZipFile:
        print(f"Error: the archive {archive_path} is corrupted")
   
def is_image(file_path):
    image_extensions = ['.JPEG', '.JPG', '.PNG', '.GIF', '.BMP', '.TIFF', '.SVG']
    file_extension = os.path.splitext(file_path)[1].upper()
    return file_extension in image_extensions

# Функції для обробки різних типів файлів
def process_images(file_path, destination_folder):
    if is_image(file_path):
        shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
    else:
        file_extension = os.path.splitext(file_path)[1].upper()
        normalized_name = normalize(os.path.basename(file_path))
        new_path = os.path.join(destination_folder, normalized_name + file_extension)
        shutil.move(file_path, new_path)
    
    
   
    



def process_videos(file_path, destination_folder):
    file_extension = os.path.splitext(file_path)[1].upper()
    allowed_video_extensions = ['.AVI', '.MP4', '.MOV', '.MKV']
    if file_extension in allowed_video_extensions:
        shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
    else:
        normalized_name = normalize(os.path.basename(file_path))
        new_path = os.path.join(destination_folder, normalized_name + file_extension)
        shutil.move(file_path, new_path)
    


def process_documents(file_path, destination_folder):
    file_extension = os.path.splitext(file_path)
    allowed_documents_extensions = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
    if file_extension.upper() in allowed_documents_extensions:
        shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
    else:
        normalized_name = normalize(os.path.basename(file_path))
        new_path = os.path.join(destination_folder, normalized_name + file_extension)
        shutil.move(file_path, new_path)


def process_music(file_path, destination_folder):
    file_extension = os.path.splitext(file_path)[1].upper()
    allowed_music_extensions = ['.MP3', '.OGG', '.WAV', '.AMR']
    if file_extension in allowed_music_extensions:
        shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
    else:
        normalized_name = normalize(os.path.basename(file_path))
        new_path = os.path.join(destination_folder, normalized_name + file_extension)
        shutil.move(file_path, new_path)
    

    
def process_unknown(file_path, destination_folder):
    file_extension = os.path.splitext(file_path)

    normalized_name = normalize(os.path.basename(file_path))
    new_path = os.path.join(destination_folder, normalized_name + file_extension)
    shutil.move(file_path, new_path)

# Основна функція для обробки папок
def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            _, file_extension = os.path.splitext(file_name)

            # Викликаємо відповідну функцію в залежності від розширення
            if file_extension.upper() in ['.JPEG', '.PNG', '.JPG', '.SVG']:
                process_images(file_path, 'images')
            elif file_extension.upper() in ['.AVI', '.MP4', '.MOV', '.MKV']:
                process_videos(file_path, 'video')
            elif file_extension.upper() in ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']:
                process_documents(file_path, 'documents')
            elif file_extension.upper() in ['.MP3', '.OGG', '.WAV', '.AMR']:
                process_music(file_path, 'audio')
            elif file_extension.upper() in ['.ZIP', '.GZ', '.TAR']:
                process_archive(file_path, 'archives')
            else:
                process_unknown(file_path, 'other')

            # Перейменовання файлів за допомогою normalize
            normalized_name = normalize(file_name)
            normalized_path = os.path.join(root, normalized_name)
            os.rename(file_path, normalized_path)

    # Видалення порожніх папок
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)


if __name__ == "__main__":
    

    if len(sys.argv) != 2:
        print("Usage: python HmW_6.py <HomeWork6>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print("Error: Folder not found.")
        sys.exit(1)

    process_folder(folder_path)

    

    print("Sorting completed.")
    print("\n Список файлів в кожній категорії:")
    print("Зображення:", os.listdir("images"))
    print("Відео:", os.listdir("video"))
    print("Документи:", os.listdir("documents"))
    print("Музика:", os.listdir("audio"))
    print("Архіви:", os.listdir("archives"))
    print("Невідомі розширення:", os.listdir("other"))
    
