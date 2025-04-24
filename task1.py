from typing import List, Dict
from dataclasses import dataclass
from itertools import combinations

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    # Конвертуємо словники в об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    constraints = PrinterConstraints(**constraints)

    # Сортуємо за пріоритетом (зростання пріоритету => спочатку найважливіші)
    jobs.sort(key=lambda job: job.priority)

    scheduled = []  # Порядок друку (групи)
    total_time = 0
    used = set()

    # Жадібно обираємо комбінації для пакету друку
    while len(used) < len(jobs):
        best_group = []
        min_priority = float('inf')

        for r in range(1, constraints.max_items + 1):
            for group in combinations([job for job in jobs if job.id not in used], r):
                total_volume = sum(job.volume for job in group)
                if total_volume > constraints.max_volume:
                    continue

                group_priority = min(job.priority for job in group)
                if group_priority < min_priority or (group_priority == min_priority and len(group) > len(best_group)):
                    best_group = group
                    min_priority = group_priority

        if not best_group:
            break

        for job in best_group:
            used.add(job.id)
        scheduled.extend(job.id for job in best_group)
        total_time += max(job.print_time for job in best_group)

    return {
        "print_order": scheduled,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
