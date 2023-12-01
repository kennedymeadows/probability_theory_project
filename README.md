# MATH 407 - Probability Theory - Final Project

## Problem One

For this problem I utilized the numpy library to achieve a sufficiently random distribution of dots on my sphere and the plotly library in order to plot my points in 3d and allow for manipulation of the sphere.

![Sphere](images/sphere.png)

For the estimation of the size of Antarctica I eyeballed it on the sphere after it was plotted and ended up with a satisfyingly close-to-truth estimation of its size.

![Antarctica](images/antarctica.png)

For the estimation of the size of Africa I split it into two regions, the narrower Southern region and the wider Northern region, and looked at the approximate latitudes and longitudes. This also came up with a pretty good estimation.

![Africa](images/africa.png)

My computer is also pretty powerful so I was able to play around with different amounts of dots being distributed and see how that affects the estimation.

```
Calculating for 1000 points:
Estimated area of Antarctica with 1000 points: 23,974,700.00 square kilometers (roughly 23.97 million km²)
Estimated area of Africa with 1000 points: 12,752,500.00 square kilometers (roughly 12.75 million km²)

Calculating for 10000 points:
Estimated area of Antarctica with 10000 points: 27,851,460.00 square kilometers (roughly 27.85 million km²)
Estimated area of Africa with 10000 points: 11,732,300.00 square kilometers (roughly 11.73 million km²)

Calculating for 100000 points:
Estimated area of Antarctica with 100000 points: 30,218,324.00 square kilometers (roughly 30.22 million km²)
Estimated area of Africa with 100000 points: 12,563,763.00 square kilometers (roughly 12.56 million km²)

Calculating for 1000000 points:
Estimated area of Antarctica with 1000000 points: 29,465,416.40 square kilometers (roughly 29.47 million km²)
Estimated area of Africa with 1000000 points: 12,354,622.00 square kilometers (roughly 12.35 million km²)
```

## Problem Two

I defined three binary string generators, one that generates a non-random string made up of repeating patterns of "1100", and then two that generate random strings using Copeland-Erdos and Champernowne.

I chose to include six different tests of random tests, each with their own strengths and weaknesses.

#### Test 1: Frequency (Monobit) Test

This test measures the balance between the number of 0's and 1's. It is good at identifying sequences with a significant imbalance, but not effective for patterns or structural randomness

