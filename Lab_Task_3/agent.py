class Student:
    def __init__(self, student_id, availability, preferences):

        self.student_id = student_id
        self.availability = availability
        self.preferences = preferences
        self.schedule = []  

    def assign_class(self, class_id, time_slot):

        self.schedule.append((class_id, time_slot))

    def clear_schedule(self):
        self.schedule = []

    def calculate_fitness(self, class_priorities):

        conflict_penalty = 0
        preference_penalty = 0

        for class_id, time_slot in self.schedule:
            if self.availability[time_slot] == 0:
                conflict_penalty += 1

            preference_penalty += (5 - self.preferences[time_slot]) * class_priorities[class_id]

        return conflict_penalty + preference_penalty
