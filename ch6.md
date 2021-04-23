---
title: "Rethink chapter 6 practice"
output: 
  html_document:
    keep_md: true
#output: html_notebook
---

Problem 6H1


```r
library(dagitty)
library(rethinking)
```

```
## Loading required package: rstan
```

```
## Loading required package: StanHeaders
```

```
## Loading required package: ggplot2
```

```
## rstan (Version 2.21.2, GitRev: 2e1f913d3ca3)
```

```
## For execution on a local, multicore CPU with excess RAM we recommend calling
## options(mc.cores = parallel::detectCores()).
## To avoid recompilation of unchanged Stan programs, we recommend calling
## rstan_options(auto_write = TRUE)
```

```
## Loading required package: parallel
```

```
## rethinking (Version 2.13)
```

```
## 
## Attaching package: 'rethinking'
```

```
## The following object is masked from 'package:stats':
## 
##     rstudent
```

```r
dag_6.2 <- dagitty( "dag {
  A -> D
  A -> M -> D
  A <- S -> M
  S -> W -> D
}")
coordinates(dag_6.2) <- list( x=c(S=0, W=2, M=1, A=0, D=2), y=c(S=0, W=0, M=1, A=2, D=2))
drawdag( dag_6.2 )
```

![](ch6_files/figure-html/unnamed-chunk-1-1.png)<!-- -->

Identifying all paths from W to D

```r
paths(dag_6.2, from ="W", to = "D", Z = list(), limit = 100,
  directed = FALSE)
```

```
## $paths
## [1] "W -> D"                "W <- S -> A -> D"      "W <- S -> A -> M -> D"
## [4] "W <- S -> M -> D"      "W <- S -> M <- A -> D"
## 
## $open
## [1]  TRUE  TRUE  TRUE  TRUE FALSE
```

Check conditional independence

```r
impliedConditionalIndependencies( dag_6.2)
```

```
## A _||_ W | S
## D _||_ S | A, M, W
## M _||_ W | S
```

Check how to close open backdoor paths (condition on S)

```r
adjustmentSets( dag_6.2 , exposure="W" , outcome="D" )
```

```
## { A, M }
## { S }
```

Loading data to fit models

```r
data("WaffleDivorce", package = "rethinking")
d <- WaffleDivorce
d
```

