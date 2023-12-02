import sys

from enigma.machine import EnigmaMachine
from tqdm import tqdm


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


def split_list(a_list, nb_split=2):
    """
    Sépare une liste en plusieurs sous-listes
    :param a_list:      liste à splitter
    :param nb_split:    nombre de sous-listes
    :return:       liste de sous-listes
    """
    avg = len(a_list) / float(nb_split)
    out = []
    last = 0.0

    while last < len(a_list):
        out.append(a_list[int(last):int(last + avg)])
        last += avg

    return out


def logic_find(
        message_decrypt,
        reflector="B",
        ring="01 01 01",
        plugboard="",
        start_word="",
        rotor_combinations=None,
        kenngruppen=None,
        q=None,
        event=None,
        result=None,
):
    if rotor_combinations is None:
        raise ValueError("The list of the rotor_combinations can't be None")

    if kenngruppen is None:
        raise ValueError("The list of kenngruppen can't be None")

    if event is None:
        raise ValueError("The event can't be None, it's used to stop all the processes")

    if result is None:
        raise ValueError("The result can't be None, it's used to send the result to the main process")

    # On teste toutes les combinaisons possibles de rotors
    for rotor_combination in rotor_combinations:
        # On teste toutes les combinaisons possibles de kenngruppen
        for kenngruppe in kenngruppen:

            # On crée une machine Enigma avec les paramètres donnés
            machine = generate_machine(reflector=reflector, rotors=rotor_combination, ring=ring,
                                       plugboard=plugboard)

            # On définit la kenngruppe
            machine.set_display(kenngruppe)

            # On crypte le message
            encrypted_message = machine.process_text(message_decrypt)

            # On incrémente la queue pour afficher la progression
            if q is not None:
                q.put(1)

            # On vérifie si le message crypté contient le mot recherché
            if start_word.upper() in encrypted_message.upper():
                # On arrête tous les processus, et on envoie le message crypté à l'event
                result.append(dict(rotors=rotor_combination, kenngruppe=kenngruppe, message=encrypted_message))
                event.set()

                sys.exit(1)

    # Si on arrive ici, c'est que le mot n'a pas été trouvé
    sys.exit(0)


def queue_listener(q, nb_combinaisons):
    """
    Affiche la progression de la recherche dans la queue
    :param q:                   queue
    :param nb_combinaisons:     nombre de combinaisons à tester
    :return:               None
    """
    pbar = tqdm(
        position=0,
        total=nb_combinaisons,
        desc="Progression",
        unit=" combinaisons",
        leave=True,
    )
    for _ in iter(q.get, None):
        pbar.update()
