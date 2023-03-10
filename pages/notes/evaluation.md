---
layout: libdoc/page
title: 4 - Evaluation
permalink: /evaluation
category: Notes
description: "Useful code for evaluation"
order: 4
---
{:toc}
- *Code:* 
<br>

### Prepare data for evaluation

```python
test_data_generator = tf.keras.preprocessing.image.ImageDataGenerator()
test_generator = test_data_generator.flow_from_directory(
        'test',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        shuffle=False)

```

### Evaluate model

```python
loss, accuracy = model.evaluate(test_generator)
```

### Classification report

```python
from sklearn.metrics import classification_report

predictions = model.predict(test_generator)

predicted_classes = np.argmax(predictions, axis=1)
true_classes = test_generator.classes
class_labels = list(test_generator.class_indices.keys())
report = classification_report(true_classes, predicted_classes, target_names=class_labels)
print(report)
```

### Confusion matrix

```python
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

predicted_classes = np.argmax(predictions, axis=1)
true_classes = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

cm = confusion_matrix(true_classes, predicted_classes)

sns.set()
plt.figure(figsize=(8, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.ylabel("True Label")
plt.xlabel("Predicted Label")
plt.show()
```

### Misclassified percentage

```python
def print_misclassified_percent(cm, class_labels):
    total_samples_per_class = np.sum(cm, axis=1)
    misclassified_samples_per_class = total_samples_per_class - np.diag(cm)
    misclassified_percent_per_class = misclassified_samples_per_class / total_samples_per_class.astype(float) * 100.0
    print("Misclassified percentage for each class:")
    for i, class_label in enumerate(class_labels):
        print("{}: {:.2f}%".format(class_label, misclassified_percent_per_class[i]))

```

### Top misclassified images

```python
def show_top_misclassified_images(cm, test_generator, class_labels, num_images=5):
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_generator.classes
    misclassified_indices = np.where(predicted_classes != true_classes)[0]
    misclassified_counts = cm[misclassified_indices, true_classes[misclassified_indices]]
    sorted_indices = np.argsort(misclassified_counts)[::-1][:num_images]
    print("Top misclassified images:")
    for i, index in enumerate(sorted_indices):
        image_path = test_generator.filepaths[misclassified_indices[index]]
        image = Image.open(image_path)
        predicted_class = class_labels[predicted_classes[misclassified_indices[index]]]
        true_class = class_labels[true_classes[misclassified_indices[index]]]
        print("{}. True class: {}; Predicted class: {}".format(i+1, true_class, predicted_class))
        plt.imshow(image)
        plt.show()

```

### Others

#### plot_loss_curves

```python
def plot_loss_curves(results):
        """ V??? ????? th??? loss v?? accuracy c???a model

        Args:
            results (dict): dictionary ch???a loss v?? accuracy c???a model. V?? d???:
                {"loss": [...],
                "accuracy": [...],
                "val_loss": [...],
                "val_accuracy": [...]}
        """
        loss = results["loss"]
        test_loss = results["val_loss"]

        accuracy = results["accuracy"]
        test_accuracy = results["val_accuracy"]

        epochs = range(len(results["loss"]))

        plt.figure(figsize=(15, 7))

        # Plot loss
        plt.subplot(1, 2, 1)
        plt.plot(epochs, loss, label="train_loss")
        plt.plot(epochs, test_loss, label="test_loss")
        plt.title("Loss")
        plt.xlabel("Epochs")
        plt.legend()

        # Plot accuracy
        plt.subplot(1, 2, 2)
        plt.plot(epochs, accuracy, label="train_accuracy")
        plt.plot(epochs, test_accuracy, label="test_accuracy")
        plt.title("Accuracy")
        plt.xlabel("Epochs")
        plt.legend()
```

#### make_confusion_matrix