```
##                Location Loc Population MedianAgeMarriage Marriage Marriage.SE
## 1               Alabama  AL       4.78              25.3     20.2        1.27
## 2                Alaska  AK       0.71              25.2     26.0        2.93
## 3               Arizona  AZ       6.33              25.8     20.3        0.98
## 4              Arkansas  AR       2.92              24.3     26.4        1.70
## 5            California  CA      37.25              26.8     19.1        0.39
## 6              Colorado  CO       5.03              25.7     23.5        1.24
## 7           Connecticut  CT       3.57              27.6     17.1        1.06
## 8              Delaware  DE       0.90              26.6     23.1        2.89
## 9  District of Columbia  DC       0.60              29.7     17.7        2.53
## 10              Florida  FL      18.80              26.4     17.0        0.58
## 11              Georgia  GA       9.69              25.9     22.1        0.81
## 12               Hawaii  HI       1.36              26.9     24.9        2.54
## 13                Idaho  ID       1.57              23.2     25.8        1.84
## 14             Illinois  IL      12.83              27.0     17.9        0.58
## 15              Indiana  IN       6.48              25.7     19.8        0.81
## 16                 Iowa  IA       3.05              25.4     21.5        1.46
## 17               Kansas  KS       2.85              25.0     22.1        1.48
## 18             Kentucky  KY       4.34              24.8     22.2        1.11
## 19            Louisiana  LA       4.53              25.9     20.6        1.19
## 20                Maine  ME       1.33              26.4     13.5        1.40
## 21             Maryland  MD       5.77              27.3     18.3        1.02
## 22        Massachusetts  MA       6.55              28.5     15.8        0.70
## 23             Michigan  MI       9.88              26.4     16.5        0.69
## 24            Minnesota  MN       5.30              26.3     15.3        0.77
## 25          Mississippi  MS       2.97              25.8     19.3        1.54
## 26             Missouri  MO       5.99              25.6     18.6        0.81
## 27              Montana  MT       0.99              25.7     18.5        2.31
## 28             Nebraska  NE       1.83              25.4     19.6        1.44
## 29        New Hampshire  NH       1.32              26.8     16.7        1.76
## 30           New Jersey  NJ       8.79              27.7     14.8        0.59
## 31           New Mexico  NM       2.06              25.8     20.4        1.90
## 32             New York  NY      19.38              28.4     16.8        0.47
## 33       North Carolina  NC       9.54              25.7     20.4        0.98
## 34         North Dakota  ND       0.67              25.3     26.7        2.93
## 35                 Ohio  OH      11.54              26.3     16.9        0.61
## 36             Oklahoma  OK       3.75              24.4     23.8        1.29
## 37               Oregon  OR       3.83              26.0     18.9        1.10
## 38         Pennsylvania  PA      12.70              27.1     15.5        0.48
## 39         Rhode Island  RI       1.05              28.2     15.0        2.11
## 40       South Carolina  SC       4.63              26.4     18.1        1.18
## 41         South Dakota  SD       0.81              25.6     20.1        2.64
## 42            Tennessee  TN       6.35              25.2     19.4        0.85
## 43                Texas  TX      25.15              25.2     21.5        0.61
## 44                 Utah  UT       2.76              23.3     29.6        1.77
## 45              Vermont  VT       0.63              26.9     16.4        2.40
## 46             Virginia  VA       8.00              26.4     20.5        0.83
## 47           Washington  WA       6.72              25.9     21.4        1.00
## 48        West Virginia  WV       1.85              25.0     22.2        1.69
## 49            Wisconsin  WI       5.69              26.3     17.2        0.79
## 50              Wyoming  WY       0.56              24.2     30.7        3.92
##    Divorce Divorce.SE WaffleHouses South Slaves1860 Population1860
## 1     12.7       0.79          128     1     435080         964201
## 2     12.5       2.05            0     0          0              0
## 3     10.8       0.74           18     0          0              0
## 4     13.5       1.22           41     1     111115         435450
## 5      8.0       0.24            0     0          0         379994
## 6     11.6       0.94           11     0          0          34277
## 7      6.7       0.77            0     0          0         460147
## 8      8.9       1.39            3     0       1798         112216
## 9      6.3       1.89            0     0          0          75080
## 10     8.5       0.32          133     1      61745         140424
## 11    11.5       0.58          381     1     462198        1057286
## 12     8.3       1.27            0     0          0              0
## 13     7.7       1.05            0     0          0              0
## 14     8.0       0.45            2     0          0        1711951
## 15    11.0       0.63           17     0          0        1350428
## 16    10.2       0.91            0     0          0         674913
## 17    10.6       1.09            6     0          2         107206
## 18    12.6       0.75           64     1     225483        1155684
## 19    11.0       0.89           66     1     331726         708002
## 20    13.0       1.48            0     0          0         628279
## 21     8.8       0.69           11     0      87189         687049
## 22     7.8       0.52            0     0          0        1231066
## 23     9.2       0.53            0     0          0         749113
## 24     7.4       0.60            0     0          0         172023
## 25    11.1       1.01           72     1     436631         791305
## 26     9.5       0.67           39     1     114931        1182012
## 27     9.1       1.71            0     0          0              0
## 28     8.8       0.94            0     0         15          28841
## 29    10.1       1.61            0     0          0         326073
## 30     6.1       0.46            0     0         18         672035
## 31    10.2       1.11            2     0          0          93516
## 32     6.6       0.31            0     0          0        3880735
## 33     9.9       0.48          142     1     331059         992622
## 34     8.0       1.44            0     0          0              0
## 35     9.5       0.45           64     0          0        2339511
## 36    12.8       1.01           16     0          0              0
## 37    10.4       0.80            0     0          0          52465
## 38     7.7       0.43           11     0          0        2906215
## 39     9.4       1.79            0     0          0         174620
## 40     8.1       0.70          144     1     402406         703708
## 41    10.9       2.50            0     0          0           4837
## 42    11.4       0.75          103     1     275719        1109801
## 43    10.0       0.35           99     1     182566         604215
## 44    10.2       0.93            0     0          0          40273
## 45     9.6       1.87            0     0          0         315098
## 46     8.9       0.52           40     1     490865        1219630
## 47    10.0       0.65            0     0          0          11594
## 48    10.9       1.34            4     1      18371         376688
## 49     8.3       0.57            0     0          0         775881
## 50    10.3       1.90            0     0          0              0
##    PropSlaves1860
## 1         4.5e-01
## 2         0.0e+00
## 3         0.0e+00
## 4         2.6e-01
## 5         0.0e+00
## 6         0.0e+00
## 7         0.0e+00
## 8         1.6e-02
## 9         0.0e+00
## 10        4.4e-01
## 11        4.4e-01
## 12        0.0e+00
## 13        0.0e+00
## 14        0.0e+00
## 15        0.0e+00
## 16        0.0e+00
## 17        1.9e-05
## 18        0.0e+00
## 19        4.7e-01
## 20        0.0e+00
## 21        1.3e-01
## 22        0.0e+00
## 23        0.0e+00
## 24        0.0e+00
## 25        5.5e-01
## 26        9.7e-02
## 27        0.0e+00
## 28        5.2e-04
## 29        0.0e+00
## 30        2.7e-05
## 31        0.0e+00
## 32        0.0e+00
## 33        3.3e-01
## 34        0.0e+00
## 35        0.0e+00
## 36        0.0e+00
## 37        0.0e+00
## 38        0.0e+00
## 39        0.0e+00
## 40        5.7e-01
## 41        0.0e+00
## 42        2.0e-01
## 43        3.0e-01
## 44        0.0e+00
## 45        0.0e+00
## 46        4.0e-01
## 47        0.0e+00
## 48        4.9e-02
## 49        0.0e+00
## 50        0.0e+00
```

