# task4

The purpose of this task is to start working on BCMS variety identification.

Datasets used:
* setimes{bs,hr,sr}
* Denis' tweets
* CLARIN webcrawls.

# Data preparation - setimes dataset

My plan was to extract the documents from the `setimes` files. This would be done by combing through and searching for the delimiter that separated the articles:

```
[Name of the journalist] za Southeast European Times -- [date]
``` 

This proved tricky, because this separator does not appear at the same rate in the file pairs, e.g. the string count for `' za Southeast European Times '` varies quite a bit:
|   file     | occurences     |     
|---|---|
|setimes.bs-hr.bs.txt |3220|
|setimes.bs-hr.hr.txt |3190|
|setimes.bs-sr.bs.txt |2890|
|setimes.bs-sr.sr.txt |2866|
|setimes.hr-sr.hr.txt |4471|
|setimes.hr-sr.sr.txt |4482|

I had found out that the most equal delimiter was `'Southeast European Times'`:

|   file     | occurences     |     
|---|---|
| setimes.bs-hr.bs.txt | 3377 |
| setimes.bs-hr.hr.txt | 3377 |
| setimes.bs-sr.bs.txt | 3047 |
| setimes.bs-sr.sr.txt | 3046 |
| setimes.hr-sr.hr.txt | 4774 |
| setimes.hr-sr.sr.txt | 4773 |

SInce the goal of this task is variety classification and not macine translation, it will be presumed the precise structure of the documents does not matter much and no one-to-one sentence mapping will be performed.

Once the data was processed more properly and finer details were included in the search, the results are as follows:

|Searched for  `{name} za Southeast European Times {rest}\n` | count |
| --- | --- |
| setimes.bs-hr.bs.txt |  3222 |
| setimes.bs-hr.hr.txt |  3192 |
| setimes.bs-sr.bs.txt |  2892 |
| setimes.bs-sr.sr.txt |  2869 |
| setimes.hr-sr.hr.txt |  4473 |
| setimes.hr-sr.sr.txt |  4485 |

|Searched for `{beginning} Southeast European Times {end}\n` | count |
| --- | --- |
| setimes.bs-hr.bs.txt |  3230 |
| setimes.bs-hr.hr.txt |  3217 |
| setimes.bs-sr.bs.txt |  2900 |
| setimes.bs-sr.sr.txt |  2891 |
| setimes.hr-sr.hr.txt |  4505 |
| setimes.hr-sr.sr.txt |  4510 |

I also examined lines that were not being picked up by my analysis:
* Nataša Radić for Southeast European Times iz Zagreba -- 03/09/08
* Da bismo bolje izašli ususret vama -- našim čitaocima -- Southeast European Times je u oktobru i novembru 2007. obavio internet anketu.
* Za Southeast European Times iz Istambula izvještava Ozgur Ogret -- 22/03/12
* Građani Kosova koje je intervjuirao Southeast European Times izrazili su različite poglede na najnovija dešavanja.
* Internet stranica Southeast European Times je glavni izvor vijesti i informacija o jugoistočnoj Evropi na deset jezika: albanskom, bosanskom, bugarskom, hrvatskom, engleskom, grčkom, makedonskom, rumunskom, srpskom i turskom.
* Cilj internet stranice Southeast European Times je da ponudi tačne i uravnotežene informacije o događanjima u Jugoistočnoj Evropi, sa pogledom u budućnost.
* Ayhan Simsek Southeast European Times -- 03/09/07
* Goran Trajkov for Southeast European Times iz Skoplja - 03/06/09

I implemented a regex search to get as much complete data as possible, focusing on the format that I deemed most likely to accurately catch all signatures. The results dissapointed a bit:

### regex: `Southeast European Times .*-- \d\d/\d\d/\d\d`

|file| counts|
|---|---|
| setimes.bs-hr.bs.txt |  2940 |
| setimes.bs-hr.hr.txt |  2596 |
| setimes.bs-sr.bs.txt |  2619 |
| setimes.bs-sr.sr.txt |  1684 |
| setimes.hr-sr.hr.txt |  3179 |
| setimes.hr-sr.sr.txt |  2566 |

### regex: `([\w+]|[|Za|za|for|For]|^) Southeast European Times .*[-\-|–] \d\d/\d\d/\d\d`
|file| counts|
|---|---|
| setimes.bs-hr.bs.txt |  3085 |
| setimes.bs-hr.hr.txt |  3066 |
| setimes.bs-sr.bs.txt |  2763 |
| setimes.bs-sr.sr.txt |  1817 |
| setimes.hr-sr.hr.txt |  4342 |
| setimes.hr-sr.sr.txt |  3395 |

The fluctuations between text pairs is gigantic, so I decided to go forward with the second implementation, where I used `parse` library to search for `{beginning} Southeast European Times {end}\n` and where the counts agree to 0.4% or better.

When I joined the data into a dataset with proper `fasttext` formatting I also created a shuffled file which will be used to produce train-test data. I trained my first model with this batch which produced suspiciously good precisions and recalls of 99%. When visually inspecting the data I noticed there were a few repeated lines, possibly because the same short document appeared in many dataset pairs. I removed those. The training was repeated and again the results were evaluated with the built-in method, yielding precision and recall of 99%.

# Data preparation - twitter