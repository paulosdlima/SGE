from datetime import date, timedelta


class InvalidLeaveDateException(Exception):
    pass


class Shift():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.leaves = []
        self.mandatory_shift_days = []
        self.free_days = []

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name

    def set_leave(self, start: date, end: date):
        if start > end:
            raise InvalidLeaveDateException(
                'DateError: leave starts after it ends')
        else:
            self.leaves.append((start, end))

    def remove_last_leave(self):
        self.leaves.pop()

    def is_available(self, day: date):
        for leave in self.leaves:
            if leave[0] <= day <= leave[1]:
                return False
        return True

    def set_mandatory_shift(self, day: date):
        self.mandatory_shift_days.append(day)

    def del_mandatory_shift(self, day: date):
        self.mandatory_shift_days.remove(day)

    def check_mandatory_shift(self, day):
        for d in self.mandatory_shift_days:
            if d == day:
                return True
        return False

    def in_shift(self, day: date, free_days=3):
        for free_day in self.free_days:
            if day <= free_day <= day + timedelta(days=3):
                free_days += 1
        self.set_leave(day, day + timedelta(days=free_days))