$$
\text{Frequency Score} = \frac{|\text{# of 1's} - \text{# of 0's}|}{\text{# of bits}}
$$

#### Test 2: Runs Test

Evaluates the occurrences of uninterrupted sequences of identical bits. It is useful for detecting sequences with unusual runs, but not for picking up on patterns such as the one in my non-random string generator.

#### Test 3: Autocorrelation Test

Measures the correlation between the sequence and itself shifted by one position. This was one of the most effective tests for my non-random string generator as I currently have it set.

$$
\text{Autocorrelation} = \frac{\text{# matching bits at given shift}}{\text{# of comparisons}}
$$

#### Test 4: Longest Run of Ones in a Block Test

Another test for runs, but this one detects runs within blocks of specified length. Useful for spotting sequences where 1s cluster unusually, but less effective for sequences with balanced but structured patterns. Mixed results in my tests.

This test divides the sequence into blocks and finds the longest run of 1s in each block. The average of these longest runs is then calculated. This test checks for the occurrence of longer runs than expected in a random sequence.

#### Test 5: Poker Test

By far the most effective test for my non-random string generator. It correctly identified the non-random string as being non-random and the random strings as being random.

$$
\text{Poker Score} = (2^{\text{block size}}) \times \frac{\sum(\text{frequency of each block}^2)}{# of blocks} - # of blocks
$$

#### Test 6: Shannon Entropy Test

I based this one off of a [Stack Overflow](https://stackoverflow.com/questions/3097949/how-can-i-determine-the-statistical-randomness-of-a-binary-string) post. This is another test which struggles with structured patterns in non-random strings such as the ones produced by my non-random generator.

$$
H = -p\log_2(p) - (1-p)\log_2(1-p)
$$

where $p$ is the proportion of 1s in the sequence. This formula calculates the average amount of information contained in each message. In a completely random sequence (where 0s and 1s occur with equal probability, i.e. $p = 0.5$), Shannon Entropy reaches its maximum value of 1.

--------------------

### Test Results - Length 1000

I generated strings of length 1000 for each of the three generators.

#### Non-Random String

```
Analyzing sequence: 1101110010111011110001001101010111100110111101111100001000110010100111010010101101101011111000110011101011011111001110111110111111000001000011000101000111001001001011001101001111010001010011010101010111011001011011011101011111100001100011100101100111101001101011101101101111110001110011110101110111111001111011111101111111000000100000110000101000011100010010001011000110100011110010001001001100101010010111001100100110110011101001111101000010100011010010101001110101001010101101011010101111011000101100110110101011011101110010111011011110101111111000001100001110001011000111100100110010111001101100111110100011010011101010110101111011001101101110111011011111110000111000111100101110011111010011101011110110111011111110001111001111101011110111111100111110111111101111111100000001000000110000010100000111000010010000101100001101000011110001000100010011000101010001011100011001000110110001110100011111001000010010001100100101001001110010100100101011001011010010111100110001001100110011010100110111001110
Frequency (Monobit) Test Result: 0.088
Runs Test Result: 502
Autocorrelation Test Result (Shift=2): 0.48597194388777554
Longest Run of Ones in a Block Test Result (Block Size=128):
  Mean: 5.857142857142857
Poker Test Result (Block Size=4): 71.536
Shannon Entropy: 0.9944066525627802
```

#### Copeland-Erdos String

```
Analyzing sequence: 1011101111101111011000110011101111110111111100101101001101011101111110101111011111101100001110001111001001100111110100111011001110000111001011100111110101111011011110001111111110000011100010011000101110010101100101111001110110100011101001111010110110110011101101011011111111000001110001011100011111010011110111111110001111100101111010011110111111110001111110111000000011000001111000011011000011111000101011000110011000110111001001011001100111001101111001110011001111011010010111010100011010110111010111011011000011011001111011011111011101011011110111011111111100001011100011011100100011100110011101000111101001011101011111101100011101101111101110111110000011110010011110011011110011111110100111110111111111001111111010111111100111111101111111111011000001001100000101110000111011000100011100010110110001100111000111001100011101110010000011001001011100101000110010101111001011001100101111110011001011001101001100110101110011101111010000001101000001110100001111010001101101001001110100101011010100001101
Frequency (Monobit) Test Result: 0.186
Runs Test Result: 449
Autocorrelation Test Result (Shift=2): 0.47695390781563124
Longest Run of Ones in a Block Test Result (Block Size=128):
  Mean: 7.714285714285714
Poker Test Result (Block Size=4): 53.615999999999985
Shannon Entropy: 0.9748983373999445
```

#### Champernowne String

```
Analyzing sequence: 1101110010111011110001001101010111100110111101111100001000110010100111010010101101101011111000110011101011011111001110111110111111000001000011000101000111001001001011001101001111010001010011010101010111011001011011011101011111100001100011100101100111101001101011101101101111110001110011110101110111111001111011111101111111000000100000110000101000011100010010001011000110100011110010001001001100101010010111001100100110110011101001111101000010100011010010101001110101001010101101011010101111011000101100110110101011011101110010111011011110101111111000001100001110001011000111100100110010111001101100111110100011010011101010110101111011001101101110111011011111110000111000111100101110011111010011101011110110111011111110001111001111101011110111111100111110111111101111111100000001000000110000010100000111000010010000101100001101000011110001000100010011000101010001011100011001000110110001110100011111001000010010001100100101001001110010100100101011001011010010111100110001001100110011010100110111001110
Frequency (Monobit) Test Result: 0.088
Runs Test Result: 502
Autocorrelation Test Result (Shift=2): 0.48597194388777554
Longest Run of Ones in a Block Test Result (Block Size=128):
  Mean: 5.857142857142857
Poker Test Result (Block Size=4): 71.536
Shannon Entropy: 0.9944066525627802
```

--------------------

### Test Results - Length 1,000,000

I decided for another test to generate even longer strings to see how the results shifted.

#### Non-Random String

```
Frequency (Monobit) Test Result: 0.0
Runs Test Result: 500000
Autocorrelation Test Result (Shift=2): 0.0
Longest Run of Ones in a Block Test Result (Block Size=128): 2.0
Poker Test Result (Block Size=4): 3750000.0
Shannon Entropy: 1.0
```

#### Copeland-Erdos String

```
Frequency (Monobit) Test Result: 0.083588
Runs Test Result: 474013
Autocorrelation Test Result (Shift=2): 0.4904029808059616
Longest Run of Ones in a Block Test Result (Block Size=128): 6.430619559651817
Poker Test Result (Block Size=4): 15647.571455999976
Shannon Entropy: 0.9949540927104001
```

#### Champernowne String

```
Frequency (Monobit) Test Result: 0.060398
Runs Test Result: 498043
Autocorrelation Test Result (Shift=2): 0.501479002958006
Longest Run of Ones in a Block Test Result (Block Size=128): 5.1552739375320025
Poker Test Result (Block Size=4): 6801.811455999996
Shannon Entropy: 0.9973669808997596
```

--------------------

### Conclusion

The results of the tests were sastisfactory, with the non-random string being correctly identified.. when you look at the *correct test* that is. This accentuates the importance of having the background in probability in order to interpret the output of the tests correctly and see how much weight to give each test result. Understanding the strengths and limitations of each test allows for a more nuanced assessment. For instance, knowing that Shannon Entropy is excellent for assessing overall distribution but less so for pattern recognition, or recognizing that the Autocorrelation Test's effectiveness varies with the shift value, is crucial for drawing accurate conclusions.