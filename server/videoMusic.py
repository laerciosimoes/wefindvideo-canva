import os


def getMusic(jsonData):
    try :
        scene1 = jsonData[0]
        file_name = scene1["Music"]
            
        folder_path = "./music"
    
        # Combine the folder path with the file name
        file_path = os.path.join(folder_path, file_name)
    
        # Check if the file exists
        if os.path.isfile(file_path):
            return file_path
        else:
            return None
    except Exception as e:
        return None
