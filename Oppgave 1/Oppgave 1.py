
# A. 
def my_str_len(str_len: str) -> int:

    #Returnerer lengden på en angitt string.
    
    return len(str_len)

print(my_str_len("heisann"))

def my_max(max_liste: list[int]) -> int:

    #Returnerer det største elementet i en liste.

    return max(max_liste)

print(my_max([1, 3, 2, 10, 4]))



# B. 

class Student:
    def __init__(self, navn):
        self.navn = navn

class Gruppe:
    def __init__(self, gruppenavn, studenter):
        self.gruppenavn = gruppenavn
        self.studenter = studenter

    def inneholder_student(self, student_navn):
        return any(student.navn == student_navn for student in self.studenter)

# Eksempel på mock data
student1 = Student("Alice")
student2 = Student("Bob")
student3 = Student("Charlie")
student4 = Student("David")
student5 = Student("Eva")
student6 = Student("Frank")

# Oppretter grupper med flere studenter
gruppe1 = Gruppe("Gruppe A", [student1, student2, student3])
gruppe2 = Gruppe("Gruppe B", [student4, student5])
gruppe3 = Gruppe("Gruppe C", [student6])

# Liste over grupper
grupper = [gruppe1, gruppe2, gruppe3]

# Testing for å finne hvilken gruppe en student tilhører
def finn_student_gruppe(student_navn, grupper):
    for gruppe in grupper:
        if gruppe.inneholder_student(student_navn):
            return gruppe.gruppenavn
    return "Studenten finnes ikke i noen gruppe"

# Tester
print(finn_student_gruppe("Alice", grupper))     # Skal returnere "Gruppe A"
print(finn_student_gruppe("David", grupper))     # Skal returnere "Gruppe B"
print(finn_student_gruppe("Frank", grupper))     # Skal returnere "Gruppe C"
print(finn_student_gruppe("Grace", grupper))     # Skal returnere "Studenten finnes ikke i noen gruppe"



# C. 

# 9.1.1

def moon_weight(earth_weight):
    # Regn ut moon_weight basert på earth_weight. 
    return earth_weight * (1/6)

print(moon_weight(1000))

# 9.1.6.1

numbers = [-1, 0, 1]

list_strings = list(map(lambda x: "pos" if x > 0 else "neg" if x < 0 else "zero", numbers))
print(list_strings)  



# 9.2.2 

from dataclasses import dataclass

@dataclass 
class Room: 
    room_name: str
    capacity: int 

info = [Room("Hei", 3),
        Room("Hade", 4)]

def capacitiy1(for_room_name: str, rooms: list):
    #Finn ut kapasitet på romnavn 
    for ro in rooms:
        if ro.room_name == for_room_name:
            return ro.capacity 
        
print(capacitiy1("Hei", info))
print(capacitiy1("Hade", info))








