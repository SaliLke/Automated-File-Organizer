import os
import shutil
import hashlib


move_history=[]

def getFilePath():
    directory=input("Enter the folder path:")
    return directory

def FileTypeSort(directory):
    file_type_mapping = {
        'Documents': ['.pdf', '.docx', '.txt'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Videos': ['.mp4', '.mov', '.avi'],
        'Music': ['.mp3', '.wav', '.flac'],
        'Archives': ['.zip', '.tar', '.gz'],
        'Scripts': ['.py', '.js', '.html'],
        'Drawings':['.dwg']
    }

    dir_list=os.listdir(directory)
    for item in dir_list:
        fileExt= os.path.splitext(item)[1].lower()
        for folder, extension in file_type_mapping.items():
            if fileExt in extension:
                original_path=os.path.join(directory, item)
                folder_path = os.path.join(directory, folder)
                new_path=os.path.join(folder_path, item)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                shutil.move( original_path,new_path)
                move_history.append((original_path, new_path))
            
def UndoAction():
    while move_history:
        original_path, new_path = move_history.pop()
        shutil.move(new_path,original_path)
        folder_name=os.path.dirname(new_path)
        if os.path.isdir(folder_name) and not os.listdir(folder_name):
            os.rmdir(folder_name)

def FileSizeSort(directory):
    File_Categories= {
        'Empty':0,
        'Small':1000000,
        'Medium':10000000,
        'Large':100000000,
        'Very Large':float('inf')
    }
    
    for item in os.listdir(directory):
        original_path=os.path.join(directory,item)
        if os.path.isfile(original_path):
            file_size=os.path.getsize(original_path)
            for category, valueBytes in File_Categories.items():
                if file_size<=valueBytes:
                    folder_path=os.path.join(directory, category)
                    new_Path=os.path.join(folder_path,item)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    shutil.move(original_path,new_Path)
                    move_history.append((original_path, new_Path))
                    break

def get_file_hash(file_path):
    with open(file_path,"rb") as file:
        file_data=file.read()
    hash_md5=hashlib.md5(file_data)
    return hash_md5.hexdigest()


def duplicateFiles(directory):
    hash_map={}

    duplicate_folder = os.path.join(directory, "Duplicates")
    for item in os.listdir(directory):
        original_path = os.path.join(directory, item)
        if os.path.isfile(original_path):
            file_hash=get_file_hash(original_path)
            if file_hash in hash_map:
                if not os.path.exists(duplicate_folder):
                6
                os.makedirs(duplicate_folder)
                new_path=os.path.join(duplicate_folder, item)
                shutil.move(original_path,new_path)
                move_history.append((original_path,new_path))
            else:
                hash_map[file_hash]=original_path

def fileNameFixing(directory):
    for item in os.listdir(directory):
        original_path=os.path.join(directory, item)
        if os.path.isfile(original_path):
            new_name= item.lower().replace(" ","_").replace("-","_")
            if new_name!= item:
                new_path=os.path.join(directory, new_name)
                os.rename(original_path,new_path)
                move_history.append((original_path, new_path))


directory=getFilePath()
while True:   
    UserInput=input("Enter the sorting method:\n1.Type Sort\n2.Size Sort\n3.Undo\n4.Change the file path\n5.Remove Duplicate Files\n6.Fix File Names\n7.Quit")
    if UserInput=='1':      
        FileTypeSort(directory)  
    elif UserInput=='2':
        FileSizeSort(directory)            
    elif UserInput=='3':
        UndoAction()
    elif UserInput=='4':
        directory=getFilePath()
    elif UserInput=='5':
        duplicateFiles(directory)
    elif UserInput=='6':
        fileNameFixing(directory)
    else:
        break
