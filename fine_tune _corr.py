import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import load_model
from sklearn.model_selection import train_test_split


model = load_model('./tmp.hdf5')
X = pd.read_csv('./info/forex_signals_corr_clean.csv', header=None)
y = pd.read_csv('./info/USD_NTD_Rate_Clean.csv', header=None)
train_data, test_data, train_targets, test_targets = train_test_split(X, y, test_size=0.2, random_state=4)

# ++++++++++++++++K-fold validation
k = 4
num_val_samples = len(train_data) // k
num_epochs = 200
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
    model = load_model('./tmp.hdf5')
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
model.summary()
model.fit(train_data,
          train_targets,
          epochs=20000,
          batch_size=16,
          verbose=1,)

test_mae, _ = model.evaluate(test_data, test_targets)
print('Test MAE:', test_mae)

pred_loadback = model.predict(test_data)
print(pred_loadback)
# +++++++++++++++++ matplotlib
# plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
# plt.xlabel('Epochs')
# plt.ylabel('Validation Mae')
# plt.savefig('./info/training_result_mae_final02.png')
