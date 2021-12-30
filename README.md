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

As demonstrated in the notebook `3del.ipynb` we have 1000 twitter users crawled, but only 614 are annotated. SO far only these 614 will be used in the examinations.

Functions to remove mentions, URLs, and hashtags have been prepared. Furthermore, I saw a lot of the tweets were retweets, which in plaintext manifests as prefix:
```
RT @celava_ti_mama: ...
```
I decided to include these tweets in the dataset for now as I suspect the majority of the Twitter users mostly retweet tweets in their own language. The aforementioned prefix will be stripped. The processed data was saved as a json file containing usernames, their annotated language and a list of all the tweets.

I later found that some tweets had this tag in the middle, probably indicating a retweet with a comment. I will have to deal with this later.

# Model training and analysis 

After a model was trained in fasttext I used it briefly on sample data. I checked the data distributions by language and it is interesting:

![SETIMES train data](./images/setimes%20train.png)

![SETIMES test data](./images/setimes%20test.png)

![Twitter data](./images/twitter.png)

I will preserve the data as is for the time being. In the future the discrepancy in the SETIMES data could be corrected by including the BS data instances twice to roughly even the ratios of languages. This of course would not work for Montenegrin tweets, for which the only available datasource is the twitter dataset. Even after CLARIN webcrawls will have been included the situation will be miserable for Montenegrin language.

After evaluating the model by hand on test data (as opposed to the results of fasttext built-in methods) I again noticed unusually high performance:

```
Accuracy: 0.997
F1 score: 0.996
```

For this result I used the model, trained on SETIMES train data, and predicted the language of the SETIMES test data.

When I used the same model on twitter data, the metrics were more modest:

```
Accuracy: 0.375
F1 score: 0.246
```

I also prepared a preliminary version of visualization for classification results, which in its current form is not yet interactive, but it is offering some insight into the working of the algorithm nonetheless.

![LIME library colouring the words as either contributing to the label or not.](./images/lime.png)

It can be seen that the most indicative words are usually not semantic word variants, but instead stop words commonly used in all three languages. This perhaps should not be surprising, as some BCMS variants differ also in syntactic uses of the language, expressed with combination of these stopwords.

I suspect lexical differences might also be captured and visualized by using a _proper_ tokenizer, but this might be difficult to get from fasttext.

# Corrections after mondays meeting

The SETIMES dataset must be structured in a more correct fashion that prevents data leakage. 

I shall repeat the processing in new IPython notebook for reproducibility, but previously used data files will be overwritten. 

I encountered some problems with connectivity that stemmed from the lack of diskspace due to all the clarin web crawl data. They have temporarily been deleted.

As per the weekly meeting I will prepare a train-dev-test split in the SETIMES dataset. For this I counted the lines in all three relevant files:

```
setimes.bs-hr.hr.txt 138402 
	split 1: 110721, split 2: 124561
setimes.bs-sr.sr.txt 135945 
	split 1: 108756, split 2: 122350
setimes.bs-sr.bs.txt 135945 
	split 1: 108756, split 2: 122350
```

To identify the same place I checked the 110721-st line in the first file:
```
$ sed -n '110721p' < ../../Varieties/BCMS/setimes.bs-hr.hr.txt
Kada je list The Economist pozvao birače na potporu oporbenoj CHP na nedavno održanim općim izborima u Turskoj, premijer Recep Tayyip Erdogan naznačio je da je za to možda kriv Izrael.
```

I identified the beginning of the document, which is shown here:

```
Budući da se Srbija sprema za opće izbore sljedeće godine, postoji sve veći pritisak na političare i kandidate da razviju svijest o snazi Facebooka.
S obzirom na neizvjesne utrke i žestoku kampanju koja slijedi, sposobnost korištenja društvenih medija mogla bi biti odlučujući čimbenik.
<--- DOCUMENT BORDER --->
Zapadni mediji i Erdogan: Odljubljivanje? 
Godina 2011. mogla bi biti upamćena kao godina u kojoj su se zapadni mediji ‘odljubili’ od turske vladajuće AKP.
Što se promijenilo?
Alexander Christie-Miller za Southeast European Times iz Istanbula – 21/06/11
Neke zapadne medijske kuće nedavno su se okrenule protiv premijera Erdogana. [Reuters]
Kada je list The Economist pozvao birače na potporu oporbenoj CHP na nedavno održanim općim izborima u Turskoj, premijer Recep Tayyip Erdogan naznačio je da je za to možda kriv Izrael.
```

