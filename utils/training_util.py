import os, pytz, datetime
import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, MaxPooling2D, GlobalAveragePooling2D

split = 0.2
epochs = 5
acc_max = 0.8
acc_min = 0.6
batch_size = 60
img_height = 200
img_width = 200

BASE_PATH = os.path.abspath(os.path.dirname("."))
FACE_SAMPLE_DIR = os.path.join(BASE_PATH, "assets/faces/")
TF_MODEL_DIR = os.path.join(BASE_PATH, "assets", "tf_trained_model", "latest")

def start_training(classes):
    results = new_training(classes)
    return {
        "acc": results[0],
        "val_acc": results[1],
        "loss": results[2],
        "val_loss": results[3]
    }

def new_training(classes):
    tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%y%m%d%H%M%S")
    
    datagen_train = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=split,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='reflect'
    )

    datagen_val = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=split
    )

    train_data_generator = datagen_train.flow_from_directory(
        batch_size=batch_size,
        directory=FACE_SAMPLE_DIR,
        shuffle=True,
        seed=40,
        subset='training',
        interpolation='bicubic',
        target_size=(img_height, img_width)
    )

    valid_data_generator = datagen_val.flow_from_directory(
        batch_size=batch_size,
        directory=FACE_SAMPLE_DIR,
        shuffle=True,
        seed=40,
        subset='validation',
        interpolation='bicubic',
        target_size=(img_height, img_width)
    )

    valid_data_generator.reset()
    train_data_generator.reset()

    if os.path.exists(TF_MODEL_DIR):
        model = keras.models.load_model(TF_MODEL_DIR)
        model.pop()
        model.add(Dense(len(classes), activation='softmax', name=f"dense_{len(classes)}.{tanggal}"))
        # model.summary()
    else:
        model = Sequential([
            Conv2D(16, 3, padding='same', activation='relu', input_shape=(img_height, img_width, 3)),
            MaxPooling2D(),
            Dropout(0.10),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(128, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(256, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(512, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(1024, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            GlobalAveragePooling2D(),
            Dense(2048, activation='relu'),
            Dropout(0.10),
            Dense(len(classes), activation='softmax')
        ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy', metrics=['accuracy']
    )

    history = model.fit(
        train_data_generator,
        steps_per_epoch=train_data_generator.samples // batch_size,
        epochs=epochs,
        validation_data=valid_data_generator,
        validation_steps=valid_data_generator.samples // batch_size
    )

    history_dict = history.history
    print(history_dict.keys())

    acc = history.history['accuracy'][epochs-1]
    val_acc = history.history['val_acc'][epochs-1]
    loss = history.history['loss'][epochs-1]
    val_loss = history.history['val_loss'][epochs-1]

    model.save(TF_MODEL_DIR)

    # acc = 1
    # val_acc = 1
    # loss = 0
    # val_loss = 0

    return [round(acc, 2), round(val_acc, 2), round(loss, 2), round(val_loss, 2)]