class Relation:
    def __init__(self, m: set[int], n: set[int], l: set[tuple[int,int]]):
        self.m = m
        self.n = n
        self.l = l
    
    def adjacency_matrix(self) -> list[list[int]]:
        rows = len(self.m)
        cols = len(self.n)
        ad_m = [[0 for _ in range(0,rows)] for _ in range(0,cols)]
        sorted_m = sorted(self.m)
        sorted_n = sorted(self.n)
        for (a,b) in self.l:
            i = sorted_m.index(a)
            j = sorted_n.index(b)
            ad_m[i][j] = 1
        return ad_m
    
    def compose(self, r):
        if self.n != r.m:
            raise Exception("Cannot compose! Sets need to match!")
        rels = set()
        for (x,y) in self.l:
            for z in [b for (a,b) in r.l if a == y]:
                rels.add((x,z))
        return Relation(self.m,r.n,rels)
    
    
    def __str__(self) -> str:
        return str(self.adjacency_matrix())
    
    def __eq__(self, other) -> bool:
        return self.m == other.m and self.n == other.n and self.l == other.l

class Mono_Set_Relation(Relation):
    def __init__(self, m: set[int], l: set[tuple[int, int]]):
        super().__init__(m, m, l)

    def compose(self, r):
        rels = set()
        for (x,y) in self.l:
            for z in [b for (a,b) in r.l if a == y]:
                rels.add((x,z))
        return Mono_Set_Relation(self.m,rels)

    def unify(self, r):
        if self.m != r.m:
            raise Exception("Cannot unify the relations because the supporting sets do not match!")
        return Mono_Set_Relation(self.m, self.l.union(r.l))

    def transitive_hull(self):
        one_step = self.unify(self.compose(self))
        if one_step == self:
            return self
        else:
            return one_step.transitive_hull()

    def is_reflexive(self) -> bool:
        for x in self.m:
            if (x,x) not in self.l:
                return False
        return True
    
    def is_antisymmetric(self) -> bool:
        for (a,b) in self.l:
            if a!=b:
                if (b,a) in self.l:
                    return False
        return True
    
    def is_symmetric(self) -> bool:
        for (a,b) in self.l:
            if (b,a) not in self.l:
                return False
        return True
    
    def is_transitive(self) -> bool:
        for (x,y) in self.l:
            for z in [b for (a,b) in self.l if a == y]:
                if (x,z) not in self.l:
                    return False
        return True

    def is_order(self) -> bool:
        return self.is_reflexive() and self.is_antisymmetric() and self.is_transitive()
    
    def is_equivalence_relation(self) -> bool:
        return self.is_reflexive() and self.is_symmetric() and self.is_transitive()
            


    
class Function(Relation):
    def __init__(self, m: set[int], n: set[int], l: set[tuple[int, int]]):
        super().__init__(m, n, l)
        if not(self.is_function()):
            raise Exception("Not a function!")

    def is_function(self) -> bool:
        for x in self.m:
            x_maps = [(a,_) for (a,_) in self.l if a==x]
            if len(x_maps) == 0 or len(x_maps)>1:
                return False
        return True
            

if __name__ == '__main__':
    r = Mono_Set_Relation({1,2,3},{(1,2),(2,3),(2,1),(3,1)})
    #m = r.adjacency_matrix()
    print(r)
    print(r.compose(r))
    print(r.unify(r.compose(r)))
    print("____")
    print(r.transitive_hull())
    print("____")
    
    r2 = Mono_Set_Relation({1,2,3},{(1,1), (2,2), (1,3), (2,3), (2,1), (3,1)})
    print(r2)
    print("relexive: " + str(r2.is_reflexive()))
    print("antisymmetric: " + str(r2.is_antisymmetric()))
    print("symmetric: " + str(r2.is_symmetric()))
    print("transitive: " + str(r2.is_transitive()))
    