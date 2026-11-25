# Statistical tests

Models: gpt-4o-mini, gpt-4o-mini (paraphrase), gpt-3.5-turbo (paper); humans included

## Model (a) vs human subjects (b), baseline: two-sided two-sample t-tests

| model | domain | measure | mean_a | mean_b | n_a | n_b | t | p |
|---|---|---|---|---|---|---|---|---|
| gpt-4o-mini | risk | CCEI | 0.9997 | 0.9804 | 100 | 115 | 4.489 | 1.717e-05 |
| gpt-4o-mini | risk | spearman | -0.9732 | -0.826 | 100 | 115 | -5.782 | 6.445e-08 |
| gpt-4o-mini | risk | HMI | 0.9964 | 0.9677 | 100 | 115 | 5.67 | 9.228e-08 |
| gpt-4o-mini | risk | MPI_mean | 0.0005 | 0.02116 | 100 | 115 | -5.227 | 7.82e-07 |
| gpt-4o-mini | risk | MCI | 1.429e-05 | 0.002536 | 100 | 115 | -2.777 | 0.006423 |
| gpt-4o-mini | time | CCEI | 0.9988 | 0.9852 | 100 | 115 | 3.194 | 0.001804 |
| gpt-4o-mini | time | spearman | -0.9543 | -0.7884 | 100 | 115 | -12.93 | 1.261e-25 |
| gpt-4o-mini | time | HMI | 0.9932 | 0.983 | 100 | 115 | 2.532 | 0.0123 |
| gpt-4o-mini | time | MPI_mean | 0.002143 | 0.01474 | 100 | 115 | -3.466 | 0.0007289 |
| gpt-4o-mini | time | MCI | 6.014e-05 | 0.001617 | 100 | 115 | -2.812 | 0.005801 |
| gpt-4o-mini | social | CCEI | 0.9983 | 0.9674 | 100 | 115 | 5.039 | 1.718e-06 |
| gpt-4o-mini | social | spearman | -0.9782 | -0.681 | 100 | 115 | -10.46 | 2.093e-18 |
| gpt-4o-mini | social | HMI | 0.9948 | 0.9482 | 100 | 115 | 6.49 | 1.922e-09 |
| gpt-4o-mini | social | MPI_mean | 0.002278 | 0.02855 | 100 | 115 | -6.058 | 1.569e-08 |
| gpt-4o-mini | social | MCI | 6.952e-05 | 0.005016 | 100 | 115 | -2.899 | 0.004489 |
| gpt-4o-mini | food | CCEI | 0.9997 | 0.9631 | 100 | 115 | 5.988 | 2.522e-08 |
| gpt-4o-mini | food | spearman | -0.9813 | -0.673 | 100 | 115 | -9.613 | 2.155e-16 |
| gpt-4o-mini | food | HMI | 0.9968 | 0.9437 | 100 | 115 | 8.458 | 7.297e-14 |
| gpt-4o-mini | food | MPI_mean | 0.0004865 | 0.03398 | 100 | 115 | -7.897 | 1.913e-12 |
| gpt-4o-mini | food | MCI | 1.068e-05 | 0.004733 | 100 | 115 | -3.905 | 0.0001598 |
| gpt-4o-mini (paraphrase) | risk | CCEI | 0.9999 | 0.9804 | 100 | 115 | 4.537 | 1.42e-05 |
| gpt-4o-mini (paraphrase) | risk | spearman | -0.9808 | -0.826 | 100 | 115 | -6.081 | 1.601e-08 |
| gpt-4o-mini (paraphrase) | risk | HMI | 0.9964 | 0.9677 | 100 | 115 | 5.67 | 9.228e-08 |
| gpt-4o-mini (paraphrase) | risk | MPI_mean | 0.000452 | 0.02116 | 100 | 115 | -5.242 | 7.348e-07 |
| gpt-4o-mini (paraphrase) | risk | MCI | 5.372e-06 | 0.002536 | 100 | 115 | -2.787 | 0.006242 |
| gpt-4o-mini (paraphrase) | time | CCEI | 0.9986 | 0.9852 | 100 | 115 | 3.066 | 0.002654 |
| gpt-4o-mini (paraphrase) | time | spearman | -0.9773 | -0.7884 | 100 | 115 | -15.38 | 4.924e-30 |
| gpt-4o-mini (paraphrase) | time | HMI | 0.9952 | 0.983 | 100 | 115 | 3.146 | 0.002017 |
| gpt-4o-mini (paraphrase) | time | MPI_mean | 0.004493 | 0.01474 | 100 | 115 | -2.159 | 0.03196 |
| gpt-4o-mini (paraphrase) | time | MCI | 5.693e-05 | 0.001617 | 100 | 115 | -2.813 | 0.005778 |
| gpt-4o-mini (paraphrase) | social | CCEI | 0.9999 | 0.9674 | 100 | 115 | 5.328 | 5.059e-07 |
| gpt-4o-mini (paraphrase) | social | spearman | -0.9806 | -0.681 | 100 | 115 | -10.56 | 1.291e-18 |
| gpt-4o-mini (paraphrase) | social | HMI | 0.9984 | 0.9482 | 100 | 115 | 7.074 | 1.191e-10 |
| gpt-4o-mini (paraphrase) | social | MPI_mean | 0.0002835 | 0.02855 | 100 | 115 | -6.63 | 1.158e-09 |
| gpt-4o-mini (paraphrase) | social | MCI | 5.553e-06 | 0.005016 | 100 | 115 | -2.937 | 0.004009 |
| gpt-4o-mini (paraphrase) | food | CCEI | 0.9997 | 0.9631 | 100 | 115 | 5.981 | 2.598e-08 |
| gpt-4o-mini (paraphrase) | food | spearman | -0.9791 | -0.673 | 100 | 115 | -9.543 | 3.118e-16 |
| gpt-4o-mini (paraphrase) | food | HMI | 0.9968 | 0.9437 | 100 | 115 | 8.458 | 7.297e-14 |
| gpt-4o-mini (paraphrase) | food | MPI_mean | 0.0007823 | 0.03398 | 100 | 115 | -7.795 | 3.011e-12 |
| gpt-4o-mini (paraphrase) | food | MCI | 1.195e-05 | 0.004733 | 100 | 115 | -3.904 | 0.0001605 |
| gpt-3.5-turbo (paper) | risk | CCEI | 0.9981 | 0.9804 | 100 | 115 | 3.976 | 0.0001147 |
| gpt-3.5-turbo (paper) | risk | spearman | -0.9843 | -0.826 | 100 | 115 | -6.144 | 1.075e-08 |
| gpt-3.5-turbo (paper) | risk | HMI | 0.9968 | 0.9677 | 100 | 115 | 5.557 | 1.309e-07 |
| gpt-3.5-turbo (paper) | risk | MPI_mean | 0.002606 | 0.02116 | 100 | 115 | -4.351 | 2.486e-05 |
| gpt-3.5-turbo (paper) | risk | MCI | 0.0002254 | 0.002536 | 100 | 115 | -2.501 | 0.01371 |
| gpt-3.5-turbo (paper) | time | CCEI | 0.9972 | 0.9852 | 100 | 115 | 2.657 | 0.00879 |
| gpt-3.5-turbo (paper) | time | spearman | -0.9664 | -0.7884 | 100 | 115 | -13.36 | 1.068e-27 |
| gpt-3.5-turbo (paper) | time | HMI | 0.9932 | 0.983 | 100 | 115 | 2.241 | 0.0261 |
| gpt-3.5-turbo (paper) | time | MPI_mean | 0.004518 | 0.01474 | 100 | 115 | -2.452 | 0.01515 |
| gpt-3.5-turbo (paper) | time | MCI | 0.0004264 | 0.001617 | 100 | 115 | -1.847 | 0.06633 |
| gpt-3.5-turbo (paper) | social | CCEI | 0.9971 | 0.9674 | 100 | 115 | 4.806 | 4.47e-06 |
| gpt-3.5-turbo (paper) | social | spearman | -0.9505 | -0.681 | 100 | 115 | -9.44 | 4.415e-16 |
| gpt-3.5-turbo (paper) | social | HMI | 0.9912 | 0.9482 | 100 | 115 | 5.881 | 3.214e-08 |
| gpt-3.5-turbo (paper) | social | MPI_mean | 0.004479 | 0.02855 | 100 | 115 | -5.425 | 2.654e-07 |
| gpt-3.5-turbo (paper) | social | MCI | 0.0001285 | 0.005016 | 100 | 115 | -2.864 | 0.004979 |
| gpt-3.5-turbo (paper) | food | CCEI | 0.9995 | 0.9631 | 100 | 115 | 5.943 | 3.099e-08 |
| gpt-3.5-turbo (paper) | food | spearman | -0.9917 | -0.673 | 100 | 115 | -9.94 | 3.769e-17 |
| gpt-3.5-turbo (paper) | food | HMI | 0.9964 | 0.9437 | 100 | 115 | 8.346 | 1.178e-13 |
| gpt-3.5-turbo (paper) | food | MPI_mean | 0.001073 | 0.03398 | 100 | 115 | -7.723 | 4.337e-12 |
| gpt-3.5-turbo (paper) | food | MCI | 1.952e-05 | 0.004733 | 100 | 115 | -3.898 | 0.0001642 |


## Model baseline CCEI vs literature mean 0.918: one-sample t-tests