```r
d$WaffleHouses
```

```
##  [1] 128   0  18  41   0  11   0   3   0 133 381   0   0   2  17   0   6  64  66
## [20]   0  11   0   0   0  72  39   0   0   0   0   2   0 142   0  64  16   0  11
## [39]   0 144   0 103  99   0   0  40   0   4   0   0
```



```r
d$d <- standardize( d$Divorce )
d$m <- standardize( d$Marriage )
d$a <- standardize( d$MedianAgeMarriage )
d$w <- standardize( d$WaffleHouses)
d$s <- d$South
```

Fitting various models for comparison

```r
m5.1 <- quap( alist(
  d ~ dnorm( mu , sigma ) , 
  mu <- intercept + bW * w ,
  intercept ~ dnorm( 0 , 0.2 ) , 
  bW ~ dnorm( 0 , 0.5 ) , 
  sigma ~ dexp( 1 )
) , data = d )
precis( m5.1)
```

```
##                    mean        sd       5.5%     94.5%
## intercept -9.889697e-07 0.1114079 -0.1780523 0.1780504
## bW         2.370539e-01 0.1308307  0.0279612 0.4461465
## sigma      9.485685e-01 0.0935642  0.7990349 1.0981022
```


```r
m5.2 <- quap( alist(
  d ~ dnorm( mu , sigma ) , 
  mu <- intercept + bW * w + bM * m,
  intercept ~ dnorm( 0 , 0.2 ) , 
  bW ~ dnorm( 0 , 0.5 ) , 
  bM ~ dnorm( 0 , 0.5 ) , 
  sigma ~ dexp( 1 )
) , data = d )
precis( m5.2)
```

```
##                   mean        sd        5.5%     94.5%
## intercept 3.656452e-06 0.1055298 -0.16865341 0.1686607
## bW        2.305895e-01 0.1217847  0.03595396 0.4252250
## bM        3.457123e-01 0.1218221  0.15101715 0.5404075
## sigma     8.784481e-01 0.0867773  0.73976127 1.0171350
```


```r
m5.3 <- quap( alist(
  d ~ dnorm( mu , sigma ) , 
  mu <- intercept + bW * w + bA * a,
  intercept ~ dnorm( 0 , 0.2 ) , 
  bW ~ dnorm( 0 , 0.5 ) , 
  bA ~ dnorm( 0 , 0.5 ) , 
  sigma ~ dexp( 1 )
) , data = d )
precis( m5.3)
```

```
##                    mean         sd         5.5%      94.5%
## intercept  1.429406e-05 0.09536230 -0.152393079  0.1524217
## bW         1.807975e-01 0.10774278  0.008603733  0.3529913
## bA        -5.494865e-01 0.10784667 -0.721846343 -0.3771267
## sigma      7.671320e-01 0.07592718  0.645785689  0.8884783
```


