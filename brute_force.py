import time
from alive_progress import alive_bar
from utils import generate_machine, generate_rotors_combinaison, generate_kenngruppen


def brut_force_enigma(message_decrypt,
                      reflector="B",
                      rotor_selection=None,
                      ring="01 01 01",
                      plugboard="",
                      start_word=""):
    """
    Lance une attaque par brut force sur une machine Enigma
    :param message_decrypt:     message à décrypter
    :param reflector:           reflecteur à utiliser
    :param rotor_selection:     liste des rotors à utiliser
    :param ring:                ring settings
    :param plugboard:           plugboard settings
    :param start_word:          mot de référence
    :return:                   None
    """

    temp1 = time.time()

    if rotor_selection is None:
        rotor_selection = ["I", "II", "III", "IV", "V"]

    if rotor_selection is not None:
        # Vérifie que les rotors sont différents
        if len(rotor_selection) != len(set(rotor_selection)):
            print("Erreur: deux rotors sont identiques")
            print("rotor_selection: ", rotor_selection)
            return

    print("Brut force lancé avec les paramètres suivants:")
    print("Message à décrypter: ", message_decrypt)
    print("Reflector: ", reflector)
    print("Rotors: ", rotor_selection)
    print("Ring: ", ring)
    print("Plugboard: ", plugboard)
    print("Mot de référence: ", start_word)

    # On génère toutes les combinaisons possibles de rotors
    rotor_combinations = generate_rotors_combinaison(rotor_selection)
    print("Nombre de combinaisons de rotors: ", len(rotor_combinations))

    # On génère toutes les combinaisons possibles de kenngruppen
    kenngruppen = generate_kenngruppen()
    print("Nombre de combinaisons de kenngruppen: ", len(kenngruppen))

    # Calcul du nombre de combinaisons à tester
    nb_combinaisons = len(rotor_combinations) * len(kenngruppen)
    print("Nombre de combinaisons à tester: ", nb_combinaisons)

    # Crée une progression de 0 à 100% avec un pas de 1%
    with alive_bar(nb_combinaisons) as progress_bar:
        # On teste toutes les combinaisons possibles de rotors
        for rotor_combination in rotor_combinations:
            # On teste toutes les combinaisons possibles de kenngruppen
            for kenngruppe in kenngruppen:

                # On crée une machine Enigma avec les paramètres donnés
                machine = generate_machine(reflector=reflector, rotors=rotor_combination, ring=ring, plugboard=plugboard)

                # On définit la kenngruppe
                machine.set_display(kenngruppe)

                # On crypte le message
                encrypted_message = machine.process_text(message_decrypt)

                # On incrémente la progression de 1/nb_combinaisons
                progress_bar()

                # On vérifie si le message crypté contient le mot recherché
                if start_word in encrypted_message:
                    temp2 = time.time()
                    print("Message trouvé en", temp2 - temp1, "s")
                    print("Temps d'execution: ", temp2 - temp1, "s")
                    print("Rotors: ", rotor_combination)
                    print("Kenngruppe: ", kenngruppe)
                    print("Message crypté: ", encrypted_message)
                    return

    temp2 = time.time()
    print("Message non trouvé")
    print("Temps d'execution: ", temp2 - temp1, "s")