```python
def make_confusion_matrix(y_true, y_pred, classes=None, figsize=(10, 10), text_size=15, norm=False, savefig=False): 
        """ T???o confusion matrix ????? ????nh gi?? model d???a tr??n y_true v?? y_pred 
        
        N???u classes ???????c truy???n v??o, confusion matrix s??? ???????c g??n nh??n, 
        n???u kh??ng, gi?? tr??? class s??? ???????c g??n nh??n b???ng s??? nguy??n

        Args:
            y_true: M???ng ch???a nh??n th???c t??? (ph???i c?? c??ng k??ch th?????c v???i y_pred).
            y_pred: M???ng ch???a nh??n d??? ??o??n (ph???i c?? c??ng k??ch th?????c v???i y_true).
            classes: M???ng ch???a nh??n c???a c??c class (v?? d???: d???ng string). N???u `None`, nh??n s??? l?? s??? nguy??n.
            figsize: K??ch th?????c c???a figure (default=(10, 10)).
            text_size: K??ch th?????c c???a ch??? (default=15).
            norm: normalize values hay kh??ng (default=False).
            savefig: L??u figure hay kh??ng (default=False).
        
        Returns:
            M???t labelled confusion matrix ???????c v??? ????? so s??nh y_true v?? y_pred.

        Example usage:
            make_confusion_matrix(y_true=test_labels, # ground truth test labels
                                y_pred=y_preds, # predicted labels
                                classes=class_names, # array of class label names
                                figsize=(15, 15),
                                text_size=10)
        """  
        # Create the confustion matrix
        cm = confusion_matrix(y_true, y_pred)
        cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] # normalize it
        n_classes = cm.shape[0] # find the number of classes we're dealing with

        # Plot the figure and make it pretty
        fig, ax = plt.subplots(figsize=figsize)
        cax = ax.matshow(cm, cmap=plt.cm.Blues) # colors will represent how 'correct' a class is, darker == better
        fig.colorbar(cax)

        # Are there a list of classes?
        if classes:
            labels = classes
        else:
            labels = np.arange(cm.shape[0])
        
        # Label the axes
        ax.set(title="Confusion Matrix",
                xlabel="Predicted label",
                ylabel="True label",
                xticks=np.arange(n_classes), # create enough axis slots for each class
                yticks=np.arange(n_classes), 
                xticklabels=labels, # axes will labeled with class names (if they exist) or ints
                yticklabels=labels)
        
        # Make x-axis labels appear on bottom
        ax.xaxis.set_label_position("bottom")
        ax.xaxis.tick_bottom()
        # set the rotation for the x axis tick labels to 45 degrees
        ax.tick_params(axis="x", rotation=45)

        # Set the threshold for different colors
        threshold = (cm.max() + cm.min()) / 2.

        # Plot the text on each cell
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if norm:
                plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
                    horizontalalignment="center",
                    color="white" if cm[i, j] > threshold else "black",
                    size=text_size)
            else:
                plt.text(j, i, f"{cm[i, j]}",
                    horizontalalignment="center",
                    color="white" if cm[i, j] > threshold else "black",
                    size=text_size)

        # Save the figure to the current working directory
        if savefig:
            fig.savefig("confusion_matrix.png")
```

#### plot_learning_rate_and_loss

```python
def plot_learning_rate_and_loss(history, epochs):
        # V??? bi???u ????? learning rate v???i loss
        lrs = 1e-4 * (10 ** (np.arange(epochs)/20))
        plt.figure(figsize=(10, 7))
        plt.semilogx(lrs, history["loss"]) # mu???n tr???c x (learning rate) theo thang log
        plt.xlabel("Learning Rate")
        plt.ylabel("Loss")
        plt.title("Learning rate vs. loss")
```

#### compare_historys

