from utils import generate_machine


def chiffrer(rotors, reflector, ring, plugboard, text):
    """
    Chiffre un texte avec les paramètres donnés
    :param rotors:      rotors à utiliser
    :param reflector:   reflecteur à utiliser
    :param ring:        réglages des anneaux
    :param plugboard:   réglages du plugboard
    :param text:        texte à chiffrer
    :return:            texte chiffré
    """
    default_machine = generate_machine(rotors, reflector, ring, plugboard)
    return default_machine.process_text(text)
