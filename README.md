INTRODUCTION:
	
This research project was conducted for Dr. Sriram Vishwanath at the University of Texas at Austin. The main goal of the project was to use Index Coding to increase the gain of wireless communication compared. The project had a software/algorithm side and a robotics side. The software/algorithm side was in charge of setting up the system to run Index Coding and the experiment on the robotics side. The robotics side was in charge of building small robot cars that could act as receivers and would move around to simulate them. I was working on the software/algorithm side and wrote the code for the MATLAB and python simulations as well as the Python version of the Index Coding and SVD based Decoding which will be talked about later. 
	We used the Alternate Projection(AP) method of Index Coding from the paper by Xiao Huang and Salim El Rouayheb. The pdf to their paper is also in the repo. This algorithm allows for a NxM sized matrix to be rank reduced via alternate projections. For our experiment, we decided to use square NxN sized matrices. The paper explained the algorithm and provided the code for the MATLAB implementation. 

INDEX CODING:

The idea of index coding is to reduce the number of messages being sent to receivers that want their desire message. Let’s imagine we have 5 receivers and 1 transmitter. If we send 5 individual messages that correspond to each receiver’s wanted message. For so we say we can T1 for receiver 1 and T2 for receiver 2 and so on. Now let’s say that after the initial sending of T1-T5 no receiver got their intended message. We would need to resend all those messages. However, receivers may have successfully received other messages that were intended to the other receivers. For example, receiver 1 could have gotten T2 and T4. It is important that we have side information, meaning messages from different receivers. The receivers send back to the transmitter acknowledges of messages they received. The transmitter can construct a NxN matrix with this information. The rows will represent receivers and the columns would represent the messages. So row 1 of the matrix would hold the information that receiver 1 got. If receiver one got T2 and T4, the row would look like [0 2 0 2 0]. We put 2s in the spots that side information messages are received and 1s in spots that are intended for the receiver. If the diagonal of the matrix has any 1s, that means that the receiver is happy and no longer needs their message resent. The matrix will lose the receiver’s row and column. Now once we have the final matrix with only 2s, we input it into the AP index coding algorithm. The algorithm will find the minimum rank of the matrix and fill in the 2s spots of the matrix with values. So if we had a 5x5 matrix, we could potential reduce it to a rank of less than 5. The minimum rank is determined by how much side information the matrix has. More side information means a lower minimum rank can be achieved. Now that is rank is smaller than the size of the matrix, we can send less messages to the receivers. What we send over instead of the messages depends on the scheme we use. We used the SVD decoding scheme for this.   

SVD DECODING SCHEME:

	The SVD decoding scheme was used because of how simple it is. It takes no time to run compared to trying to use Gaussian elimination. The algorithm encodes a message vector called X. We send each message in the vector separately over to the receivers until everyone receiver has X. We also send the updated matrix M to every receiver after it has gone through AP index coding. The only downside to this method is that all the receivers have to get every message in X and M. Another small issue with this method is that after the receiver decodes it’s original message with the X vector and M matrix, it has small loss of precision, usually around 10^-5 off. In real practice, this issue would need to be resolved. 

MATLAB System:

	For the MATLAB system simulation guide, there is a pdf with slides in the MATLAB folder. Here I will describe the layout of the system. This part of the project was mainly aimed to help me understand the project more and outline what we needed to do. The system was broken into several modules that simulated a different part of the system. A random message would be created, then with a certain probability, a matrix M would be composed with side information. Then AP Index Coding would run. Afterwards the message would be encoded and decoded with the SVD based decoding scheme. This is also explained in the slides posted in the MATLAB directory.

PYTHON SIMULATION:
	
	The python simulation gives theoretical data for different sized matrices and probability of side information and probability of message transmission. This is further discussed in the pdf of slides.

FILES: 

SVD.py
	Routines:
	
	APIndexCode(M): This routine is the structure of the index code. It inputs a matrix M with side information and outputs the minimum rank and the updated matrix M. Within the function it calls dirSVDAP multiple times until it converges at the minimum rank. 

	dirSVDAP(r, N, OneIndex, ZeroIndex, Rnk): This function is called by APIndexCode. Further detail on how the algorithm work is in the research paper pdf in the repo.

	getVals(M): This is also called by APIndexCode. It gets the indices of ones and zeros of the matrix M.

	reduce(acks): This inputs a matrix and reduces the amount of side information within it by some set probability within the function. This was used in the experiment if too much side information was present. 

	prepare(N, p): This constructs a NxN sized matrix with p probability of having side information. This returns that matrix, M. This is used in the test.

	test(): This has a set NxN sized matrix that is run with AP index code for a range of probability of side information.

	singletest(N, p): This runs a single test of a NxN sized matrix with p probability with AP index coding. 

	

SVD_enc.py

	Routines:

	SVDdec (M, Xp, row, A): This is done on the receiver side. It inputs matrix M, message vector Xp, the receiver’s number, and the receiver’s side information vector. With this information it is able to decode the initial message meant for the receiver.

	SVDenc(M, T, minRank): This is done on the transmitter side. It inputs matrix M, message vector T, and the minRank of M. It outputs a encoded message vector called X. 

	test(N): This tests a single run of AP index coding with SVD decoding. It basically runs singletest() from SVD.py and then runs SVDenc and SVDdec. Used to see if SVD decoded the message correctly.

	ready(M): This is used on the receiver side. It waits until matrix M is sent to the receiver. Then it finds how many X messages are going to be sent over. The receiver initially doesn’t know how many messages are in the X vector, but this allows the receiver to be able to know how many messages it needs to get from the transmitter.

	test_ready(N, p): This is just a test to see if ready is working correctly.

Simulation.py

	Routines:

	simulation_APIC(N, p): One run simulation of AP index coding. It initializes N number of nodes with probability p of receiving messages. Returns number of rounds and count of messages.

	simulation_RR(N, p): One run simulation of Round Robin. It initializes N number of nodes with probability p of receiving messages. Returns number of rounds and count of messages.



	test_sim(N): Tests both RR and APIC simulations a set number of times with a range of probabilities. It counts how many messages are sent and how many rounds it takes. 

	sim_test_once(N): Tests both RR and APIC once instead of with multiple P. 

	sim_test_2(): Tests RR and APIC with different sized matrices with set P.

	
	

	

