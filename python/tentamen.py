def __init__(self, name):
    self.name = name

def __init__(self, train_name, nr_of_seats)
    self.name = train_name
    self.nr_of_seats = nr_of_seats
    self.seats = [None] * nr_of_seats

def find_empty_seat(self):
    1e optie
    for seat in range(self.nr_of_seats)
        if self.is_empty(seat):
            return seat
    2e optie
    counter = 0
    for seat in self.seats
        if seat == None
            return counter
        counter += 1

def assign_seat(self, passenger)
    1e optie
    seat = self.find_empty_seat()
    self.seats[seat] = passenger

    2e optie
    self.seats[self.find_empty_seat()] = passenger

def get_seat_load(self):
    1e optie
    for i in self.seats
        if i == None
            counter += 1
    return int((counter/self.nr_of_seats)*100)
    2e optie
    for seat in range(self.nr_of_seats)
        if self.is_empty(seat)
            counter += 1
