from .utilities.config import Config
import colorama

def do(config_file):
    conf = Config(config_file)
    art_colorized = conf.art
    colorama.init()
    for light in conf.lights():
        if light < 0 or light > 9:
            # Multi-digit lights not yet supported
            continue
        light_str = str(light)
        color = (colorama.Back.YELLOW + colorama.Fore.BLACK) if conf.light_on(light) else colorama.Back.BLUE
        light_str_colored = color + \
                            light_str + \
                            colorama.Style.RESET_ALL
        art_colorized = art_colorized.replace(light_str, light_str_colored)
    white_character = 'w'
    white_colored = colorama.Back.WHITE + ' ' + colorama.Style.RESET_ALL
    art_colorized = art_colorized.replace(white_character, white_colored)
    cyan_character = 'c'
    cyan_colored = colorama.Back.CYAN + ' ' + colorama.Style.RESET_ALL
    art_colorized = art_colorized.replace(cyan_character, cyan_colored)
    print(art_colorized)
