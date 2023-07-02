# Constructing the list of common sense variables c1 to c3 with random truth values
import random
import time
c1 = bool(random.getrandbits(1))
c2 = bool(random.getrandbits(1))
c3 = bool(random.getrandbits(1))

common_sense_list = [c1, c2, c3]

# Create initial knowledge list
knowledge_list = []
knowledge_count = int(input("How many pieces of knowledge exists in this beehive:")) # Number of unique knowledge pieces (k1, k2, ..., ki)

for i in range(1, knowledge_count + 1):
    knowledge = f'k{i}'
    knowledge_list.append(knowledge)

#The Bees class
class Bees:
    def __init__(self, index, commonSense, knowledge):
        self.commonSense = commonSense
        self.knowledge = knowledge
        self.lifespan = 100
        self.index = index

    def Communicate(self, other):

        print("Bee {} is the sender, Bee {} is the receiver".format(self.index, other.index))
        print("Communicating...")
        time.sleep(1)  # Simulating communication time

        if not self.knowledge:
            print("No knowledge to share.")
            return

        sender_knowledge = set(self.knowledge)
        receiver_knowledge = set(other.knowledge)

        new_knowledge = sender_knowledge - receiver_knowledge
        new_knowledge = [k for k in new_knowledge if k != '']  # Remove empty strings

        if not new_knowledge:
            print("No knowledge gained by Bee {}.".format(other.index))
        else:
            new_knowledge = list(set(sender_knowledge) - set(receiver_knowledge))
            other.knowledge.extend(new_knowledge)
            other.knowledge = sorted(list(set(other.knowledge)))
            print("Bee {} gained knowledge: {}".format(other.index, new_knowledge))
        print("\n")
            
        # Check if a knowledge becomes common sense
        for knowledge in other.knowledge:
            if all(knowledge in bee.knowledge for bee in bees):
                if knowledge not in self.commonSense:
                    self.commonSense.append(knowledge)
                    print(f"{knowledge} has become common sense.")

#The honest bees class, inherits Bees
class Honest(Bees):
    def __init__(self, index,commonSense, knowledge):
        super().__init__(index,commonSense, knowledge)

#The mutant bees class, also inherits Bees
class Mutant(Bees):
    def __init__(self, index,commonSense, knowledge):
        super().__init__(index,commonSense, knowledge)
        #self.lying_function = lying_function

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Interface to create bees
n = get_integer_input("Enter the number of bees: ")
m = get_integer_input("Enter the number of muntant bees:")
if m > n:
    print("Error: The number of mutant bees cannot exceed the total number of bees.")
    exit()
h = n - m  # Number of honest bees
# Create bees list
bees = []
for i in range(n):
    if i < m:
        bee = Mutant(i+1,common_sense_list, random.sample(knowledge_list, random.randint(0, knowledge_count)))
        print(f"Bee {i+1} is a mutant.")
    else:
        bee = Honest(i+1,common_sense_list, random.sample(knowledge_list, random.randint(0, knowledge_count)))
    bees.append(bee)
for bee in bees:
    print(f"Bee {bee.index} knowledge base: {bee.knowledge}")
# Communication process
while True:
    time.sleep(5)  # Wait for 5 seconds
    sender = random.choice(bees)
    receiver = random.choice(bees)
    while receiver == sender:
        receiver = random.choice(bees)

    sender.Communicate(receiver)
    # Check if a knowledge becomes common sense
    all_knowledge = [bee.knowledge for bee in bees]
    common_knowledge = set(all_knowledge[0]).intersection(*all_knowledge)
    common_sense = list(common_knowledge)
    if set(common_sense) == set(all_knowledge[0]):
        print("All knowledge has been upgraded to common sense.")
        break

