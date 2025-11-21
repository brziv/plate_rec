import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Load the training log CSV
df = pd.read_csv('project/trained/2025-11-21_11-29-06/training_log.csv')
df = df[df['epoch'] <= 40]

# Plot Loss
plt.figure(figsize=(10, 6))
plt.plot(df['epoch'], df['loss'], label='Train Loss')
plt.plot(df['epoch'], df['val_loss'], label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.grid(True)
plt.savefig('train_loss.png')
plt.close()

# Plot Accuracies
plt.figure(figsize=(10, 6))
plt.plot(df['epoch'], df['cat_acc'], label='Train Cat Acc')
plt.plot(df['epoch'], df['val_cat_acc'], label='Val Cat Acc')
plt.plot(df['epoch'], df['plate_acc'], label='Train Plate Acc')
plt.plot(df['epoch'], df['val_plate_acc'], label='Val Plate Acc')
plt.plot(df['epoch'], df['plate_len_acc'], label='Train Plate Len Acc')
plt.plot(df['epoch'], df['val_plate_len_acc'], label='Val Plate Len Acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracies')
plt.legend()
plt.grid(True)
plt.savefig('train_acc.png')
plt.close()
