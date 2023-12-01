import time
from multiprocessing import Process, cpu_count

from alive_progress import alive_bar
from enigma.machine import EnigmaMachine


def chiffrer(rotors, reflecteur, ring, plugboard, text):
    machine = EnigmaMachine.from_key_sheet(
        rotors=rotors,
        reflector=reflecteur,
        ring_settings=ring,
        plugboard_settings=plugboard,
    )

    return machine.process_text(text)


def dechiffrer(rotors, reflecteur, ring, plugboard, text):
    machine = EnigmaMachine.from_key_sheet(
        rotors=rotors,
        reflector=reflecteur,
        ring_settings=ring,
        plugboard_settings=plugboard,
    )

    return machine.process_text(text)


def brut_force_enigma(message_to_find, reflecteur="B", ring="01 01 01",
                      plugboard=""):

    first_word = "meteorologie".upper()

    # Vous allez devoir créer une fonction bruteforce qui va tester toutes les possibilités restantes afin de
    # tester toutes les combinaisons de rotors différentes (3 parmi les 5) en testant toute les clés possibles
    # (3 caractères). La seule façon va donc d’être de comparer une partie de l’entrée avec un bout de la
    # sortie qui est connu. Une fois que vous aurez trouvé les rotors utilisés & la clé vous pourrez déchiffrer
    # tout le message.
    temp1 = time.time()

    rotors_check = ["I", "II", "III", "IV", "V"]

    # 5! 2!
    with alive_bar((5 * 4 * 3) * 26 * 26 * 26, title="Brut force en cours...") as bar:
        for k, rotor1 in enumerate(rotors_check.copy()):
            rotor2_list = rotors_check.copy()
            rotor2_list.pop(k)

            for j, rotor2 in enumerate(rotor2_list):
                rotor3_list = rotor2_list.copy()
                rotor3_list.pop(j)

                for rotor3 in rotor3_list:

                    rotors_test = rotor1 + " " + rotor2 + " " + rotor3
                    machine = EnigmaMachine.from_key_sheet(
                        rotors=rotors_test,
                        reflector=reflecteur,
                        ring_settings=ring,
                        plugboard_settings=plugboard,
                    )

                    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    for key1 in alphabet:
                        for key2 in alphabet:
                            for key3 in alphabet:
                                kenngruppenheft = key1 + key2 + key3
                                machine.set_display(kenngruppenheft)

                                bar()

                                message_process = machine.process_text(message_to_find)
                                if message_process.startswith(first_word):
                                    temp2 = time.time()
                                    print("Temps de calcul :", str(temp2 - temp1), "secondes")

                                    print("Message trouvé : " + message_process)
                                    print("Rotors utilisés : " + rotor1 + " " + rotor2 + " " + rotor3)
                                    print("Clé utilisée : " + str(key1) + " " + str(key2) + " " + str(key3))
                                    print("Plugboard utilisé : " + plugboard)
                                    return

    print("Message non trouvé")
    print("Temps de calcul :", str(time.time() - temp1), "secondes")


if __name__ == '__main__':
    # Config pour le 11 novembre
    rotors = "I V IV"
    reflecteur = "B"
    ring = "13 15 11"
    plugboard = "NX EC RV GP SU DK IT FY BL AZ"

    message = "Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir."

    message_chiffrer = chiffrer(rotors, reflecteur, ring, plugboard, message)
    print(message_chiffrer)

    message_dechiffrer = dechiffrer(rotors, reflecteur, ring, plugboard, message_chiffrer)
    print(message_dechiffrer)

    # # # # # # # # # # # # # # # # # # # #
    #            BRUT FORCE               #
    # # # # # # # # # # # # # # # # # # # #

    # Les allemands commencaient toujours le premier message de la journée en annonçant le Wetterbericht soit la météo. Dans ce message ça correspond au mot « meteorologie ».
    # La disposition des rotors est la suivante : 19 6 8
    # Les lettres sont branchées de la façon suivante : GH QW TZ RO IP AL SJ DK CN YM

    print("Nombre de cpu: ", cpu_count())

    message_brut_force = "UFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"

    procs = []
    rotors_tests = [
        ["I", "II", "III", "IV", "V"],
    ]

    for rotor_test in rotors_tests:
        proc = Process(target=brut_force_enigma, args=(
            message_brut_force, "B", "19 6 8", "GH QW TZ RO IP AL SJ DK CN YM"))

        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
