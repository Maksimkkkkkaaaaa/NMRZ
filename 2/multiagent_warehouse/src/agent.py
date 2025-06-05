import threading
import time

from src.pathfinding import a_star
from src.config import MAX_STEPS, PACK_ZONE


class Agent(threading.Thread):
    def __init__(self, agent_id, start_pos, warehouse, blackboard):
        super().__init__(daemon=True)
        self.agent_id = agent_id
        self.pos = start_pos
        self.warehouse = warehouse
        self.bb = blackboard
        self.status = 'idle'
        self.target = None
        self.route = []
        self.collected = 0
        self.step_count = 0
        self.wait_counter = 0
        self.current_order = None

    def run(self):
        while self.step_count < MAX_STEPS:
            if self.status == 'idle':
                self.try_assign_order()

            if self.target and not self.route:
                self.plan_route()

            if self.route:
                next_pos = self.route[1]
                self.bb.post_intent(self.agent_id, next_pos)
                time.sleep(0.01)
                intents = self.bb.get_intents()
                conflict = self.detect_conflict(next_pos, intents)
                if conflict:
                    self.bb.clear_intent(self.agent_id)
                    self.wait_counter += 1
                    time.sleep(0.05)
                    if self.wait_counter > 3:
                        self.route = []
                        self.wait_counter = 0
                else:
                    self.bb.clear_intent(self.agent_id)
                    self.pos = next_pos
                    self.step_count += 1
                    self.wait_counter = 0
                    if self.pos == self.target:
                        self.arrive_at_target()
                    else:
                        self.route.pop(0)
                continue

            time.sleep(0.01)
            self.step_count += 1

    def try_assign_order(self):
        unassigned = self.bb.get_unassigned_orders()
        if not unassigned:
            return
        best = None
        best_dist = None
        for ord_pos in unassigned:
            d = abs(self.pos[0] - ord_pos[0]) + abs(self.pos[1] - ord_pos[1])
            if best_dist is None or d < best_dist:
                best_dist = d
                best = ord_pos
        if self.bb.assign_order(best, self.agent_id):
            self.status = 'to_order'
            self.target = best
            self.route = []

    def plan_route(self):
        occupied = set(pos for aid, pos in self.bb.get_intents().items() if aid != self.agent_id)
        path = a_star(self.pos, self.target, self.warehouse, occupied)
        if path:
            self.route = path
        else:
            self.route = []
            time.sleep(0.05)

    def detect_conflict(self, next_pos, intents):
        for aid, pos in intents.items():
            if aid == self.agent_id:
                continue
            if pos == next_pos:
                return True
            if pos == self.pos and next_pos == self.bb.intentions.get(aid):
                return True
        return False

    def arrive_at_target(self):
        if self.status == 'to_order':
            if self.warehouse.pick_order(*self.target):
                self.status = 'to_pack'
                self.current_order = self.target
                self.target = PACK_ZONE
                self.route = []
            else:
                self.status = 'idle'
                self.target = None

        elif self.status == 'to_pack':
            if self.pos == PACK_ZONE:
                self.collected += 1
                self.bb.complete_order(self.current_order)
                self.status = 'idle'
                self.target = None
                self.route = []
                self.current_order = None
