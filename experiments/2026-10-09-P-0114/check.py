"""P-0114: recompute 4DA's headline numbers from the confusion matrix its README publishes,
and show what 'noise accuracy' rewards by scoring two trivial filters on the same corpus shape."""
TP, FP, TN, FN = 119, 19, 1646, 213
total = TP + FP + TN + FN
relevant, noise = TP + FN, TN + FP
print("total evaluations", total, "(README: 1,997)")
print("rejection rate (TN+FN)/total  %.1f%%  (README 93.1%%)" % (100 * (TN + FN) / total))
print("noise accuracy TN/(TN+FP)     %.1f%%  (README 98.9%%)" % (100 * TN / noise))
print("precision TP/(TP+FP)          %.1f%%  (README 86.2%%)" % (100 * TP / (TP + FP)))
print("recall TP/(TP+FN)             %.1f%%  (README 35.8%%)" % (100 * TP / relevant))
print("relevant items rejected       %d of %d (%.1f%%)" % (FN, relevant, 100 * FN / relevant))
print("share of corpus that is noise %.1f%%" % (100 * noise / total))
print("reject-everything filter: noise accuracy 100.0%, rejection rate 100.0%, recall 0%")
print("keep-everything filter:   noise accuracy 0.0%%, precision %.1f%%" % (100 * relevant / total))
