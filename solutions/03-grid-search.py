import dask

parameter_scores = []

for i in range(4):
    X_train, X_test, y_train, y_test = dask.delayed(train_test_split, nout=4)(data.data, data.target, pure=False)

    for max_df in [0.5, 0.75, 1.0]:
        for ngram_range in [(1, 1), (1, 2)]:
            vect = dask.delayed(CountVectorizer)(max_df=max_df, ngram_range=ngram_range)
            vect = vect.fit(X_train)
            X2_train = vect.transform(X_train)
            X2_test = vect.transform(X_test)
            for norm in ['l1', 'l2']:
                tfidf = dask.delayed(TfidfTransformer)(norm=norm)
                tfidf = tfidf.fit(X2_train)
                X3_train = tfidf.transform(X2_train)
                X3_test = tfidf.transform(X2_test)

                for max_iter in [5]:
                    for alpha in [0.00001, 0.000001]:
                        for penalty in ['l2', 'elasticnet']:
                            clf = dask.delayed(SGDClassifier)(max_iter=max_iter, alpha=alpha, penalty=penalty)
                            clf = clf.fit(X3_train, y_train)

                            score = clf.score(X3_test, y_test)
                            params = {
                                'max_df': max_df,
                                'ngram_range': ngram_range,
                                'norm': norm,
                                'max_iter': max_iter,
                                'alpha': alpha,
                                'penalty': penalty
                            }

                            parameter_scores.append((params, score))

best = dask.delayed(max)(parameter_scores,
                         key=lambda param_score: param_score[1])
