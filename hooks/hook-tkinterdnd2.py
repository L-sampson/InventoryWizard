from PyInstaller.utils.hooks import collect_data_files

def hook(hook_api):
    datas = collect_data_files('tkinterdnd2')
    hook_api.add_datas(datas)