```r
m5.4 <- quap( alist(
  d ~ dnorm( mu , sigma ) , 
  mu <- intercept + bW * w + bS * s,
  intercept ~ dnorm( 0 , 0.2 ) , 
  bW ~ dnorm( 0 , 0.5 ) , 
  bS ~ dnorm( 0 , 0.5 ) , 
  sigma ~ dexp( 1 )
) , data = d )
precis( m5.4)
```

```
##                  mean         sd        5.5%     94.5%
## intercept -0.07726869 0.12384293 -0.27519360 0.1206562
## bW         0.12309372 0.15331599 -0.12193485 0.3681223
## bS         0.39442838 0.29088746 -0.07046597 0.8593227
## sigma      0.92660143 0.09197923  0.77960085 1.0736020
```


```r
m5.5 <- quap( alist(
  d ~ dnorm( mu , sigma ) , 
  mu <- intercept + bW * w + bA * a + bM * m,
  intercept ~ dnorm( 0 , 0.2 ) , 
  bW ~ dnorm( 0 , 0.5 ) , 
  bA ~ dnorm( 0 , 0.5 ) , 
  bM ~ dnorm( 0 , 0.5 ) , 
  sigma ~ dexp( 1 )
) , data = d )
precis( m5.5)
```

```
##                    mean         sd         5.5%      94.5%
## intercept  3.123621e-05 0.09516310 -0.152057782  0.1521203
## bW         1.782179e-01 0.10774008  0.006028434  0.3504073
## bA        -5.843606e-01 0.14882252 -0.822207694 -0.3465134
## bM        -5.005919e-02 0.14775273 -0.286196588  0.1860782
## sigma      7.650600e-01 0.07584017  0.643852727  0.8862672
```

Plotting the coefficient of bW, the last 2 models that closed the backdoor paths are showing that W isn't really correlated with D, while the other models do. m5.4 that conditioned on S has a clearer effect comparing to m5.5 that conditioned on A and M. 

```r
coeftab_plot( coeftab(m5.1, m5.2, m5.3, m5.4, m5.5), pars = "bW")
```

![](ch6_files/figure-html/unnamed-chunk-13-1.png)<!-- -->





Using tidyverse below

load tidyverse

```r
library(tidyverse)
```

```
## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.1 ──
```

```
## ✓ tibble  3.1.1     ✓ dplyr   1.0.5
## ✓ tidyr   1.1.3     ✓ stringr 1.4.0
## ✓ readr   1.4.0     ✓ forcats 0.5.1
## ✓ purrr   0.3.4
```

```
## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
## x tidyr::extract() masks rstan::extract()
## x dplyr::filter()  masks stats::filter()
## x dplyr::lag()     masks stats::lag()
## x purrr::map()     masks rethinking::map()
```

```r
library(ggdag)
```

```
## 
## Attaching package: 'ggdag'
```

```
## The following object is masked from 'package:stats':
## 
##     filter
```


```r
data("WaffleDivorce", package = "rethinking")
d <- WaffleDivorce
d
```