In Bosnian dataset the same document is identified here:
```
Sa pripremama za opće izbore naredne godine u Srbiji, dolazi do povećanog pritiska na političare i kandidate da budu obavješteniji po pitanju Facebooka.
S predstojećim tijesnim utrkama i oštrim kampanjama, sposobnost zauzdavanja društvenih medija mogla bi predstavljati odlučujući faktor
<--- DOCUMENT BORDER --->
Zapadni mediji i Erdogan: ljubav prestaje?
Godina 2011. mogla bi biti zabilježena kao godina kad su zapadni mediji 'prestali s ljubavlju' prema vladajućoj turskoj stranci AKP.
Šta je pošlo nakrivo?
Alexander Christie-Miller za Southeast European Times iz Istanbula – 21/06/11
Neke zapadne medijske kuće nedavno su se okrenule na premijera Erdogana. [Reuters]
Kad je časopis The Economist glasače pozvao da podrže opozicionu CHP na nedavnim općim izborima u Turskoj, premijer Recep Tayyip Erdogan nagovijestio je da bi za to mogao biti kriv Izrael.
```

And in Serbian:

```
S obzirom da se Srbija sprema za opšte izbore sledeće godine, sve je veći pritisak na političare i kandidate da postanu svesniji Fejsbuka.
S obzirom na tesne trke i žestoku kampanju koja sledi, sposobnost da se iskoriste društveni mediji mogla bi da bude odlučujući faktor.
<--- DOCUMENT BORDER --->
Zapadni mediji i Erdogan: Odljubljivanje?
Godina 2011. mogla bi da se pamti kao godina u kojoj su se zapadni mediji ‘odljubili’ od turske vladajuće AKP.
Šta se promenilo?
Neke zapadne medijske kuće nedavno su se okrenule preotiv premijera Erdogana. [Rojters]
Kada je magazin Ekonomist pozvao birače da podrže opozicionu CHP na nedavno održanim opštim izborima u Turskoj, premijer Redžep Tajip Erdogan nagovestio je da je za to možda kriv Izrael.
```

In a similar fashion the second split has been identified in all three datasets. For reproducibility they are logged below:

|split|hr|bs|sr|
|---|---|---|---|
| 1|110716 |110716 | 108659|
|2|124549|124549|112302|

Special care was taken to prevent dual inclusion of the lines, as `sed -n '1,2' file` will print first and second line. The data was split and stored in the interim directory, awaiting further processing (i.e. automated document splitting by the existing heuristic algorithm).

Searching for:  {beginning} Southeast European Times {end}
|filename | count |
|---|---|
|hr_train.txt| 2577|
|bs_train.txt| 2591|
|sr_train.txt| 2289|
|hr_dev.txt| 328|
|bs_dev.txt| 327|
|sr_dev.txt| 307|
|hr_test.txt| 312|
|bs_test.txt| 312|
|sr_test.txt| 295|

Searching for:  {beginning}Southeast European Times{middle}{dd:d}/{mm:d}/{yy:d}

|filename | count |
|---|---|
|hr_train.txt| 2495|
|bs_train.txt| 2518|
|sr_train.txt| 1455|
|hr_dev.txt| 319|
|bs_dev.txt| 323|
|sr_dev.txt| 212|
|hr_test.txt| 305|
|bs_test.txt| 306|
|sr_test.txt| 183|

After some examination, particularly of the Serbian dataset, it was found that the following works quite well:

Searching for:  {beginning}Southeast European Times{middle}{dd:d}{sep1}{mm:d}{sep2}{yy:d}{end}
|filename | count |
|---|---|
|hr_train.txt| 2557|
|bs_train.txt| 2557|
|sr_train.txt| 2261|
|hr_dev.txt| 326|
|bs_dev.txt| 326|
|sr_dev.txt| 308|
|hr_test.txt| 310|
|bs_test.txt| 309|
|sr_test.txt| 295|

After this splitting has been found I proceeded with training a fasttext model. Given that we also prepared a `dev` split we can use it to optimize fasttext hyperparameters. As before the optimization time was capped at 600 seconds. Only SETIMES dataset was used for the training, validation and evaluation. Before tweaking the tokenization parameters the results are as follows:

```
Accuracy: 0.989
F1 score: 0.989
```

In the next run I increased the maximal number of character n-grams to 10, but this did not improve the metrics:

```
Accuracy: 0.989
F1 score: 0.989
```
My next attempt was increasing the wordNgram parameter to 4, which might cover some syntactical differences. Interestingly, the model actually performed way worse: Accuracy: 0.475
F1 score: 0.382

# Addendum 2021-12-28T08:18:17

I revisited the twitter dataset and discovered I can clean it better. First I improved the retweet text replacing function, and then I checked what characters appear in the tweets. It is concearning. I extract 1170 different characters, other than normal latin characters also a great deal of emojis, some asian characters, and some raw unicode characters (e.g. '\U000fe330', '\x94',...) These will have to be removed. I counted their occurances and found that the frequency dropps off radically fast, so most of the text is ok. See [file](/home/peterr/macocu/taskB/task4/8_counts_of_original_tweet_characters.csv).

