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


# Confir pour le 11 novembre
rotors = "I V IV"
reflecteur = "B"
ring = "13 15 11"
plugboard = "NX EC RV GP SU DK IT FY BL AZ"

message = "Les troupes britanniques sont entrees a Cuxhaven a quatorze heures le six mai Desormais tout le trafic radio cessera je vous souhaite le meilleur Fermeture pour toujours tout le meilleur au revoir."

message_chiffrer = chiffrer(rotors, reflecteur, ring, plugboard, message)
print(message_chiffrer)

message_dechiffrer = dechiffrer(rotors, reflecteur, ring, plugboard, message_chiffrer)
print(message_dechiffrer)