```python
def compare_historys(original_history, new_history, initial_epochs=5):
        """ So s??nh 2 history c???a model
            Th?????ng l?? so s??nh history c???a model g???c v???i history c???a model sau khi fine-tuning

        Args:
            original_history (dict): History c???a model g???c
            new_history (dict): History c???a model m???i
            initial_epochs (int, optional): S??? epochs ban ?????u c???a model g???c. Defaults to 5.
        """
        
        # Get original history measurements
        acc = original_history.history["accuracy"]
        loss = original_history.history["loss"]

        val_acc = original_history.history["val_accuracy"]
        val_loss = original_history.history["val_loss"]

        # Combine original history with new history
        total_acc = acc + new_history.history["accuracy"]
        total_loss = loss + new_history.history["loss"]

        total_val_acc = val_acc + new_history.history["val_accuracy"]
        total_val_loss = val_loss + new_history.history["val_loss"]

        # Make plots
        plt.figure(figsize=(8, 8))
        plt.subplot(2, 1, 1)
        plt.plot(total_acc, label='Training Accuracy')
        plt.plot(total_val_acc, label='Validation Accuracy')
        plt.plot([initial_epochs-1, initial_epochs-1], plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(2, 1, 2)
        plt.plot(total_loss, label='Training Loss')
        plt.plot(total_val_loss, label='Validation Loss')
        plt.plot([initial_epochs-1, initial_epochs-1], plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.xlabel('epoch')
        plt.show()
```

#### prepare_for_evaluation

```python
def prepare_for_evaluation(model, test_dataset):
        """ Chu???n b??? d??? li???u cho vi???c ????nh gi?? model

        Args:
            model (Model): Model ???? ???????c train
            test_dataset (Dataset): Dataset d??ng ????? test

        Returns:
            (y_true, y_pred, classes): Nh??n th???c t???, nh??n d??? ??o??n, t??n c??c l???p
        """
        
        pred_probs = model.predict(test_dataset)
        y_pred = pred_probs.argmax(axis=1)
        y_true = []
        for _, labels in test_dataset.unbatch(): # d??? li???u ki???m tra v?? l???y ???nh, nh??n
            y_true.append(labels.numpy().argmax()) # n???i ch??? m???c c?? gi?? tr??? l???n nh???t (nh??n ??? ?????nh d???ng one-hot)
        return y_true, y_pred, pred_probs, test_dataset.class_names
```

#### plot_f1_score

```python
def plot_f1_score(y_true, y_pred, classes):
        """ In ra classification report c???a model

        Args:
            y_true (list): Ground truth labels
            y_pred (list): Predicted labels
            classes (list): T??n c??c class
        """
        classification_report_dict = classification_report(y_true, y_pred, target_names=classes, output_dict=True)
        class_f1_scores = {}
        for key, value in classification_report_dict.items():
            if key in classes:
                class_f1_scores[key] = value['f1-score']
        f1_scores = pd.DataFrame({"class_name": list(class_f1_scores.keys()), 
                          "f1-score": list(class_f1_scores.values())}).sort_values(by='f1-score', ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 25))
        scores = ax.barh(range(len(f1_scores)), f1_scores["f1-score"].values)
        ax.set_yticks(range(len(f1_scores)))
        ax.set_yticklabels(list(f1_scores["class_name"]))
        ax.set_xlabel("f1-score")
        ax.set_title(f"F1-Scores for {len(classes)} Different Classes")
        ax.invert_yaxis(); # ?????o ng?????c th??? t???

        def autolabel(rects): # Phi??n b???n ???? s???a c???a: https://matplotlib.org/examples/api/barchart_demo.html
            """
            Attach a text label above each bar displaying its height (it's value).
            """
            for rect in rects:
                width = rect.get_width()
                ax.text(1.03*width, rect.get_y() + rect.get_height()/1.5,
                        f"{width:.2f}",
                        ha='center', va='bottom')

        autolabel(scores)
```

#### create_predict_dataframe

```python
def create_predict_dataframe(y_true, y_pred, pred_probs ,classes, filepaths):
        """ T???o dataframe ch???a th??ng tin ???nh, nh??n th???c t???, nh??n d??? ??o??n, x??c su???t d??? ??o??n, t??n l???p

        Args:
            model (Model): Model ???? ???????c train
            test_dataset (Dataset): Dataset d??ng ????? test
            test_dir (str): ???????ng d???n th?? m???c ch???a ???nh test

        Returns:
            DataFrame: Dataframe ch???a th??ng tin ???nh, nh??n th???c t???, nh??n d??? ??o??n, x??c su???t d??? ??o??n, t??n l???p
            
        Example:
            ```python
            filepaths = [filepath.numpy() for filepath in test_dataset.list_files(test_dir + "/*/*.jpg", shuffle=False)]
            pred_df = Evaluation.create_predict_dataframe(y_true, y_pred, pred_probs ,classes, filepaths)
