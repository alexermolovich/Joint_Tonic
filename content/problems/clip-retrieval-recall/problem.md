# Evaluate Cross-Modal Retrieval Recall at K

Implement retrieval_recall(scores, k). scores is a finite NumPy float64 array (N,N), 1<=N<=2048, absolute entries <=1e6. Row i is image i; column j is text j. The only positive for image i is text i and vice versa. k is a built-in Python int excluding bool with 1<=k<=N. Rank by descending score and break equal scores by lower candidate index. Return exactly {'image_to_text': float, 'text_to_image': float}, fractions of queries whose paired item ranks within k. For image-to-text rank each row; for text-to-image rank each column. Preserve scores. Noncontiguous arrays supported. TypeError for non-array scores; ValueError for all other violations. Empty collections are rejected; k=N gives both recalls1. Scores are dimensionless, not probabilities; no timestamps or robot frames. This exercise computes single-positive recall, not image encoder inference, multi-positive retrieval, average precision, or confidence intervals.

## Examples

## Retrieval direction matters

scores=[[.9,.8],[.95,.1]], k=1. Image0 retrieves text0, image1 retrieves text0: image_to_text=0.5. Text0 retrieves image1, text1 retrieves image0: text_to_image=0.0. Output {'image_to_text':0.5,'text_to_image':0.0}.

## Deterministic ties

scores is a 3x3 all-zero float64 matrix; k=2. Every query selects candidates0,1. Two of three diagonal positives are included in each direction. Output both2/3. At k=3 both become1.

## Hints

1. Use stable descending sorting, preserving original candidate order for ties.
2. Sort rows and columns separately.
3. Compare selected indices with the query's diagonal label, then average booleans.
