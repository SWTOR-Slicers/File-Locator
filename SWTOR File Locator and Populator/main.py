import os
import shutil
import json

eyeMatInfo = None

def main():
    config_data = read_config()
    paths_json = read_paths(config_data['toon-folder'])
    parsed_paths = grab_files_to_load(paths_json)
    extraction_resource_folder = config_data['extraction-folder']
    if os.path.exists(extraction_resource_folder) and os.path.exists(config_data['toon-folder']):
        if eyeMatInfo is not None:
            material_folder_copy_location = os.path.join(config_data['toon-folder'], 'assets\\materials\\eye\\')
            if not os.path.exists(material_folder_copy_location):
                os.makedirs(material_folder_copy_location)

            for texture in eyeMatInfo.textures:
                if (texture != None):
                    texture_path = os.path.join(extraction_resource_folder, texture[1:])
                    if os.path.exists(texture_path):
                        shutil.copy(texture_path, material_folder_copy_location)
            
        for path_obj in parsed_paths:
            locate_and_copy_files(path_obj, config_data['toon-folder'], extraction_resource_folder)

    else:
        print("your extraction or toon folder does not exist")


def locate_and_copy_files(path_obj, toon_folder_path, extracted_files_location):
    if path_obj.slot_name == "skinMats":
        for mat in path_obj.mats:
            material_folder_copy_location = os.path.join(toon_folder_path, 'assets\\materials\\skinMats\\', mat.slot_name + "\\")
            material_file_path = os.path.join(extracted_files_location, mat.mat_path[1:])
            if os.path.exists(material_file_path):
                shutil.copy(material_file_path, material_folder_copy_location)

            for texture in mat.textures:
                if (texture != None):
                    texture_path = os.path.join(extracted_files_location, texture[1:])
                    if os.path.exists(texture_path):
                        shutil.copy(texture_path, material_folder_copy_location)

    else:
        model_folder_copy_location = os.path.join(toon_folder_path, 'assets\\models\\', path_obj.slot_name + "\\")
        material_folder_copy_location = os.path.join(toon_folder_path, 'assets\\materials\\', path_obj.slot_name + "\\")
        for model in path_obj.models:
            model_path = os.path.join(extracted_files_location, model[1:])
            if os.path.exists(model_path):
                shutil.copy(model_path, model_folder_copy_location)

        material_file_path = os.path.join(extracted_files_location, path_obj.mat_path[1:])
        if os.path.exists(material_file_path):
            shutil.copy(material_file_path, material_folder_copy_location)

        for texture in path_obj.textures:
            if (texture != None):
                texture_path = os.path.join(extracted_files_location, texture[1:])
                if os.path.exists(texture_path):
                    shutil.copy(texture_path, material_folder_copy_location)


def grab_files_to_load(paths_json):
    parsed_objs = []
    global eyeMatInfo
    for entry in paths_json:
        if entry['slotName'] == "skinMats":
            to_push = skin_mats_list_obj()
            for mat in entry['materialInfo']['mats']:
                to_push.mats.append(skin_mats_obj(mat))

            parsed_objs.append(to_push)

        else:
            s = slot_obj(entry)
            if s.slot_name == "head":
                eyeMatInfo = slot_obj_mat_only(entry['materialInfo']['eyeMatInfo'])
            
            parsed_objs.append(s)
    
    return parsed_objs
    

def read_paths(paths_json_path):
    path = os.path.join(paths_json_path, 'assets\\paths.json')
    with open(path) as json_file:
        data = json.load(json_file)

    return data


def read_config():
    with open('config.json') as json_file:
        data = json.load(json_file)

    return data


class slot_obj():
    def __init__(self, dict_from_json):
        self.slot_name = dict_from_json['slotName']
        self.models = dict_from_json['models']
        self.mat_path = dict_from_json['materialInfo']['matPath']
        dds_dict = dict_from_json['materialInfo']['ddsPaths']
        self.textures = [
            dds_dict['diffuseMap'] if 'diffuseMap' in dds_dict else None,
            dds_dict['glossMap'] if 'glossMap'in dds_dict else None,
            dds_dict['rotationMap'] if 'rotationMap'in dds_dict else None,
            dds_dict['paletteMap'] if 'paletteMap'in dds_dict else None,
            dds_dict['paletteMaskMap'] if 'paletteMaskMap'in dds_dict else None,
            dds_dict['complexionMap'] if 'complexionMap'in dds_dict else None,
            dds_dict['facepaintMap'] if 'facepaintMap'in dds_dict else None,
            dds_dict['ageMap'] if 'ageMap'in dds_dict else None
        ]

    def __repr__ (self):
        return "{\n" + "slotName: " + self.slot_name + "\n" + "models: " + ", ".join(self.models) + "\n" + "matPath: " + self.mat_path + "\n" + "textures: " + ", ".join(self.textures) + "\n" + "}"


class slot_obj_mat_only():
    def __init__(self, dict_from_json):
        dds_dict = dict_from_json['ddsPaths']
        self.textures = [
            dds_dict['diffuseMap'] if 'diffuseMap' in dds_dict else None,
            dds_dict['glossMap'] if 'glossMap'in dds_dict else None,
            dds_dict['rotationMap'] if 'rotationMap'in dds_dict else None,
            dds_dict['paletteMap'] if 'paletteMap'in dds_dict else None,
            dds_dict['paletteMaskMap'] if 'paletteMaskMap'in dds_dict else None
        ]

    def __repr__ (self):
        return "{\n" + "textures: " + ", ".join(self.textures) + "\n" + "}"


class skin_mats_obj():
    def __init__(self, dict_from_json):
        self.slot_name = dict_from_json['slotName']
        self.mat_path = dict_from_json['materialInfo']['matPath']
        dds_dict = dict_from_json['ddsPaths']
        self.textures = [
            dds_dict['diffuseMap'] if 'diffuseMap' in dds_dict else None,
            dds_dict['glossMap'] if 'glossMap'in dds_dict else None,
            dds_dict['rotationMap'] if 'rotationMap'in dds_dict else None,
            dds_dict['paletteMap'] if 'paletteMap'in dds_dict else None,
            dds_dict['paletteMaskMap'] if 'paletteMaskMap'in dds_dict else None,
        ]

    def __repr__ (self):
        return "{\n" + "slotName: " + self.slot_name + "\n" + "textures: " + ", ".join(self.textures) + "\n" + "}"


class skin_mats_list_obj():
    def __init__(self):
        self.slot_name = "skinMats"
        self.mats = []

    def __repr__ (self):
        return "{\n" + "slotName: " + self.slot_name + "\n" + "mats: " + ", ".join(self.mats) + "\n" + "}"

if __name__ == "__main__":
    main()