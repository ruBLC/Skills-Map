import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Укажите путь к файлу CSV и имя столбца для считывания названий процессов
csv_file_path = r'D:\GIT\Skills-Map\scripts\python\otf.csv'
column_name = 'NameOTF'

# Загрузите данные из файла CSV
data = pd.read_csv(csv_file_path)

# Создайте список названий процессов из выбранного столбца
process_names = data[column_name].tolist()

# Преобразуйте названия в числовой формат с помощью TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(process_names)

# Определите оптимальное количество кластеров с использованием метода "локтя"
wcss = []  # Within-Cluster-Sum-of-Squares
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(tfidf_matrix)
    wcss.append(kmeans.inertia_)

# Постройте график метода "локтя"
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Метод "локтя" для определения числа кластеров')
plt.xlabel('Количество кластеров')
plt.ylabel('Within-Cluster-Sum-of-Squares')
plt.grid()
plt.show()