I found a snippet that only allows latin characters, which includes "exotic" letters like `'Šđßå'`, but filters out math symbols, currency characters, emojis and asian characters. The preprocessing will be performed anew and since the preprocessing takes a while and it's a breeding ground for bugs, I suggest the data be split and saved.

The problem with the preprocessing as implemented is that the results are now quite weird; emoticons like `:D` now become just `D` and the punctuation is removed. 

Summarized approaches and problems:
* `import regex; result = regex.sub(u'[^\p{Latin}]', u'', tweet)`: removes the puctuation as well
* `re.sub(u'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', tweet)`: does not remove math symbols and similar chars.

I opted for option 2. I pickled the dictionary containing the tweets as [/home/peterr/macocu/taskB/data/final/twitter_full_ds.pickle](/home/peterr/macocu/taskB/data/final/twitter_full_ds.pickle).


# Addendum 2021-12-28T11:09:01


I also noticed fasttext would not work if string to be predicted contains newlines. I added this newline removal to the preprocessing pipeline and saved the new data.

I repeated the finetuning on SETimes data which works like a charm:
```
Accuracy: 0.991
F1 score: 0.991 (macro)
```

With the model thus obtained I predicted the language of the Twitter dataset. It did not go as flawlessly:
```
Macro f1: 0.262
Micro f1: 0.42
Accuracy: 0.42
```

![](images/SETimes_model_on_twitter_CM.png)

To discuss with Nikola:
* Future steps
* ~~I deleted the webcrawl data in one episode of desperately cleaning the disk to assure training, can I get the link again? ~~ Found the [link](http://hdl.handle.net/11356/1426) Now we can use it.

Reminder of where we left off:
> what is with montenegrin? how is it classified? can we somehow synthesize data for that category?
> 
> can we somehow visualise the classifier decisions, might be very useful for understanding what we have and what we need
> 
> what is the setup that will make good classifiers for all three (news, web, twitter)?
> 
> is the classification over twitter data better if mentions, hashtags, urls are removed?

For now I can answer the following:
* Montenegrin is pretty much randomly classified. I don't think we'll be able to synthesize anything with fasttext, shall we go to transformers?
* We can visualize classifier decisions. This has been already demonstrated with Lime in October, and the same framework can be extended even further.
* That is the final problem.

# Meeting notes 2021-12-28T13:49:17

* Classify `users`, not individual tweets! Use the same model.
* Get also tweet count for each user. Should be O(100) or more.
* After this: we'll start with larger corpora (linked above). Think about efficient preprocessing and token importance calculation. Google `true casing`, but probably we won't have to do that here as we have lots of data.

# Addendum 2021-12-28T18:52:51

I repeated the analysis on user level and it is muuch better :) 

```
Macro f1: 0.379
Micro f1: 0.707
Accuracy: 0.707
```

![](images/SETimes_model_on_twitter_CM_on_user_level.png)

I also checked the stats on the number of the users and as Nikola foretold, we always have at least 100 tweets for each user, so we suspect we have a solid sample.

```
Tweets per user:
count     614.000000
mean      635.615635
std       430.146903
min       100.000000
25%       280.000000
50%       489.000000
75%       925.750000
max      1779.000000
```




# Addendum 2021-12-29T11:55:13

I downloaded and unzipped all the files to `~/macocu/taskB/data/raw`.

Filesizes:
* SR: 3 GB
* HR: 7.4 GB
* CNR: 558 MB
* BS: 1.6 GB


Memos on preprocessing:
* Transliteration?
* Splitting on blank lines: either `csplit`, `sed`, or with python.
* Delete all numbers.
* Delete all words that contain any capital letters.
* Delete all punctuation.

These steps can't be guaranteed to be commutative (e.g.: line `USLUGE KOMORE` would be replaced with a single space, which could be picked up as a blank line if implementation is not precise).

As fasttext can't process multiline input it would also be a good idea to squash documents into a single line.



# Meeting notes 2021-12-29T13:29:00

* use python to preprocess crawl data
* transliterate cnrwac
* ignore tokens with less than 20 occurences for now
* see skype chat for the idea of token frequency dictionary
* start with toy samples, not the entire dataset
* don't lose time with punctuation removal, should work also with the DS as is. Might repeat the calculation later to check differences.
* we are after good results on long documents, don't worry about edge cases


```
Nikola, 1:31 PM
dict={}
for token in line.split():
if token in dict:
add to dict
elif token satisfies regex:
add to dict
regex - low-cased alphabet ([a-zšđčćž])
O(1)
\w\D
Nikola, 1:42 PM
d[k]=d.get(k,0)+1
HR-SR-feat-candidates
SR-HR-feat-candidates
```