```
##                Location Loc Population MedianAgeMarriage Marriage Marriage.SE
## 1               Alabama  AL       4.78              25.3     20.2        1.27
## 2                Alaska  AK       0.71              25.2     26.0        2.93
## 3               Arizona  AZ       6.33              25.8     20.3        0.98
## 4              Arkansas  AR       2.92              24.3     26.4        1.70
## 5            California  CA      37.25              26.8     19.1        0.39
## 6              Colorado  CO       5.03              25.7     23.5        1.24
## 7           Connecticut  CT       3.57              27.6     17.1        1.06
## 8              Delaware  DE       0.90              26.6     23.1        2.89
## 9  District of Columbia  DC       0.60              29.7     17.7        2.53
## 10              Florida  FL      18.80              26.4     17.0        0.58
## 11              Georgia  GA       9.69              25.9     22.1        0.81
## 12               Hawaii  HI       1.36              26.9     24.9        2.54
## 13                Idaho  ID       1.57              23.2     25.8        1.84
## 14             Illinois  IL      12.83              27.0     17.9        0.58
## 15              Indiana  IN       6.48              25.7     19.8        0.81
## 16                 Iowa  IA       3.05              25.4     21.5        1.46
## 17               Kansas  KS       2.85              25.0     22.1        1.48
## 18             Kentucky  KY       4.34              24.8     22.2        1.11
## 19            Louisiana  LA       4.53              25.9     20.6        1.19
## 20                Maine  ME       1.33              26.4     13.5        1.40
## 21             Maryland  MD       5.77              27.3     18.3        1.02
## 22        Massachusetts  MA       6.55              28.5     15.8        0.70
## 23             Michigan  MI       9.88              26.4     16.5        0.69
## 24            Minnesota  MN       5.30              26.3     15.3        0.77
## 25          Mississippi  MS       2.97              25.8     19.3        1.54
## 26             Missouri  MO       5.99              25.6     18.6        0.81
## 27              Montana  MT       0.99              25.7     18.5        2.31
## 28             Nebraska  NE       1.83              25.4     19.6        1.44
## 29        New Hampshire  NH       1.32              26.8     16.7        1.76
## 30           New Jersey  NJ       8.79              27.7     14.8        0.59
## 31           New Mexico  NM       2.06              25.8     20.4        1.90
## 32             New York  NY      19.38              28.4     16.8        0.47
## 33       North Carolina  NC       9.54              25.7     20.4        0.98
## 34         North Dakota  ND       0.67              25.3     26.7        2.93
## 35                 Ohio  OH      11.54              26.3     16.9        0.61
## 36             Oklahoma  OK       3.75              24.4     23.8        1.29
## 37               Oregon  OR       3.83              26.0     18.9        1.10
## 38         Pennsylvania  PA      12.70              27.1     15.5        0.48
## 39         Rhode Island  RI       1.05              28.2     15.0        2.11
## 40       South Carolina  SC       4.63              26.4     18.1        1.18
## 41         South Dakota  SD       0.81              25.6     20.1        2.64
## 42            Tennessee  TN       6.35              25.2     19.4        0.85
## 43                Texas  TX      25.15              25.2     21.5        0.61
## 44                 Utah  UT       2.76              23.3     29.6        1.77
## 45              Vermont  VT       0.63              26.9     16.4        2.40
## 46             Virginia  VA       8.00              26.4     20.5        0.83
## 47           Washington  WA       6.72              25.9     21.4        1.00
## 48        West Virginia  WV       1.85              25.0     22.2        1.69
## 49            Wisconsin  WI       5.69              26.3     17.2        0.79
## 50              Wyoming  WY       0.56              24.2     30.7        3.92
##    Divorce Divorce.SE WaffleHouses South Slaves1860 Population1860
## 1     12.7       0.79          128     1     435080         964201
## 2     12.5       2.05            0     0          0              0
## 3     10.8       0.74           18     0          0              0
## 4     13.5       1.22           41     1     111115         435450
## 5      8.0       0.24            0     0          0         379994
## 6     11.6       0.94           11     0          0          34277
## 7      6.7       0.77            0     0          0         460147
## 8      8.9       1.39            3     0       1798         112216
## 9      6.3       1.89            0     0          0          75080
## 10     8.5       0.32          133     1      61745         140424
## 11    11.5       0.58          381     1     462198        1057286
## 12     8.3       1.27            0     0          0              0
## 13     7.7       1.05            0     0          0              0
## 14     8.0       0.45            2     0          0        1711951
## 15    11.0       0.63           17     0          0        1350428
## 16    10.2       0.91            0     0          0         674913
## 17    10.6       1.09            6     0          2         107206
## 18    12.6       0.75           64     1     225483        1155684
## 19    11.0       0.89           66     1     331726         708002
## 20    13.0       1.48            0     0          0         628279
## 21     8.8       0.69           11     0      87189         687049
## 22     7.8       0.52            0     0          0        1231066
## 23     9.2       0.53            0     0          0         749113
## 24     7.4       0.60            0     0          0         172023
## 25    11.1       1.01           72     1     436631         791305
## 26     9.5       0.67           39     1     114931        1182012
## 27     9.1       1.71            0     0          0              0
## 28     8.8       0.94            0     0         15          28841
## 29    10.1       1.61            0     0          0         326073
## 30     6.1       0.46            0     0         18         672035
## 31    10.2       1.11            2     0          0          93516
## 32     6.6       0.31            0     0          0        3880735
## 33     9.9       0.48          142     1     331059         992622
## 34     8.0       1.44            0     0          0              0
## 35     9.5       0.45           64     0          0        2339511
## 36    12.8       1.01           16     0          0              0
## 37    10.4       0.80            0     0          0          52465
## 38     7.7       0.43           11     0          0        2906215
## 39     9.4       1.79            0     0          0         174620
## 40     8.1       0.70          144     1     402406         703708
## 41    10.9       2.50            0     0          0           4837
## 42    11.4       0.75          103     1     275719        1109801
## 43    10.0       0.35           99     1     182566         604215
## 44    10.2       0.93            0     0          0          40273
## 45     9.6       1.87            0     0          0         315098
## 46     8.9       0.52           40     1     490865        1219630
## 47    10.0       0.65            0     0          0          11594
## 48    10.9       1.34            4     1      18371         376688
## 49     8.3       0.57            0     0          0         775881
## 50    10.3       1.90            0     0          0              0
##    PropSlaves1860
## 1         4.5e-01
## 2         0.0e+00
## 3         0.0e+00
## 4         2.6e-01
## 5         0.0e+00
## 6         0.0e+00
## 7         0.0e+00
## 8         1.6e-02
## 9         0.0e+00
## 10        4.4e-01
## 11        4.4e-01
## 12        0.0e+00
## 13        0.0e+00
## 14        0.0e+00
## 15        0.0e+00
## 16        0.0e+00
## 17        1.9e-05
## 18        0.0e+00
## 19        4.7e-01
## 20        0.0e+00
## 21        1.3e-01
## 22        0.0e+00
## 23        0.0e+00
## 24        0.0e+00
## 25        5.5e-01
## 26        9.7e-02
## 27        0.0e+00
## 28        5.2e-04
## 29        0.0e+00
## 30        2.7e-05
## 31        0.0e+00
## 32        0.0e+00
## 33        3.3e-01
## 34        0.0e+00
## 35        0.0e+00
## 36        0.0e+00
## 37        0.0e+00
## 38        0.0e+00
## 39        0.0e+00
## 40        5.7e-01
## 41        0.0e+00
## 42        2.0e-01
## 43        3.0e-01
## 44        0.0e+00
## 45        0.0e+00
## 46        4.0e-01
## 47        0.0e+00
## 48        4.9e-02
## 49        0.0e+00
## 50        0.0e+00
```


