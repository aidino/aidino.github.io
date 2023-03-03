---
layout: libdoc/page
title: 3 - Modeling
permalink: /modeling
category: Notes
description: "Reusable code for modeling"
order: 3
---
{:toc}
- *Code:* 
<br>

### Create models

```python
def create_model(max_len, max_features, embed_size):
    '''
    input: max_len, max_features, embed_size
    output: model.
    '''
    input_layer = Input(shape=(max_len,))
    x = Embedding(max_features, embed_size, weights=[embedding_matrix], trainable=False)(input_layer)
    x = Bidirectional(LSTM(50, dropout=0.1, recurrent_dropout=0.1, return_sequences=True))(x)
    x = GlobalMaxPool1D()(x)
    x = Dense(50, activation='relu')(x)
    x = Dropout(0.1)(x)
    output_layer = Dense(2, activation='sigmoid')(x)
    model = Model(inputs=input_layer, outputs=output_layer)
    
    return model

model = create_model(max_len, max_features, embed_size)
```

**or**

```python
def create_model():
  # A simple CNN architecture based on the one found here: https://www.tensorflow.org/tutorials/images/classification
  model = models.Sequential([
  layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
  layers.MaxPooling2D((2, 2)),
  layers.Conv2D(64, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.Conv2D(64, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.Conv2D(128, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),
  layers.Flatten(),
  layers.Dense(512, activation='relu'),
  layers.Dense(3, activation='softmax')
  ])
  # Compile the model
  model.compile(
      loss=tf.keras.losses.SparseCategoricalCrossentropy(),
      optimizer=optimizers.Adam(),
      metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
  )
  return model
```

**or**

```python
baseModel = EfficientNetB0(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
for layer in baseModel.layers:
    layer.trainable = False
    
headModel = baseModel.output
headModel = AveragePooling2D()(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(128, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(2, activation="softmax")(headModel)

model = Model(inputs = baseModel.input, outputs = headModel)
```

**or**

```python
base_model = tf.keras.applications.EfficientNetB0(include_top=False)
base_model.trainable = False

inputs = tf.keras.layers.Input(shape=(image_size[0], image_size[1], 3), name='input_layer')
data_augmentation = ModelHelper.data_augmentation_layer()

x = data_augmentation(inputs)
x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D(name='global_average_pooling_layer')(x)
outputs = tf.keras.layers.Dense(len(class_names), activation='softmax', name='output_layer')(x)
model = tf.keras.Model(inputs, outputs)
```



### Optimizer model

```python
def optimize(model):
    '''
    Input: 
        Mô hình.
    Return: 
        Mô hình đã biên dịch.
    '''
    f1 = tfa.metrics.F1Score(num_classes=2, average='macro')
    model.compile(
        optimizer=Optimizer.Adam(learning_rate=1e-2), 
        loss='binary_crossentropy', 
        metrics=[f1])
    
    return model

model = optimize(model)
```



### Setup callbacks

```python
def callback_model(checkpoint_name, logs_name):
    '''
    Input: 
        Checkpoint name, logs name tốt nhất.
    Return: 
        Callback list có chứa tensorboard callback và checkpoint callback.
    '''
    tensorboard_callback = TensorBoard(log_dir=logs_name)
    checkpoint_callback = ModelCheckpoint(checkpoint_name, save_best_only=True, monitor='val_f1_score')
    reduce_lr_callback = ReduceLROnPlateau(monitor='val_f1_score', factor=0.3, patience=1)
    early_stopping_callback = EarlyStopping(monitor='val_f1_score', patience=7, mode='max')

    callbacks_list = [tensorboard_callback, checkpoint_callback, reduce_lr_callback, early_stopping_callback]

    return callbacks_list

checkpoint_name = 'weights.best.hdf5'
logs_name = 'training_logs'
callbacks_list = callback_model(checkpoint_name, logs_name)

```



### Training model

```python
def train_model(model, callbacks_list):
    '''
    Input: 
        Mô hình và callback list,
    Return: 
        Mô hình với trọng số checkpoint tốt nhất.
    '''
    model.fit(
        X_tr,
        y_tr,
        epochs = 20, 
        batch_size = 4096,
        validation_data = (X_va, y_va),
        callbacks = callbacks_list
    )
    
    model = load_model(checkpoint_name)

    return model

model = train_model(model, callbacks_list)
```

### [Optional] Display trainable layer 

```python
def print_trainable_info(model):
        """ In ra summary của model

        Args:
            model (Model): Model
        """    
        print(
            "STT".ljust(6) 
            + "Name".ljust(30) 
            + "Shape".ljust(30)
            +  "Trainable".ljust(15)
            + "dtype".ljust(15)
            + "Policy".ljust(15))
        print("-"*109)
        info = list()
        for i, layer in enumerate(model.layers):
            info_dict = {}
            info_dict['STT'] = i
            info_dict['Name'] = layer.name
            info_dict['Shape'] = layer.output_shape
            info_dict['Trainable'] = layer.trainable
            info_dict['Policy'] = layer.dtype_policy
            info_dict['dtype'] = layer.dtype
            info.append(info_dict)
        for d in reversed(info):
            print(
                str(d['STT']).ljust(6) 
                + d['Name'].ljust(30) 
                + str(d['Shape']).ljust(30) 
                + str(d['Trainable']).ljust(15)
                + str(d['dtype']).ljust(15)
                + str(d['Policy']).ljust(15)) 

```

### [Optional] Fine-turning

```python
# Setting up for fine-tuning last 5 layers of base model
base_model.trainable = True
for layer in base_model.layers[:-5]:
    layer.trainable = False
ModelHelper.print_trainable_info(base_model)
```

### [Optional] Callbacks

#### tensorboard callback

```python
log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
```

#### learning rate callback

```python
lr_schedule = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-4 * 10**(epoch/20))
```

#### checkpoint callback

```python
checkpoint_path = dir_name + "/" + experiment_name +  "/cp.ckpt"
# Tạo ModelCheckpoint callback chỉ để lưu các trọn số của mô hình 
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    save_best_only=True, # đặt là True để chỉ lưu những mô hình tốt nhất thay vì một mô hình mỗi epoch
    monitor='val_loss')
print(f"Saving model checkpoints to: {checkpoint_path}")
```

#### early stopping callback

```python
tf.keras.callbacks.EarlyStopping(
  monitor="val_loss", # theo dõi phép đo val loss
  patience=3) # nếu val loss giảm trong 3 epoch liên tiếp, hãy ngừng huấn luyện
```

#### reduce learning rate callback

```python
tf.keras.callbacks.ReduceLROnPlateau(
  monitor="val_loss", 
  factor=0.2, # nhân learning rate với 0.2 (giảm 5 lần)
  patience=2,
  verbose=1, # in ra khi nào learning rate giảm
  min_lr=1e-7)
```