| model | domain | mean | mu | n | t | p |
|---|---|---|---|---|---|---|
| gpt-4o-mini | risk | 0.9997 | 0.918 | 100 | 458.4 | 1.634e-166 |
| gpt-4o-mini | time | 0.9988 | 0.918 | 100 | 193.1 | 2.124e-129 |
| gpt-4o-mini | social | 0.9983 | 0.918 | 100 | 110.2 | 2.103e-105 |
| gpt-4o-mini | food | 0.9997 | 0.918 | 100 | 648.5 | 2.019e-181 |
| gpt-4o-mini (paraphrase) | risk | 0.9999 | 0.918 | 100 | 1309 | 1.281e-211 |
| gpt-4o-mini (paraphrase) | time | 0.9986 | 0.918 | 100 | 78.33 | 7.031e-91 |
| gpt-4o-mini (paraphrase) | social | 0.9999 | 0.918 | 100 | 839.2 | 1.672e-192 |
| gpt-4o-mini (paraphrase) | food | 0.9997 | 0.918 | 100 | 427.9 | 1.479e-163 |
| gpt-3.5-turbo (paper) | risk | 0.9981 | 0.918 | 100 | 66.05 | 1.1e-83 |
| gpt-3.5-turbo (paper) | time | 0.9972 | 0.918 | 100 | 52.58 | 3.805e-74 |
| gpt-3.5-turbo (paper) | social | 0.9971 | 0.918 | 100 | 75.58 | 2.272e-89 |
| gpt-3.5-turbo (paper) | food | 0.9995 | 0.918 | 100 | 385.8 | 4.146e-159 |


## Within model: baseline (a) vs variation (b)