```r
# standardize the continuous focal variables.
d <-
  d %>% 
  mutate(a = rethinking::standardize(MedianAgeMarriage),
         d = rethinking::standardize(Divorce),
         m = rethinking::standardize(Marriage),
         s = factor(South, levels = 0:1, labels = c("North", "South")),
         w = rethinking::standardize(WaffleHouses))
```


```r
library(GGally)
```

```
## Registered S3 method overwritten by 'GGally':
##   method from   
##   +.gg   ggplot2
```

```r
# define a couple custom functions
my_diag <- function(data, mapping, ...) {
  ggplot(data = data, mapping = mapping) + 
    geom_density(fill = "steelblue", color = "black")
}

my_lower <- function(data, mapping, ...) {
  ggplot(data = data, mapping = mapping) + 
    geom_smooth(method = "lm", color = "orange", se = F) +
    geom_point(alpha = .8, size = 1/4, color = "blue")
  }

ggpairs(data = d, columns = c(14:16, 18, 17),
        upper = list(continuous = wrap("cor", family = "sans", color = "black", size = 3)),
        diag = list(continuous = my_diag),
        lower = list(continuous = my_lower),
        mapping = aes(color = s)) +
  scale_fill_manual(values = c("forestgreen", "lightblue"))
```

```
## `geom_smooth()` using formula 'y ~ x'
```

```
## `geom_smooth()` using formula 'y ~ x'
## `geom_smooth()` using formula 'y ~ x'
## `geom_smooth()` using formula 'y ~ x'
## `geom_smooth()` using formula 'y ~ x'
## `geom_smooth()` using formula 'y ~ x'
```

```
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
```

![](ch6_files/figure-html/unnamed-chunk-17-1.png)<!-- -->


```r
library(brms)
```

```
## Loading required package: Rcpp
```

```
## Loading 'brms' package (version 2.15.0). Useful instructions
## can be found by typing help('brms'). A more detailed introduction
## to the package is available through vignette('brms_overview').
```

```
## 
## Attaching package: 'brms'
```

```
## The following objects are masked from 'package:rethinking':
## 
##     LOO, stancode, WAIC
```

```
## The following object is masked from 'package:rstan':
## 
##     loo
```

```
## The following object is masked from 'package:stats':
## 
##     ar
```

