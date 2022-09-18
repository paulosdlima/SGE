from sge.domain.models.area import Area
from sge.domain.models.employee import Employee
from sge.domain.models.regional import Regional


def employee_helper(employee: Employee) -> dict:
    """Converte um objeto do servidor para um dicionário."""
    return {
        'id': str(employee['_id']),
        'area': str(employee['area']),
        'enrollment': employee['enrollment'],
        'name': employee['name'],
        'gender': employee['gender'],
        'phone': employee['phone'],
        'active': employee['active']
    }


def regional_helper(regional: Regional) -> dict:
    """Converte um objeto da regional para um dicionário."""
    return {
        'id': str(regional['_id']),
        'name': regional['name'],
        'description': regional['description']
    }


def area_helper(area: Area) -> dict:
    """Converte um objeto da área para um dicionário."""
    return {
        'id': str(area['_id']),
        'regional': str(area['regional']),
        'name': area['name'],
        'description': area['description']
    }


def shift_helper(shift) -> dict:
    """Converte um objeto da escala para um dicionário."""
    return {
        'id': str(shift['_id']),
        'area': str(shift['area']),
        'year': shift['year'],
        'month': shift['month'],
        'shifts': dict(shift['shifts'])
    }