| model | condition | domain | measure | mean_a | mean_b | n_a | n_b | t | p |
|---|---|---|---|---|---|---|---|---|---|
| gpt-4o-mini | temp_0.5 | risk | CCEI | 0.9997 | 0.9991 | 100 | 100 | 1.202 | 0.2313 |
| gpt-4o-mini | temp_0.5 | risk | spearman | -0.9732 | -0.9757 | 100 | 100 | 1.073 | 0.2846 |
| gpt-4o-mini | temp_0.5 | time | CCEI | 0.9988 | 0.9965 | 100 | 100 | 1.724 | 0.08729 |
| gpt-4o-mini | temp_0.5 | time | spearman | -0.9543 | -0.9535 | 100 | 100 | -0.1151 | 0.9084 |
| gpt-4o-mini | temp_0.5 | social | CCEI | 0.9983 | 0.9976 | 100 | 100 | 0.574 | 0.5667 |
| gpt-4o-mini | temp_0.5 | social | spearman | -0.9782 | -0.9748 | 100 | 100 | -1.236 | 0.218 |
| gpt-4o-mini | temp_0.5 | food | CCEI | 0.9997 | 0.9993 | 100 | 100 | 1.39 | 0.1668 |
| gpt-4o-mini | temp_0.5 | food | spearman | -0.9813 | -0.9773 | 100 | 100 | -1.878 | 0.06189 |
| gpt-4o-mini | temp_1 | risk | CCEI | 0.9997 | 0.9993 | 100 | 100 | 0.8606 | 0.391 |
| gpt-4o-mini | temp_1 | risk | spearman | -0.9732 | -0.9733 | 100 | 100 | 0.02484 | 0.9802 |
| gpt-4o-mini | temp_1 | time | CCEI | 0.9988 | 0.9942 | 100 | 100 | 2.278 | 0.02472 |
| gpt-4o-mini | temp_1 | time | spearman | -0.9543 | -0.9518 | 100 | 100 | -0.4005 | 0.6892 |
| gpt-4o-mini | temp_1 | social | CCEI | 0.9983 | 0.9973 | 100 | 100 | 0.4515 | 0.6524 |
| gpt-4o-mini | temp_1 | social | spearman | -0.9782 | -0.971 | 100 | 100 | -0.8593 | 0.392 |
| gpt-4o-mini | temp_1 | food | CCEI | 0.9997 | 0.999 | 100 | 100 | 1.107 | 0.2709 |
| gpt-4o-mini | temp_1 | food | spearman | -0.9813 | -0.9786 | 100 | 100 | -1.434 | 0.1532 |
| gpt-4o-mini | price_framing | risk | CCEI | 0.9997 | 0.9926 | 100 | 100 | 3.223 | 0.001712 |
| gpt-4o-mini | price_framing | risk | spearman | -0.9732 | -0.9557 | 100 | 100 | -5.674 | 5.986e-08 |
| gpt-4o-mini | price_framing | time | CCEI | 0.9988 | 0.9986 | 100 | 100 | 0.3395 | 0.7346 |
| gpt-4o-mini | price_framing | time | spearman | -0.9543 | -0.9526 | 100 | 100 | -0.3213 | 0.7483 |
| gpt-4o-mini | price_framing | social | CCEI | 0.9983 | 0.9993 | 100 | 100 | -1.325 | 0.1876 |
| gpt-4o-mini | price_framing | social | spearman | -0.9782 | -0.9453 | 100 | 100 | -7.792 | 1.064e-12 |
| gpt-4o-mini | price_framing | food | CCEI | 0.9997 | 0.9984 | 100 | 100 | 2.525 | 0.01298 |
| gpt-4o-mini | price_framing | food | spearman | -0.9813 | -0.9687 | 100 | 100 | -4.916 | 2.089e-06 |
| gpt-4o-mini | discrete | risk | CCEI | 0.9997 | 0.9626 | 100 | 57 | 2.398 | 0.01984 |
| gpt-4o-mini | discrete | risk | spearman | -0.9732 | -0.9862 | 100 | 57 | 2.492 | 0.01511 |
| gpt-4o-mini | discrete | time | CCEI | 0.9988 | 0.969 | 100 | 95 | 3.426 | 0.0009096 |
| gpt-4o-mini | discrete | time | spearman | -0.9543 | -0.9903 | 100 | 95 | 7.104 | 2.745e-11 |
| gpt-4o-mini | discrete | social | CCEI | 0.9983 | 0.9858 | 100 | 94 | 2.493 | 0.01436 |
| gpt-4o-mini | discrete | social | spearman | -0.9782 | -0.9487 | 100 | 94 | -2.787 | 0.006374 |
| gpt-4o-mini | discrete | food | CCEI | 0.9997 | 0.9919 | 100 | 100 | 3.545 | 0.0006004 |
| gpt-4o-mini | discrete | food | spearman | -0.9813 | -0.9333 | 100 | 100 | -4.207 | 5.588e-05 |
| gpt-4o-mini | female | risk | CCEI | 0.9997 | 0.9998 | 100 | 30 | -0.738 | 0.4619 |
| gpt-4o-mini | female | risk | spearman | -0.9732 | -0.972 | 100 | 30 | -0.2024 | 0.8408 |
| gpt-4o-mini | female | time | CCEI | 0.9988 | 0.9987 | 100 | 30 | 0.1504 | 0.8809 |
| gpt-4o-mini | female | time | spearman | -0.9543 | -0.9543 | 100 | 30 | -0.0004453 | 0.9996 |
| gpt-4o-mini | female | social | CCEI | 0.9983 | 0.9985 | 100 | 30 | -0.2039 | 0.839 |
| gpt-4o-mini | female | social | spearman | -0.9782 | -0.9716 | 100 | 30 | -1.818 | 0.07454 |
| gpt-4o-mini | female | food | CCEI | 0.9997 | 0.9995 | 100 | 30 | 0.7044 | 0.4853 |
| gpt-4o-mini | female | food | spearman | -0.9813 | -0.9782 | 100 | 30 | -0.9768 | 0.3342 |
| gpt-4o-mini | male | risk | CCEI | 0.9997 | 0.9999 | 100 | 30 | -0.9617 | 0.338 |
| gpt-4o-mini | male | risk | spearman | -0.9732 | -0.9781 | 100 | 30 | 1.57 | 0.1222 |
| gpt-4o-mini | male | time | CCEI | 0.9988 | 0.9977 | 100 | 30 | 0.53 | 0.5998 |
| gpt-4o-mini | male | time | spearman | -0.9543 | -0.9469 | 100 | 30 | -0.5368 | 0.5949 |
| gpt-4o-mini | male | social | CCEI | 0.9983 | 0.9975 | 100 | 30 | 0.4906 | 0.6263 |
| gpt-4o-mini | male | social | spearman | -0.9782 | -0.9738 | 100 | 30 | -1.11 | 0.2722 |
| gpt-4o-mini | male | food | CCEI | 0.9997 | 0.9996 | 100 | 30 | 0.3459 | 0.7313 |
| gpt-4o-mini | male | food | spearman | -0.9813 | -0.9784 | 100 | 30 | -0.8131 | 0.4211 |
| gpt-4o-mini | young_child | risk | CCEI | 0.9997 | 0.9997 | 100 | 30 | -0.1037 | 0.9177 |
| gpt-4o-mini | young_child | risk | spearman | -0.9732 | -0.9674 | 100 | 30 | -1.183 | 0.2444 |
| gpt-4o-mini | young_child | time | CCEI | 0.9988 | 0.9985 | 100 | 30 | 0.4 | 0.6909 |
| gpt-4o-mini | young_child | time | spearman | -0.9543 | -0.9445 | 100 | 30 | -0.8457 | 0.4031 |
| gpt-4o-mini | young_child | social | CCEI | 0.9983 | 0.999 | 100 | 30 | -0.686 | 0.4946 |
| gpt-4o-mini | young_child | social | spearman | -0.9782 | -0.9724 | 100 | 30 | -1.875 | 0.06489 |
| gpt-4o-mini | young_child | food | CCEI | 0.9997 | 0.9989 | 100 | 30 | 1.415 | 0.1667 |
| gpt-4o-mini | young_child | food | spearman | -0.9813 | -0.9782 | 100 | 30 | -1.131 | 0.2633 |
| gpt-4o-mini | elderly | risk | CCEI | 0.9997 | 1 | 100 | 30 | -1.655 | 0.1009 |
| gpt-4o-mini | elderly | risk | spearman | -0.9732 | -0.9744 | 100 | 30 | 0.3768 | 0.7078 |
| gpt-4o-mini | elderly | time | CCEI | 0.9988 | 0.9977 | 100 | 30 | 0.9534 | 0.3464 |
| gpt-4o-mini | elderly | time | spearman | -0.9543 | -0.9496 | 100 | 30 | -0.3833 | 0.7037 |
| gpt-4o-mini | elderly | social | CCEI | 0.9983 | 0.9988 | 100 | 30 | -0.4862 | 0.6281 |
| gpt-4o-mini | elderly | social | spearman | -0.9782 | -0.9722 | 100 | 30 | -1.611 | 0.113 |
| gpt-4o-mini | elderly | food | CCEI | 0.9997 | 0.9988 | 100 | 30 | 1.384 | 0.1762 |
| gpt-4o-mini | elderly | food | spearman | -0.9813 | -0.9784 | 100 | 30 | -1.005 | 0.3199 |
| gpt-4o-mini | elementary_edu | risk | CCEI | 0.9997 | 0.9999 | 100 | 30 | -1.166 | 0.2458 |
| gpt-4o-mini | elementary_edu | risk | spearman | -0.9732 | -0.9704 | 100 | 30 | -0.5473 | 0.5876 |
| gpt-4o-mini | elementary_edu | time | CCEI | 0.9988 | 0.9977 | 100 | 30 | 0.8054 | 0.426 |
| gpt-4o-mini | elementary_edu | time | spearman | -0.9543 | -0.9474 | 100 | 30 | -0.6704 | 0.5064 |
| gpt-4o-mini | elementary_edu | social | CCEI | 0.9983 | 0.9996 | 100 | 30 | -1.622 | 0.1073 |
| gpt-4o-mini | elementary_edu | social | spearman | -0.9782 | -0.9739 | 100 | 30 | -0.8307 | 0.4112 |
| gpt-4o-mini | elementary_edu | food | CCEI | 0.9997 | 0.9992 | 100 | 30 | 1.049 | 0.3019 |
| gpt-4o-mini | elementary_edu | food | spearman | -0.9813 | -0.9767 | 100 | 30 | -1.112 | 0.2735 |
| gpt-4o-mini | college_edu | risk | CCEI | 0.9997 | 0.9998 | 100 | 30 | -0.6219 | 0.5352 |
| gpt-4o-mini | college_edu | risk | spearman | -0.9732 | -0.9815 | 100 | 30 | 2.113 | 0.04052 |
| gpt-4o-mini | college_edu | time | CCEI | 0.9988 | 0.9981 | 100 | 30 | 0.5619 | 0.5775 |
| gpt-4o-mini | college_edu | time | spearman | -0.9543 | -0.9527 | 100 | 30 | -0.1779 | 0.8596 |
| gpt-4o-mini | college_edu | social | CCEI | 0.9983 | 1 | 100 | 30 | -2.314 | 0.02274 |
| gpt-4o-mini | college_edu | social | spearman | -0.9782 | -0.98 | 100 | 30 | 0.4057 | 0.6869 |
| gpt-4o-mini | college_edu | food | CCEI | 0.9997 | 0.9989 | 100 | 30 | 1.501 | 0.143 |
| gpt-4o-mini | college_edu | food | spearman | -0.9813 | -0.9787 | 100 | 30 | -0.8431 | 0.4037 |
| gpt-4o-mini | asian | risk | CCEI | 0.9997 | 1 | 100 | 30 | -1.602 | 0.1122 |
| gpt-4o-mini | asian | risk | spearman | -0.9732 | -0.9734 | 100 | 30 | 0.05586 | 0.9557 |
| gpt-4o-mini | asian | time | CCEI | 0.9988 | 0.9983 | 100 | 30 | 0.5313 | 0.5977 |
| gpt-4o-mini | asian | time | spearman | -0.9543 | -0.9535 | 100 | 30 | -0.1038 | 0.9177 |
| gpt-4o-mini | asian | social | CCEI | 0.9983 | 0.9989 | 100 | 30 | -0.5892 | 0.5573 |
| gpt-4o-mini | asian | social | spearman | -0.9782 | -0.9735 | 100 | 30 | -1.168 | 0.2487 |
| gpt-4o-mini | asian | food | CCEI | 0.9997 | 1 | 100 | 30 | -2.118 | 0.03672 |
| gpt-4o-mini | asian | food | spearman | -0.9813 | -0.9825 | 100 | 30 | 0.4756 | 0.6361 |
| gpt-4o-mini | african_american | risk | CCEI | 0.9997 | 0.9999 | 100 | 30 | -1.112 | 0.2682 |
| gpt-4o-mini | african_american | risk | spearman | -0.9732 | -0.9755 | 100 | 30 | 0.6566 | 0.5146 |
| gpt-4o-mini | african_american | time | CCEI | 0.9988 | 0.9985 | 100 | 30 | 0.2603 | 0.796 |
| gpt-4o-mini | african_american | time | spearman | -0.9543 | -0.9563 | 100 | 30 | 0.2394 | 0.8118 |
| gpt-4o-mini | african_american | social | CCEI | 0.9983 | 0.9998 | 100 | 30 | -1.978 | 0.05045 |
| gpt-4o-mini | african_american | social | spearman | -0.9782 | -0.9732 | 100 | 30 | -1.291 | 0.2025 |
| gpt-4o-mini | african_american | food | CCEI | 0.9997 | 0.9994 | 100 | 30 | 0.9843 | 0.3313 |
| gpt-4o-mini | african_american | food | spearman | -0.9813 | -0.9773 | 100 | 30 | -1.363 | 0.1796 |
| gpt-4o-mini (paraphrase) | price_framing | risk | CCEI | 0.9999 | 0.9978 | 100 | 100 | 1.674 | 0.09736 |
| gpt-4o-mini (paraphrase) | price_framing | risk | spearman | -0.9808 | -0.9674 | 100 | 100 | -4.683 | 5.537e-06 |
| gpt-4o-mini (paraphrase) | price_framing | time | CCEI | 0.9986 | 0.9947 | 100 | 100 | 2.217 | 0.02789 |
| gpt-4o-mini (paraphrase) | price_framing | time | spearman | -0.9773 | -0.9564 | 100 | 100 | -5.273 | 4.751e-07 |
| gpt-4o-mini (paraphrase) | price_framing | social | CCEI | 0.9999 | 0.9977 | 100 | 100 | 3.79 | 0.0002515 |
| gpt-4o-mini (paraphrase) | price_framing | social | spearman | -0.9806 | -0.9228 | 100 | 100 | -8.533 | 9.516e-14 |
| gpt-4o-mini (paraphrase) | price_framing | food | CCEI | 0.9997 | 0.9948 | 100 | 100 | 1.951 | 0.05381 |
| gpt-4o-mini (paraphrase) | price_framing | food | spearman | -0.9791 | -0.969 | 100 | 100 | -2.843 | 0.005148 |
| gpt-4o-mini (paraphrase) | discrete | risk | CCEI | 0.9999 | 0.8804 | 100 | 100 | 7.698 | 1.059e-11 |
| gpt-4o-mini (paraphrase) | discrete | risk | spearman | -0.9808 | -0.9499 | 100 | 100 | -4.785 | 5.186e-06 |
| gpt-4o-mini (paraphrase) | discrete | time | CCEI | 0.9986 | 0.9787 | 100 | 100 | 5.88 | 3.838e-08 |
| gpt-4o-mini (paraphrase) | discrete | time | spearman | -0.9773 | -0.8949 | 100 | 100 | -8.074 | 1.196e-12 |
| gpt-4o-mini (paraphrase) | discrete | social | CCEI | 0.9999 | 0.9676 | 100 | 100 | 4.19 | 6.055e-05 |
| gpt-4o-mini (paraphrase) | discrete | social | spearman | -0.9806 | -0.8176 | 100 | 100 | -6.571 | 2.304e-09 |
| gpt-4o-mini (paraphrase) | discrete | food | CCEI | 0.9997 | 0.8065 | 100 | 100 | 8.817 | 4.141e-14 |
| gpt-4o-mini (paraphrase) | discrete | food | spearman | -0.9791 | -0.9003 | 100 | 100 | -7.747 | 6.754e-12 |
| gpt-3.5-turbo (paper) | temp_0.5 | risk | CCEI | 0.9981 | 0.9991 | 100 | 100 | -0.7981 | 0.4264 |
| gpt-3.5-turbo (paper) | temp_0.5 | risk | spearman | -0.9843 | -0.9904 | 100 | 100 | 1.388 | 0.168 |
| gpt-3.5-turbo (paper) | temp_0.5 | time | CCEI | 0.9972 | 0.997 | 100 | 100 | 0.08887 | 0.9293 |
| gpt-3.5-turbo (paper) | temp_0.5 | time | spearman | -0.9664 | -0.9659 | 100 | 100 | -0.07968 | 0.9366 |
| gpt-3.5-turbo (paper) | temp_0.5 | social | CCEI | 0.9971 | 0.997 | 100 | 100 | 0.08022 | 0.9362 |
| gpt-3.5-turbo (paper) | temp_0.5 | social | spearman | -0.9505 | -0.9567 | 100 | 100 | 1.463 | 0.1452 |
| gpt-3.5-turbo (paper) | temp_0.5 | food | CCEI | 0.9995 | 0.9995 | 100 | 100 | -0.2091 | 0.8346 |
| gpt-3.5-turbo (paper) | temp_0.5 | food | spearman | -0.9917 | -0.9913 | 100 | 100 | -0.2903 | 0.7719 |
| gpt-3.5-turbo (paper) | temp_1 | risk | CCEI | 0.9981 | 0.9996 | 100 | 100 | -1.229 | 0.2218 |
| gpt-3.5-turbo (paper) | temp_1 | risk | spearman | -0.9843 | -0.9893 | 100 | 100 | 1.144 | 0.2552 |
| gpt-3.5-turbo (paper) | temp_1 | time | CCEI | 0.9972 | 0.9977 | 100 | 100 | -0.3156 | 0.7529 |
| gpt-3.5-turbo (paper) | temp_1 | time | spearman | -0.9664 | -0.9662 | 100 | 100 | -0.04676 | 0.9628 |
| gpt-3.5-turbo (paper) | temp_1 | social | CCEI | 0.9971 | 0.997 | 100 | 100 | 0.1181 | 0.9061 |
| gpt-3.5-turbo (paper) | temp_1 | social | spearman | -0.9505 | -0.957 | 100 | 100 | 1.625 | 0.1063 |
| gpt-3.5-turbo (paper) | temp_1 | food | CCEI | 0.9995 | 0.9996 | 100 | 100 | -0.397 | 0.6918 |
| gpt-3.5-turbo (paper) | temp_1 | food | spearman | -0.9917 | -0.9894 | 100 | 100 | -1.647 | 0.1012 |
| gpt-3.5-turbo (paper) | price_framing | risk | CCEI | 0.9981 | 0.9008 | 100 | 100 | 9.745 | 2.992e-16 |
| gpt-3.5-turbo (paper) | price_framing | risk | spearman | -0.9843 | -0.05342 | 100 | 100 | -33.91 | 5.065e-58 |
| gpt-3.5-turbo (paper) | price_framing | time | CCEI | 0.9972 | 0.8843 | 100 | 100 | 10.91 | 6.637e-19 |
| gpt-3.5-turbo (paper) | price_framing | time | spearman | -0.9664 | -0.1162 | 100 | 100 | -25.78 | 4.143e-47 |
| gpt-3.5-turbo (paper) | price_framing | social | CCEI | 0.9971 | 0.6976 | 100 | 100 | 18.22 | 1.603e-33 |
| gpt-3.5-turbo (paper) | price_framing | social | spearman | -0.9505 | 0.2671 | 100 | 100 | -34.08 | 3.612e-57 |
| gpt-3.5-turbo (paper) | price_framing | food | CCEI | 0.9995 | 0.8936 | 100 | 100 | 11.31 | 1.544e-19 |
| gpt-3.5-turbo (paper) | price_framing | food | spearman | -0.9917 | -0.4992 | 100 | 100 | -13.85 | 6.582e-25 |
| gpt-3.5-turbo (paper) | discrete | risk | CCEI | 0.9981 | 0.8427 | 100 | 100 | 7.121 | 1.697e-10 |
| gpt-3.5-turbo (paper) | discrete | risk | spearman | -0.9843 | -0.5886 | 100 | 100 | -11.05 | 3.952e-19 |
| gpt-3.5-turbo (paper) | discrete | time | CCEI | 0.9972 | 0.9084 | 100 | 100 | 6.342 | 6.396e-09 |
| gpt-3.5-turbo (paper) | discrete | time | spearman | -0.9664 | -0.4968 | 100 | 100 | -17.85 | 5.526e-34 |
| gpt-3.5-turbo (paper) | discrete | social | CCEI | 0.9971 | 0.8707 | 100 | 100 | 5.727 | 1.089e-07 |
| gpt-3.5-turbo (paper) | discrete | social | spearman | -0.9505 | -0.5195 | 100 | 100 | -15.81 | 3.122e-29 |
| gpt-3.5-turbo (paper) | discrete | food | CCEI | 0.9995 | 0.78 | 100 | 100 | 9.586 | 8.756e-16 |
| gpt-3.5-turbo (paper) | discrete | food | spearman | -0.9917 | -0.5334 | 100 | 100 | -15.92 | 4.484e-29 |
| gpt-3.5-turbo (paper) | female | risk | CCEI | 0.9981 | 0.9995 | 100 | 100 | -1.144 | 0.2554 |
| gpt-3.5-turbo (paper) | female | risk | spearman | -0.9843 | -0.9895 | 100 | 100 | 1.139 | 0.2569 |
| gpt-3.5-turbo (paper) | female | time | CCEI | 0.9972 | 0.9982 | 100 | 100 | -0.6833 | 0.4958 |
| gpt-3.5-turbo (paper) | female | time | spearman | -0.9664 | -0.9714 | 100 | 100 | 0.8496 | 0.3972 |
| gpt-3.5-turbo (paper) | female | social | CCEI | 0.9971 | 0.9964 | 100 | 100 | 0.5299 | 0.5969 |
| gpt-3.5-turbo (paper) | female | social | spearman | -0.9505 | -0.957 | 100 | 100 | 1.61 | 0.1095 |
| gpt-3.5-turbo (paper) | female | food | CCEI | 0.9995 | 0.9994 | 100 | 100 | 0.1245 | 0.9011 |
| gpt-3.5-turbo (paper) | female | food | spearman | -0.9917 | -0.9972 | 100 | 100 | 4.298 | 2.762e-05 |
| gpt-3.5-turbo (paper) | male | risk | CCEI | 0.9981 | 0.9998 | 100 | 100 | -1.393 | 0.1666 |
| gpt-3.5-turbo (paper) | male | risk | spearman | -0.9843 | -0.9913 | 100 | 100 | 1.612 | 0.1099 |
| gpt-3.5-turbo (paper) | male | time | CCEI | 0.9972 | 0.9973 | 100 | 100 | -0.1046 | 0.9168 |
| gpt-3.5-turbo (paper) | male | time | spearman | -0.9664 | -0.9661 | 100 | 100 | -0.05366 | 0.9573 |
| gpt-3.5-turbo (paper) | male | social | CCEI | 0.9971 | 0.9974 | 100 | 100 | -0.2257 | 0.8217 |
| gpt-3.5-turbo (paper) | male | social | spearman | -0.9505 | -0.9594 | 100 | 100 | 2.243 | 0.02635 |
| gpt-3.5-turbo (paper) | male | food | CCEI | 0.9995 | 0.9994 | 100 | 100 | 0.08795 | 0.9301 |
| gpt-3.5-turbo (paper) | male | food | spearman | -0.9917 | -0.9987 | 100 | 100 | 6.446 | 1.904e-09 |
| gpt-3.5-turbo (paper) | young_child | risk | CCEI | 0.9981 | 0.9994 | 100 | 100 | -1.064 | 0.2898 |
| gpt-3.5-turbo (paper) | young_child | risk | spearman | -0.9843 | -0.9911 | 100 | 100 | 1.538 | 0.1267 |
| gpt-3.5-turbo (paper) | young_child | time | CCEI | 0.9972 | 0.9971 | 100 | 100 | 0.05047 | 0.9598 |
| gpt-3.5-turbo (paper) | young_child | time | spearman | -0.9664 | -0.9703 | 100 | 100 | 0.6635 | 0.5082 |
| gpt-3.5-turbo (paper) | young_child | social | CCEI | 0.9971 | 0.9974 | 100 | 100 | -0.2316 | 0.8172 |
| gpt-3.5-turbo (paper) | young_child | social | spearman | -0.9505 | -0.9557 | 100 | 100 | 1.196 | 0.2334 |
| gpt-3.5-turbo (paper) | young_child | food | CCEI | 0.9995 | 1 | 100 | 100 | -2.499 | 0.01411 |
| gpt-3.5-turbo (paper) | young_child | food | spearman | -0.9917 | -0.9989 | 100 | 100 | 6.807 | 3.984e-10 |
| gpt-3.5-turbo (paper) | elderly | risk | CCEI | 0.9981 | 0.9995 | 100 | 100 | -1.104 | 0.2723 |
| gpt-3.5-turbo (paper) | elderly | risk | spearman | -0.9843 | -0.99 | 100 | 100 | 1.271 | 0.2063 |
| gpt-3.5-turbo (paper) | elderly | time | CCEI | 0.9972 | 0.9973 | 100 | 100 | -0.106 | 0.9157 |
| gpt-3.5-turbo (paper) | elderly | time | spearman | -0.9664 | -0.9708 | 100 | 100 | 0.7549 | 0.4518 |
| gpt-3.5-turbo (paper) | elderly | social | CCEI | 0.9971 | 0.9981 | 100 | 100 | -0.8916 | 0.3743 |
| gpt-3.5-turbo (paper) | elderly | social | spearman | -0.9505 | -0.9588 | 100 | 100 | 2.038 | 0.04325 |
| gpt-3.5-turbo (paper) | elderly | food | CCEI | 0.9995 | 0.9998 | 100 | 100 | -1.407 | 0.1613 |
| gpt-3.5-turbo (paper) | elderly | food | spearman | -0.9917 | -0.9969 | 100 | 100 | 3.726 | 0.0002535 |
| gpt-3.5-turbo (paper) | elementary_edu | risk | CCEI | 0.9981 | 0.9996 | 100 | 100 | -1.172 | 0.2438 |
| gpt-3.5-turbo (paper) | elementary_edu | risk | spearman | -0.9843 | -0.9907 | 100 | 100 | 1.451 | 0.1494 |
| gpt-3.5-turbo (paper) | elementary_edu | time | CCEI | 0.9972 | 0.9973 | 100 | 100 | -0.06054 | 0.9518 |
| gpt-3.5-turbo (paper) | elementary_edu | time | spearman | -0.9664 | -0.97 | 100 | 100 | 0.5944 | 0.5532 |
| gpt-3.5-turbo (paper) | elementary_edu | social | CCEI | 0.9971 | 0.9973 | 100 | 100 | -0.1411 | 0.8879 |
| gpt-3.5-turbo (paper) | elementary_edu | social | spearman | -0.9505 | -0.9558 | 100 | 100 | 1.267 | 0.2068 |
| gpt-3.5-turbo (paper) | elementary_edu | food | CCEI | 0.9995 | 0.9997 | 100 | 100 | -0.6491 | 0.5171 |
| gpt-3.5-turbo (paper) | elementary_edu | food | spearman | -0.9917 | -0.9973 | 100 | 100 | 3.761 | 0.0002232 |
| gpt-3.5-turbo (paper) | college_edu | risk | CCEI | 0.9981 | 0.9999 | 100 | 100 | -1.443 | 0.1521 |
| gpt-3.5-turbo (paper) | college_edu | risk | spearman | -0.9843 | -0.9896 | 100 | 100 | 1.169 | 0.2447 |
| gpt-3.5-turbo (paper) | college_edu | time | CCEI | 0.9972 | 0.9975 | 100 | 100 | -0.2243 | 0.8229 |
| gpt-3.5-turbo (paper) | college_edu | time | spearman | -0.9664 | -0.971 | 100 | 100 | 0.784 | 0.4345 |
| gpt-3.5-turbo (paper) | college_edu | social | CCEI | 0.9971 | 0.9983 | 100 | 100 | -1.069 | 0.2869 |
| gpt-3.5-turbo (paper) | college_edu | social | spearman | -0.9505 | -0.9579 | 100 | 100 | 1.814 | 0.0716 |
| gpt-3.5-turbo (paper) | college_edu | food | CCEI | 0.9995 | 0.9995 | 100 | 100 | -0.1146 | 0.9089 |
| gpt-3.5-turbo (paper) | college_edu | food | spearman | -0.9917 | -0.9972 | 100 | 100 | 4.336 | 2.369e-05 |
| gpt-3.5-turbo (paper) | asian | risk | CCEI | 0.9981 | 0.9993 | 100 | 100 | -0.9051 | 0.3673 |
| gpt-3.5-turbo (paper) | asian | risk | spearman | -0.9843 | -0.9905 | 100 | 100 | 1.414 | 0.1602 |
| gpt-3.5-turbo (paper) | asian | time | CCEI | 0.9972 | 0.9982 | 100 | 100 | -0.6564 | 0.5128 |
| gpt-3.5-turbo (paper) | asian | time | spearman | -0.9664 | -0.9722 | 100 | 100 | 1.008 | 0.3153 |
| gpt-3.5-turbo (paper) | asian | social | CCEI | 0.9971 | 0.9973 | 100 | 100 | -0.189 | 0.8503 |
| gpt-3.5-turbo (paper) | asian | social | spearman | -0.9505 | -0.9572 | 100 | 100 | 1.607 | 0.11 |
| gpt-3.5-turbo (paper) | asian | food | CCEI | 0.9995 | 0.9996 | 100 | 100 | -0.339 | 0.735 |
| gpt-3.5-turbo (paper) | asian | food | spearman | -0.9917 | -0.9974 | 100 | 100 | 4.109 | 5.809e-05 |
| gpt-3.5-turbo (paper) | african_american | risk | CCEI | 0.9981 | 0.9993 | 100 | 100 | -0.9466 | 0.3459 |
| gpt-3.5-turbo (paper) | african_american | risk | spearman | -0.9843 | -0.9893 | 100 | 100 | 1.138 | 0.2575 |
| gpt-3.5-turbo (paper) | african_american | time | CCEI | 0.9972 | 0.9969 | 100 | 100 | 0.1519 | 0.8795 |
| gpt-3.5-turbo (paper) | african_american | time | spearman | -0.9664 | -0.9681 | 100 | 100 | 0.2844 | 0.7766 |
| gpt-3.5-turbo (paper) | african_american | social | CCEI | 0.9971 | 0.9976 | 100 | 100 | -0.4251 | 0.6714 |
| gpt-3.5-turbo (paper) | african_american | social | spearman | -0.9505 | -0.9567 | 100 | 100 | 1.504 | 0.1344 |
| gpt-3.5-turbo (paper) | african_american | food | CCEI | 0.9995 | 1 | 100 | 100 | -2.425 | 0.01712 |
| gpt-3.5-turbo (paper) | african_american | food | spearman | -0.9917 | -0.9987 | 100 | 100 | 6.475 | 1.777e-09 |


