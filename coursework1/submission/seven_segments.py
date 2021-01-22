#for the submission uncomment the submission statements
#see submission.README

from math import *
import numpy as np

from submission import *



def seven_segment(pattern):

    def to_bool(a):
        if a==1:
            return True
        return False
    

    def hor(d):
        if d:
            print(" _ ")
        else:
            print("   ")
    
    def vert(d1,d2,d3):
        word=""

        if d1:
            word="|"
        else:
            word=" "
        
        if d3:
            word+="_"
        else:
            word+=" "
        
        if d2:
            word+="|"
        else:
            word+=" "
        
        print(word)

    

    pattern_b=list(map(to_bool,pattern))

    hor(pattern_b[0])
    vert(pattern_b[1],pattern_b[2],pattern_b[3])
    vert(pattern_b[4],pattern_b[5],pattern_b[6])

    number=0
    for i in range(0,4):
        if pattern_b[7+i]:
            number+=pow(2,i)
    print(int(number))
        
submission=Submission("Chanthru_Uthaya-Shankar")
submission.header("Chanthru Uthaya-shankar")


def initalise_matrix(patterns):
    weights= np.zeros((11,11))
    N = len(patterns)
    for i in range(weights.shape[0]):
        for j in range(weights.shape[1]):
            sum = float(0)
            for pattern in patterns:
                if(i != j):
                    sum += float(pattern[i]*pattern[j])  
            weights[i][j] = float(sum/N)
    return weights

def h(sum):
    if(sum > 0):
        return 1
    else:
        return -1

def evolve(weights, pattern):
    temp_pattern = pattern[:]
    for i in range(len(pattern)):
        sum = 0
        for j in range(weights.shape[0]):
            sum += weights[i][j]*temp_pattern[j]
        pattern[i] = h(sum)
    return temp_pattern


def converge(pattern, weights):
    temp_pattern = evolve(weights, pattern)
    submission.seven_segment(pattern)
    while(temp_pattern != pattern):
        temp_pattern = evolve(weights, pattern)
        submission.seven_segment(pattern)


six=[1,1,-1,1,1,1,1,-1,1,1,-1]
three=[1,-1,1,1,-1,1,1,1,1,-1,-1]
one=[-1,-1,1,-1,-1,1,-1,1,-1,-1,-1]

patterns = [six, three, one]

seven_segment(three)
seven_segment(six)
seven_segment(one)

weight_matrix = initalise_matrix(patterns)

##this assumes you have called your weight matrix "weight_matrix"
submission.section("Weight matrix")
submission.matrix_print("W",weight_matrix)

print("test1")
submission.section("Test 1")

test=[1,-1,1,1,-1,1,1,-1,-1,-1,-1]



print("done test1")

#seven_segment(test)
converge(test, weight_matrix)
submission.seven_segment(test)
##for COMSM0027

##where energy is the energy of test
#submission.qquad()
#submission.print_number(energy)

##this prints a space
submission.qquad()

#here the network should run printing at each step
#for the final submission it should also output to submission on each step

print("test2")
submission.section("Test 2")

test=[1,1,1,1,1,1,1,-1,-1,-1,-1]

#print("done test2")

#seven_segment(test)

converge(test, weight_matrix)

submission.seven_segment(test)

##for COMSM0027
##where energy is the energy of test
#submission.qquad()
#submission.print_number(energy)

##this prints a space
submission.qquad()

#here the network should run printing at each step
#for the final submission it should also output to submission on each step


submission.bottomer()