```r
b6.13 <- 
  brm(data = d, 
      family = gaussian,
      d ~ 1 + w,
      prior = c(prior(normal(0, 0.2), class = Intercept),
                prior(normal(0, 0.5), class = b),
                prior(exponential(1), class = sigma)),
      iter = 2000, warmup = 1000, chains = 4, cores = 4,
      seed = 6,
      file = "fits/b06.13")

b6.14 <- 
  brm(data = d, 
      family = gaussian,
      d ~ 1 + w + s,
      prior = c(prior(normal(0, 0.2), class = Intercept),
                prior(normal(0, 0.5), class = b),
                prior(exponential(1), class = sigma)),
      iter = 2000, warmup = 1000, chains = 4, cores = 4,
      seed = 6,
      file = "fits/b06.14")

b6.15 <- 
  brm(data = d, 
      family = gaussian,
      d ~ 1 + w + a + m,
      prior = c(prior(normal(0, 0.2), class = Intercept),
                prior(normal(0, 0.5), class = b),
                prior(exponential(1), class = sigma)),
      iter = 2000, warmup = 1000, chains = 4, cores = 4,
      seed = 6,
      file = "fits/b06.15")

b6.16 <- 
  brm(data = d, 
      family = gaussian,
      d ~ 1 + w + a,
      prior = c(prior(normal(0, 0.2), class = Intercept),
                prior(normal(0, 0.5), class = b),
                prior(exponential(1), class = sigma)),
      iter = 2000, warmup = 1000, chains = 4, cores = 4,
      seed = 6,
      file = "fits/b06.16")

b6.17 <- 
  brm(data = d, 
      family = gaussian,
      d ~ 1 + w + m,
      prior = c(prior(normal(0, 0.2), class = Intercept),
                prior(normal(0, 0.5), class = b),
                prior(exponential(1), class = sigma)),
      iter = 2000, warmup = 1000, chains = 4, cores = 4,
      seed = 6,
      file = "fits/b06.17")
```




```r
gg_simple_dag <- function(d) {
  
  d %>% 
    ggplot(aes(x = x, y = y, xend = xend, yend = yend)) +
    geom_dag_point(color = "steelblue", alpha = 1/2, size = 6.5) +
    geom_dag_text(color = "black") +
    geom_dag_edges() + 
    theme_dag()
  
}

dag_coords <-
  tibble(name = c("A", "D", "M", "S", "W"),
         x    = c(1, 3, 2, 1, 3),
         y    = c(1, 1, 2, 3, 3))

dagify(A ~ S,
       D ~ A + M + W,
       M ~ A + S,
       W ~ S,
       coords = dag_coords) %>%
  gg_simple_dag()
```

![](ch6_files/figure-html/unnamed-chunk-20-1.png)<!-- -->

Standardising all data

```r
d$D <- standardize(d$Divorce)
d$M <- standardize(d$Marriage)
d$A <- standardize(d$MedianAgeMarriage)
```


```r
d$D
```

```
##  [1]  1.65420530  1.54436431  0.61071590  2.09356925 -0.92705795  1.05007986
##  [7] -1.64102438 -0.43277350 -1.86070636 -0.65245548  0.99515936 -0.76229646
## [13] -1.09181943 -0.92705795  0.72055689  0.28119293  0.50087491  1.59928480
## [19]  0.72055689  1.81896678 -0.48769399 -1.03689894 -0.26801201 -1.25658092
## [25]  0.77547738 -0.10325053 -0.32293251 -0.48769399  0.22627244 -1.97054734
## [31]  0.28119293 -1.69594487  0.11643145 -0.92705795 -0.10325053  1.70912579
## [37]  0.39103392 -1.09181943 -0.15817102 -0.87213745  0.66563639  0.94023887
## [43]  0.17135194  0.28119293 -0.04833004 -0.43277350  0.17135194  0.66563639
## [49] -0.76229646  0.33611343
## attr(,"scaled:center")
## [1] 9.688
## attr(,"scaled:scale")
## [1] 1.820814
```


```r
d$South
```

```
##  [1] 1 0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 1 1 0 0 0 0 0 0 1 0 0 0 0 0
## [39] 0 1 0 1 1 0 0 1 0 1 0 0
```

```r
d$WaffleHouses
```

```
##  [1] 128   0  18  41   0  11   0   3   0 133 381   0   0   2  17   0   6  64  66
## [20]   0  11   0   0   0  72  39   0   0   0   0   2   0 142   0  64  16   0  11
## [39]   0 144   0 103  99   0   0  40   0   4   0   0
```

