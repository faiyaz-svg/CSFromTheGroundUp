# Data science and machine learning

Cheat sheet for the chapter. Each section names the lesson it comes from.

## Statistics for data work

Lesson: [Statistics for data work](01-statistics-for-data-work.md)

| Need | Use |
|---|---|
| Typical value, symmetric data | Mean |
| Typical value, skewed data (latency, income) | Median, plus p95 or p99 |
| Spread | Standard deviation (`statistics.stdev` is the sample version, divides by $n-1$) |
| Tail experience | Percentiles: `statistics.quantiles(data, n=100, method="inclusive")` |
| Two columns move together | Correlation, then look for a confounder |

A page that makes $k$ independent calls, each with a 5% chance of being slower than p95, hits at least one slow call with probability $1 - 0.95^k$.

Traps: sampling bias, confounders, Simpson's paradox (a trend in each group reverses in the pooled data).

## Analytics in SQL

Lesson: [Analytics in SQL](02-analytics-sql-cohorts-funnels-retention.md)

| Question | Pattern |
|---|---|
| Daily active users | `count(DISTINCT user_id)` grouped by local date |
| Day in Toronto from a UTC `timestamp` | `(ts AT TIME ZONE 'UTC') AT TIME ZONE 'America/Toronto'` |
| Compare with the previous period | `lag(x) OVER (ORDER BY day)` |
| Signup cohort | `date_trunc('month', signup_date)` |
| Retention | Active users in month $n$ divided by cohort size |
| Funnel | One row per user with `min(ts) FILTER (WHERE event_type = ...)`, steps in order, then `first_value` and `lag` |

## A/B testing

Lesson: [A/B testing](03-ab-testing.md)

| Term | Meaning |
|---|---|
| Null hypothesis | No real difference |
| p-value | Chance of a gap this large if the null were true |
| 95% confidence interval | Range from a procedure that covers the true value 95% of the time |
| Power | Chance of detecting a real effect of the chosen size (aim for 80%) |

Two-proportion z-test: $z = (\hat p_B - \hat p_A)/\sqrt{\hat p(1-\hat p)(1/n_A + 1/n_B)}$. Halving the detectable effect needs about 4 times the sample. Fix the sample size first, look once, and pick one primary metric. Ten looks turned a 5% false positive rate into 19% in the lesson's simulation.

## What machine learning is

Lesson: [What machine learning is](04-what-machine-learning-is.md)

| Term | Meaning |
|---|---|
| Feature, label | Input column, column to predict |
| Supervised, unsupervised | With labels, without labels |
| Regression, classification, clustering | Predict a number, a category, groups |
| Parameter, hyperparameter | Set by training, set by you |
| Training, inference | Fitting, predicting |

Always compare with a baseline (`DummyRegressor`, `DummyClassifier`). Use a rule or query when the logic is known and must be exact.

## Training, testing and metrics

Lesson: [Training, testing and metrics](05-training-testing-and-metrics.md)

| Metric | Formula |
|---|---|
| Accuracy | (TP + TN) / all |
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1 | $2PR/(P+R)$ |
| MAE | mean of absolute errors |
| RMSE | square root of mean squared error |
| ROC-AUC | Chance a random positive is ranked above a random negative; 0.5 is chance |

Rules: split before anything else, fit every preprocessing step on training rows only (use a `Pipeline`), touch the test set once, use stratified splits for imbalanced classes, and split by time for time series. A large train/test gap means overfitting.

## scikit-learn

Lesson: [Regression and classification with scikit-learn](06-regression-and-classification-with-scikit-learn.md)

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
model.score(X_te, y_te)
cross_val_score(model, X, y, cv=5)
```

| Model | Task | Needs scaling | Reads as |
|---|---|---|---|
| `LinearRegression` | Number | Yes, for comparing coefficients | Coefficients |
| `LogisticRegression` | Category | Yes | Coefficients (log-odds) |
| `DecisionTreeClassifier`, `DecisionTreeRegressor` | Either | No | Questions; limit `max_depth` |
| `RandomForestClassifier`, `RandomForestRegressor` | Either | No | `feature_importances_` |

## Neural networks

Lesson: [Neural networks and deep learning](07-neural-networks-and-deep-learning.md)

| Term | Meaning |
|---|---|
| Neuron | $f(w \cdot x + b)$ |
| Activation | ReLU $\max(0,z)$ or sigmoid; makes stacked layers non-linear |
| Loss | One number for how wrong the predictions are |
| Gradient descent | $w \leftarrow w - \eta \cdot \text{gradient}$ |
| Learning rate | Step size $\eta$: too big diverges, too small crawls |
| Epoch | One pass over the training data |
| Embedding | Learned vector for an item |

Parameters in a dense layer: inputs $\times$ outputs $+$ outputs. GPUs run the matrix multiplications in parallel.