```

        """        
        pred_df = pd.DataFrame({"img_path": filepaths,
                        "pred_conf": pred_probs.max(axis=1), # l???y gi?? tr??? x??c su???t d??? ??o??n l???n nh???t
                        "y_true_classname": [classes[i] for i in y_true],
                        "y_pred_classname": [classes[i] for i in y_pred]})
        # 3. D??? ??o??n c?? ????ng kh??ng?
        pred_df["pred_correct"] = pred_df["y_true_classname"] == pred_df["y_pred_classname"]
        
        return pred_df
```

#### get_top_wrong_df

```python
def get_top_wrong_df(y_true, y_pred, pred_probs ,classes, filepaths, n = 100):
        """ L???y n ???nh d??? ??o??n sai c?? x??c su???t d??? ??o??n cao nh???t

        Args:
            model (Model): Model ???? ???????c train
            test_dataset (Dataset): Dataset d??ng ????? test
            test_dir (str): ???????ng d???n th?? m???c ch???a ???nh test
            n (int, optional): S??? ???nh d??? ??o??n sai c?? x??c su???t d??? ??o??n cao nh???t. Defaults to 100.

        Returns:
            DataFrame: Dataframe ch???a th??ng tin ???nh, nh??n th???c t???, nh??n d??? ??o??n, x??c su???t d??? ??o??n, t??n l???p
            
        Example:
            ```python
            filepaths = [filepath.numpy() for filepath in test_dataset.list_files(test_dir + "/*/*.jpg", shuffle=False)]
            top_wrongs = Evaluation.get_top_wrong_df(y_true, y_pred, pred_probs , classes, filepaths, n = 100)
```
        """        
        
        pred_df = create_predict_dataframe(y_true, y_pred, pred_probs ,classes, filepaths)
        return pred_df[pred_df["pred_correct"] == False].sort_values("pred_conf", ascending=False)[:n]
```


#### load_and_prep_image

```python
def load_and_prep_image(filename, img_shape, scale=False):
        """
        ?????c m???t ???nh t??? filename, bi???n n?? th??nh m???t tensor v?? reshape th??nh
        (224, 224, 3).

        Args:
            filename (str): string filename c???a ???nh m???c ti??u
            img_shape (int): k??ch th?????c ????? resize ???nh m???c ti??u, m???c ?????nh l?? 224
            scale (bool): c?? co gi??n c??c gi?? tr??? pixel th??nh range(0, 1) kh??ng, m???c ?????nh l?? True
        Returns:
            image (Tensor): ???nh ???? ???????c x??? l?? th??nh tensor
        """
        # ?????c trong ???nh
        img = tf.io.read_file(filename)
        # Gi???i m?? n?? th??nh m???t tensor
        img = tf.io.decode_image(img)
        # Thay ?????i k??ch th?????c ???nh
        img = tf.image.resize(img, img_shape)
        if scale:
            # Co gi??n ???nh (nh???n t???t c??? c??c gi?? tr??? t??? 0 ?????n 1)
            return img/255.
        else:
            return img  
```


#### plot_predicted

```python
def plot_predicted(imagepaths, y_trues, y_preds, pred_probs ,image_size):
        # Create the figure and axes objects
        ncols = 5
        nrows = math.ceil(len(imagepaths)/ncols)
        
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3+1))
        axes = axes.ravel()
        
        for i in ncols*nrows:
            axes[i].axis('off')

        # Iterate over the test images
        for i, imagepath in enumerate(imagepaths):
            # Read the image
            image = tf.keras.preprocessing.image.load_img(imagepath, target_size=image_size)
            # Convert the image to a numpy array
            image = tf.keras.preprocessing.image.img_to_array(image)
            # Normalize the image
            image = image/255
            # Plot the image on the current axis
            axes[i].imshow(image)
            axes[i].set_title(f"True: {y_trues[i]}, \n Pred: {y_preds[i]}, \n Prob: {pred_probs[i]}", fontsize=15, color='r')

        # Add a tight layout to the figure
        plt.tight_layout()
```

