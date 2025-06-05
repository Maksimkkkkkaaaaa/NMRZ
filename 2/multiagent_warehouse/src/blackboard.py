import threading

class Blackboard:
    def __init__(self, initial_orders):
        self.lock = threading.Lock()
        self.intentions = {}
        self.order_status = {pos: 'unassigned' for pos in initial_orders}
        self.order_owner = {}

    def post_intent(self, agent_id, pos):
        with self.lock:
            self.intentions[agent_id] = pos

    def clear_intent(self, agent_id):
        with self.lock:
            if agent_id in self.intentions:
                del self.intentions[agent_id]

    def get_intents(self):
        with self.lock:
            return dict(self.intentions)

    def assign_order(self, pos, agent_id):
        with self.lock:
            if self.order_status.get(pos) == 'unassigned':
                self.order_status[pos] = 'assigned'
                self.order_owner[pos] = agent_id
                return True
            return False

    def complete_order(self, pos):
        with self.lock:
            if self.order_status.get(pos) == 'assigned':
                self.order_status[pos] = 'delivered'
                return True
            return False

    def get_unassigned_orders(self):
        with self.lock:
            return [pos for pos, st in self.order_status.items() if st == 'unassigned']

    def get_assigned_orders(self):
        with self.lock:
            return {pos: owner for pos, owner in self.order_owner.items() if self.order_status[pos] == 'assigned'}
