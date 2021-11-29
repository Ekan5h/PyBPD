""" Author: https://github.com/Ekan5h
"""

class TraceReader:
    def __init__(self, fname):
        self.fname = fname
        with open(fname, 'r') as f:
            s = f.readlines()
            self.nodes = [[y if y=='-' else int(y) if y[:2]!='0x' else int(y,16) for y in x.split()[1:5]] for x in s if x[:4] == 'NODE']
            self.edges = [[y if y in ['T', 'N', '-'] else int(y) if y[:2]!='0x' else int(y,16) for y in x.split()[1:7]] for x in s if x[:4] == 'EDGE']
            idx = s.index('BT9_EDGE_SEQUENCE\n')
            self.seq = [int(x) for x in s[idx+1:-1]][1:]
            del s
            # NODE -> id virtual_address physical_address opcode
            # EDGE -> id src_id dest_id taken br_virt_target br_phy_target
            self.nodes = {x[0]:x[1:] for x in self.nodes}
            self.edges = {x[0]:x[1:] for x in self.edges}
            print("READING TRACE:", fname)
            print("NODES", len(self.nodes))
            print("EDGES", len(self.edges))
            print("INSCOUNT", len(self.seq))
            print('-'*10)
            self.inscount = len(self.seq)
            self.i = 0

    def reset_reader(self):
        self.i = 0

    # Return PC, taken/not-taken, opcode
    def update(self):
        if self.i%10000==0: print('\b'*2000 + self.fname + ': ' + str(self.i), end='', flush=True)
        if self.i>=self.inscount:
            print()
            return -1, -1, -1
        edge = self.edges[self.seq[self.i]]
        node = self.nodes[edge[0]]
        self.i+=1
        return node[0], int(edge[2]=='T'), node[-1]

