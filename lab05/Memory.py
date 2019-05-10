class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.vars = {}

    def __contains__(self, item):  # variable name
        return True if item in self.vars else False

    def get(self, name):  # gets from memory current value of variable <name>
        return self.vars[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.vars[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memstack = [memory if memory is not None else Memory('globalMemory')]

    def get(self, name):  # gets from memory stack current value of variable <name>
        for mem in self.memstack:
            if name in mem:
                return mem.get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.memstack[0].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        for mem in self.memstack:
            if name in mem:
                mem[name] = value
                return

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.memstack.insert(0, memory)

    def pop(self):  # pops the top memory from the stack
        return self.memstack.pop(0)