#### predict_and_plot

```python
# Example
    # foie gras c?? f1 score th???p nh???t, th??? hi???n th??? ng???u nhi??n m??t s??? ???nh trong class n??y
    # foie_gras_dir = test_dir + "/foie_gras"
    # random_foie_gras = np.random.choice(os.listdir(foie_gras_dir), size=20, replace=False)
    # random_foie_gras_paths = [foie_gras_dir + "/" + foie_gras for foie_gras in random_foie_gras]
    # random_foie_gras_paths
    # Evaluation.predict_and_plot(model, random_foie_gras_paths, class_names, image_size, true_class='foie_gras', scale = False)
    def predict_and_plot(model, image_paths, class_names, image_shape, true_class=None, scale = False):
        ncols = 5
        nrows = math.ceil(len(image_paths)/ncols)
        
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 3+1))
        axes = axes.ravel()
        
        for i in range(ncols*nrows):
            axes[i].axis('off')
            
        for i, image_name in enumerate(image_paths):
            # ?????c trong ???nh
            img = tf.io.read_file(image_name)
            # Gi???i m?? n?? th??nh m???t tensor
            img = tf.io.decode_image(img)
            # Thay ?????i k??ch th?????c ???nh
            img = tf.image.resize(img, image_shape)
            
            if scale:
                # Co gi??n ???nh (nh???n t???t c??? c??c gi?? tr??? t??? 0 ?????n 1)
                # V???i pretrained model l?? EfficientNetB0, kh??ng c???n co gi??n ???nh
                img = img/255.
                axes[i].imshow(img)
            else:
                axes[i].imshow(img/255.)
                
            pred_prob = model.predict(tf.expand_dims(img, axis=0))
            pred_class = class_names[np.argmax(pred_prob)]
            
            if true_class is None:
                axes[i].set_title(f"Pred: {pred_class}, \n Prob: {pred_prob.max():.2f}", fontsize=15)
            else:
                if true_class == pred_class:
                    axes[i].set_title(f"True: {true_class}, \n Pred: {pred_class}, \n Prob: {pred_prob.max():.2f}", fontsize=15, color='g')
                else:
                    axes[i].set_title(f"True: {true_class}, \n Pred: {pred_class}, \n Prob: {pred_prob.max():.2f}", fontsize=15, color='r')
            # Add a tight layout to the figure
            plt.tight_layout()
```
#### --- [Kaggle] Predict image in a folder ---

```python
import os
import csv
import tensorflow as tf

# Load the saved model
model = tf.keras.models.load_model('path/to/saved/model')

# Define the image size and batch size
img_size = (224, 224)
batch_size = 32

# Create a list of all the image file names in the "test" folder
image_paths = [os.path.join('test', f) for f in os.listdir('test') if f.endswith('.jpg')]

# Create a list to store the results
results = []

# Iterate through each batch of images
for i in range(0, len(image_paths), batch_size):
    # Load the batch of images
    batch_paths = image_paths[i:i+batch_size]
    batch_images = []
    batch_ids = []
    for path in batch_paths:
        # Load the image and resize it
        img = tf.keras.preprocessing.image.load_img(path, target_size=img_size)
        # Convert the image to a numpy array
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        # Scale the pixel values to between 0 and 1
        img_array /= 255.0
        batch_images.append(img_array)
        # Extract the ID from the file name and add it to the batch_ids list
        id = os.path.splitext(os.path.basename(path))[0]
        batch_ids.append(id)
    # Convert the list of images to a numpy array
    batch_images = tf.stack(batch_images)
    # Make a prediction on the batch of images
    predictions = model.predict(batch_images)
    # Convert the prediction to a list of class names
    class_names = [model.output_names[np.argmax(pred)] for pred in predictions]
    # Append the results to the results list
    results += zip(batch_ids, class_names)

# Save the results to a CSV file
with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Id', 'Predicted Class'])
    writer.writerows(results)

```