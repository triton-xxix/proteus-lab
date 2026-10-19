# P-0182: fast.ai lesson 5, from scratch, against a one-line rule

Refill source #10, course.fast.ai lesson 5 ("From-scratch model"). What I took from the page: the lesson
builds a linear model and then a small neural net by hand, with its own gradient loop, on Kaggle's
Titanic, and its reading list includes notebooks showing how far a name- or gender-only rule gets. So the
question: does the from-scratch machinery beat "women survive, men do not"?

`run.py` does it in numpy with hand-written gradients (log loss), features as in the lesson's notebook,
on the public 891-row training file (`titanic.csv`, datasciencedojo mirror). Twenty random 80/20 splits.

| Model | Mean held-out accuracy | sd | Beats the rule on |
|---|---|---|---|
| Women survive | 79.6% | 2.7 | n/a |
| Linear, 400 epochs | 79.5% | 3.1 | 8 of 20 splits |
| One hidden layer, 20 ReLU, 1500 epochs | 81.4% | 2.8 | 14 of 20 splits |

Verdict: works. The net adds about 1.8 points over the rule on average and wins 14 of 20 splits; the
linear model adds nothing (-0.1 points). That is the lesson's point in miniature: most of the signal is
one feature, and the gain from the machinery is small next to split-to-split noise (sd near 3 points).

Not checked: whether the linear model is under-trained at 400 epochs and lr 0.5 (I did not sweep), and
no Kaggle test-set score (that needs an account). Results in `results.json`.
