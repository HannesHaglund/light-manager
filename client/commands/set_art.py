from .utilities.config import Config

def do(config_file, art_file):
    with open(art_file) as f:
        art = f.read()
    conf = Config(config_file)
    conf.art = art
    conf.write()
