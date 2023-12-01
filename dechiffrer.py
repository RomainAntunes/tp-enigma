from utils import generate_machine


def dechiffrer(rotors, reflector, ring, plugboard, text):
    """
    Dechiffrer un message
    :param rotors:      rotors à utiliser
    :param reflector:   reflecteur à utiliser
    :param ring:        réglages des anneaux
    :param plugboard:   réglages du plugboard
    :param text:        texte à chiffrer
    :return: text dechiffrer
    """
    default_machine = generate_machine(rotors, reflector, ring, plugboard)
    return default_machine.process_text(text)
