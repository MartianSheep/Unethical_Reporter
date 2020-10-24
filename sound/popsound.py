from playsound import playsound

sound1="knocking_an_iron_door1.mp3"
sound2="door_chime0.mp3"
sound3="door_chime0.mp3"
def pop(request):
    if request=="start" :
        playsound(sound1)
        return True
    if request=="end":
        playsound(sound2)
        return True
    if request=="cancel":
        playsound(sound3)
        return True
    return False

pop("start")