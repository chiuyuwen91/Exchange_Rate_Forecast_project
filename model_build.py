import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras import models
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.noise import AlphaDropout
from keras.layers import GaussianNoise
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
def build_model(n_dense=6,
                   dense_units=16,
                   activation='selu',
                   dropout=AlphaDropout,
                   dropout_rate=0.1,
                   kernel_initializer='lecun_normal',
                   optimizer = 'rmsprop',
                   # lr = 1e-4,
                   # loss='mae',
                   num_classes=1,):

    model = models.Sequential()

    model.add(Dense(dense_units,
                           input_shape=(train_data.shape[1],),
                           kernel_initializer=kernel_initializer,
                           ))
    model.add(Activation(activation))
    model.add(dropout(dropout_rate))
    for i in range(n_dense - 1):
        model.add(Dense(dense_units, kernel_initializer=kernel_initializer))
        model.add(Activation(activation))
        model.add(GaussianNoise(0.01))
        model.add(dropout(dropout_rate))

    # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.add(Dense(num_classes))
    model.add(Activation(activation))
    model.compile(loss='mae',
                  metrics=['mae'],
                  optimizer=optimizer)

    return model

X = pd.read_csv('./info/forex_signals_clean.csv', header=None)
y = pd.read_csv('./info/USD_NTD_Rate_Clean.csv', header=None)
# x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
train_data, test_data, train_targets, test_targets = train_test_split(X, y, test_size=0.2, random_state=4)
# (train_data, train_targets), (test_data, test_targets) = \
#     boston_housing.load_data()

# mean = train_data.mean(axis=0)
# std = train_data.std(axis=0)
# train_data -= mean
# train_data /= std
#
# test_data -= mean
# test_data /= std

# ++++++++++++++++K-fold validation
k = 4
num_val_samples = len(train_data) // k
num_epochs = 500
all_mae_histories = []

for i in range(k):
    print('Processing fold #', i)
    val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
    val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

    partial_train_data = np.concatenate(
        [train_data[: i * num_val_samples],
         train_data[(i + 1) * num_val_samples:]],
        axis=0)
    partial_train_targets = np.concatenate(
        [train_targets[: i * num_val_samples],
         train_targets[(i + 1) * num_val_samples:]],
        axis=0)
    model = build_model()
    history = model.fit(partial_train_data,
                        partial_train_targets,
                        validation_data=(val_data, val_targets),
                        epochs=num_epochs,
                        batch_size=1,
                        verbose=1)
    mae_history = history.history['val_mean_absolute_error']
    all_mae_histories.append(mae_history)
    average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]


# +++++++++++++++++ triaining final model
model = build_model()
model.fit(train_data,
          train_targets,
          epochs=300,
          batch_size=16,
          verbose=1)
model.save("final_model.h5")
model.save_weights("model_weights.h5")
test_mae, _ = model.evaluate(test_data, test_targets)
print('Test MAE:', test_mae)
# +++++++++++++++++ matplotlib
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation Mae')
plt.savefig('C:/share_VM/work/Project_PPI/training_result_mae.png')