## Model (a) vs model (b), same condition

| model_a | model_b | condition | domain | measure | mean_a | mean_b | n_a | n_b | t | p |
|---|---|---|---|---|---|---|---|---|---|---|
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | risk | CCEI | 0.9997 | 0.9999 | 100 | 100 | -1.014 | 0.3127 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | risk | spearman | -0.9732 | -0.9808 | 100 | 100 | 3.22 | 0.001496 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | time | CCEI | 0.9988 | 0.9986 | 100 | 100 | 0.2106 | 0.8335 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | time | spearman | -0.9543 | -0.9773 | 100 | 100 | 5.157 | 8.776e-07 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | social | CCEI | 0.9983 | 0.9999 | 100 | 100 | -2.105 | 0.03777 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | social | spearman | -0.9782 | -0.9806 | 100 | 100 | 1.019 | 0.3094 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | food | CCEI | 0.9997 | 0.9997 | 100 | 100 | 0.1398 | 0.889 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | baseline | food | spearman | -0.9813 | -0.9791 | 100 | 100 | -1.08 | 0.2812 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | risk | CCEI | 0.9926 | 0.9978 | 100 | 100 | -2.1 | 0.03737 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | risk | spearman | -0.9557 | -0.9674 | 100 | 100 | 3.374 | 0.0008949 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | time | CCEI | 0.9986 | 0.9947 | 100 | 100 | 2.566 | 0.01148 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | time | spearman | -0.9526 | -0.9564 | 100 | 100 | 0.7995 | 0.4249 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | social | CCEI | 0.9993 | 0.9977 | 100 | 100 | 2.704 | 0.007794 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | social | spearman | -0.9453 | -0.9228 | 100 | 100 | -2.963 | 0.003523 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | food | CCEI | 0.9984 | 0.9948 | 100 | 100 | 1.392 | 0.1667 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | price_framing | food | spearman | -0.9687 | -0.969 | 100 | 100 | 0.08479 | 0.9325 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | risk | CCEI | 0.9626 | 0.8804 | 57 | 100 | 3.749 | 0.0002568 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | risk | spearman | -0.9862 | -0.9499 | 57 | 100 | -4.56 | 1.033e-05 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | time | CCEI | 0.969 | 0.9787 | 95 | 100 | -1.049 | 0.2963 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | time | spearman | -0.9903 | -0.8949 | 95 | 100 | -9.1 | 2.955e-15 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | social | CCEI | 0.9858 | 0.9676 | 94 | 100 | 1.993 | 0.04791 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | social | spearman | -0.9487 | -0.8176 | 94 | 100 | -4.879 | 3e-06 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | food | CCEI | 0.9919 | 0.8065 | 100 | 100 | 8.42 | 2.651e-13 |
| gpt-4o-mini | gpt-4o-mini (paraphrase) | discrete | food | spearman | -0.9333 | -0.9003 | 100 | 100 | -2.18 | 0.03044 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | risk | CCEI | 0.9997 | 0.9981 | 100 | 100 | 1.262 | 0.21 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | risk | spearman | -0.9732 | -0.9843 | 100 | 100 | 2.41 | 0.01738 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | time | CCEI | 0.9988 | 0.9972 | 100 | 100 | 1.057 | 0.2929 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | time | spearman | -0.9543 | -0.9664 | 100 | 100 | 1.786 | 0.07582 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | social | CCEI | 0.9983 | 0.9971 | 100 | 100 | 0.9456 | 0.3457 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | social | spearman | -0.9782 | -0.9505 | 100 | 100 | -6.91 | 1.201e-10 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | food | CCEI | 0.9997 | 0.9995 | 100 | 100 | 1.06 | 0.2907 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | baseline | food | spearman | -0.9813 | -0.9917 | 100 | 100 | 6.074 | 7.174e-09 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | risk | CCEI | 0.9991 | 0.9991 | 100 | 100 | 0.01962 | 0.9844 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | risk | spearman | -0.9757 | -0.9904 | 100 | 100 | 7.46 | 3.732e-12 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | time | CCEI | 0.9965 | 0.997 | 100 | 100 | -0.3277 | 0.7435 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | time | spearman | -0.9535 | -0.9659 | 100 | 100 | 2.089 | 0.03819 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | social | CCEI | 0.9976 | 0.997 | 100 | 100 | 0.4348 | 0.6643 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | social | spearman | -0.9748 | -0.9567 | 100 | 100 | -6.073 | 6.651e-09 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | food | CCEI | 0.9993 | 0.9995 | 100 | 100 | -0.5877 | 0.5575 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_0.5 | food | spearman | -0.9773 | -0.9913 | 100 | 100 | 7.326 | 1.121e-11 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | risk | CCEI | 0.9993 | 0.9996 | 100 | 100 | -0.7761 | 0.4391 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | risk | spearman | -0.9733 | -0.9893 | 100 | 100 | 6.192 | 6.015e-09 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | time | CCEI | 0.9942 | 0.9977 | 100 | 100 | -1.693 | 0.09326 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | time | spearman | -0.9518 | -0.9662 | 100 | 100 | 2.825 | 0.005449 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | social | CCEI | 0.9973 | 0.997 | 100 | 100 | 0.1781 | 0.859 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | social | spearman | -0.971 | -0.957 | 100 | 100 | -1.685 | 0.09486 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | food | CCEI | 0.999 | 0.9996 | 100 | 100 | -0.8567 | 0.3934 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | temp_1 | food | spearman | -0.9786 | -0.9894 | 100 | 100 | 6.492 | 7.772e-10 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | risk | CCEI | 0.9926 | 0.9008 | 100 | 100 | 9.042 | 6.68e-15 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | risk | spearman | -0.9557 | -0.05342 | 100 | 100 | -33.13 | 5.323e-56 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | time | CCEI | 0.9986 | 0.8843 | 100 | 100 | 11.16 | 3.121e-19 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | time | spearman | -0.9526 | -0.1162 | 100 | 100 | -25.58 | 6.279e-46 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | social | CCEI | 0.9993 | 0.6976 | 100 | 100 | 18.4 | 1.031e-33 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | social | spearman | -0.9453 | 0.2671 | 100 | 100 | -33.91 | 4.591e-57 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | food | CCEI | 0.9984 | 0.8936 | 100 | 100 | 11.18 | 2.778e-19 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | price_framing | food | spearman | -0.9687 | -0.4992 | 100 | 100 | -13.18 | 1.423e-23 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | risk | CCEI | 0.9626 | 0.8427 | 57 | 100 | 4.485 | 1.418e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | risk | spearman | -0.9862 | -0.5886 | 57 | 100 | -11.08 | 3.05e-19 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | time | CCEI | 0.969 | 0.9084 | 95 | 100 | 3.695 | 0.0002987 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | time | spearman | -0.9903 | -0.4968 | 95 | 100 | -19.05 | 2.564e-35 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | social | CCEI | 0.9858 | 0.8707 | 94 | 100 | 5.095 | 1.474e-06 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | social | spearman | -0.9487 | -0.5195 | 94 | 100 | -14.82 | 1.668e-29 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | food | CCEI | 0.9919 | 0.78 | 100 | 100 | 9.214 | 4.902e-15 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | discrete | food | spearman | -0.9333 | -0.5334 | 100 | 100 | -12.93 | 4.776e-25 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | risk | CCEI | 0.9998 | 0.9995 | 30 | 100 | 1.388 | 0.1677 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | risk | spearman | -0.972 | -0.9895 | 30 | 100 | 2.956 | 0.005619 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | time | CCEI | 0.9987 | 0.9982 | 30 | 100 | 0.7026 | 0.4849 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | time | spearman | -0.9543 | -0.9714 | 30 | 100 | 1.412 | 0.1679 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | social | CCEI | 0.9985 | 0.9964 | 30 | 100 | 1.865 | 0.06602 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | social | spearman | -0.9716 | -0.957 | 30 | 100 | -3.99 | 0.0001912 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | food | CCEI | 0.9995 | 0.9994 | 30 | 100 | 0.1585 | 0.8743 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | female | food | spearman | -0.9782 | -0.9972 | 30 | 100 | 6.271 | 4.142e-07 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | risk | CCEI | 0.9999 | 0.9998 | 30 | 100 | 0.3533 | 0.7247 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | risk | spearman | -0.9781 | -0.9913 | 30 | 100 | 4.735 | 3.179e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | time | CCEI | 0.9977 | 0.9973 | 30 | 100 | 0.17 | 0.866 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | time | spearman | -0.9469 | -0.9661 | 30 | 100 | 1.434 | 0.1615 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | social | CCEI | 0.9975 | 0.9974 | 30 | 100 | 0.04338 | 0.9656 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | social | spearman | -0.9738 | -0.9594 | 30 | 100 | -3.728 | 0.0005055 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | food | CCEI | 0.9996 | 0.9994 | 30 | 100 | 0.3049 | 0.761 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | male | food | spearman | -0.9784 | -0.9987 | 30 | 100 | 5.978 | 1.492e-06 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | risk | CCEI | 0.9997 | 0.9994 | 30 | 100 | 0.8903 | 0.3758 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | risk | spearman | -0.9674 | -0.9911 | 30 | 100 | 4.959 | 2.045e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | time | CCEI | 0.9985 | 0.9971 | 30 | 100 | 1.345 | 0.1821 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | time | spearman | -0.9445 | -0.9703 | 30 | 100 | 2.352 | 0.02513 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | social | CCEI | 0.999 | 0.9974 | 30 | 100 | 1.774 | 0.08136 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | social | spearman | -0.9724 | -0.9557 | 30 | 100 | -4.801 | 5.813e-06 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | food | CCEI | 0.9989 | 1 | 30 | 100 | -1.901 | 0.06732 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | young_child | food | spearman | -0.9782 | -0.9989 | 30 | 100 | 8.474 | 1.772e-09 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | risk | CCEI | 1 | 0.9995 | 30 | 100 | 2.196 | 0.0304 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | risk | spearman | -0.9744 | -0.99 | 30 | 100 | 5.351 | 3.021e-06 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | time | CCEI | 0.9977 | 0.9973 | 30 | 100 | 0.2781 | 0.7819 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | time | spearman | -0.9496 | -0.9708 | 30 | 100 | 1.809 | 0.08035 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | social | CCEI | 0.9988 | 0.9981 | 30 | 100 | 0.8275 | 0.4124 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | social | spearman | -0.9722 | -0.9588 | 30 | 100 | -3.602 | 0.0006743 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | food | CCEI | 0.9988 | 0.9998 | 30 | 100 | -1.506 | 0.1421 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elderly | food | spearman | -0.9784 | -0.9969 | 30 | 100 | 6.651 | 7.983e-08 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | risk | CCEI | 0.9999 | 0.9996 | 30 | 100 | 1.299 | 0.1966 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | risk | spearman | -0.9704 | -0.9907 | 30 | 100 | 4.112 | 0.0002533 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | time | CCEI | 0.9977 | 0.9973 | 30 | 100 | 0.3215 | 0.7493 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | time | spearman | -0.9474 | -0.97 | 30 | 100 | 2.343 | 0.02537 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | social | CCEI | 0.9996 | 0.9973 | 30 | 100 | 3.123 | 0.002226 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | social | spearman | -0.9739 | -0.9558 | 30 | 100 | -3.429 | 0.001353 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | food | CCEI | 0.9992 | 0.9997 | 30 | 100 | -0.9028 | 0.3711 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | elementary_edu | food | spearman | -0.9767 | -0.9973 | 30 | 100 | 5.07 | 1.406e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | risk | CCEI | 0.9998 | 0.9999 | 30 | 100 | -0.4894 | 0.6266 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | risk | spearman | -0.9815 | -0.9896 | 30 | 100 | 2.066 | 0.04506 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | time | CCEI | 0.9981 | 0.9975 | 30 | 100 | 0.5009 | 0.619 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | time | spearman | -0.9527 | -0.971 | 30 | 100 | 2.291 | 0.02829 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | social | CCEI | 1 | 0.9983 | 30 | 100 | 3.85 | 0.0002093 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | social | spearman | -0.98 | -0.9579 | 30 | 100 | -4.905 | 1.27e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | food | CCEI | 0.9989 | 0.9995 | 30 | 100 | -0.956 | 0.3432 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | college_edu | food | spearman | -0.9787 | -0.9972 | 30 | 100 | 6.406 | 2.655e-07 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | risk | CCEI | 1 | 0.9993 | 30 | 100 | 2.149 | 0.03406 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | risk | spearman | -0.9734 | -0.9905 | 30 | 100 | 4.104 | 0.0002621 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | time | CCEI | 0.9983 | 0.9982 | 30 | 100 | 0.1445 | 0.8856 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | time | spearman | -0.9535 | -0.9722 | 30 | 100 | 2.715 | 0.01045 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | social | CCEI | 0.9989 | 0.9973 | 30 | 100 | 1.682 | 0.09773 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | social | spearman | -0.9735 | -0.9572 | 30 | 100 | -3.866 | 0.0002941 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | food | CCEI | 1 | 0.9996 | 30 | 100 | 1.36 | 0.1769 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | asian | food | spearman | -0.9825 | -0.9974 | 30 | 100 | 6.869 | 1.673e-08 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | risk | CCEI | 0.9999 | 0.9993 | 30 | 100 | 1.962 | 0.05224 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | risk | spearman | -0.9755 | -0.9893 | 30 | 100 | 4.294 | 0.0001193 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | time | CCEI | 0.9985 | 0.9969 | 30 | 100 | 1.22 | 0.227 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | time | spearman | -0.9563 | -0.9681 | 30 | 100 | 1.526 | 0.1359 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | social | CCEI | 0.9998 | 0.9976 | 30 | 100 | 4.312 | 3.351e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | social | spearman | -0.9732 | -0.9567 | 30 | 100 | -4.234 | 9.071e-05 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | food | CCEI | 0.9994 | 1 | 30 | 100 | -1.787 | 0.08443 |
| gpt-4o-mini | gpt-3.5-turbo (paper) | african_american | food | spearman | -0.9773 | -0.9987 | 30 | 100 | 7.984 | 6.011e-09 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | risk | CCEI | 0.9999 | 0.9981 | 100 | 100 | 1.431 | 0.1556 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | risk | spearman | -0.9808 | -0.9843 | 100 | 100 | 0.7513 | 0.4538 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | time | CCEI | 0.9986 | 0.9972 | 100 | 100 | 0.7773 | 0.438 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | time | spearman | -0.9773 | -0.9664 | 100 | 100 | -1.887 | 0.06153 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | social | CCEI | 0.9999 | 0.9971 | 100 | 100 | 2.619 | 0.01019 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | social | spearman | -0.9806 | -0.9505 | 100 | 100 | -7.942 | 7.637e-13 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | food | CCEI | 0.9997 | 0.9995 | 100 | 100 | 0.8034 | 0.4227 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | baseline | food | spearman | -0.9791 | -0.9917 | 100 | 100 | 6.985 | 5.807e-11 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | risk | CCEI | 0.9978 | 0.9008 | 100 | 100 | 9.718 | 3.453e-16 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | risk | spearman | -0.9674 | -0.05342 | 100 | 100 | -33.59 | 2.001e-56 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | time | CCEI | 0.9947 | 0.8843 | 100 | 100 | 10.68 | 2.262e-18 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | time | spearman | -0.9564 | -0.1162 | 100 | 100 | -25.68 | 3.72e-46 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | social | CCEI | 0.9977 | 0.6976 | 100 | 100 | 18.29 | 1.518e-33 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | social | spearman | -0.9228 | 0.2671 | 100 | 100 | -32.89 | 2.142e-57 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | food | CCEI | 0.9948 | 0.8936 | 100 | 100 | 10.46 | 2.649e-18 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | price_framing | food | spearman | -0.969 | -0.4992 | 100 | 100 | -13.16 | 1.326e-23 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | risk | CCEI | 0.8804 | 0.8427 | 100 | 100 | 1.409 | 0.1605 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | risk | spearman | -0.9499 | -0.5886 | 100 | 100 | -10.01 | 5.776e-17 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | time | CCEI | 0.9787 | 0.9084 | 100 | 100 | 4.925 | 3.007e-06 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | time | spearman | -0.8949 | -0.4968 | 100 | 100 | -14.41 | 1.319e-28 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | social | CCEI | 0.9676 | 0.8707 | 100 | 100 | 4.149 | 6.187e-05 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | social | spearman | -0.8176 | -0.5195 | 100 | 100 | -8.129 | 4.768e-14 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | food | CCEI | 0.8065 | 0.78 | 100 | 100 | 0.8358 | 0.4043 |
| gpt-4o-mini (paraphrase) | gpt-3.5-turbo (paper) | discrete | food | spearman | -0.9003 | -0.5334 | 100 | 100 | -12.04 | 1.609e-22 |