Target: get list of strongest features for CR to discriminate against SR and vice versa, and expand this to all combinations.

# Addendum 2021-12-29T14:26:12

So, let's get started. I'm opening a new notebook to sort it out. I started by creating a toy dataset with the first 10000 lines from all files to test, but this will have to be increased in the future to get better distribution estimates.



# Addendum 2021-12-29T16:10:37

I prepared the second part of the machinery, namely a script to generate the frequency dictionary. On the toy corpus it takes about 11s to get generated, so I think this will not be the bottleneck. Upon brief inspection I noticed that we get some unwanted behavior, specifically stuff like:

```
 'vještine\n': 80,
 'nastali': 200,
 'razni': 224,
 'stilovi\n': 4,
 ```

This will be corrected within the frequency extractor itself.

# Addendum 2021-12-29T17:54:58

The frequency extractor has been corrected and for the toy corpora the resulting jsons are ready and added to the repo.



# Addendum 2021-12-30T08:07:31

I started with the combination of HR <-> SR toy corpora.

For the most important features that distinguish Croatian toy corpus from the Serbian, I get the following table (only the first 30 items are shown):

|              |    HR_SR |      SR_HR |
|:-------------|---------:|-----------:|
| kn           | 179.556  | 0.0055693  |
| sustav       | 150.153  | 0.00665988 |
| sustava      | 149.265  | 0.00669948 |
| suradnji     | 125.406  | 0.00797411 |
| natjecanja   | 115.761  | 0.0086385  |
| lipnja       | 110.973  | 0.00901122 |
| rujna        | 110.86   | 0.00902038 |
| okoliša      | 110.521  | 0.00904808 |
| tvrtke       | 109.443  | 0.00913722 |
| svibnja      | 109.307  | 0.00914858 |
| ožujka       | 109.117  | 0.00916446 |
| travnja      | 107.848  | 0.00927227 |
| udruge       | 105.651  | 0.00946512 |
| listopada    | 103.449  | 0.0096666  |
| uvjetima     |  84.6988 | 0.0118065  |
| veljače      |  84.0536 | 0.0118972  |
| gospodarstva |  82.3719 | 0.0121401  |
| sudionika    |  81.2523 | 0.0123073  |
| primjerice   |  80.2788 | 0.0124566  |
| udruga       |  80.1087 | 0.012483   |
| tjedna       |  78.8446 | 0.0126832  |
| kuna         |  78.6973 | 0.0127069  |
| županije     |  78.1412 | 0.0127974  |
| sudjelovanje |  77.9331 | 0.0128315  |
| milijuna     |  77.1661 | 0.0129591  |
| tijekom      |  76.9481 | 0.0129958  |
| siječnja     |  76.888  | 0.0130059  |
| natjecanje   |  76.3397 | 0.0130993  |
| glazbe       |  75.3042 | 0.0132795  |
| tvrtki       |  75.1313 | 0.01331    |

Mutatis mutandis, we can get the importances of Serbian tokens in comparison with the Croatian corpus:

|             |   SR_HR |      HR_SR |
|:------------|--------:|-----------:|
| rešenja     | 203.882 | 0.0049048  |
| odsto       | 195.017 | 0.00512775 |
| opštine     | 193.647 | 0.00516403 |
| preduzeća   | 186.179 | 0.00537119 |
| gde         | 167.978 | 0.00595317 |
| deo         | 164.964 | 0.00606195 |
| cena        | 164.217 | 0.00608949 |
| mesta       | 163.866 | 0.00610255 |
| cene        | 163.412 | 0.00611949 |
| evra        | 157.018 | 0.00636869 |
| časova      | 155.753 | 0.00642043 |
| predsednika | 154.401 | 0.00647663 |
| saradnji    | 152.997 | 0.00653608 |
| vreme       | 139.484 | 0.00716929 |
| meseca      | 138.417 | 0.00722453 |
| predsednik  | 134.998 | 0.00740753 |
| dece        | 132.495 | 0.00754746 |
| meseci      | 125.721 | 0.00795413 |
| uslovima    | 124.393 | 0.00803905 |
| uvek        | 122.46  | 0.00816596 |
| delu        | 121.249 | 0.00824752 |
| posle       | 119.203 | 0.00838903 |
| dve         | 117.117 | 0.00853847 |
| korišćenje  | 114.489 | 0.00873448 |
| decu        | 112.382 | 0.0088982  |
| mesto       | 111.11  | 0.00900005 |
| čoveka      | 110.924 | 0.00901519 |
| zahteva     | 109.001 | 0.00917422 |
| dela        | 108.295 | 0.00923403 |
| saradnje    | 106.124 | 0.00942292 |

What we should improve is replacing all `NaN` values that occur because a token was not present in corpus and repeat the analysis to get more realistic numbers. I did this, but this specific example did not change. 