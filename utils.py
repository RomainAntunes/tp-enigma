from enigma.machine import EnigmaMachine


def generate_machine(rotors="I V IV", reflector="B", ring="13 15 11", plugboard="NX EC RV GP SU DK IT FY BL AZ"):
    """
    Génère une machine Enigma avec les paramètres donnés
    :param rotors:      rotors à utiliser
    :param reflector:   reflecteur à utiliser
    :param ring:        ring settings
    :param plugboard:   plugboard settings
    :return:           machine Enigma
    """
    return EnigmaMachine.from_key_sheet(
        rotors=rotors,
        reflector=reflector,
        ring_settings=ring,
        plugboard_settings=plugboard,
    )


def generate_rotors_combinaison(rotors=None):
    """
    Génère toutes les combinaisons possibles de rotors
    :param rotors:  liste des rotors à utiliser
    :return:      liste des combinaisons de rotors (5!2! = 60 combinaisons)
    """
    if rotors is None:
        rotors = ["I", "II", "III", "IV", "V"]

    rotors_combinaisons: list[str] = []
    for rotor1 in rotors:

        rotors_without_rotor1 = rotors.copy()
        rotors_without_rotor1.remove(rotor1)

        for rotor2 in rotors_without_rotor1:

            rotors_without_rotor2 = rotors_without_rotor1.copy()
            rotors_without_rotor2.remove(rotor2)

            for rotor3 in rotors_without_rotor2:
                rotors_combinaisons.append(" ".join([rotor1, rotor2, rotor3]))

    return rotors_combinaisons


def generate_kenngruppen():
    """
    Génère toutes les combinaisons possibles de kenngruppen
    :return: liste des combinaisons de kenngruppen
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    kenngruppen: list[str] = []
    for letter1 in alphabet:
        for letter2 in alphabet:
            for letter3 in alphabet:
                kenngruppen.append(letter1 + letter2 + letter3)

    return kenngruppen