## Heterogeneity of individual parameters: Levene tests (sd_a vs sd_b)

| model | comparison | domain | param | sd_a | sd_b | W | p |
|---|---|---|---|---|---|---|---|
| gpt-4o-mini | baseline vs temp_0.5 | risk | alpha | 0.0266 | 0.0243 | 0.2169 | 0.6419 |
| gpt-4o-mini | baseline vs temp_0.5 | risk | rho | 0.07506 | 0.07445 | 0.003941 | 0.95 |
| gpt-4o-mini | baseline vs temp_0.5 | time | alpha | 0.0156 | 0.05011 | 1.141 | 0.2868 |
| gpt-4o-mini | baseline vs temp_0.5 | time | rho | 0.05941 | 0.1268 | 23.64 | 2.371e-06 |
| gpt-4o-mini | baseline vs temp_0.5 | social | alpha | 0.01275 | 0.01372 | 0.7999 | 0.3722 |
| gpt-4o-mini | baseline vs temp_0.5 | social | rho | 0.11 | 0.1051 | 0.261 | 0.61 |
| gpt-4o-mini | baseline vs temp_0.5 | food | alpha | 0.01142 | 0.01173 | 0.4687 | 0.4944 |
| gpt-4o-mini | baseline vs temp_0.5 | food | rho | 0.04727 | 0.0463 | 0.1251 | 0.724 |
| gpt-4o-mini | baseline vs temp_1 | risk | alpha | 0.0266 | 0.02974 | 0.01639 | 0.8982 |
| gpt-4o-mini | baseline vs temp_1 | risk | rho | 0.07506 | 0.07948 | 0.1138 | 0.7362 |
| gpt-4o-mini | baseline vs temp_1 | time | alpha | 0.0156 | 0.01782 | 1.08 | 0.2999 |
| gpt-4o-mini | baseline vs temp_1 | time | rho | 0.05941 | 0.1379 | 31.91 | 5.65e-08 |
| gpt-4o-mini | baseline vs temp_1 | social | alpha | 0.01275 | 0.01046 | 0.7218 | 0.3966 |
| gpt-4o-mini | baseline vs temp_1 | social | rho | 0.11 | 0.1139 | 0.002494 | 0.9602 |
| gpt-4o-mini | baseline vs temp_1 | food | alpha | 0.01142 | 0.01135 | 0.0923 | 0.7616 |
| gpt-4o-mini | baseline vs temp_1 | food | rho | 0.04727 | 0.05817 | 2.611 | 0.1077 |
| gpt-4o-mini | model vs Human | risk | alpha | 0.0266 | 0.1333 | 28.88 | 2.011e-07 |
| gpt-4o-mini | model vs Human | risk | rho | 0.07506 | 4.769 | 11.94 | 0.000663 |
| gpt-4o-mini | model vs Human | time | alpha | 0.0156 | 0.09992 | 16.82 | 5.853e-05 |
| gpt-4o-mini | model vs Human | time | rho | 0.05941 | 0.3667 | 28.18 | 2.77e-07 |
| gpt-4o-mini | model vs Human | social | alpha | 0.01275 | 0.1962 | 326.6 | 8.395e-45 |
| gpt-4o-mini | model vs Human | social | rho | 0.11 | 5.166 | 17.93 | 3.416e-05 |
| gpt-4o-mini | model vs Human | food | alpha | 0.01142 | 0.237 | 89.77 | 5.385e-18 |
| gpt-4o-mini | model vs Human | food | rho | 0.04727 | 5.073 | 19.1 | 1.937e-05 |
| gpt-4o-mini (paraphrase) | model vs Human | risk | alpha | 0.01573 | 0.1333 | 36.06 | 8.17e-09 |
| gpt-4o-mini (paraphrase) | model vs Human | risk | rho | 0.05197 | 4.769 | 12.07 | 0.0006214 |
| gpt-4o-mini (paraphrase) | model vs Human | time | alpha | 0.009748 | 0.09992 | 20.62 | 9.406e-06 |
| gpt-4o-mini (paraphrase) | model vs Human | time | rho | 0.05692 | 0.3667 | 28.87 | 2.027e-07 |
| gpt-4o-mini (paraphrase) | model vs Human | social | alpha | 0.008906 | 0.1962 | 340.4 | 4.757e-46 |
| gpt-4o-mini (paraphrase) | model vs Human | social | rho | 0.03975 | 5.166 | 19.17 | 1.878e-05 |
| gpt-4o-mini (paraphrase) | model vs Human | food | alpha | 0.01294 | 0.237 | 88.63 | 8.061e-18 |
| gpt-4o-mini (paraphrase) | model vs Human | food | rho | 0.0592 | 5.073 | 19.09 | 1.952e-05 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | risk | alpha | 0.03489 | 0.03734 | 0.2431 | 0.6225 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | risk | rho | 0.1081 | 0.1282 | 4.632 | 0.03259 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | time | alpha | 0.02333 | 0.03207 | 0.1271 | 0.7219 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | time | rho | 0.07595 | 0.1018 | 13.07 | 0.0003802 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | social | alpha | 0.0195 | 0.03242 | 1.016 | 0.3146 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | social | rho | 0.04672 | 0.07234 | 22.96 | 3.237e-06 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | food | alpha | 0.005423 | 0.01115 | 5.815 | 0.01681 |
| gpt-3.5-turbo (paper) | baseline vs temp_0.5 | food | rho | 0.02374 | 0.03817 | 31.62 | 6.317e-08 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | risk | alpha | 0.03489 | 0.02929 | 0.1707 | 0.6799 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | risk | rho | 0.1081 | 0.1122 | 10.43 | 0.001453 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | time | alpha | 0.02333 | 0.0332 | 0.009175 | 0.9238 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | time | rho | 0.07595 | 0.09338 | 17.71 | 3.892e-05 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | social | alpha | 0.0195 | 0.02473 | 0.08548 | 0.7703 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | social | rho | 0.04672 | 0.06918 | 12.48 | 0.000513 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | food | alpha | 0.005423 | 0.008983 | 4.901 | 0.02798 |
| gpt-3.5-turbo (paper) | baseline vs temp_1 | food | rho | 0.02374 | 0.04352 | 33.76 | 2.461e-08 |
| gpt-3.5-turbo (paper) | model vs Human | risk | alpha | 0.03489 | 0.1333 | 32.53 | 3.9e-08 |
| gpt-3.5-turbo (paper) | model vs Human | risk | rho | 0.1081 | 4.769 | 11.99 | 0.0006449 |
| gpt-3.5-turbo (paper) | model vs Human | time | alpha | 0.02333 | 0.09992 | 12.9 | 0.0004074 |
| gpt-3.5-turbo (paper) | model vs Human | time | rho | 0.07595 | 0.3667 | 26.79 | 5.224e-07 |
| gpt-3.5-turbo (paper) | model vs Human | social | alpha | 0.0195 | 0.1962 | 302.6 | 9.169e-43 |
| gpt-3.5-turbo (paper) | model vs Human | social | rho | 0.04672 | 5.166 | 19.07 | 1.962e-05 |
| gpt-3.5-turbo (paper) | model vs Human | food | alpha | 0.005423 | 0.237 | 94.56 | 9.933e-19 |
| gpt-3.5-turbo (paper) | model vs Human | food | rho | 0.02374 | 5.073 | 19.49 | 1.605e-05 |


