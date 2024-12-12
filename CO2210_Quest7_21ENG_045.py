import random
import matplotlib.pyplot as plt

#create person class
class Person:
    def __init__(self, age_group):
        self.infected = False
        self.days_infected = 0
        self.hospitalized = False
        self.recovered = False
        self.dead = False
        self.detect = False
        self.age_group = age_group

    def infect(self, mask_w):#function to infect virus
        if not self.infected and random.uniform(0, 1) < self.infection_probability(mask_w) and self.days_infected == 0 and not self.dead:
            self.infected = True

    def infection_probability(self, mask):#function to get infection probability for different situation
        if mask.upper() == "N":#infection probability when not wearing mask
            if self.age_group == 'children':
                return random.uniform(0.1, 0.2)
            elif self.age_group == 'adults':
                return random.uniform(0.15, 0.4)
            elif self.age_group == 'senior_citizens':
                return random.uniform(0.35, 0.6)
        elif mask.upper() == "Y":#infection probability when wearing mask
            if self.age_group == 'children':
                return random.uniform(0.05, 0.1)
            elif self.age_group == 'adults':
                return random.uniform(0.1, 0.3)
            elif self.age_group == 'senior_citizens':
                return random.uniform(0.3, 0.5)

    def recover(self):#function to set recovered person
        if self.infected and not self.dead:#for recover that person should infected and not dead
            self.days_infected = self.days_infected + 1
            if self.days_infected >= 14:#normally it take 14+ days to recover(assuming)
                if self.hospitalized or (not self.hospitalized and random.uniform(0, 1) < 0.40):#assumption : to recover person should get hospitalized treatments or based on immunity level which is ranbom they can recover without get in to a hospital
                    self.recovered = True
                    self.infected = False
                    self.hospitalized = False
    def fatality(self):#function to set fatality person
        if self.infected and not self.dead:
            if random.uniform(0, 1) < 0.001 and not self.recovered:#check the dead probability < 0.1%
                self.dead = True

    def detected(self):#detect that person infected with virus or not(used when hospitalizing)
        if self.infected and not self.dead and not self.hospitalized:#by detecting time person should infected not dead and not hospitalized
            if random.uniform(0, 1) < 0.45: #assuming that detecting rate is 45%
                self.detect = True

class Family:
    def __init__(self, members):  # no. of family members
        self.members = members

    def spread_within_family(self, w_mask):  # inside the family spearding
        infected_members = [member for member in self.members if
                            member.infected]  # condition and loop to find infected member in family
        for member in self.members:
            if not member.infected and any(infected_members):  # check member infected has any infected members
                if random.uniform(0, 1) < 0.6:  # Assume 60% chance of transmission within family(40%-80%)
                    member.infect(w_mask)  # set member as infected


