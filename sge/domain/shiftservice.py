import calendar
import random
from datetime import date, datetime, timedelta

from sge.domain.pygadservice import PygadService

class ShiftService:
    #employee_indexes = []
    #employee_ids = [];
    #num_genes = 0;
    def __init__(self):
        self.employee_indexes = []
        self.employee_ids = [];
        self.num_genes = 0
        #self.name = name

    def generateIndices(self, payload):
        employees = payload['employees']
        self.employee_ids = [];
        self.employee_indexes = []
        i = 1;
        for employee in employees:
            self.employee_indexes.append(i)
            self.employee_ids.append(employee['id'])
            i = i+1;

    async def generate(self, payload):
        
        num_days = calendar.monthrange(payload['year'], payload['month'])[1]
        planning = {date(payload['year'], payload['month'], day):
                [] for day in range(1, num_days+1)}
        #return num_days
        self.num_genes = num_days
        self.generateIndices(payload)

        pygad_service = PygadService(
            self.num_genes,
            self.employee_indexes,
            4
            )
        pygad_instance = pygad_service.runInstance()
        solution, solution_fitness, solution_idx = pygad_instance.best_solution()
        r = {
            'solution': "Parameters of the best solution : {solution}".format(solution=solution),
            'solution_fitness': "Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness),
            'solution_idx': "Index of the best solution : {solution_idx}".format(solution_idx=solution_idx)
        }
        return r # "Parameters of the best solution : {solution}".format(solution=solution) # { 'solution': solution, 'solution_fitness': solution_fitness, 'solution_idx': solution_idx} #ReturnTest(solution, solution_fitness, solution_idx)
        #print("Parameters of the best solution : {solution}".format(solution=solution))
        #print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        #print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))



class ReturnTest:
    def __init__(self, solution, solution_fitness, solution_idx):
        self.solution = solution
        self.solution_fitness = solution_fitness
        self.solution_idx = solution_idx

    #def data(self):

        