## gpt-4o-mini: OLS of CCEI on model, price_framing, interaction (HC1 SE)

| domain | term | coef | se | t | p |
|---|---|---|---|---|---|
| risk | const | 0.9804 | 0.004291 | 228.5 | 0 |
| risk | model | 0.01927 | 0.004295 | 4.487 | 9.313e-06 |
| risk | price_framing | -0.04838 | 0.01379 | -3.51 | 0.0004972 |
| risk | model x price_framing | 0.04131 | 0.01396 | 2.959 | 0.003261 |
| time | const | 0.9852 | 0.004235 | 232.7 | 0 |
| time | model | 0.01359 | 0.004255 | 3.193 | 0.001512 |
| time | price_framing | -0.05747 | 0.01686 | -3.408 | 0.0007172 |
| time | model x price_framing | 0.05724 | 0.01688 | 3.392 | 0.0007597 |
| social | const | 0.9674 | 0.006094 | 158.7 | 0 |
| social | model | 0.03092 | 0.006137 | 5.037 | 7.017e-07 |
| social | price_framing | -0.005322 | 0.01154 | -0.4612 | 0.6449 |
| social | model x price_framing | 0.006331 | 0.01157 | 0.5474 | 0.5844 |
| food | const | 0.9631 | 0.006127 | 157.2 | 0 |
| food | model | 0.03668 | 0.006128 | 5.986 | 4.609e-09 |
| food | price_framing | 0.00456 | 0.01063 | 0.4289 | 0.6682 |
| food | model x price_framing | -0.005918 | 0.01065 | -0.5558 | 0.5786 |


