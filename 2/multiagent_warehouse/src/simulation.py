import time

from src.warehouse import Warehouse
from src.blackboard import Blackboard
from src.agent import Agent
from src.config import DOCK_STATIONS, ORDERS, MAX_STEPS


class Simulation:
    def __init__(self):
        self.warehouse = Warehouse()
        self.blackboard = Blackboard(initial_orders=ORDERS)

        self.agents = []
        for i, dock in enumerate(DOCK_STATIONS):
            agent = Agent(
                agent_id=i,
                start_pos=dock,
                warehouse=self.warehouse,
                blackboard=self.blackboard
            )
            self.agents.append(agent)

    def run(self):
        for ag in self.agents:
            ag.start()

        start_time = time.time()
        while time.time() - start_time < MAX_STEPS * 0.01:
            if all(status == 'delivered' for status in self.blackboard.order_status.values()):
                break
            time.sleep(0.05)

        for ag in self.agents:
            ag.join(timeout=0.1)

        total_collected = sum(ag.collected for ag in self.agents)
        print(f"\nСимуляция завершена. Всего доставлено заказов: {total_collected}")
        for ag in self.agents:
            print(f"  Агент {ag.agent_id} доставил: {ag.collected}")

        delivered = [pos for pos, st in self.blackboard.order_status.items() if st == 'delivered']
        undelivered = [pos for pos, st in self.blackboard.order_status.items() if st != 'delivered']

        print(f"\nДоставленные заказы (координаты): {delivered}")
        if undelivered:
            print(f"Невыполненные заказы (координаты): {undelivered}")
        else:
            print("Все заказы выполнены!")
