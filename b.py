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
	Bob=CQCConnection("Bob")

	n = 128
	m_arr = []
	basis_arr = []
        
	for i in range(0,n):
		q=Bob.recvQubit()
		b=random.randint(0,1)
		if b==1:
			q.H()
			m=q.measure(inplace=False)
		else:
			m=q.measure(inplace=False)
		basis_arr.append(b)
		m_arr.append(m)

	print("Bob basis     ---BBB>>> ",basis_arr)
	print("Bob measure   ---BBB>>> ",m_arr)
	
	Bob.openClassicalChannel("Alice")
	Bob.sendClassical("Alice",n)
	
	alice_bas = Bob.recvClassical()
	print("Bob receives Alice's basis")

	print("Bob sends his basis")
	Bob.sendClassical("Alice",basis_arr)
	
	common_bas = []
	m_arr_filtered = []
	for i in range(0,len(basis_arr)):
		if(basis_arr[i]==alice_bas[i]):
			common_bas.append(basis_arr[i])
			m_arr_filtered.append(m_arr[i])
	print("Bob's filtered = ",m_arr_filtered)

	subset_seed = Bob.recvClassical()
	subset_seed_l = []
	for i in range(0,len(subset_seed)):
		if(i%8==0):
			subset_seed_l.append(subset_seed[i])
	subset = []
	count = 0
	for i in range(0, len(m_arr_filtered)):
		if(subset_seed_l[i]==1):
			subset.append(m_arr_filtered[i-count])
			del(m_arr_filtered[i-count])
			count+=1
	#print("what Bob send = ", subset)
	Bob.sendClassical("Alice",subset)
#===========================================================
	key = 0
	r = Bob.recvClassical()
	r_l = []
	for i in range(0,len(r)):
		if(i%8==0):
			r_l.append(r[i])
	#print("r_1=",r_l)
	for i in range(0,len(r_l)):
		key = key + m_arr_filtered[i]*r_l[i]
	key = key%2
	print("Bob's key = ",key)
	Bob.closeClassicalChannel("Alice")
	Bob.close()


##################################################################################################
main()

