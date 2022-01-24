# Twitter dataset

## Dataset description

This dataset consists of 390268 tweets from 614 Twitter users. The users have been manually annotated with the BCMS variant they use. Twitter handles and URLs have been filtered from the tweets and all tweets have been transliterated from cyrillic to latin script. The intended use for this dataset is BCMS variant identification.

## Dataset structure
An 80-10-10 train-dev-test split has been performed on user level, meaning that all the tweets from a specific user are in a single fold. The splits are stratified by language on user level.

The [JSON file](twitter.json) is a dictionary with sequential keys. Each instance has the following fields:
| field      | type            | meaning                                                        |
|------------|-----------------|----------------------------------------------------------------|
| `user`     | string          | Twitter username                                               |
| `language` | string          | manually annotated language variant (`hr`, `bs`, `sr` or `me`) |
| `split`    | string          | which split the instance belongs to                            |
| `tweets`   | list of strings | individual tweets                                              |

### Sample instance
```
    "0":{
        "user":"danijelzv",
        "language":"bs",
        "split":"train",
        "tweets":[
            " Isto srce kao '95! ",
            " ne otkrivaj nam polo\u017eaj :-)",
            ....
            ]
        }
```

## Dataset composition

![](images/language_length_distribution.png)

![](images/users_length_distribution.png)

## Known issues:
As seen up to line 3000

* Transliteration module transforms capital letter "Љ" and "Њ" as "Lj" and "Nj", respectively.
* Some tweets are in English, consist only of smileys, or are not complete sentences (e.g. "Apuglia, Italy")
* Some tweets are clearly written by bots (e.g. "2 people followed me and 3 people unfollowed me \/\/ automatically checked by ", note how the sentence has a missing TW handle that was removed in the preprocessing).
* Certain users use a great deal of offensive words.
* If the tweet was a reply or a retweet, there is often little text remaining, sometimes as little as "haha" or "...".