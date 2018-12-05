#!/usr/bin/python
from zetafold.parameters import get_params
from zetafold.data.training_examples import *
from zetafold.training import *
from scipy.optimize import minimize
from multiprocessing import Pool
import math
import argparse


parser = argparse.ArgumentParser( description = "Test nearest neighbor model partitition function for RNA sequence" )
parser.add_argument("-params","--parameters",type=str, default='', help='Parameter file to use [default: '', which triggers latest version]')
parser.add_argument( "--train_params",help="Parameters to optimize. Give none to get list.",nargs='*')
parser.add_argument( "--init_log_params",help="Initial values for parameters",nargs='*')
parser.add_argument("--no_coax", action='store_true', default=False, help='Turn off coaxial stacking')
parser.add_argument("--jobs","-j", type=int, default=4, help='Number of jobs to run in parallel')
args     = parser.parse_args()

# set up parameter file
params = get_params( args.parameters, suppress_all_output = True )
if args.no_coax: params.set_parameter( 'K_coax', 0.0 )

# set up training examples
training_examples = [ tRNA ] #, P4P6_outerjunction ]
train_parameters = args.train_params # ['C_init','C_eff_stack_WC_WC','C_eff_stack_WC_GU','C_eff_stack_WC_UG','C_eff_stack_GU_GU','C_eff_stack_UG_GU','C_eff_stack_GU_UG']
x0      = args.init_log_params # np.array( [     0.5,                5.3,                4.1,                5.6,                4.9,                4,                    4] ) * np.log(10.0)

if train_parameters == None:
    params.show_parameters()
    exit()
if x0 == None:
    x0 = np.zeros( len(train_parameters) )
    for n,param_tag in enumerate(train_parameters): x0[ n ] = math.log( params.get_parameter_value( param_tag ) )
    print x0

#train_parameters = ['C_init']
#x0      = np.array( [     0.5 ] )

pool = Pool( args.jobs )

loss = lambda x:free_energy_gap(      x,params,train_parameters,training_examples,pool)
grad = lambda x:free_energy_gap_deriv(x,params,train_parameters,training_examples,pool)

result = minimize( loss, x0, method = 'L-BFGS-B') #, jac = free_energy_gap_deriv )
final_loss = loss( result.x )
print( 'Deriv: ', grad( result.x ) )

print(result)
print('Final parameters:', result.x, 'Loss:',final_loss)