## gpt-4o-mini: OLS of CCEI on model, discrete, interaction (HC1 SE)

| domain | term | coef | se | t | p |
|---|---|---|---|---|---|
| risk | const | 0.9804 | 0.004293 | 228.4 | 0 |
| risk | model | 0.01927 | 0.004297 | 4.486 | 9.586e-06 |
| risk | discrete | -0.01573 | 0.007096 | -2.217 | 0.02719 |
| risk | model x discrete | -0.02137 | 0.01697 | -1.259 | 0.2087 |
| time | const | 0.9852 | 0.004234 | 232.7 | 0 |
| time | model | 0.01359 | 0.004255 | 3.194 | 0.00151 |
| time | discrete | -0.02045 | 0.007504 | -2.725 | 0.006702 |
| time | model x discrete | -0.009337 | 0.01148 | -0.8132 | 0.4165 |
| social | const | 0.9674 | 0.006094 | 158.8 | 0 |
| social | model | 0.03092 | 0.006137 | 5.037 | 6.984e-07 |
| social | discrete | -0.003242 | 0.00943 | -0.3438 | 0.7312 |
| social | model x discrete | -0.009239 | 0.01068 | -0.8655 | 0.3873 |
| food | const | 0.9631 | 0.006126 | 157.2 | 0 |
| food | model | 0.03668 | 0.006127 | 5.986 | 4.516e-09 |
| food | discrete | 0.002863 | 0.009109 | 0.3143 | 0.7535 |
| food | model x discrete | -0.01068 | 0.009371 | -1.139 | 0.2552 |


