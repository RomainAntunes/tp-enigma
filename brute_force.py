import time
from multiprocessing import cpu_count, Process, Queue, Event, Manager

from utils import generate_rotors_combinaison, generate_kenngruppen, split_list, logic_find, queue_listener


def brute_force_enigma(message_decrypt,
                       reflector="B",
                       ring="01 01 01",
                       plugboard="",
                       start_word="",
                       mp=True):
    """
    Lance une attaque par brut force sur une machine Enigma
    :param message_decrypt:     message à décrypter
    :param reflector:           reflecteur à utiliser
    :param ring:                ring settings
    :param plugboard:           plugboard settings
    :param start_word:          mot de référence
    :param mp:                  True si on veut utiliser le multiprocessing
    :return:                   None
    """

    temp1 = time.perf_counter()

    print("Brut force lancé avec les paramètres suivants:")
    print("Message à décrypter: ", message_decrypt)
    print("Reflector: ", reflector)
    print("Ring: ", ring)
    print("Plugboard: ", plugboard)
    print("Mot de référence: ", start_word)

    # On génère toutes les combinaisons possibles de rotors
    rotor_combinations = generate_rotors_combinaison()

    # On récupère le nombre de cpu [Attention peut manger beaucoup de CPU si on enlève le // 2]
    # nb_cpu = cpu_count() // 2
    nb_cpu = 1 if not mp else cpu_count() // 2
    print("Nombre de CPU Total:\t", cpu_count())
    print("Nombre de CPU utilisés:\t", nb_cpu)

    # On génère toutes les combinaisons possibles de kenngruppen
    kenngruppen = generate_kenngruppen()
    print("Nombre de combinaisons de kenngruppen: ", len(kenngruppen))

    # Calcul du nombre de combinaisons à tester
    nb_combinaisons = len(rotor_combinations) * len(kenngruppen)
    print("Nombre de combinaisons à tester: ", nb_combinaisons)

    # Vérifie que ne divise pas plus que le nombre de cœurs du processeur
    if nb_cpu > cpu_count():
        # Si c'est le cas, on met le nombre de cpu au nombre de cœurs du processeur - 1 (pour ne pas bloquer le PC)
        nb_cpu = cpu_count() - 1

    # On sépare les rotors en plusieurs listes selon le nombre de cpu
    rotors_splited = split_list(rotor_combinations, nb_cpu)

    procs = []

    # On lance un processus qui va écouter la queue
    q = Queue()
    listener_proc = Process(target=queue_listener, args=(q, nb_combinaisons,), daemon=True)
    procs.append(listener_proc)

    # Event qui permet de détecter quand le message est trouvé
    event = Event()

    # On crée une variable qui va contenir le résultat
    manager = Manager()
    result = manager.list()

    # On lance un processus par liste de rotors
    for i in range(len(rotors_splited)):
        proc = Process(target=logic_find,
                       args=(message_decrypt, reflector, ring, plugboard, start_word, rotors_splited[i],
                             kenngruppen, q, event, result),
                       daemon=True)
        procs.append(proc)

    # On lance tous les processus
    for proc in procs:
        proc.start()

    # On attend que le message soit trouvé
    event.wait()

    # On arrête tous les processus
    for proc in procs:
        proc.terminate()

    # On affiche le résultat
    for r in result:
        print("Résultat:")
        print("Rotors: ", r["rotors"])
        print("Kenngruppe: ", r["kenngruppe"])
        print("Message: ", r["message"])

    temp2 = time.perf_counter()
    print("Temps d'execution: ", temp2 - temp1, "s")
