from copy import deepcopy

class DynamicProgrammingMatrix:
    '''
    Dynamic Programming Matrix that automatically does wrapping modulo N
    '''
    def __init__( self, N, val = 0.0, diag_val = 0.0 ):
        self.N = N
        self.DPmatrix = []
        for i in range( N ):
            self.DPmatrix.append( [] )
            for j in range( N ):
                self.DPmatrix[i].append( DynamicProgrammingData( val ) )
                self.DPmatrix[i][j].info = (self,i,j)

        for i in range( N ): self.DPmatrix[i][i].Q = diag_val

    def __getitem__( self, idx ):
        return self.DPmatrix[ idx ]

    def __len__( self ): return len( self.DPmatrix )

class DynamicProgrammingData:
    '''
    Dynamic programming object, with derivs and contribution accumulation.
     Q   = value
     dQ  = derivative (later will generalize to gradient w.r.t. all parameters)
     contrib = contributions
    '''
    def __init__( self, val = 0.0 ):
        self.Q = val
        self.dQ = 0.0
        self.contrib = []
        self.info = []

    def __iadd__(self, other):
        self.Q += other.Q
        if  len( other.contrib ) > 0: self.contrib += other.contrib
        elif len( other.info ) > 0: self.contrib.append( [other.Q, [other.info]] )
        return self

    def __mul__(self, other):
        prod = DynamicProgrammingData()
        if isinstance( other, DynamicProgrammingData ):
            prod.Q       = self.Q * other.Q
            contribs1 = initialize_contribs( self )
            contribs2 = initialize_contribs( other )
            for contrib1 in contribs1:
                for contrib2 in contribs2:
                    prod.contrib.append( [ contrib1[0]*contrib2[0],
                                           contrib1[1]+contrib2[1] ] )
        else:
            prod.Q = self.Q * other
            for contrib in self.contrib:
                prod.contrib.append( [contrib[0]*other, contrib[1] ] )
        prod.info = self.info
        return prod

    def __truediv__( self, other ):
        quot = deepcopy( self )
        quot.Q /= other
        return quot

    __rmul__ = __mul__
    __floordiv__ = __truediv__
    __div__ = __truediv__


def initialize_contribs( DP ):
    '''
    Contribs (or dummy contribs) when taking products
    '''
    contribs = DP.contrib
    if len( contribs ) == 0:
        contribs =[ [1.0,[]] ] if len( DP.info ) == 0 else [ [1.0,[DP.info]] ]
    return contribs