## gpt-4o-mini (paraphrase): OLS of CCEI on model, price_framing, interaction (HC1 SE)

| domain | term | coef | se | t | p |
|---|---|---|---|---|---|
| risk | const | 0.9804 | 0.004291 | 228.5 | 0 |
| risk | model | 0.01946 | 0.004292 | 4.535 | 7.505e-06 |
| risk | price_framing | -0.04838 | 0.01379 | -3.51 | 0.0004972 |
| risk | model x price_framing | 0.04636 | 0.01384 | 3.35 | 0.0008804 |
| time | const | 0.9852 | 0.004235 | 232.7 | 0 |
| time | model | 0.01335 | 0.004358 | 3.065 | 0.00232 |
| time | price_framing | -0.05747 | 0.01686 | -3.408 | 0.0007172 |
| time | model x price_framing | 0.05355 | 0.01696 | 3.159 | 0.001699 |
| social | const | 0.9674 | 0.006094 | 158.7 | 0 |
| social | model | 0.03246 | 0.006095 | 5.326 | 1.635e-07 |
| social | price_framing | -0.005322 | 0.01154 | -0.4612 | 0.6449 |
| social | model x price_framing | 0.003137 | 0.01155 | 0.2715 | 0.7862 |
| food | const | 0.9631 | 0.006127 | 157.2 | 0 |
| food | model | 0.03665 | 0.00613 | 5.979 | 4.791e-09 |
| food | price_framing | 0.00456 | 0.01063 | 0.4289 | 0.6682 |
| food | model x price_framing | -0.009415 | 0.01092 | -0.8621 | 0.3891 |


## gpt-4o-mini (paraphrase): OLS of CCEI on model, discrete, interaction (HC1 SE)

| domain | term | coef | se | t | p |
|---|---|---|---|---|---|
| risk | const | 0.9804 | 0.004291 | 228.5 | 0 |
| risk | model | 0.01946 | 0.004291 | 4.536 | 7.444e-06 |
| risk | discrete | -0.01573 | 0.007093 | -2.218 | 0.02706 |
| risk | model x discrete | -0.1037 | 0.01705 | -6.081 | 2.635e-09 |
| time | const | 0.9852 | 0.004234 | 232.7 | 0 |
| time | model | 0.01335 | 0.004357 | 3.065 | 0.002314 |
| time | discrete | -0.02045 | 0.007504 | -2.725 | 0.006696 |
| time | model x discrete | 0.00061 | 0.008227 | 0.07415 | 0.9409 |
| social | const | 0.9674 | 0.006093 | 158.8 | 0 |
| social | model | 0.03246 | 0.006094 | 5.327 | 1.612e-07 |
| social | discrete | -0.003242 | 0.00943 | -0.3438 | 0.7311 |
| social | model x discrete | -0.02904 | 0.01217 | -2.385 | 0.0175 |
| food | const | 0.9631 | 0.006126 | 157.2 | 0 |
| food | model | 0.03665 | 0.006129 | 5.979 | 4.695e-09 |
| food | discrete | 0.002863 | 0.009109 | 0.3143 | 0.7535 |
| food | model x discrete | -0.1961 | 0.02372 | -8.265 | 1.733e-15 |


## gpt-3.5-turbo (paper): OLS of CCEI on model, price_framing, interaction (HC1 SE)

| domain | term | coef | se | t | p |
|---|---|---|---|---|---|
| risk | const | 0.9804 | 0.004291 | 228.5 | 0 |
| risk | model | 0.01773 | 0.004459 | 3.975 | 8.275e-05 |
| risk | price_framing | -0.04838 | 0.01379 | -3.51 | 0.0004972 |
| risk | model x price_framing | -0.04893 | 0.01702 | -2.875 | 0.004247 |
| time | const | 0.9852 | 0.004235 | 232.7 | 0 |
| time | model | 0.01194 | 0.004494 | 2.656 | 0.008204 |
| time | price_framing | -0.05747 | 0.01686 | -3.408 | 0.0007172 |
| time | model x price_framing | -0.05544 | 0.01978 | -2.803 | 0.005304 |
| social | const | 0.9674 | 0.006094 | 158.7 | 0 |
| social | model | 0.02971 | 0.006183 | 4.805 | 2.156e-06 |
| social | price_framing | -0.005322 | 0.01154 | -0.4612 | 0.6449 |
| social | model x price_framing | -0.2941 | 0.02007 | -14.65 | 1.367e-39 |
| food | const | 0.9631 | 0.006127 | 157.2 | 0 |
| food | model | 0.03642 | 0.00613 | 5.941 | 5.935e-09 |
| food | price_framing | 0.00456 | 0.01063 | 0.4289 | 0.6682 |
| food | model x price_framing | -0.1104 | 0.01417 | -7.796 | 5.03e-14 |


## gpt-3.5-turbo (paper): OLS of CCEI on model, discrete, interaction (HC1 SE)

| domain | term | coef | se | t | p |
|---|---|---|---|---|---|
| risk | const | 0.9804 | 0.004291 | 228.5 | 0 |
| risk | model | 0.01773 | 0.004459 | 3.976 | 8.23e-05 |
| risk | discrete | -0.01573 | 0.007093 | -2.218 | 0.02706 |
| risk | model x discrete | -0.1396 | 0.02294 | -6.089 | 2.519e-09 |
| time | const | 0.9852 | 0.004234 | 232.7 | 0 |
| time | model | 0.01194 | 0.004494 | 2.656 | 0.00819 |
| time | discrete | -0.02045 | 0.007504 | -2.725 | 0.006696 |
| time | model x discrete | -0.06827 | 0.01587 | -4.302 | 2.094e-05 |
| social | const | 0.9674 | 0.006093 | 158.8 | 0 |
| social | model | 0.02971 | 0.006183 | 4.805 | 2.135e-06 |
| social | discrete | -0.003242 | 0.00943 | -0.3438 | 0.7311 |
| social | model x discrete | -0.1232 | 0.024 | -5.134 | 4.307e-07 |
| food | const | 0.9631 | 0.006126 | 157.2 | 0 |
| food | model | 0.03642 | 0.00613 | 5.942 | 5.819e-09 |
| food | discrete | 0.002863 | 0.009109 | 0.3143 | 0.7535 |
| food | model x discrete | -0.2223 | 0.02463 | -9.026 | 5.907e-18 |
