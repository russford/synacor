#include <iostream>

using namespace std;

int* output;
int r7;
const int N = 32768*5;

int recursive (int m, int n)
{
	int hash = m*32768+n;
	if (output[hash] < 32768) return output[hash];
	int a;
	if (m == 0)
	{
		a = (n+1)%32768;
	}
	else if (n == 0)
	{
		a = recursive(m-1, r7);
	}
	else 
	{
		a = recursive(m, n-1);
		a = recursive (m-1, a);
	}
	return (output[hash] = a);
}

int main(int argc, char* argv[])
{
	int i, j, a;
	output = new int[32768*5];
	for (i=1; i<32768; ++i)
	{
		if (i%100 == 0) cout << "completed " << i << endl;
		for (j=0; j<N; ++j) output[j] = 32768;
		r7 = i;
		a = recursive (4,1);
		if (a == 6)
		{
			cout << "i = " << i << endl;
			return 1;
		}
	}
	return 0;
}