import calendar
import random
from datetime import date, datetime, timedelta

from sge.data.mongo import database
from sge.domain.helpers import shift_helper
from sge.domain.models.shift import Shift
from sge.domain.repositories.crud import get_list_data
from sge.utils import date_converter


class NoShiftsAvailableException(Exception):
    pass


class ConflitDateException(Exception):
    pass


def verify_all_planning_conditions(payload, planning):
    if not payload['employees']:
        return None

    for emp in payload['employees']:
        try:
            for mand in emp['mandatory_shifts']:
                for d in planning:
                    if (mand == d) and (emp['id'] !=
                                        planning[d][0].__getattribute__('id')):
                        return False
        except KeyError:
            pass

    return True


async def generate_shift(payload):
    num_days = calendar.monthrange(payload['year'], payload['month'])[1]
    planning = {date(payload['year'], payload['month'], day):
                [] for day in range(1, num_days+1)}

    def setup_employees(payload):
        # Team init
        employees = []

        # Team setup + leaves + mandatory shifts + free days
        for employee in payload['employees']:
            p = Shift(str(employee['id']), employee['name'])
            try:
                # leaves
                for leave in employee['leaves']:
                    p.set_leave(start=date_converter(leave['start_date']),
                                end=date_converter(leave['end_date']))

                # mandatory shifts
                for mandatory_day in employee['mandatory_shifts']:
                    for period in p.leaves:
                        if period[0] <= \
                                date_converter(mandatory_day) <= period[1]:
                            raise ConflitDateException(
                                'Mandatory shift is in a leave period: ',
                                f'{mandatory_day}')
                        else:
                            p.set_mandatory_shift(day=mandatory_day)
                    p.set_leave(
                        start=date_converter(mandatory_day)-timedelta(days=1),
                        end=date_converter(mandatory_day)-timedelta(days=1))

                # free days
                if isinstance(employee['free_days'], int):
                    i = 1
                    while i <= employee['free_days']:
                        free_day = date(
                            payload['year'], payload['month'],
                            random.randint(1, num_days))
                        if free_day not in p.mandatory_shift_days:
                            if free_day in p.free_days:
                                continue
                            for leave_days in employee['leaves']:
                                if leave_days['start_date'] <= free_day <= \
                                                        leave_days['end_date']:
                                    break
                                else:
                                    p.free_days.append(free_day)
                                    p.set_leave(start=free_day, end=free_day)
                                    i += 1
                                    break
            except KeyError:
                pass
            employees.append(p)

        return employees

    # Check for last month planning
    async def check_last_planning(employees):
        previous_planning = date(
            payload['year'], payload['month'], 1) - timedelta(days=1)
        shifts = await get_list_data(
            database.shifts, shift_helper, area=payload['area'],
            year=previous_planning.year, month=previous_planning.month)
        # print(shifts['shifts'])
        if shifts:
            for shift in list(shifts[0]['shifts'].items())[-4:]:
                day = datetime.strptime(shift[0], '%Y-%m-%d').date()
                for e in employees:
                    for record in shift[1]:
                        if record['name'] == e.name:
                            e.in_shift(day)
        else:
            print('Last month\'s planning not found')

    # Init Blacklist (used for backtracking)

    global blacklist
    blacklist = []

    def backtrack(plan, day, team, limit):

        # randomly mix the team (for equity)
        random.shuffle(team)

        # Exit case (plan is complete)
        if list(plan.values())[-1]:
            return plan

        # Check mandatory shifts first
        for person in team:
            if person.check_mandatory_shift(day):
                plan[day].append(person)
                person.in_shift(day)

        # Main loop
        for person in team:
            # check if available (not in leave)
            if not person.is_available(day):
                continue

            # check if in blacklist (backtracking)
            if (person, day) in blacklist:
                continue

            # check if more than 2 people in shift
            elif len(plan[day]) >= limit:
                limit = 1
                break

            # if all the above are met assign person to shift
            else:
                plan[day].append(person)
                person.in_shift(day)

        # If for loop exits without break (no person was found available)
        else:
            if not plan[day]:
                day -= timedelta(days=1)
                try:
                    if len(plan[day]) == 2:
                        plan[day][0].remove_last_leave()
                        plan[day][1].remove_last_leave()
                        blacklist.append(
                            (plan[day][random.randint(0, 1)], day))
                    elif len(plan[day]) == 1:
                        plan[day][0].remove_last_leave()
                        blacklist.append((plan[day][0], day))
                    plan[day] = []
                    for (person, d) in blacklist:
                        if d > day:
                            blacklist.remove((person, d))
                except KeyError:
                    raise NoShiftsAvailableException('No possible solution!')

                backtrack(plan, day, team, 1)  # previous day

        backtrack(plan, day + timedelta(days=1), team, limit)  # next day

    # For shift continuity
    employees = setup_employees(payload)
    await check_last_planning(employees)

    # Call to main function
    backtrack(plan=planning,
              day=list(planning.keys())[0],
              team=employees,
              limit=1)

    return dict((day.isoformat(), value) for (day, value) in planning.items())
