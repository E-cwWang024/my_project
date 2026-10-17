"""
This Python file is a basic test for the new project.
I will create some simple vectors and perform a quick opreation.
"""
import numpy as np

vectorA = np.array([1,2,3], dtype = np.int32)
vectorB = np.array([2,3,4], dtype = np.int32)

vectorC = vectorA + vectorB

print(vectorA)
print(vectorB)
print(vectorC)