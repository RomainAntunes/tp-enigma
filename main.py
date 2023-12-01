from multiprocessing import cpu_count

from brute_force import brut_force_enigma
from chiffrer import chiffrer
from dechiffrer import dechiffrer

if __name__ == '__main__':
    # Config pour le 11 novembre
    rotors = "I V IV"
    reflecteur = "B"
    ring = "13 15 11"
    plugboard = "NX EC RV GP SU DK IT FY BL AZ"

    message = "Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir."

    message_chiffrer = chiffrer(rotors, reflecteur, ring, plugboard, message)
    print(message_chiffrer)

    # LESXTROUPESXBRITANNIQUESXSONTXENTREESXAXCUXHAVENXAXQUATORZEXHEURESXLEXSIXXMAIXDESORMAISXTOUTXLEXTRAFICXRADIOXCESSERAXJEXVOUSXSOUHAITEXLEXMEILLEURXFERMETUREXPOURXTOUJOURSXTOUTXLEXMEILLEURXAUXREVOIRX
    message_dechiffrer = dechiffrer(rotors, reflecteur, ring, plugboard, message_chiffrer)
    print(message_dechiffrer)

    # # # # # # # # # # # # # # # # # # # #
    #            BRUT FORCE               #
    # # # # # # # # # # # # # # # # # # # #

    # Les Allemands commencaient toujours le premier message de la journée en annonçant le Wetterbericht soit la météo. Dans ce message ça correspond au mot « meteorologie ».
    # La disposition des rotors est la suivante : 19 6 8
    # Les lettres sont branchées de la façon suivante : GH QW TZ RO IP AL SJ DK CN YM

    print("Nombre de cpu: ", cpu_count())

    message_brut_force = "UFLTVDIPVYDQFLDZGEHBNLVVPNCMDTJBSBCISSQAJPWTIMJMRPTOMIKKYKGCJXBNKEQHSUAOMGUJOKLSNABOCSOMYGVLXCJCGVAAYSJFOSISJCAIYFHUJYYJDGGWNCZ"

    brut_force_enigma(message_brut_force, "B", ["I", "II", "III", "IV", "V"], "19 6 8",
                      "GH QW TZ RO IP AL SJ DK CN YM", "meteorologie")

    # procs = []
    # rotors_tests = [
    #     ["I", "II", "III", "III", "IV", "V"],
    # ]
    #
    # for rotor_test in rotors_tests:
    #     proc = Process(target=brut_force_enigma, args=(
    #         message_brut_force, "B", rotor_test, "19 6 8", "GH QW TZ RO IP AL SJ DK CN YM", "meteorologie"))
    #
    #     procs.append(proc)
    #     proc.start()
    #
    # for proc in procs:
    #     proc.join()
