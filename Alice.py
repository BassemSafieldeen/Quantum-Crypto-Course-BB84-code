#
# Copyright (c) 2017, Stephanie Wehner and Axel Dahlberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Stephanie Wehner, QuTech.
# 4. Neither the name of the QuTech organization nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from SimulaQron.cqc.pythonLib.cqc import *

import random
import numpy as np


#####################################################################################################
#
# main
#
def main():
	n = 128
	basis_arr = [] 
	m_arr = [] 
	Alice=CQCConnection("Alice")

	for i in range(0,n):
		q=Alice.createEPR("Eve")
		b=random.randint(0,1)
		if b==1:
			q.H()
			m=q.measure(inplace=False)
		else:
			m=q.measure(inplace=False)
		
		basis_arr.append(b)
		m_arr.append(m)

	print("Alice basis   ---AAA>>> ",basis_arr)
	print("Alice measure ---AAA>>> ",m_arr)

	Alice.startClassicalServer()
	bobs_conf = Alice.recvClassical()[0]
	if bobs_conf == n:
		print("Alice send her basis")
		Alice.sendClassical("Bob",basis_arr)
		bob_bas = Alice.recvClassical()
		print("Alice receives Bob's basis")

	common_bas = []
	m_arr_filtered = []
	for i in range(0,len(basis_arr)):
		if(basis_arr[i]==bob_bas[i]):
			common_bas.append(basis_arr[i])
			m_arr_filtered.append(m_arr[i])
	print("Alice's filtered = ", m_arr_filtered)


	subset_seed = np.random.randint(0,2,size=len(m_arr_filtered))
	subset = []
	count = 0
	for i in range(0, len(m_arr_filtered)):
		if(subset_seed[i]==1):
			subset.append(m_arr_filtered[i-count])
			del(m_arr_filtered[i-count])
			count+=1
	Alice.sendClassical("Bob", subset_seed)
	Bobs_subset = Alice.recvClassical()

	error_count = 0
	#print("subset_seed = ",subset_seed)
	print("subset = ", subset)
	for i in range(0, len(subset)):
		if(subset[i]!=Bobs_subset[i]):
			error_count+=1
	print("error rate is ", error_count / len(subset))
#==========================================================================
	if error_count / len(subset) > 0.1 :
		print("Ohh...? The error is too high. We still show their keys but they should abort : their keys are likely to be different.")
	seed_len = len(m_arr_filtered)
	r = np.random.randint(0,2, size=seed_len)
	#  print(r)	
	
	Alice.sendClassical("Bob",r)
	key = 0
	for i in range(0,len(r)):
		key = key + m_arr_filtered[i]*r[i]
	key = key%2
	print("Alice's key = ",key)
	
	Alice.closeClassicalServer()
	Alice.close()


##################################################################################################
main()

