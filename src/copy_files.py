import os
import shutil

from src.config import BASE_DIR


def static_to_public(dest="public", src="static"):
    destination_absolute_path = BASE_DIR / dest
    source_absolute_path = BASE_DIR / src
    
    if destination_absolute_path.exists():
        shutil.rmtree(destination_absolute_path)
    os.makedirs(destination_absolute_path, exist_ok=True)
    
    list_dir = os.listdir(source_absolute_path)
    for item in list_dir:
        abs_path_item = os.path.join(source_absolute_path, item)
        if os.path.isfile(abs_path_item):
            shutil.copy(src=abs_path_item, dst=destination_absolute_path)
        
        if os.path.isdir(abs_path_item):
            
            if os.path.isfile(abs_path_item):
                shutil.copy(src=abs_path_item, dst=destination_absolute_path)
            
            static_to_public(src=abs_path_item, dest=destination_absolute_path / item)