class Community:  # starting point
    def __init__(self, population_size):  # input 1000000 here
        self.population = self.generate_population(population_size)  # push input to generate population function

    def generate_population(self, population_size):
        population = []
        for _ in range(population_size):  # loop for 1 to 1000000
            if random.uniform(0, 1) < 0.2:
                person = Person('children')  # creating children
            elif random.uniform(0, 1) < 0.3:
                person = Person('senior_citizens')  # creating senior citizen
            else:
                person = Person('adults')
            population.append(person)  # put person object in population list
        return population

    def simulate_day(self,count):
        while True:
            wear_mask = input(
                "Start wearing face mask or put travel restriction? (started = 'y' / stop or not started = 'n'): ")
            if wear_mask.lower() == 'y' or wear_mask.lower() == 'n':
                break  # Valid input, exit loop
            else:
                print(
                    "Invalid input. Please enter 'y' for starting or 'n' for not starting.")  # Error message if input is invalid

        into_infected = 0 #count the new count added to infected in a considered day
        for person in self.population:
            if random.uniform(0, 0.4) < (count/1000000):#outside the house spreading probability is base on infected
                into_infected = into_infected + 1
                if into_infected > 25000:
                    break
                person.infect(wear_mask)  # set infected people upto that date

        for person in self.population:  # set recovered people upto that date
            person.recover()

        for person in self.population:  # set fatality people upto that date
            person.fatality()  # for person in self.population:
        # person.wear_face_mask()
        for person in self.population:  # set detected people upto that date
            person.detected()

        families = [Family(random.sample(self.population, random.randint(2, 7))) for _ in range(
            100000)]  # select 7 to 2 member from population and put then to a family and create 100000 of it in a list

        for family in families:
            family.spread_within_family(wear_mask)
        for person in self.population:
            if person.infected:
                count = count + 1
        return count
    def run_simulation(self, days):
        #create list to hold per-day count based on different parameters
        infected_count = []
        hospitalized_count = []
        fatalities_count = []
        recovered_count = []
        infect_count = 1#infect_count need to set infected person(used in person.infected() function)
        for day in range(1, days + 1):
            infect_count = self.simulate_day(infect_count)  # consider the data related to a date
            # Count statistics
            if day == 1:
                infected_count.append(1)#day 1 we have only 1 infected person (that is given)
                fatalities_count.append(0)#day 1 no deads can be reported
            else:
                infected_count.append(sum(person.infected for person in self.population)+1)
                fatalities_count.append(sum(person.dead for person in self.population))
            hospitalized_count.append(sum(person.hospitalized for person in self.population))
            recovered_count.append(sum(person.recovered for person in self.population))
            print("-------------------------------------------------------")#code segment to print summary
            print(" Day - " + str(day) + " Summary ")
            if day != 1: #perday summary
                if infected_count[-1]-infected_count[-2] > 0:
                    print(" Today's Infected Count    : " + str(infected_count[-1]-infected_count[-2]))
                else:
                    print(" Today's Infected Count    :  0")
                if hospitalized_count[-1]-hospitalized_count[-2] > 0:
                    print(" Today's Hospitalized Count    : " + str(hospitalized_count[-1]-hospitalized_count[-2]))
                else:
                    print(" Today's Hospitalized Count:  0")
                if fatalities_count[-1]-fatalities_count[-2] > 0:
                    print(" Today's fatalities Count    : " + str(fatalities_count[-1]-fatalities_count[-2]))
                else:
                    print(" Today's fatalities Count    :  0")
                if recovered_count[-1]-recovered_count[-2] > 0:
                    print(" Today's recovered Count    : " + str(recovered_count[-1]-recovered_count[-2]))
                else:
                    print(" Today's recovered Count    :  0")
            #summary upto a given date
            print(" Total Infected Count    : " + str(infected_count[-1]))
            print(" Total Hospitalized Count: " + str(hospitalized_count[-1]))
            print(" Total Fatalities Count  : " + str(fatalities_count[-1]))
            print(" Total Recovered Count   : " + str(recovered_count[-1]))

            #set hospitalized person
            for person in self.population:
                if person.infected and person.days_infected == 5 and not person.dead and person.detect:#to get hospitalized person should infected not dead and get correctly detect that he/she has infected or not
                    person.hospitalized = True

        self.plot_results(infected_count, hospitalized_count, fatalities_count, recovered_count)

    def plot_results(self, infected_count, hospitalized_count, fatalities_count, recovered_count):#function to display result in graphs
        days = list(range(1, len(infected_count) + 1))

        fig, ax = plt.subplots(2, 2)#create place to $ plots
        ax[0, 0].plot(days, infected_count)#plot infected_count vs days graph
        ax[0, 0].title.set_text("Infected")
        ax[0, 0].set_xlabel('Days')
        ax[0, 0].set_ylabel('Count')
        ax[0, 1].plot(days, hospitalized_count)#plot hospitalized_count vs days graph
        ax[0, 1].title.set_text("Hospitalized")
        ax[0, 1].set_xlabel('Days')
        ax[0, 1].set_ylabel('Count')
        ax[1, 0].bar(days, fatalities_count)#plot fatalities_count vs days graph
        ax[1, 0].title.set_text("Fatalities")
        ax[1, 0].set_xlabel('Days')
        ax[1, 0].set_ylabel('Count')
        ax[1, 1].plot(days, recovered_count)#plot recovered_count vs days graph
        ax[1, 1].title.set_text("Recovered")
        ax[1, 1].set_xlabel('Days')
        ax[1, 1].set_ylabel('Count')

        fig.tight_layout(pad=0.5)
        plt.show()


# Example usage
community = Community(1000000)#get no. of people as input
community.run_simulation(50)#get no. of day to simulate as input